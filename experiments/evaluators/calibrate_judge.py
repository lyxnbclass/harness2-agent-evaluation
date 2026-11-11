"""Compare a deterministic judge with Codex-authored manual reference labels."""

import argparse
import json
from pathlib import Path

from experiments.evaluators.judge import Rubric, compare_pair, judge_answer


DEFAULT_CASES = Path(__file__).resolve().parents[1] / "datasets" / "stage04_judge_cases.jsonl"


def load_cases(path: Path) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON") from exc
        if not isinstance(row, dict) or not isinstance(row.get("case_id"), str):
            raise ValueError(f"{path}:{line_number}: invalid case")
        if row["case_id"] in seen:
            raise ValueError(f"duplicate case_id: {row['case_id']}")
        if row.get("manual_verdict") not in {"pass", "fail"}:
            raise ValueError(f"{row['case_id']}: invalid manual verdict")
        seen.add(row["case_id"])
        rows.append(row)
    return rows


def calibrate(cases: list[dict]) -> dict:
    results: list[dict] = []
    for case in cases:
        spec = case["rubric"]
        rubric = Rubric(
            spec["expected_answer"],
            tuple(spec.get("required_terms", [])),
            tuple(spec.get("forbidden_terms", [])),
        )
        decision = judge_answer(case["answer"], case["explanation"], rubric)
        results.append({
            "case_id": case["case_id"],
            "tag": case["tag"],
            "manual_verdict": case["manual_verdict"],
            "judge_output": decision,
            "agrees": decision["verdict"] == case["manual_verdict"],
        })
    disagreements = [row["case_id"] for row in results if not row["agrees"]]
    by_id = {row["case_id"]: row["judge_output"] for row in results}
    pair_order_probe = {
        "concise_correct_first": compare_pair(by_id["j01"], by_id["j02"]),
        "verbose_wrong_first": compare_pair(by_id["j02"], by_id["j01"]),
    } if {"j01", "j02"}.issubset(by_id) else None
    return {
        "kind": "local_deterministic_judge_calibration",
        "annotation_source": "Codex-authored manual reference labels; user review pending",
        "cases": results,
        "summary": {
            "total": len(results),
            "agreements": len(results) - len(disagreements),
            "disagreements": len(disagreements),
            "disagreement_ids": disagreements,
            "pair_order_probe": pair_order_probe,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = calibrate(load_cases(args.cases))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
