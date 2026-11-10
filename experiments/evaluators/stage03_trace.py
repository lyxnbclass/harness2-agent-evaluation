"""Capture, sanitize, validate and replay scripted local Agent events."""

import argparse
import json
from pathlib import Path
import re

from experiments.evaluators.stage02_demo import DATASETS, load_jsonl, run_suite
from experiments.evaluators.bad_case_registry import candidate_from_result
from experiments.evaluators.trace_validator import validate_trace


PRIVATE_KEY = re.compile(r"(?:password|secret|token|api[_-]?key|authorization)", re.I)
PRIVATE_VALUE = re.compile(
    r"(?i)\b((?:password|secret|token|api[_-]?key|authorization)\s*[:=]\s*)(?:Bearer\s+)?[^\s,;]+"
)
TOKEN_VALUE = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")


def redact(value):
    """Mask common credential fields and assignments before persistent output."""
    if isinstance(value, dict):
        return {key: "<redacted>" if PRIVATE_KEY.search(str(key)) else redact(item)
                for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, str):
        return TOKEN_VALUE.sub("<redacted>", PRIVATE_VALUE.sub(r"\1<redacted>", value))
    return value


def build_artifacts(cases_path: Path, fixtures_path: Path, run_id: str) -> list[dict]:
    cases = load_jsonl(cases_path)
    _, rows = run_suite(cases_path, fixtures_path, run_id, record_events=True)
    output: list[dict] = []
    for row in rows:
        case_id = row["case_id"]
        events = redact(row.pop("events"))
        row.pop("trace")  # The old raw Trace must not reach the Stage 03 artifact.
        findings = validate_trace(
            events, cases[case_id]["tool_constraints"],
            observed_status=row["observed_status"],
        )
        row.update({
            "task_id": case_id,
            "stage": "03",
            "model_id": "FakeModel/scripted",
            "harness_sha": None,  # This toy runner does not execute upstream Harness².
            "events": events,
            "findings": [finding.as_dict() for finding in findings],
        })
        output.append(redact(row))
    return output


def replay(path: Path, run_id: str, case_id: str | None = None) -> list[str]:
    lines: list[str] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        row = json.loads(raw)
        if row.get("run_id") != run_id or (case_id and row.get("case_id") != case_id):
            continue
        lines.append(f"{row['run_id']} / {row['case_id']}: outcome={row['outcome']} status={row['observed_status']}")
        for event in row["events"]:
            lines.append(f"  [{event['step']}] {event['timestamp']} +{event['elapsed_ms']}ms {json.dumps(event['message'], ensure_ascii=False)}")
        for finding in row["findings"]:
            lines.append(f"  finding {finding['code']} at step {finding['step']}: {finding['evidence']}")
    if not lines:
        raise ValueError(f"no events for run_id={run_id!r}, case_id={case_id!r}")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    capture = sub.add_parser("capture")
    capture.add_argument("--cases", type=Path, default=DATASETS / "stage02_multitool_cases.jsonl")
    capture.add_argument("--fixtures", type=Path, default=DATASETS / "stage02_fake_decisions.jsonl")
    capture.add_argument("--run-id", default="stage03-fake-v1")
    capture.add_argument("--output", type=Path, required=True)
    capture.add_argument("--registry-output", type=Path)
    view = sub.add_parser("replay")
    view.add_argument("--input", type=Path, required=True)
    view.add_argument("--run-id", required=True)
    view.add_argument("--case-id")
    args = parser.parse_args()
    if args.command == "capture":
        rows = build_artifacts(args.cases, args.fixtures, args.run_id)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
            encoding="utf-8",
        )
        if args.registry_output is not None:
            candidates = [candidate_from_result(row) for row in rows]
            args.registry_output.parent.mkdir(parents=True, exist_ok=True)
            args.registry_output.write_text(
                "".join(json.dumps(item.as_dict(), ensure_ascii=False) + "\n"
                        for item in candidates if item is not None),
                encoding="utf-8",
            )
        print(f"captured {len(rows)} local scripted cases in {args.output}")
    else:
        print("\n".join(replay(args.input, args.run_id, args.case_id)))


if __name__ == "__main__":
    main()
