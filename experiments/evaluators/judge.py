"""Deterministic local judge for rubric calibration; no model API or benchmark verdict."""

from dataclasses import dataclass
from typing import Callable


REASONS = {"incorrect_answer", "missing_evidence", "forbidden_content"}


@dataclass(frozen=True)
class Rubric:
    expected_answer: str
    required_terms: tuple[str, ...] = ()
    forbidden_terms: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.expected_answer, str):
            raise ValueError("expected_answer must be a string")
        for terms in (self.required_terms, self.forbidden_terms):
            if not isinstance(terms, tuple) or any(not isinstance(term, str) or not term for term in terms):
                raise ValueError("rubric terms must be nonempty strings")


class JudgeUnavailable(RuntimeError):
    """All bounded attempts returned an invalid structured decision."""


def validate_judge_output(value: object) -> dict:
    """Reject malformed or internally inconsistent judge output."""
    if not isinstance(value, dict) or set(value) != {
        "schema_version", "verdict", "score", "dimensions", "reason_codes"
    }:
        raise ValueError("judge output fields do not match schema")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ValueError("unsupported judge schema or verdict")
    if not isinstance(value["verdict"], str) or value["verdict"] not in {"pass", "fail"}:
        raise ValueError("unsupported judge schema or verdict")
    dimensions = value["dimensions"]
    if not isinstance(dimensions, dict) or set(dimensions) != {"correctness", "evidence", "safety"}:
        raise ValueError("invalid judge dimensions")
    if any(type(item) is not bool for item in dimensions.values()):
        raise ValueError("judge dimensions must be booleans")
    reasons = value["reason_codes"]
    if not isinstance(reasons, list) or any(not isinstance(item, str) or item not in REASONS for item in reasons):
        raise ValueError("invalid reason codes")
    expected_reasons = [
        code for key, code in (
            ("correctness", "incorrect_answer"),
            ("evidence", "missing_evidence"),
            ("safety", "forbidden_content"),
        ) if not dimensions[key]
    ]
    score = 2 * dimensions["correctness"] + dimensions["evidence"]
    verdict = "pass" if all(dimensions.values()) else "fail"
    if type(value["score"]) is not int or value["score"] != score:
        raise ValueError("judge score conflicts with dimensions")
    if value["verdict"] != verdict or reasons != expected_reasons:
        raise ValueError("judge verdict or reasons conflict with dimensions")
    return value


def judge_answer(answer: str, explanation: str, rubric: Rubric) -> dict:
    """Apply explicit answer/evidence/safety checks to local teaching text."""
    if not isinstance(answer, str) or not isinstance(explanation, str) or not isinstance(rubric, Rubric):
        raise ValueError("judge input must be answer, explanation and Rubric")
    normalized_answer = answer.strip()
    normalized_explanation = explanation.casefold()
    dimensions = {
        "correctness": normalized_answer == rubric.expected_answer.strip(),
        "evidence": all(term.casefold() in normalized_explanation for term in rubric.required_terms),
        "safety": not any(term.casefold() in normalized_explanation for term in rubric.forbidden_terms),
    }
    reasons = [
        code for key, code in (
            ("correctness", "incorrect_answer"),
            ("evidence", "missing_evidence"),
            ("safety", "forbidden_content"),
        ) if not dimensions[key]
    ]
    return validate_judge_output({
        "schema_version": 1,
        "verdict": "pass" if all(dimensions.values()) else "fail",
        "score": 2 * dimensions["correctness"] + dimensions["evidence"],
        "dimensions": dimensions,
        "reason_codes": reasons,
    })


def judge_with_retry(call: Callable[[], object], *, attempts: int = 2) -> dict:
    """Bound retries for malformed external judge responses; never return fake success."""
    if type(attempts) is not int or attempts < 1:
        raise ValueError("attempts must be positive")
    last_error: ValueError | TimeoutError | None = None
    for _ in range(attempts):
        try:
            return validate_judge_output(call())
        except (ValueError, TimeoutError) as exc:
            last_error = exc
    raise JudgeUnavailable(f"judge output invalid after {attempts} attempts") from last_error


def compare_pair(left: dict, right: dict) -> str:
    """Compare independently scored outputs; ties remain ties across swaps."""
    a, b = validate_judge_output(left), validate_judge_output(right)
    rank_a = tuple(a["dimensions"][key] for key in ("safety", "correctness", "evidence"))
    rank_b = tuple(b["dimensions"][key] for key in ("safety", "correctness", "evidence"))
    return "A" if rank_a > rank_b else "B" if rank_b > rank_a else "TIE"
