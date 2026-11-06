"""Transactional project history, stage attempts and revision-bound approval."""

import base64
import copy
import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .contracts import (
    SCORES,
    WORKFLOWS,
    ContractError,
    actual_metrics,
    brief_data,
    brief_issues,
    canonical,
    digest,
    fields,
    integer,
    project_id,
    require,
    safe_name,
    stage_output,
    stage_plan,
    storyboard,
    string,
    timeline_issues,
    rights_issues,
)
from .media_import import ingest, safe_path, sha_file

ACTIVE = {"running", "cancelling"}
PRESERVE = ("brief", "workflow", "shots", "hooks", "selectedHook", "tracks", "cuts", "assets")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def picture_revision(state):
    return digest({key: state[key] for key in PRESERVE})


def blank(project, workflow, brief, demo=False):
    brief = brief_data(brief)
    stage_plan(workflow, brief, [])
    return {
        "id": project,
        "workflow": workflow,
        "brief": brief,
        "demo": demo,
        "revision": 1,
        "updatedAt": now(),
        "artifacts": {},
        "shots": [],
        "assets": [],
        "hooks": [],
        "selectedHook": "",
        "tracks": [],
        "cuts": {},
        "findings": [],
        "metrics": [],
        "render": None,
        "hookPreviews": {},
        "review": None,
        "approval": None,
        "attempt": None,
        "report": None,
        "release": None,
        "providerCalls": 0,
        "trace": [],
    }


def public(state):
    result = copy.deepcopy(state)
    result["stages"] = stage_plan(state["workflow"], state["brief"], state["metrics"])
    result["profiles"] = WORKFLOWS[state["workflow"]][1]
    result["primaryCut"] = next(iter(result["profiles"]))
    result["nextStage"] = next((s["id"] for s in result["stages"] if s["id"] not in state["artifacts"]), None)
    result["issues"] = brief_issues(state) + timeline_issues(state) + rights_issues(state)
    for name in ("render", "report", "release"):
        if result[name]:
            result[name].pop("folder", None)
    for hook in result["hookPreviews"].values():
        hook.pop("folder", None)
    return result


def trace(state, action, **details):
    state["trace"] = (
        state["trace"]
        + [
            {
                "run": state["id"],
                "revision": state["revision"] + 1,
                "at": now(),
                "action": action,
                **details,
            }
        ]
    )[-180:]


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


