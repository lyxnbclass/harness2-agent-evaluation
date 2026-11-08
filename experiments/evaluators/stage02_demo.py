"""Run the Stage 02 teaching cases with scripted FakeModel decisions.

This local contract exercise is not a coding benchmark or SWE-bench verdict.
"""

import argparse
import json
from pathlib import Path
from time import perf_counter

from experiments.evaluators.metrics import TaskResult, summarize
from experiments.toy_agent.runtime import FakeModel, SCHEMAS, run_agent


DATASETS = Path(__file__).resolve().parents[1] / "datasets"
SPLITS = {"dev", "validation", "local-held-out"}
EXPECTED_STATUSES = {"completed", "invalid_args", "unknown_tool", "max_steps"}


def load_jsonl(path: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON") from exc
        if not isinstance(row, dict) or not isinstance(row.get("case_id"), str):
            raise ValueError(f"{path}:{line_number}: missing case_id")
        case_id = row["case_id"]
        if case_id in rows:
            raise ValueError(f"{path}:{line_number}: duplicate case_id {case_id}")
        rows[case_id] = row
    return rows


def validate_case(case: dict) -> None:
    required = {"case_id", "input", "split", "expected_outcome", "tool_constraints", "tags"}
    if not required.issubset(case):
        raise ValueError(f"{case.get('case_id')}: missing case fields")
    if not isinstance(case["input"], str) or case["split"] not in SPLITS:
        raise ValueError(f"{case['case_id']}: invalid input or split")
    expectation = case["expected_outcome"]
    if not isinstance(expectation, dict) or expectation.get("status") not in EXPECTED_STATUSES:
        raise ValueError(f"{case['case_id']}: invalid expected_outcome")
    if expectation["status"] == "completed" and not isinstance(expectation.get("answer"), str):
        raise ValueError(f"{case['case_id']}: completed case requires expected answer")
    constraints = case["tool_constraints"]
    if not isinstance(constraints, dict):
        raise ValueError(f"{case['case_id']}: invalid tool_constraints")
    allowed = constraints.get("allowed_tools")
    steps = constraints.get("max_steps")
    if not isinstance(allowed, list) or not all(isinstance(name, str) for name in allowed):
        raise ValueError(f"{case['case_id']}: invalid allowed_tools")
    if len(allowed) != len(set(allowed)) or not set(allowed).issubset(SCHEMAS):
        raise ValueError(f"{case['case_id']}: invalid allowed_tools")
    if type(steps) is not int or steps < 1:
        raise ValueError(f"{case['case_id']}: invalid max_steps")
    if not isinstance(case["tags"], list) or not all(isinstance(tag, str) for tag in case["tags"]):
        raise ValueError(f"{case['case_id']}: invalid tags")


def call_is_schema_valid(call: dict) -> bool:
    name, args = call.get("name"), call.get("args")
    if not isinstance(name, str) or name not in SCHEMAS or not isinstance(args, dict):
        return False
    expected = SCHEMAS[name]["args"]
    return set(args) == set(expected) and all(
        type(args[key]) is kind for key, kind in expected.items()
    )


def tool_counts(trace: list[dict], allowed_tools: list[str]) -> tuple[int, int, int]:
    calls = [event["tool_call"] for event in trace if "tool_call" in event]
    valid = sum(call_is_schema_valid(call) for call in calls)
    unsafe = sum(call.get("name") not in allowed_tools for call in calls)
    return len(calls), valid, unsafe


def run_case(
    case: dict, fixture: dict, run_id: str, *, record_events: bool = False
) -> tuple[TaskResult, dict]:
    case_id = case["case_id"]
    if fixture.get("case_id") != case_id:
        raise ValueError(f"{case_id}: fixture ID mismatch")
    if fixture.get("simulated_infra_error") and fixture.get("simulated_unscored"):
        raise ValueError(f"{case_id}: conflicting simulated outcomes")
    reason = fixture.get("simulated_infra_error") or fixture.get("simulated_unscored")
    events: list[dict] = []
    if fixture.get("simulated_infra_error"):
        outcome, status, answer, trace, latency = "infra_error", None, None, [], None
    elif fixture.get("simulated_unscored"):
        outcome, status, answer, trace, latency = "unscored", None, None, [], None
    else:
        decisions = fixture.get("decisions")
        if not isinstance(decisions, list):
            raise ValueError(f"{case_id}: missing decisions")
        started = perf_counter()
        result = run_agent(
            case["input"], FakeModel(decisions),
            max_steps=case["tool_constraints"]["max_steps"],
            event_sink=events.append if record_events else None,
        )
        latency = perf_counter() - started
        status, answer, trace = result.status, result.answer, result.trace
        expected = case["expected_outcome"]
        matches = status == expected["status"] and answer == expected.get("answer")
        outcome = "resolved" if matches else "failed"

    calls, valid, unsafe = tool_counts(trace, case["tool_constraints"]["allowed_tools"])
    metric_row = TaskResult(case_id, outcome, calls, valid, unsafe, latency)
    artifact = {
        "run_id": run_id,
        "case_id": case_id,
        "split": case["split"],
        "verdict_source": "local_scripted_contract",
        "outcome": outcome,
        "observed_status": status,
        "observed_answer": answer,
        "reason": reason,
        "tool_calls": calls,
        "schema_valid_calls": valid,
        "unsafe_tool_calls": unsafe,
        "latency_sec": latency,
        "trace": trace,
    }
    if record_events:
        artifact["events"] = events
    return metric_row, artifact


def run_suite(
    cases_path: Path, fixtures_path: Path, run_id: str, *, record_events: bool = False
) -> tuple[list[TaskResult], list[dict]]:
    cases, fixtures = load_jsonl(cases_path), load_jsonl(fixtures_path)
    if cases.keys() != fixtures.keys():
        raise ValueError("case and fixture IDs differ")
    metrics, artifacts = [], []
    for case_id, case in cases.items():
        validate_case(case)
        metric, artifact = run_case(case, fixtures[case_id], run_id, record_events=record_events)
        metrics.append(metric)
        artifacts.append(artifact)
    return metrics, artifacts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=DATASETS / "stage02_multitool_cases.jsonl")
    parser.add_argument("--fixtures", type=Path, default=DATASETS / "stage02_fake_decisions.jsonl")
    parser.add_argument("--run-id", default="stage02-fake-v1")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    metrics, artifacts = run_suite(args.cases, args.fixtures, args.run_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in artifacts),
        encoding="utf-8",
    )
    print(json.dumps(summarize(metrics).as_dict(), indent=2))


if __name__ == "__main__":
    main()
