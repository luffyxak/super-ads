"""Exercise the legacy public CLI against a disposable copy of its source."""

import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "scripts").mkdir()
        shutil.copy2(ROOT / "scripts/new_ad.py", self.root / "scripts")
        shutil.copytree(
            ROOT / "examples/hyperframes-diwali-8s",
            self.root / "examples/hyperframes-diwali-8s",
            ignore=shutil.ignore_patterns(".hyperframes", "node_modules", "*.mp4", "gsap.min.js"),
        )
        self.outputs = self.root / "outputs"

    def scaffold(self, brand="Test Co", product="Desk mat", format="reel15", *flags):
        return subprocess.run(
            [
                sys.executable,
                str(self.root / "scripts/new_ad.py"),
                "--brand",
                brand,
                "--product",
                product,
                "--format",
                format,
                *flags,
            ],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

    def test_duplicate_preserves_edited_brief(self):
        self.assertEqual(self.scaffold().returncode, 0)
        brief = self.outputs / "test-co-desk-mat/brief.md"
        brief.write_text("Edited brief\n")
        duplicate = self.scaffold()
        self.assertEqual(brief.read_text(), "Edited brief\n")
        self.assertNotEqual(duplicate.returncode, 0)

    def test_concurrent_duplicates_reserve_one_output(self):
        with ThreadPoolExecutor(max_workers=2) as workers:
            runs = list(workers.map(lambda _: self.scaffold(), range(2)))
        self.assertEqual(sorted(run.returncode for run in runs), [0, 2])
        self.assertTrue((self.outputs / "test-co-desk-mat/brief.md").is_file())

    def test_normalized_slug_collision_refuses_existing_project(self):
        self.assertEqual(self.scaffold("Test & Co").returncode, 0)
        self.assertNotEqual(self.scaffold("Test+Co").returncode, 0)
        self.assertIn("Test &amp; Co", (self.outputs / "test-co-desk-mat/brief.md").read_text())

    def test_html_fields_are_literal_text(self):
        payload = '<img src=x onerror="alert(1)">'
        self.assertEqual(self.scaffold(payload, payload, "reel15", "--hyperframes").returncode, 0)
        project = next(self.outputs.iterdir())
        self.assertNotIn(payload, (project / "brief.md").read_text())
        for name in ("hook", "product", "cta"):
            html = (project / f"hyperframes/compositions/{name}.html").read_text()
            self.assertNotIn(payload, html)
            self.assertIn("&lt;img src=x", html)

    def test_cta_and_total_match_timing_contract(self):
        for format, duration in (("reel15", 15), ("tvc30", 30), ("launch10", 10)):
            with self.subTest(format=format):
                self.assertEqual(self.scaffold(format, "Desk mat", format, "--hyperframes").returncode, 0)
                project = self.outputs / f"{format}-desk-mat"
                html = (project / "hyperframes/index.html").read_text()
                cta = re.search(
                    r'id="cta"[\s\S]*?data-start="([\d.]+)"\s+data-duration="([\d.]+)"',
                    html,
                )
                start, hold = (float(value) for value in cta.groups())
                self.assertEqual(start, max(duration * 0.8, duration - 3))
                self.assertAlmostEqual(start + hold, duration)
                scene = (project / "hyperframes/compositions/cta.html").read_text()
                self.assertIn(
                    f'id="cta-sub" class="clip" data-start="0" data-duration="{hold:g}"',
                    scene,
                )
                csv_text = (project / "shot-list.csv").read_text()
                self.assertIn(f"{start:g}-{duration:g}s", csv_text)

    def test_rejects_unsafe_or_unbounded_input_before_writing(self):
        for brand in ("\tUnsafe", "Line\nbreak", "   ", "x" * 600):
            with self.subTest(brand=brand[:20]):
                self.assertNotEqual(self.scaffold(brand).returncode, 0)
                self.assertFalse(self.outputs.exists())

    def test_symlinked_outputs_are_refused(self):
        outside = self.root / "outside"
        outside.mkdir()
        self.outputs.symlink_to(outside, target_is_directory=True)
        self.assertNotEqual(self.scaffold().returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])

    def test_existing_project_symlink_is_refused(self):
        outside = self.root / "outside"
        outside.mkdir()
        self.outputs.mkdir()
        (self.outputs / "test-co-desk-mat").symlink_to(outside, target_is_directory=True)
        self.assertNotEqual(self.scaffold().returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])

    def test_traversal_like_display_name_stays_in_outputs(self):
        self.assertEqual(self.scaffold("../../outside").returncode, 0)
        self.assertTrue((self.outputs / "outside-desk-mat/brief.md").is_file())
        self.assertFalse((self.root / "outside").exists())

    def test_non_ascii_names_keep_distinct_slugs(self):
        for brand in ("चमक", "दीप"):
            self.assertEqual(self.scaffold(brand).returncode, 0)
        self.assertEqual(len(list(self.outputs.iterdir())), 2)

    def test_failed_hyperframes_scaffold_cleans_partial_project(self):
        (self.root / "examples/hyperframes-diwali-8s/package-lock.json").unlink()
        self.assertNotEqual(self.scaffold("Test Co", "Desk mat", "reel15", "--hyperframes").returncode, 0)
        self.assertEqual(list(self.outputs.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
