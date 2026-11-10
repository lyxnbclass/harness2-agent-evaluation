"""Behavioral checks for Stage 03 trajectory evidence."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from experiments.evaluators.stage03_trace import build_artifacts, redact, replay
from experiments.evaluators.bad_case_registry import candidate_from_result
from experiments.evaluators.trace_validator import validate_trace


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "datasets" / "stage02_multitool_cases.jsonl"
FIXTURES = ROOT / "datasets" / "stage02_fake_decisions.jsonl"


def event(step, message):
    return {"step": step, "timestamp": "2026-01-01T00:00:00+00:00", "elapsed_ms": 0, "message": message}


class TraceValidatorTests(unittest.TestCase):
    def test_resolved_case_can_have_unauthorized_tool(self):
        rows = build_artifacts(CASES, FIXTURES, "test-run")
        case = next(row for row in rows if row["case_id"] == "dev-08")
        self.assertEqual(case["outcome"], "resolved")
        self.assertEqual(case["findings"][0]["code"], "unauthorized_tool")
        self.assertEqual(case["findings"][0]["step"], 1)
        self.assertNotIn("trace", case)
        self.assertIsNone(case["harness_sha"])
        self.assertTrue(all("timestamp" in item for item in case["events"]))
        self.assertEqual([item["event_type"] for item in case["events"]],
                         ["input", "tool_call", "tool_result", "final"])

    def test_wrong_final_is_not_mislabeled_tool_failure(self):
        rows = build_artifacts(CASES, FIXTURES, "test-run")
        case = next(row for row in rows if row["case_id"] == "val-04")
        self.assertEqual(case["outcome"], "failed")
        self.assertEqual(case["events"][2]["message"]["content"], "4")
        self.assertEqual(case["events"][3]["message"]["content"], "5")
        self.assertEqual(case["findings"], [])

    def test_infra_error_has_no_inferred_correctness_or_trace(self):
        rows = build_artifacts(CASES, FIXTURES, "test-run")
        case = next(row for row in rows if row["case_id"] == "val-08")
        self.assertEqual(case["outcome"], "infra_error")
        self.assertEqual(case["events"], [])
        self.assertEqual(case["findings"], [])
        candidate = candidate_from_result(case)
        self.assertEqual(candidate.category, "infrastructure")
        self.assertIsNone(candidate.first_evidence_step)
        self.assertIsNone(candidate.root_cause_hypothesis)

    def test_schema_retry_budget_required_and_order(self):
        events = [
            event(0, {"role": "user", "content": "go"}),
            event(1, {"role": "assistant", "tool_call": {"name": "add", "args": {"a": True, "b": 2}}}),
            event(2, {"role": "assistant", "tool_call": {"name": "add", "args": {"a": True, "b": 2}}}),
            event(3, {"role": "tool", "name": "add", "error": "invalid args"}),
        ]
        findings = validate_trace(events, {
            "allowed_tools": ["add"], "required_tools": ["uppercase"], "max_steps": 1,
        }, observed_status="max_steps")
        codes = {finding.code for finding in findings}
        self.assertTrue({"invalid_args", "repeated_call", "missing_tool_result",
                         "tool_error", "step_limit_exceeded", "step_budget_exhausted",
                         "required_tool_missing"}.issubset(codes))

    def test_secret_scrubbing_and_replay_filter(self):
        self.assertEqual(redact({"api_key": "abc", "args": {"text": "token=abc"}}),
                         {"api_key": "<redacted>", "args": {"text": "token=<redacted>"}})
        self.assertEqual(redact("Authorization: Bearer abc"), "Authorization: <redacted>")
        rows = build_artifacts(CASES, FIXTURES, "test-run")
        with TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            import json
            path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
            lines = replay(path, "test-run", "dev-08")
            self.assertTrue(any("unauthorized_tool at step 1" in line for line in lines))
            self.assertFalse(any("val-04" in line for line in lines))
            with self.assertRaisesRegex(ValueError, "no events"):
                replay(path, "other-run")

    def test_registry_keeps_expected_rejection_for_review_without_claiming_failure(self):
        rows = build_artifacts(CASES, FIXTURES, "test-run")
        case = next(row for row in rows if row["case_id"] == "dev-06")
        candidate = candidate_from_result(case)
        self.assertEqual((candidate.outcome, candidate.category),
                         ("resolved", "trajectory_review"))
        self.assertIsNone(candidate.root_cause_hypothesis)


if __name__ == "__main__":
    unittest.main()
