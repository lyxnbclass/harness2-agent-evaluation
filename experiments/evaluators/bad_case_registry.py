"""Build review candidates from verdicts and trace findings, preserving evidence."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class BadCaseCandidate:
    run_id: str
    task_id: str
    outcome: str
    category: str
    first_evidence_step: int | None
    evidence: str
    root_cause_hypothesis: str | None = None

    def as_dict(self) -> dict:
        return asdict(self)


def candidate_from_result(row: dict) -> BadCaseCandidate | None:
    """Select items for human analysis; do not infer a causal explanation."""
    findings = row.get("findings", [])
    actionable = [finding for finding in findings if finding["code"] in {
        "unauthorized_tool", "invalid_args", "orphan_tool_result",
        "missing_tool_result", "step_limit_exceeded", "step_budget_exhausted",
        "required_tool_missing", "tool_error", "repeated_call",
    }]
    if row["outcome"] == "infra_error":
        category, step = "infrastructure", None
        evidence = row.get("reason") or "runner failed before a verdict was available"
    elif row["outcome"] == "unscored":
        category, step = "unscored", None
        evidence = row.get("reason") or "judge verdict unavailable"
    elif row["outcome"] == "failed":
        category = "task_failure"
        step = next((event["step"] for event in reversed(row.get("events", []))
                     if event["message"].get("role") == "assistant"), None)
        evidence = f"local contract failed: status={row.get('observed_status')}, answer={row.get('observed_answer')!r}"
    elif actionable:
        first = min(actionable, key=lambda finding: finding["step"] if finding["step"] is not None else float("inf"))
        category, step, evidence = "trajectory_review", first["step"], first["evidence"]
    else:
        return None
    return BadCaseCandidate(
        row["run_id"], row["task_id"], row["outcome"], category,
        step, evidence,
    )
