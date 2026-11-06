import tempfile
import unittest

from studio.contracts import WORKFLOWS, ContractError, stage_plan
from studio.store import Store


class StorageTestCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = Store(self.temp.name)


class StudioTests(StorageTestCase):
    def test_authored_routes(self):
        self.assertEqual(len(WORKFLOWS), 6)
        ugc = [stage["id"] for stage in stage_plan("ugc-creator", {}, [])]
        self.assertEqual(ugc, ["strategy", "concept", "script", "capture", "edit", "qa"])
        diwali = stage_plan("diwali-campaign", {"festival": "Diwali"}, [])
        self.assertIn("ad-diwali-festive", diwali[0]["skills"])
        tvc = stage_plan("30s-tvc", {"footage": True}, [])
        self.assertIn("ad-realistic-video", tvc[5]["skills"])
        self.assertNotIn("performance", [s["id"] for s in tvc])
        self.assertEqual(
            stage_plan("product-launch", {}, [{"name": "hold", "sample": 100, "value": 0.5}])[-1]["id"],
            "performance",
        )

    def test_project_persists_and_revision_conflicts(self):
        before = self.store.create("sample", "15s-reel", {"brand": "Brand"})
        after = self.store.change("sample", before["revision"], "brief", {"brief": {"brand": "Updated"}})
        self.assertEqual(Store(self.temp.name).get("sample")["brief"]["brand"], "Updated")
        self.assertNotEqual(before["revision"], after["revision"])
        with self.assertRaisesRegex(ContractError, "Revision changed"):
            self.store.change("sample", before["revision"], "brief", {"brief": {"brand": "Stale"}})
        with self.assertRaises(ContractError):
            self.store.create("../escape", "15s-reel", {})
        with self.assertRaises(ContractError):
            self.store.create("sample", "15s-reel", {})

    def test_blocked_stage_leaves_current_state(self):
        before = self.store.create("sample", "15s-reel", {"brand": "Brand"})
        with self.assertRaisesRegex(ContractError, "Brief needs"):
            self.store.change(
                "sample", before["revision"], "stage", {"output": {"summary": "Test", "items": ["test"]}}
            )
        self.assertEqual(self.store.get("sample")["revision"], before["revision"])
        self.assertEqual(self.store.get("sample")["artifacts"], {})


