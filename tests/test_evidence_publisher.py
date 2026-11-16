"""Tests for local evidence publication; no real model or private data needed."""
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path

from measure_extension import OPINIONS
from publish_capstone_evidence import publish


class EvidencePublisherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.original_dir = Path.cwd()
        os.chdir(self.temp.name)
        Path("logs").mkdir()
        Path("README.md").write_text(
            "Existing project notes\n\n## Capstone\n\n"
            "**Instrumentation**\n\nExisting instrumentation.\n\n"
            "**What It Costs**\n\nExisting cost.\n\n"
            "**Run Log and Verdicts**\n\nExisting before results.\n\n"
            "**The Improvement**\n\nPending improvement.\n\n"
            "**What's Still Broken**\n\nPending hosting.\n",
            encoding="utf-8",
        )
        rows = []
        for opinion in OPINIONS:
            rows.append(self.record(opinion, "ok", {"label": "proposal", "confidence": 0.75}))
        rows.append(self.record("", "invalid_input", None))
        with Path("logs/before_trial_events.jsonl").open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row) + "\n")
        for phase, avg in (("before", 0.0228), ("after", 0.0192)):
            results = {
                "phase": phase,
                "mean_wall_seconds_per_valid_request": avg,
                "trials": [
                    {"valid_predictions": "10/10", "invalid_rejections": "6/6",
                     "structured_logs": "16/16", "under_5_seconds": "10/10",
                     "model_agreement": "10/10"}
                    for _ in range(3)
                ],
            }
            Path(f"capstone_results_{phase}.json").write_text(json.dumps(results))

    def tearDown(self):
        os.chdir(self.original_dir)
        self.temp.cleanup()

    @staticmethod
    def record(value, status, output):
        return {
            "timestamp": "2026-11-15T12:00:00+00:00",
            "input": {"length": len(value),
                      "sha256": hashlib.sha256(value.encode("utf-8")).hexdigest(),
                      "text": "PRIVATE TEXT THAT MUST NOT APPEAR"},
            "status": status,
            "output": output,
            "error": "PRIVATE ERROR THAT MUST NOT APPEAR",
            "duration_ms": 22.8,
            "model": "PRIVATE MODEL PATH",
        }

    def test_before_inserts_actual_sanitized_logs(self):
        publish(False)
        output = Path("README.md").read_text()
        self.assertIn("Eleven actual sanitized JSONL entries", output)
        self.assertIn("Cooking classes should be required", output)
        self.assertIn("invalid_input", output)
        self.assertNotIn("PRIVATE", output)
        self.assertLess(output.index("**Instrumentation**"), output.index("Eleven actual"))
        self.assertLess(output.index("Eleven actual"), output.index("**What It Costs**"))

    def test_after_inserts_three_trial_table_and_comparison(self):
        publish(True)
        output = Path("README.md").read_text()
        self.assertIn("| Valid predictions | 10/10 | 10/10 | 10/10 | 10/10 | MET |", output)
        self.assertIn("0.0228", output)
        self.assertIn("0.0192", output)
        self.assertIn("**What's Still Broken**", output)
        self.assertNotIn("PRIVATE", output)
        self.assertLess(output.index("**The Improvement**"), output.index("**What's Still Broken**"))


if __name__ == "__main__":
    unittest.main()