class Store:
    def __init__(self, root):
        self.root = Path(root).absolute()
        require(not self.root.is_symlink(), "Storage root must be a real directory.")
        self.root.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.database = safe_path(self.root, "studio.sqlite3")
        with self.connection() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, state TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS revisions (
                    id TEXT NOT NULL, number INTEGER NOT NULL, state TEXT NOT NULL,
                    PRIMARY KEY (id, number)
                );
            """)
        self.database.chmod(0o600)

    @contextmanager
    def connection(self, write=False):
        require(not self.database.is_symlink(), "Unsafe database path.")
        db = sqlite3.connect(self.database, timeout=10)
        try:
            if write:
                db.execute("BEGIN IMMEDIATE")
            with db:
                yield db
        finally:
            db.close()

    @staticmethod
    def _load(db, project):
        row = db.execute("SELECT state FROM projects WHERE id = ?", (project_id(project),)).fetchone()
        require(row, "Project does not exist.")
        return json.loads(row[0])

    @staticmethod
    def _record(db, state):
        data = canonical(state)
        db.execute(
            "INSERT INTO projects VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET state = excluded.state",
            (state["id"], data),
        )
        db.execute("INSERT INTO revisions VALUES (?, ?, ?)", (state["id"], state["revision"], data))

    def _recover(self, db, state):
        attempt = state["attempt"]
        if attempt and attempt["status"] in ACTIVE and not alive(attempt["pid"]):
            if attempt["kind"] in {"render", "hook"}:
                from shutil import rmtree

                workspace = self.path(state["id"], "renders")
                folder = safe_path(workspace, attempt["id"])
                if folder.is_dir():
                    rmtree(folder)
            attempt["status"] = "ambiguous" if attempt["kind"] == "provider" else "interrupted"
            attempt["message"] = (
                "The previous worker exited before committing. The last checkpoint is intact."
            )
            trace(state, "recovered", attempt=attempt["id"], status=attempt["status"])
            self._commit(db, state)
        return state

    def _commit(self, db, state):
        state["revision"] += 1
        state["updatedAt"] = now()
        self._record(db, state)

    def create(self, project, workflow, brief, demo=False):
        state = blank(project_id(project), workflow, brief, demo)
        with self.connection(write=True) as db:
            require(
                not db.execute("SELECT 1 FROM projects WHERE id = ?", (project,)).fetchone(),
                "Project ID already exists. Choose a different ID.",
            )
            self.path(project)
            self._record(db, state)
        return public(state)

    def get(self, project, raw=False):
        with self.connection(write=True) as db:
            state = self._recover(db, self._load(db, project))
        return state if raw else public(state)

    def list(self):
        with self.connection() as db:
            projects = [json.loads(row[0]) for row in db.execute("SELECT state FROM projects ORDER BY id")]
        return [
            {key: item[key] for key in ("id", "revision", "brief", "workflow", "demo")} for item in projects
        ]

    def history(self, project):
        with self.connection() as db:
            return [
                {"revision": n, "updatedAt": json.loads(raw)["updatedAt"]}
                for n, raw in db.execute(
                    "SELECT number,state FROM revisions WHERE id = ? ORDER BY number", (project_id(project),)
                )
            ]

    def path(self, project, *parts):
        return safe_path(self.root, "projects", project_id(project), *parts)

    def asset_path(self, state, asset_id):
        asset = next((item for item in state["assets"] if item["id"] == asset_id), None)
        require(asset is not None, "Asset does not exist.")
        path = self.path(state["id"], "assets", asset["id"] + asset["ext"])
        require(sha_file(path) == asset["sha256"], "Stored asset bytes changed.")
        return path

    def _validate_assets(self, state):
        for asset in state["assets"]:
            self.asset_path(state, asset["id"])

    def file_path(self, state, filename):
        safe_name(filename)
        records = [state[key] for key in ("report", "release", "render")]
        records.extend(state["hookPreviews"].values())
        for info in records:
            if info and (filename in info.get("files", []) or filename == info.get("file")):
                path = self.path(state["id"], *info["folder"].split("/"), filename)
                expected = info.get("hashes", {}).get(filename)
                require(
                    expected and sha_file(path) == expected, "Export bytes changed. Regenerate the files."
                )
                return path
        raise ContractError("File is unavailable for this revision.")

    @staticmethod
    def _next(state):
        return next(
            (
                stage
                for stage in stage_plan(state["workflow"], state["brief"], state["metrics"])
                if stage["id"] not in state["artifacts"]
            ),
            None,
        )

    @staticmethod
    def _invalidate(state, from_stage=None, media=True):
        if from_stage:
            order = [s["id"] for s in stage_plan(state["workflow"], state["brief"], state["metrics"])]
            if from_stage in order:
                for stage in order[order.index(from_stage) :]:
                    state["artifacts"].pop(stage, None)
        if media:
            state["render"] = None
            state["hookPreviews"] = {}
        state.update(review=None, approval=None, release=None, report=None)

    def _stage(self, state, output, provider="manual"):
        next_stage = self._next(state)
        require(next_stage, "Every routed stage is already complete.")
        stage = next_stage["id"]
        if stage == "strategy":
            require(not brief_issues(state), " ".join(brief_issues(state)))
        if stage in {"capture", "edit", "qa"}:
            issues = timeline_issues(state) + rights_issues(state)
            require(not issues, " ".join(issues))
        if stage == "qa":
            self._require_render(state)
        if stage == "performance":
            require(
                state["metrics"] and state["approval"] and not state["demo"],
                "Performance requires observed metrics and approved client work.",
            )
        value = stage_output(output, stage)
        state["artifacts"][stage] = {
            **value,
            "role": next_stage["role"],
            "skills": next_stage["skills"],
            "provider": provider,
            "id": digest([state["id"], stage, state["revision"], value]),
            "at": now(),
        }
        state["report"] = None
        trace(
            state,
            "stage-accepted",
            stage=stage,
            skills=next_stage["skills"],
            provider=provider,
            artifact=state["artifacts"][stage]["id"],
        )

    def _require_render(self, state):
        issues = brief_issues(state) + timeline_issues(state) + rights_issues(state)
        require(not issues, " ".join(issues))
        self._validate_assets(state)
        render = state["render"]
        require(
            render and render["verified"] and render["input"] == picture_revision(state),
            "Render and verify the current campaign first.",
        )
        require(
            render["hashes"] and set(render["files"]) == set(render["hashes"]),
            "Render manifest is incomplete.",
        )
        for name, expected in render["hashes"].items():
            path = self.path(state["id"], *render["folder"].split("/"), name)
            require(sha_file(path) == expected, "Rendered files changed. Render again.")
        return render

    def change(self, project, revision, action, value):
        with self.connection(write=True) as db:
            state = self._recover(db, self._load(db, project))
            require(
                type(revision) is int and revision == state["revision"], "Revision changed. Reload and retry."
            )
            active = state["attempt"] and state["attempt"]["status"] in ACTIVE
            require(not active or action == "cancel", "A project operation is already running.")
            require(isinstance(value, dict), "Expected an action object.")
            if action == "brief":
                new = brief_data(value.get("brief"))
                if new == state["brief"]:
                    return public(state)
                state["brief"] = new
                self._invalidate(state, "strategy")
            elif action == "storyboard":
                changes = storyboard(state, value)
                if all(state[key] == val for key, val in changes.items()):
                    return public(state)
                state.update(changes)
                self._invalidate(state, "capture" if state["workflow"] == "ugc-creator" else "shots")
            elif action == "import":
                require(len(state["assets"]) < 64, "Project asset limit reached.")
                asset = ingest(value, self.path(project, "assets"))
                if any(old["id"] == asset["id"] for old in state["assets"]):
                    return public(state)
                state["assets"].append(asset)
                self._invalidate(state, "qa")
                trace(state, "asset-validated", asset=asset["id"], role=asset["role"])
            elif action == "stage":
                self._stage(state, value.get("output"))
            elif action == "finding":
                maximum = max(0, sum(shot["durationMs"] for shot in state["shots"]) - 1)
                at = value.get("time")
                require(
                    type(at) in (int, float) and 0 <= at * 1000 <= maximum, "Finding time is outside the cut."
                )
                require(len(state["findings"]) < 100, "Finding limit reached.")
                state["findings"].append(
                    {"time": at, "text": string(value.get("text"), "Finding", 1500, True)}
                )
                self._invalidate(state, media=False)
            elif action == "review":
                render = self._require_render(state)
                require("qa" in state["artifacts"], "Complete the QA role handoff before independent review.")
                verdict = value.get("verdict")
                require(verdict in ("pass", "changes"), "Choose pass or changes.")
                scores = fields(value.get("scores", {}), SCORES, "Review scores")
                scores = {key: integer(score, key, 1, 10) for key, score in scores.items()}
                require(
                    verdict != "pass" or len(scores) == len(SCORES) and min(scores.values()) >= 7,
                    "Passing review requires all six scores at 7 or above.",
                )
                self._invalidate(state, media=False)
                state["review"] = {
                    "reviewer": string(value.get("reviewer"), "Reviewer", 100, True),
                    "verdict": verdict,
                    "notes": string(value.get("notes"), "Review notes", 2500, True),
                    "scores": scores,
                    "binding": digest(render["hashes"]),
                    "revision": state["revision"] + 1,
                }
            elif action == "approve":
                render = self._require_render(state)
                review = state["review"]
                reviewer = string(value.get("reviewer"), "Human approver", 100, True)
                require(
                    review and review["verdict"] == "pass" and review["binding"] == digest(render["hashes"]),
                    "The exact renders need a passing independent review.",
                )
                require(
                    reviewer.casefold() != review["reviewer"].casefold(),
                    "Human approval requires a different person from the independent reviewer.",
                )
                state["approval"] = {
                    "reviewer": reviewer,
                    "binding": digest(render["hashes"]),
                    "input": picture_revision(state),
                    "revision": state["revision"] + 1,
                    "kind": "demo-approval-test" if state["demo"] else "human",
                }
                state.update(release=None, report=None)
            elif action == "metrics":
                require(not state["demo"] and state["approval"], "Metrics require approved client work.")
                state["metrics"] = actual_metrics(value.get("metrics"))
                state["artifacts"].pop("performance", None)
                state["report"] = None
            elif action == "cancel":
                require(
                    active and state["attempt"]["kind"] in {"render", "hook"},
                    "There is no cancellable render.",
                )
                state["attempt"]["status"] = "cancelling"
            elif action == "resolve":
                require(
                    state["attempt"] and state["attempt"]["status"] == "ambiguous",
                    "There is no ambiguous attempt to resolve.",
                )
                require(value.get("acknowledge") is True, "Acknowledge the previous call before retrying.")
                state["attempt"]["status"] = "resolved"
            else:
                raise ContractError("Unknown studio action.")
            trace(state, action)
            self._commit(db, state)
            return public(state)

    def reserve(self, project, revision, kind, *, provider=None):
        require(kind in {"render", "hook", "provider"}, "Unsupported attempt.")
        with self.connection(write=True) as db:
            state = self._recover(db, self._load(db, project))
            require(revision == state["revision"], "Revision changed. Reload and retry.")
            attempt = state["attempt"]
            require(not attempt or attempt["status"] not in ACTIVE, "A project operation is already running.")
            require(
                not attempt or attempt["status"] != "ambiguous",
                "Resolve the ambiguous provider outcome first.",
            )
            if kind == "render":
                require("edit" in state["artifacts"], "Complete the editor handoff before rendering.")
                issues = brief_issues(state) + timeline_issues(state) + rights_issues(state)
                require(not issues, " ".join(issues))
                self._validate_assets(state)
            if kind == "hook":
                require(state["shots"], "Add a storyboard before rendering a hook.")
                require(not rights_issues(state), " ".join(rights_issues(state)))
                self._validate_assets(state)
            if kind == "provider":
                require(state["providerCalls"] < 12, "Project provider-call budget exhausted.")
                stage = self._next(state)
                require(
                    stage and stage["id"] not in {"capture", "qa", "performance"},
                    "This handoff requires local operator evidence.",
                )
                require(not brief_issues(state), " ".join(brief_issues(state)))
                state["providerCalls"] += 1
            identifier = uuid4().hex
            state["attempt"] = {
                "id": identifier,
                "kind": kind,
                "status": "running",
                "pid": os.getpid(),
                "provider": provider or "local",
                "message": "",
            }
            trace(state, "attempt-reserved", attempt=identifier, kind=kind, provider=provider or "local")
            self._commit(db, state)
        return state

    def finish(self, project, identifier, status, *, message="", render=None, hook=None, output=None):
        with self.connection(write=True) as db:
            state = self._load(db, project)
            attempt = state["attempt"]
            require(
                attempt and attempt["id"] == identifier and attempt["status"] in ACTIVE,
                "Attempt no longer owns this project.",
            )
            if attempt["status"] == "cancelling":
                status = "cancelled"
            if status == "succeeded":
                if render:
                    self._invalidate(state, "qa", media=False)
                    state["render"] = render
                if hook:
                    state["hookPreviews"][hook["hook"]] = hook
                if output is not None:
                    self._stage(state, output, attempt["provider"])
            attempt.update(status=status, message=message)
            trace(state, "attempt-finished", attempt=identifier, status=status)
            self._commit(db, state)
            return public(state)

    def build_files(self, project, revision, release=False):
        from .reports import build_report, build_release

        with self.connection(write=True) as db:
            state = self._recover(db, self._load(db, project))
            require(revision == state["revision"], "Revision changed. Reload and retry.")
            require(
                not state["attempt"] or state["attempt"]["status"] not in ACTIVE,
                "Wait for the current operation.",
            )
            folder = f"reports/{uuid4().hex}"
            path = self.path(project, *folder.split("/"))
            if release:
                render = self._require_render(state)
                approval = state["approval"]
                require(not state["demo"], "Fictional demo projects can generate draft reports only.")
                require(
                    approval
                    and approval["kind"] == "human"
                    and approval["input"] == picture_revision(state)
                    and approval["binding"] == digest(render["hashes"]),
                    "Human approval of the exact revision and render hashes is required.",
                )
                name = build_release(state, path, self.path(project, *render["folder"].split("/")))
                state["release"] = {"file": name, "folder": folder, "hashes": {name: sha_file(path / name)}}
            else:
                artwork = None
                if state["render"] and "contact-9x16.jpg" in state["render"]["files"]:
                    contact = self.file_path(state, "contact-9x16.jpg")
                    if contact.stat().st_size <= 2 * 1024 * 1024:
                        artwork = "data:image/jpeg;base64," + base64.b64encode(contact.read_bytes()).decode()
                files = build_report(state, path, artwork)
                state["report"] = {
                    "files": files,
                    "folder": folder,
                    "hashes": {name: sha_file(path / name) for name in files},
                }
            trace(state, "delivery-built" if release else "report-built")
            self._commit(db, state)
            return public(state)