class ReleaseIntegration(StorageTestCase):
    def prepared(self, project="release"):
        from studio.demo import load_demo
        from studio.media_import import sha_file
        from studio.store import picture_revision

        state = load_demo(self.store, project, with_assets=False)
        with self.store.connection(write=True) as db:
            private = self.store._load(db, project)
            private["demo"] = False
            self.store._commit(db, private)
        state = self.store.get(project)
        attempt = self.store.reserve(project, state["revision"], "render")
        ident = attempt["attempt"]["id"]
        folder = self.store.path(project, "renders", ident)
        folder.mkdir(parents=True)
        # Fixture files exercise integrity and delivery logic only.
        names = ["master-9x16.mp4", "master-1x1.mp4", "master-16x9.mp4"]
        for name in names:
            (folder / name).write_bytes(b"test render")
        return self.store.finish(
            project,
            ident,
            "succeeded",
            render={
                "files": names,
                "verified": True,
                "stats": {},
                "folder": f"renders/{ident}",
                "hashes": {name: sha_file(folder / name) for name in names},
                "input": picture_revision(attempt),
            },
        )

    def reviewed(self, state):
        from studio.contracts import SCORES

        state = self.store.change(
            state["id"],
            state["revision"],
            "stage",
            {"output": {"summary": "Fixture QA", "items": ["Test hashes"]}},
        )
        return self.store.change(
            state["id"],
            state["revision"],
            "review",
            {
                "verdict": "pass",
                "reviewer": "Fixture reviewer",
                "notes": "Test only",
                "scores": dict.fromkeys(SCORES, 8),
            },
        )

    def test_release_blocks_stale_approval_and_modified_media(self):
        import json
        import zipfile

        state = self.prepared()
        project = state["id"]
        with self.assertRaisesRegex(ContractError, "Human approval"):
            self.store.build_files(project, state["revision"], release=True)
        state = self.reviewed(state)
        with self.assertRaisesRegex(ContractError, "different person"):
            self.store.change(project, state["revision"], "approve", {"reviewer": "Fixture reviewer"})
        state = self.store.change(project, state["revision"], "approve", {"reviewer": "Fixture approver"})
        state = self.store.build_files(project, state["revision"], release=True)
        private = self.store.get(project, raw=True)
        with zipfile.ZipFile(self.store.file_path(private, state["release"]["file"])) as bundle:
            manifest = json.loads(bundle.read("file-hash-manifest.json"))
            self.assertEqual(set(bundle.namelist()) - {"file-hash-manifest.json"}, set(manifest["sha256"]))
        frame = self.store.file_path(private, "master-9x16.mp4")
        frame.write_bytes(b"modified")
        with self.assertRaisesRegex(ContractError, "Rendered files changed"):
            self.store.build_files(project, state["revision"], release=True)
        new = self.store.change(project, state["revision"], "finding", {"time": 1.5, "text": "Review again."})
        self.assertIsNone(new["approval"])
        self.assertIsNone(new["release"])

    def test_concurrent_reserve_and_cancellation(self):
        from concurrent.futures import ThreadPoolExecutor

        state = self.prepared("race")
        project = state["id"]

        def attempt():
            try:
                return self.store.reserve(project, state["revision"], "render")
            except ContractError:
                return None

        with ThreadPoolExecutor(max_workers=2) as pool:
            attempts = [result for result in pool.map(lambda _: attempt(), range(2)) if result]
        self.assertEqual(len(attempts), 1)
        active = self.store.get(project)
        active = self.store.change(project, active["revision"], "cancel", {})
        final = self.store.finish(project, active["attempt"]["id"], "failed")
        self.assertEqual(final["attempt"]["status"], "cancelled")
        self.assertEqual(Store(self.temp.name).get(project)["render"], state["render"])

    def test_rights_and_timing_block_output(self):
        state = self.prepared("gates")
        payload = {key: state[key] for key in ("shots", "hooks", "selectedHook", "tracks")}
        payload["shots"][-2]["durationMs"] -= 1000
        payload["shots"][-1]["durationMs"] += 1000
        revised = self.store.change("gates", state["revision"], "storyboard", payload)
        self.assertIn("reel: CTA starts before the approved window.", revised["issues"])
        self.assertIsNone(revised["render"])
        with self.assertRaisesRegex(ContractError, "wrong role"):
            payload["shots"][0]["asset"] = "missing"
            self.store.change("gates", revised["revision"], "storyboard", payload)

    def test_unsafe_paths_and_media_are_rejected(self):
        import base64
        from pathlib import Path

        state = self.store.create("safe", "15s-reel", {})
        payload = {"role": "packshot", "name": "test.png", "data": base64.b64encode(b"<script>").decode()}
        with self.assertRaisesRegex(ContractError, "signature"):
            self.store.change("safe", state["revision"], "import", payload)
        with self.assertRaisesRegex(ContractError, "filename"):
            self.store.change("safe", state["revision"], "import", {**payload, "name": "../escape.png"})
        path = Path(self.temp.name) / "projects" / "safe"
        path.mkdir(parents=True, exist_ok=True)
        (path / "outside").symlink_to(Path(self.temp.name).parent, target_is_directory=True)
        with self.assertRaises(ContractError):
            self.store.path("safe", "outside", "elsewhere")

    def test_draft_report_escapes_operator_text_and_survives_restart(self):
        state = self.store.create("script", "15s-reel", {"brand": "<script>alert(1)</script>"})
        state = self.store.build_files("script", state["revision"])
        fresh = Store(self.temp.name)
        report = fresh.file_path(fresh.get("script", raw=True), "super-ads-report.html").read_text()
        self.assertIn("&lt;script&gt;", report)
        self.assertNotIn("<script>", report)

    def test_interrupted_worker_recovers_at_checkpoint(self):
        from unittest.mock import patch

        state = self.prepared("interrupt")
        self.store.reserve("interrupt", state["revision"], "render")
        with patch("studio.store.alive", return_value=False):
            recovered = Store(self.temp.name).get("interrupt")
        self.assertEqual(recovered["attempt"]["status"], "interrupted")
        self.assertIn("edit", recovered["artifacts"])
        self.assertEqual(recovered["render"], state["render"])

    def test_provider_timeout_locks_retry_and_redacts_key(self):
        import os
        from unittest.mock import patch

        from studio.demo import BRIEF
        from studio.provider import ProviderFailure, run_provider

        state = self.store.create("provider", "15s-reel", BRIEF)

        def timeout(*_):
            raise ProviderFailure("ambiguous", "Outcome unknown.")

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-secret"}):
            with self.assertRaisesRegex(ContractError, "allow-provider"):
                run_provider(self.store, "provider", state["revision"], "gpt-4.1-mini", False, timeout)
            revised = run_provider(self.store, "provider", state["revision"], "gpt-4.1-mini", True, timeout)
            with self.assertRaisesRegex(ContractError, "ambiguous"):
                run_provider(self.store, "provider", revised["revision"], "gpt-4.1-mini", True, timeout)
        self.assertEqual(revised["providerCalls"], 1)
        self.assertNotIn("test-secret", str(self.store.get("provider", raw=True)))

    def test_provider_response_rejects_actions_and_malformed_data(self):
        import io
        import json

        from studio.demo import BRIEF
        from studio.provider import ProviderFailure, request_stage

        self.store.create("request", "15s-reel", BRIEF)
        state = self.store.get("request", raw=True)

        def forged(request, timeout):
            payload = json.loads(request.data)
            self.assertEqual(payload["tools"], [])
            self.assertEqual(timeout, 30)
            return io.BytesIO(b'{"status":"completed","output":[{"type":"shell_call"}]}')

        with self.assertRaisesRegex(ProviderFailure, "contract"):
            request_stage(state, self.store._next(state), "gpt-4.1-mini", "test-secret", forged)
