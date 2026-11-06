"""Contract for the deterministic eval entry point."""

import json
import subprocess
import sys
import unittest
from pathlib import Path


class EvalEntryPointTests(unittest.TestCase):
    def test_keyless_suite_covers_routing_handoffs_and_adversarial_cases(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "-m", "evals.run", "--json"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        evidence = json.loads(result.stdout)
        self.assertEqual(evidence["mode"], "keyless-fixtures")
        self.assertEqual(evidence["liveTrials"], 0)
        self.assertEqual(evidence["failed"], 0)
        self.assertEqual(evidence["groups"]["routing"], 22)
        self.assertEqual(evidence["groups"]["workflow"], 6)
        self.assertGreaterEqual(evidence["groups"]["adversarial"], 8)
        self.assertEqual(len(evidence["cases"]), evidence["passed"])
