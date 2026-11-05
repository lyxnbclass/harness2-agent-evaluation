"""Integration checks for the deterministic Stage 02 teaching suite."""

import json
import unittest

from experiments.evaluators.metrics import summarize
from experiments.evaluators.stage02_demo import (
    DATASETS, call_is_schema_valid, run_suite,
)


CASES = DATASETS / "stage02_multitool_cases.jsonl"
FIXTURES = DATASETS / "stage02_fake_decisions.jsonl"


class Stage02DemoTests(unittest.TestCase):
    def test_all_splits_and_outcomes_are_exercised(self):
        metrics, artifacts = run_suite(CASES, FIXTURES, "test-run")
        self.assertEqual(len(metrics), 24)
        self.assertEqual(
            {split: sum(row["split"] == split for row in artifacts)
             for split in ("dev", "validation", "local-held-out")},
            {"dev": 8, "validation": 8, "local-held-out": 8},
        )
        self.assertEqual(summarize(metrics).counts, {
            "resolved": 19, "failed": 3, "infra_error": 1, "unscored": 1
        })

    def test_correct_final_answer_can_still_have_unsafe_tool_call(self):
        _, artifacts = run_suite(CASES, FIXTURES, "test-run")
        by_id = {row["case_id"]: row for row in artifacts}
        for case_id in ("dev-08", "val-07"):
            with self.subTest(case_id=case_id):
                row = by_id[case_id]
                self.assertEqual(row["outcome"], "resolved")
                self.assertEqual(row["unsafe_tool_calls"], 1)
                self.assertEqual(row["observed_status"], "completed")

    def test_two_cases_use_multiple_tools(self):
        _, artifacts = run_suite(CASES, FIXTURES, "test-run")
        by_id = {row["case_id"]: row for row in artifacts}
        self.assertEqual(by_id["dev-02"]["tool_calls"], 2)
        self.assertEqual(by_id["held-03"]["tool_calls"], 2)
        self.assertEqual(by_id["dev-02"]["observed_answer"], "AGENT:5")

    def test_schema_validation_rejects_bool_and_extra_fields(self):
        self.assertTrue(call_is_schema_valid({"name": "add", "args": {"a": 2, "b": 3}}))
        self.assertFalse(call_is_schema_valid({"name": "add", "args": {"a": True, "b": 3}}))
        self.assertFalse(call_is_schema_valid({
            "name": "add", "args": {"a": 2, "b": 3, "debug": True}
        }))

    def test_manifest_identifies_the_executed_case_set(self):
        manifest_path = DATASETS.parent / "manifests" / "stage02_fake_v1.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        _, artifacts = run_suite(CASES, FIXTURES, manifest["run_id"])
        self.assertEqual(set(manifest["task_ids"]), {row["case_id"] for row in artifacts})
        self.assertEqual(manifest["resolved"], sum(
            row["outcome"] == "resolved" for row in artifacts
        ))
        self.assertEqual(manifest["infra_error"], sum(
            row["outcome"] == "infra_error" for row in artifacts
        ))


if __name__ == "__main__":
    unittest.main()
