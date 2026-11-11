"""Behavior checks for the local teaching Runtime."""

import unittest
from unittest.mock import patch

from experiments.toy_agent.runtime import FakeModel, ToolError, run_agent, run_tool


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
        bad_name = run_agent("bad name", FakeModel([
            {"type": "tool_call", "name": [], "args": {}}
        ]))
        self.assertEqual(bad_name.status, "invalid_args")

    def test_invalid_tool_output_is_not_forwarded_to_model(self):
        model = FakeModel([
            {"type": "tool_call", "name": "add", "args": {"a": 2, "b": 3}},
            {"type": "final", "answer": "The sum is 5"},
        ])
        with patch("experiments.toy_agent.runtime._execute_tool", return_value=5):
            result = run_agent("Add 2 and 3", model)
        self.assertEqual((result.status, result.answer), ("invalid_tool_result", None))
        self.assertEqual(len(model.seen), 1)
        self.assertIn("returned int; expected str", result.trace[-1]["error"])

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

    def test_one_step_stops_after_tool_result_without_final_answer(self):
        model = FakeModel([
            {"type": "tool_call", "name": "add", "args": {"a": 2, "b": 3}},
            {"type": "final", "answer": "The sum is 5"},
        ])
        result = run_agent("Add 2 and 3", model, max_steps=1)
        self.assertEqual((result.status, result.answer), ("max_steps", None))
        self.assertEqual(len(result.trace), 3)
        self.assertEqual(result.trace[-1], {"role": "tool", "name": "add", "content": "5"})
        self.assertEqual(len(model.seen), 1)

    def test_task_allowlist_blocks_dispatch_even_when_global_schema_allows_tool(self):
        decisions = [
            {"type": "tool_call", "name": "uppercase", "args": {"text": "5"}},
            {"type": "final", "answer": "5"},
        ]
        with patch("experiments.toy_agent.runtime._execute_tool") as execute:
            result = run_agent("Only add is allowed", FakeModel(decisions),
                               allowed_tools=frozenset({"add"}))
        self.assertEqual((result.status, result.answer), ("unauthorized_tool", None))
        self.assertEqual(result.trace[-1]["role"], "tool")
        execute.assert_not_called()

    def test_transient_timeout_retries_only_pure_tool_and_records_attempts(self):
        decisions = [
            {"type": "tool_call", "name": "add", "args": {"a": 2, "b": 3}},
            {"type": "final", "answer": "5"},
        ]
        with patch("experiments.toy_agent.runtime._execute_tool",
                   side_effect=[ToolError("tool_timeout", "transient"), "5"]) as execute, \
             patch("experiments.toy_agent.runtime.sleep") as wait:
            result = run_agent("Add 2 and 3", FakeModel(decisions), max_tool_retries=1)
        self.assertEqual((result.status, result.answer), ("completed", "5"))
        self.assertEqual(execute.call_count, 2)
        self.assertEqual(result.trace[2]["attempts"], 2)
        wait.assert_called_once_with(0.01)

    def test_delay_and_schema_errors_are_never_retried(self):
        with patch("experiments.toy_agent.runtime._execute_tool",
                   side_effect=ToolError("tool_timeout", "transient")) as execute:
            result = run_agent("Delay", FakeModel([
                {"type": "tool_call", "name": "delay", "args": {"seconds": 0}}
            ]), max_tool_retries=2)
        self.assertEqual(result.status, "tool_timeout")
        self.assertEqual(execute.call_count, 1)
        with patch("experiments.toy_agent.runtime._execute_tool") as execute:
            result = run_agent("Bad args", FakeModel([
                {"type": "tool_call", "name": "add", "args": {"a": "2", "b": 3}}
            ]), max_tool_retries=2)
        self.assertEqual(result.status, "invalid_args")
        execute.assert_not_called()

    def test_retry_exhaustion_keeps_timeout_status(self):
        with patch("experiments.toy_agent.runtime._execute_tool",
                   side_effect=ToolError("tool_timeout", "transient")) as execute, \
             patch("experiments.toy_agent.runtime.sleep") as wait:
            result = run_agent("Add", FakeModel([
                {"type": "tool_call", "name": "add", "args": {"a": 2, "b": 3}}
            ]), max_tool_retries=2)
        self.assertEqual(result.status, "tool_timeout")
        self.assertEqual(result.trace[-1]["attempts"], 3)
        self.assertEqual(execute.call_count, 3)
        self.assertEqual([call.args[0] for call in wait.call_args_list], [0.01, 0.02])


if __name__ == "__main__":
    unittest.main()
