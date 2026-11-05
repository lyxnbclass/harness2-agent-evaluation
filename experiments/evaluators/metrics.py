"""Aggregate normalized task results without changing native judge verdicts."""

from dataclasses import asdict, dataclass
from math import isfinite
from statistics import median
from typing import Literal


Outcome = Literal["resolved", "failed", "infra_error", "unscored"]
OUTCOMES = ("resolved", "failed", "infra_error", "unscored")


@dataclass(frozen=True)
class TaskResult:
    case_id: str
    outcome: Outcome
    tool_calls: int
    schema_valid_calls: int
    unsafe_tool_calls: int
    latency_sec: float | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.case_id, str) or not self.case_id:
            raise ValueError("case_id must be a nonempty string")
        if self.outcome not in OUTCOMES:
            raise ValueError(f"unsupported outcome: {self.outcome}")
        for field in ("tool_calls", "schema_valid_calls", "unsafe_tool_calls"):
            value = getattr(self, field)
            if type(value) is not int or value < 0:
                raise ValueError(f"{field} must be a nonnegative integer")
        if self.schema_valid_calls > self.tool_calls:
            raise ValueError("schema_valid_calls exceeds tool_calls")
        if self.unsafe_tool_calls > self.tool_calls:
            raise ValueError("unsafe_tool_calls exceeds tool_calls")
        if self.latency_sec is not None:
            if type(self.latency_sec) is bool or not isinstance(self.latency_sec, (int, float)) or not isfinite(self.latency_sec):
                raise ValueError("latency_sec must be finite or null")
            if self.latency_sec < 0:
                raise ValueError("latency_sec must be nonnegative")


@dataclass(frozen=True)
class MetricsSummary:
    total: int
    counts: dict[str, int]
    scored: int
    success_rate: float | None
    scored_coverage: float | None
    tool_calls: int
    tool_schema_valid_rate: float | None
    unsafe_tool_rate: float | None
    observed_latencies: int
    median_latency_sec: float | None

    def as_dict(self) -> dict:
        return asdict(self)


def summarize(results: list[TaskResult]) -> MetricsSummary:
    """Use scored tasks for success and observed tool calls for tool rates.

    Infra errors and unscored tasks remain in the total and status counts. Missing
    denominators return None instead of implying a measured zero.
    """
    counts = {outcome: 0 for outcome in OUTCOMES}
    seen: set[str] = set()
    for result in results:
        if result.case_id in seen:
            raise ValueError(f"duplicate case_id: {result.case_id}")
        seen.add(result.case_id)
        counts[result.outcome] += 1

    total = len(results)
    scored = counts["resolved"] + counts["failed"]
    tool_calls = sum(result.tool_calls for result in results)
    valid_calls = sum(result.schema_valid_calls for result in results)
    unsafe_calls = sum(result.unsafe_tool_calls for result in results)
    latencies = [result.latency_sec for result in results if result.latency_sec is not None]
    return MetricsSummary(
        total=total,
        counts=counts,
        scored=scored,
        success_rate=counts["resolved"] / scored if scored else None,
        scored_coverage=scored / total if total else None,
        tool_calls=tool_calls,
        tool_schema_valid_rate=valid_calls / tool_calls if tool_calls else None,
        unsafe_tool_rate=unsafe_calls / tool_calls if tool_calls else None,
        observed_latencies=len(latencies),
        median_latency_sec=median(latencies) if latencies else None,
    )
