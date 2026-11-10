"""Validate structured local Agent events without changing task verdicts."""

from dataclasses import asdict, dataclass
from typing import Any

from experiments.toy_agent.runtime import SCHEMAS


@dataclass(frozen=True)
class Finding:
    code: str
    step: int | None
    evidence: str

    def as_dict(self) -> dict:
        return asdict(self)


def _valid_args(name: str, args: Any) -> bool:
    if not isinstance(name, str) or name not in SCHEMAS or not isinstance(args, dict):
        return False
    expected = SCHEMAS[name]["args"]
    return set(args) == set(expected) and all(
        type(args[key]) is kind for key, kind in expected.items()
    )


def validate_trace(
    events: list[dict], constraints: dict, *, observed_status: str | None = None
) -> list[Finding]:
    """Check observable order and policy; do not infer task correctness or root cause."""
    if not isinstance(events, list) or not isinstance(constraints, dict):
        raise ValueError("events and constraints must be a list and a mapping")
    allowed = constraints.get("allowed_tools")
    required = constraints.get("required_tools", [])
    max_steps = constraints.get("max_steps")
    if not isinstance(allowed, list) or not all(isinstance(x, str) for x in allowed):
        raise ValueError("allowed_tools must be a list of names")
    if not isinstance(required, list) or not all(isinstance(x, str) for x in required):
        raise ValueError("required_tools must be a list of names")
    if type(max_steps) is not int or max_steps < 1:
        raise ValueError("max_steps must be positive")

    findings: list[Finding] = []
    pending: str | None = None
    seen_calls: set[tuple[str, str]] = set()
    called: set[str] = set()
    decisions = 0
    final_seen = False
    for index, event in enumerate(events):
        if not isinstance(event, dict) or event.get("step") != index:
            raise ValueError(f"event {index} has invalid step")
        message = event.get("message")
        if not isinstance(message, dict):
            raise ValueError(f"event {index} has no message")
        role = message.get("role")
        if "tool_call" in message:
            call = message["tool_call"]
            if role != "assistant" or not isinstance(call, dict):
                findings.append(Finding("invalid_event", index, "malformed tool call"))
                continue
            name, args = call.get("name"), call.get("args")
            decisions += 1
            if pending is not None:
                findings.append(Finding("missing_tool_result", index, f"prior call {pending} has no result"))
            pending = name if isinstance(name, str) else "<invalid>"
            if name not in allowed:
                findings.append(Finding("unauthorized_tool", index, f"tool {name!r} is outside task allowlist"))
            if not isinstance(name, str) or not _valid_args(name, args):
                findings.append(Finding("invalid_args", index, f"tool {name!r} arguments do not match schema"))
            # Repetition is diagnostic evidence; a repeated call is not automatically a failed task.
            key = (str(name), repr(args))
            if key in seen_calls:
                findings.append(Finding("repeated_call", index, f"same call to {name!r} observed again"))
            seen_calls.add(key)
            if isinstance(name, str):
                called.add(name)
        elif role == "tool":
            name = message.get("name")
            if pending is None or name != pending:
                findings.append(Finding("orphan_tool_result", index, f"tool result for {name!r} has no matching call"))
            pending = None
            if "error" in message:
                findings.append(Finding("tool_error", index, f"tool {name!r} returned an error"))
        elif role == "assistant" and "content" in message:
            decisions += 1
            final_seen = True
            if pending is not None:
                findings.append(Finding("missing_tool_result", index, f"prior call {pending} has no result"))
                pending = None
        elif role != "user":
            findings.append(Finding("invalid_event", index, f"unexpected role {role!r}"))
    if pending is not None:
        findings.append(Finding("missing_tool_result", len(events) - 1, f"call {pending} has no result"))
    if decisions > max_steps:
        findings.append(Finding("step_limit_exceeded", None, f"{decisions} decisions exceed limit {max_steps}"))
    if observed_status == "max_steps" and not final_seen:
        findings.append(Finding("step_budget_exhausted", None, f"no final answer within {max_steps} decisions"))
    for name in sorted(set(required) - called):
        findings.append(Finding("required_tool_missing", None, f"required tool {name!r} was not called"))
    return findings
