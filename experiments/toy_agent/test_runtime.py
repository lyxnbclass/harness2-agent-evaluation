"""Behavior checks for the local teaching Runtime."""

import unittest
from unittest.mock import patch

from experiments.toy_agent.runtime import FakeModel, run_agent, run_tool


class RuntimeTests(unittest.TestCase):
    def test_tool_result_reaches_next_model_decision(self):
        model = FakeModel([
            {"type": "tool_call", "name": "add", "args": {"a": 2, "b": 3}},
            {"type": "final", "answer": "The sum is 5"},
        ])

        result = run_agent("Add 2 and 3", model)

        self.assertEqual((result.status, result.answer), ("completed", "The sum is 5"))
        self.assertEqual(model.seen[1][-1], {"role": "tool", "name": "add", "content": "5"})
        self.assertEqual(result.trace[-1], {"role": "assistant", "content": "The sum is 5"})

    def test_three_local_tools_and_closed_schema(self):
        self.assertEqual(run_tool("add", {"a": -2, "b": 3}), "1")
        self.assertEqual(run_tool("uppercase", {"text": "Agent"}), "AGENT")
        self.assertEqual(run_tool("delay", {"seconds": 0}), "done")
        for args in ({"a": True, "b": 3}, {"a": 2, "b": 3, "debug": True}):
            with self.subTest(args=args):
                result = run_agent("bad args", FakeModel([
                    {"type": "tool_call", "name": "add", "args": args}
                ]))
                self.assertEqual(result.status, "invalid_args")

    def test_unknown_tool_is_not_executed(self):
        result = run_agent("call missing tool", FakeModel([
            {"type": "tool_call", "name": "delete_all", "args": {}}
        ]))
        self.assertEqual(result.status, "unknown_tool")
        self.assertIn("unknown tool", result.trace[-1]["error"])

    def test_actual_timeout_is_reported(self):
        result = run_agent("wait", FakeModel([
            {"type": "tool_call", "name": "delay", "args": {"seconds": 1}}
        ]), tool_timeout=0.01)
        self.assertEqual(result.status, "tool_timeout")
        self.assertIsNone(result.answer)
        self.assertEqual(result.trace[-1]["role"], "tool")

    def test_dependency_failure_is_distinct_from_timeout(self):
        with patch("experiments.toy_agent.runtime.subprocess.run", side_effect=OSError("no python")):
            result = run_agent("wait", FakeModel([
                {"type": "tool_call", "name": "delay", "args": {"seconds": 0}}
            ]))
        self.assertEqual(result.status, "tool_error")

    def test_step_budget_and_model_output(self):
        calls = [{"type": "tool_call", "name": "uppercase", "args": {"text": "a"}}] * 2
        self.assertEqual(run_agent("repeat", FakeModel(calls), max_steps=2).status, "max_steps")
        self.assertEqual(run_agent("empty", FakeModel([])).status, "model_exhausted")
        self.assertEqual(run_agent("invalid", FakeModel([{"type": "final", "answer": 7}])).status,
                         "invalid_model_output")


if __name__ == "__main__":
    unittest.main()
