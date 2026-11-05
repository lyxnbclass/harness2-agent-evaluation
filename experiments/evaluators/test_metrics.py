"""Behavior checks for normalized evaluation metrics."""

import unittest

from experiments.evaluators.metrics import TaskResult, summarize


def row(case_id, outcome, *, calls=0, valid=0, unsafe=0, latency=None):
    return TaskResult(case_id, outcome, calls, valid, unsafe, latency)


class MetricsTests(unittest.TestCase):
    def test_success_excludes_infra_and_unscored_but_coverage_does_not(self):
        summary = summarize([
            row("a", "resolved"),
            row("b", "failed"),
            row("c", "infra_error"),
            row("d", "unscored"),
        ])
        self.assertEqual(summary.counts, {
            "resolved": 1, "failed": 1, "infra_error": 1, "unscored": 1
        })
        self.assertEqual((summary.success_rate, summary.scored_coverage), (0.5, 0.5))

    def test_no_scored_cases_is_unknown_not_zero_success(self):
        summary = summarize([row("a", "infra_error"), row("b", "unscored")])
        self.assertIsNone(summary.success_rate)
        self.assertEqual(summary.scored_coverage, 0.0)

    def test_empty_run_has_no_rates_or_median(self):
        summary = summarize([])
        self.assertEqual(summary.total, 0)
        self.assertIsNone(summary.success_rate)
        self.assertIsNone(summary.scored_coverage)
        self.assertIsNone(summary.tool_schema_valid_rate)
        self.assertIsNone(summary.unsafe_tool_rate)
        self.assertIsNone(summary.median_latency_sec)

    def test_tool_rates_use_calls_and_can_expose_successful_unsafe_case(self):
        summary = summarize([
            row("a", "resolved", calls=2, valid=2, unsafe=1),
            row("b", "failed", calls=1, valid=0),
        ])
        self.assertEqual(summary.success_rate, 0.5)
        self.assertEqual(summary.tool_schema_valid_rate, 2 / 3)
        self.assertEqual(summary.unsafe_tool_rate, 1 / 3)

    def test_latency_uses_observed_values_only_including_infra(self):
        summary = summarize([
            row("a", "resolved", latency=1),
            row("b", "failed", latency=None),
            row("c", "infra_error", latency=3),
        ])
        self.assertEqual(summary.observed_latencies, 2)
        self.assertEqual(summary.median_latency_sec, 2)

    def test_duplicate_case_id_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate case_id"):
            summarize([row("same", "resolved"), row("same", "failed")])

    def test_invalid_counts_and_latency_are_rejected(self):
        invalid = [
            {"tool_calls": -1},
            {"tool_calls": True},
            {"tool_calls": 1, "schema_valid_calls": 2},
            {"tool_calls": 1, "unsafe_tool_calls": 2},
            {"latency_sec": float("nan")},
            {"latency_sec": True},
            {"latency_sec": -1},
        ]
        for fields in invalid:
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                data = {
                    "case_id": "a", "outcome": "resolved", "tool_calls": 0,
                    "schema_valid_calls": 0, "unsafe_tool_calls": 0,
                    "latency_sec": None,
                }
                data.update(fields)
                TaskResult(**data)

    def test_unsupported_outcome_and_missing_id_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "unsupported outcome"):
            row("a", "success")
        with self.assertRaisesRegex(ValueError, "case_id"):
            row("", "resolved")


if __name__ == "__main__":
    unittest.main()
