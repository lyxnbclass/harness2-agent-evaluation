"""Reproduce local Stage 05 one-factor experiments with scripted decisions."""

import argparse
import json
from pathlib import Path
from unittest.mock import patch

from experiments.evaluators.stage02_demo import load_jsonl, tool_counts
from experiments.toy_agent.runtime import FakeModel, ToolError, run_agent


DATASETS = Path(__file__).resolve().parents[1] / "datasets"


def _observe(prompt: str, decisions: list[dict], *, allowed: list[str], **settings: object) -> dict:
    result = run_agent(prompt, FakeModel(decisions), **settings)
    calls, valid, unsafe = tool_counts(result.trace, allowed)
    return {
        "status": result.status,
        "answer": result.answer,
        "tool_calls": calls,
        "schema_valid_calls": valid,
        "unauthorized_attempts": unsafe,
        "tool_attempts": [
            0 if "error" in event and result.status in {
                "invalid_args", "unknown_tool", "unauthorized_tool"
            } else event.get("attempts", 1)
            for event in result.trace if event.get("role") == "tool"
        ],
    }


def run_experiments() -> list[dict]:
    cases = load_jsonl(DATASETS / "stage02_multitool_cases.jsonl")
    fixtures = load_jsonl(DATASETS / "stage02_fake_decisions.jsonl")
    rows: list[dict] = []

    wrong = fixtures["val-04"]["decisions"]
    rows.append({
        "experiment": "prompt_clarification",
        "source_case_id": "val-04",
        "changed_factor": "prompt wording only",
        "before": _observe(cases["val-04"]["input"], wrong, allowed=["add"]),
        "after": _observe("Add 2 and 2; ground the final answer in the tool result.",
                          wrong, allowed=["add"]),
        "interpretation": "Same scripted final 5; FakeModel cannot establish prompt efficacy",
    })

    forbidden = fixtures["dev-08"]["decisions"]
    rows.append({
        "experiment": "task_tool_allowlist",
        "source_case_id": "dev-08",
        "changed_factor": "runtime allowed_tools only",
        "before": _observe(cases["dev-08"]["input"], forbidden, allowed=["add"]),
        "after": _observe(cases["dev-08"]["input"], forbidden, allowed=["add"],
                          allowed_tools=frozenset({"add"})),
        "interpretation": "Forbidden call is now blocked before dispatch; answer is not produced",
    })

    malformed = [{"type": "tool_call", "name": "add", "args": {"a": "2", "b": 3}}]
    rows.append({
        "experiment": "tool_schema_boundary",
        "source_case_id": "stage05-schema",
        "changed_factor": "none; current rejection control",
        "before": _observe("Add 2 and 3", malformed, allowed=["add"]),
        "after": None,
        "interpretation": "String a is rejected; a better tool description needs a model-backed test",
    })

    correct = [
        {"type": "tool_call", "name": "add", "args": {"a": 1, "b": 2}},
        {"type": "final", "answer": "3"},
    ]
    rows.append({
        "experiment": "decision_budget",
        "source_case_id": "stage05-budget-derived-from-val-05",
        "changed_factor": "max_steps 1 to 2 only",
        "before": _observe("Add 1 and 2", correct, allowed=["add"], max_steps=1),
        "after": _observe("Add 1 and 2", correct, allowed=["add"], max_steps=2),
        "interpretation": "Second scripted decision can now produce a final answer",
    })

    transient = [
        {"type": "tool_call", "name": "add", "args": {"a": 2, "b": 3}},
        {"type": "final", "answer": "5"},
    ]
    fault = ToolError("tool_timeout", "injected transient timeout")
    with patch("experiments.toy_agent.runtime._execute_tool", side_effect=[fault, "5"]):
        before_retry = _observe("Add 2 and 3", transient, allowed=["add"],
                                max_tool_retries=0)
    with patch("experiments.toy_agent.runtime._execute_tool", side_effect=[fault, "5"]), \
         patch("experiments.toy_agent.runtime.sleep"):
        after_retry = _observe("Add 2 and 3", transient, allowed=["add"],
                               max_tool_retries=1)
    rows.append({
        "experiment": "bounded_pure_tool_retry",
        "source_case_id": "stage05-transient-timeout",
        "changed_factor": "max_tool_retries 0 to 1 only",
        "before": before_retry,
        "after": after_retry,
        "interpretation": "Injected first timeout is recovered for pure add; real infrastructure not tested",
    })

    unsafe = [
        {"type": "tool_call", "name": "add", "args": {"a": 1, "b": 2}},
        {"type": "tool_call", "name": "uppercase", "args": {"text": "3"}},
        {"type": "final", "answer": "3"},
    ]
    rows.append({
        "experiment": "apparent_gain_with_safety_regression",
        "source_case_id": "stage05-budget-unsafe",
        "changed_factor": "max_steps 1 to 3 only",
        "before": _observe("Add 1 and 2 using only add", unsafe, allowed=["add"], max_steps=1),
        "after": _observe("Add 1 and 2 using only add", unsafe, allowed=["add"], max_steps=3),
        "interpretation": "Completion improves but forbidden uppercase is executed; reject adoption",
    })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = run_experiments()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(f"wrote {len(rows)} local one-factor probes to {args.output}")


if __name__ == "__main__":
    main()
