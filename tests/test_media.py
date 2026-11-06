"""Keyless render contract tests, with real media checks opt-in."""

import tempfile
import unittest
from pathlib import Path

from studio.render import (
    FORMAT_SIZES,
    PreviewError,
    RenderCancelled,
    render_campaign,
    preview_html,
    reference_html,
    srt_captions,
)

HOOK = {
    "id": "hook-01",
    "durationMs": 2400,
    "beat": "hook",
    "style": "citation",
    "title": "Evict the keys?",
    "caption": "The keys are on notice.",
    "action": "The citation lands.",
    "audio": "Key click.",
    "asset": "",
    "reference": "reference-01",
    "evidence": "",
    "trimMs": 0,
}
SETUP = {
    **HOOK,
    "id": "setup-01",
    "durationMs": 2600,
    "beat": "setup",
    "style": "clipboard",
    "title": "One loud tenant.",
    "reference": "",
}
STATE = {
    "id": "quiet-hours",
    "revision": 1,
    "brief": {"brand": "HUSH", "product": "Desk Mat"},
    "shots": [HOOK, SETUP],
    "assets": [
        {
            "id": "reference-01",
            "role": "reference",
            "ext": ".png",
            "name": "Studio notes",
        }
    ],
    "hooks": [
        {"id": "a", "title": "Evict the keys?", "variable": "opening"},
        {"id": "b", "title": "Who called security?", "variable": "opening"},
    ],
    "selectedHook": "a",
    "tracks": [],
}


class MediaContract(unittest.TestCase):
    def test_preview_uses_exact_shot_boundary_and_ratio(self):
        self.assertEqual(FORMAT_SIZES["16x9"], (1920, 1080))
        self.assertIn("Who called security?", preview_html(STATE, 0, hook="b"))
        self.assertIn("One loud tenant.", preview_html(STATE, 2400, "16x9"))
        self.assertIn("width=1920", preview_html(STATE, 2400, "16x9"))
        with self.assertRaises(PreviewError):
            preview_html(STATE, 5001)

    def test_preview_escapes_story_and_excludes_planning_assets(self):
        state = {
            **STATE,
            "hooks": [],
            "selectedHook": "",
            "shots": [
                {
                    **HOOK,
                    "title": "<img onerror=alert(1)>",
                    "asset": "reference-01",
                }
            ],
        }
        html = preview_html(state, 0, media_url=lambda a: "/media/" + a)
        self.assertIn("&lt;img onerror=alert(1)&gt;", html)
        self.assertNotIn("/media/reference-01", html)

    def test_captions_follow_editable_timeline(self):
        self.assertIn("00:00:02,400 --> 00:00:05,000", srt_captions(STATE))
        self.assertIn("The keys are on notice.", srt_captions(STATE))

    def test_cancelled_render_has_no_publishable_files(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            with self.assertRaises(RenderCancelled):
                render_campaign(STATE, root, root / "out", root / "cache", lambda: True)
            self.assertFalse((root / "out").exists())

    def test_reference_has_continuity_and_no_external_asset_requests(self):
        with tempfile.TemporaryDirectory() as path:
            html = reference_html(STATE, "setup-01", Path(path))
        self.assertIn("The citation lands.", html)
        self.assertIn("HUSH", html)
        self.assertNotIn('src="https:', html)


if __name__ == "__main__":
    unittest.main()
