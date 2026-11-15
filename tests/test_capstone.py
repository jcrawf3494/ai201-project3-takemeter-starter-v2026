"""Unit tests for the new opinion input capability (no model download)."""
import json
import tempfile
import unittest
from pathlib import Path

from takemeter_inference import InvalidOpinion, classify_opinion


class OpinionInputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.log = Path(self.temp.name) / "events.jsonl"
        self.calls = []

    def tearDown(self):
        self.temp.cleanup()

    def predictor(self, opinion):
        self.calls.append(opinion)
        return "proposal", 0.82

    def records(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def test_valid_input_returns_label_confidence_and_private_log(self):
        result = classify_opinion(" Schools should teach cooking ", self.predictor, self.log)
        self.assertEqual(result, {"label": "proposal", "confidence": 0.82})
        self.assertEqual(self.calls, ["Schools should teach cooking"])
        record = self.records()[0]
        self.assertEqual(record["status"], "ok")
        self.assertIsInstance(record["duration_ms"], float)
        self.assertIn("timestamp", record)
        self.assertIn("sha256", record["input"])
        self.assertNotIn("text", record["input"])

    def test_invalid_values_are_logged_without_predicting(self):
        invalid = ["", "  ", None, "X" * 3001, " Y" * 3000, "Z" * 4000]
        for value in invalid:
            with self.assertRaises(InvalidOpinion):
                classify_opinion(value, self.predictor, self.log)
        self.assertEqual(self.calls, [])
        self.assertEqual(len(self.records()), len(invalid))
        self.assertTrue(all(r["status"] == "invalid_input" for r in self.records()))

    def test_model_failure_is_logged_without_sensitive_exception_details(self):
        def broken(_):
            raise OSError("private token must not appear in the log")
        with self.assertRaises(OSError):
            classify_opinion("A post", broken, self.log)
        record = self.records()[0]
        self.assertEqual(record["status"], "model_error")
        self.assertNotIn("private token", json.dumps(record))

    def test_rejects_invalid_model_output(self):
        with self.assertRaises(RuntimeError):
            classify_opinion("A post", lambda _: ("unknown", 0.9), self.log)
        self.assertEqual(self.records()[0]["status"], "model_error")

    def test_rejects_nonfinite_confidence(self):
        with self.assertRaises(RuntimeError):
            classify_opinion("A post", lambda _: ("proposal", float("nan")), self.log)
        self.assertEqual(self.records()[0]["status"], "model_error")


if __name__ == "__main__":
    unittest.main()
