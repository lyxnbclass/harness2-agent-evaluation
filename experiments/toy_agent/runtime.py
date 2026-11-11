"""A deterministic local Agent loop for studying tool calls, without a model API."""

from dataclasses import dataclass
from datetime import datetime, timezone
from math import isfinite
import subprocess
import sys
from time import perf_counter, sleep
from typing import Callable


class ToolError(Exception):
    def __init__(self, status: str, message: str):
        super().__init__(message)
        self.status = status


SCHEMAS = {
    "add": {"args": {"a": int, "b": int}, "output": str},
    "uppercase": {"args": {"text": str}, "output": str},
    "delay": {"args": {"seconds": int}, "output": str},
}
RETRYABLE_TOOLS = frozenset({"add", "uppercase"})


def run_tool(
    name: str, args: dict, *, timeout: float = 1.0,
    allowed_tools: frozenset[str] | None = None,
    max_retries: int = 0, retry_backoff: float = 0.01,
    on_retry: Callable[[int, ToolError], None] | None = None,
) -> str:
    if type(max_retries) is not int or not 0 <= max_retries <= 3:
        raise ValueError("max_retries must be between 0 and 3")
    if type(retry_backoff) not in (int, float) or not isfinite(retry_backoff) or not 0 <= retry_backoff <= 1:
        raise ValueError("retry_backoff must be between 0 and 1 second")
    if not isinstance(name, str):
        raise ToolError("invalid_args", "tool name must be a string")
    if allowed_tools is not None and name not in allowed_tools:
        raise ToolError("unauthorized_tool", f"tool {name!r} is outside task allowlist")
    schema = SCHEMAS.get(name)
    if schema is None:
        raise ToolError("unknown_tool", f"unknown tool: {name}")
    expected_args = schema["args"]
    if not isinstance(args, dict) or set(args) != set(expected_args):
        raise ToolError("invalid_args", f"{name} expects {sorted(expected_args)}")
    if any(type(args[key]) is not kind for key, kind in expected_args.items()):
        raise ToolError("invalid_args", f"{name} argument types do not match schema")
    for attempt in range(max_retries + 1):
        try:
            output = _execute_tool(name, args, timeout=timeout)
            break
        except ToolError as exc:
            if exc.status != "tool_timeout" or name not in RETRYABLE_TOOLS or attempt == max_retries:
                raise
            if on_retry is not None:
                on_retry(attempt + 1, exc)
            sleep(retry_backoff * (2 ** attempt))
    if type(output) is not schema["output"]:
        raise ToolError(
            "invalid_tool_result",
            f"{name} returned {type(output).__name__}; expected {schema['output'].__name__}",
        )
    return output


def _execute_tool(name: str, args: dict, *, timeout: float) -> str:
    if name == "add":
        return str(args["a"] + args["b"])
    if name == "uppercase":
        return args["text"].upper()
    if name != "delay":
        raise ToolError("tool_error", f"no executor for {name}")
    seconds = args["seconds"]
    if not 0 <= seconds <= 5:
        raise ToolError("invalid_args", "delay seconds must be between 0 and 5")
    try:
        subprocess.run(
            [sys.executable, "-c", f"import time; time.sleep({seconds})"],
            check=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise ToolError("tool_timeout", f"delay exceeded {timeout}s") from exc
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ToolError("tool_error", f"delay execution failed: {exc}") from exc
    return "done"


@dataclass
class RunResult:
    status: str
    answer: str | None
    trace: list[dict]


class FakeModel:
    def __init__(self, decisions: list[dict]):
        self.decisions = decisions
        self.index = 0
        self.seen: list[list[dict]] = []

    def next(self, messages: list[dict]) -> dict:
        self.seen.append([dict(message) for message in messages])
        if self.index >= len(self.decisions):
            raise StopIteration
        decision = self.decisions[self.index]
        self.index += 1
        return decision


def run_agent(
    prompt: str, model: FakeModel, *, max_steps: int = 5, tool_timeout: float = 1.0,
    event_sink: Callable[[dict], None] | None = None,
    allowed_tools: frozenset[str] | None = None,
    max_tool_retries: int = 0, retry_backoff: float = 0.01,
) -> RunResult:
    if type(max_steps) is not int or max_steps < 1 or tool_timeout <= 0:
        raise ValueError("max_steps and tool_timeout must be positive")
    if (allowed_tools is not None and
            (not isinstance(allowed_tools, frozenset) or not allowed_tools.issubset(SCHEMAS))):
        raise ValueError("allowed_tools must be a frozenset of known tool names")
    if type(max_tool_retries) is not int or not 0 <= max_tool_retries <= 3:
        raise ValueError("max_tool_retries must be between 0 and 3")
    if type(retry_backoff) not in (int, float) or not isfinite(retry_backoff) or not 0 <= retry_backoff <= 1:
        raise ValueError("retry_backoff must be between 0 and 1 second")
    trace: list[dict] = []
    started = perf_counter()

    def record(event: dict) -> None:
        trace.append(event)
        if event_sink is not None:
            event_type = (
                "tool_call" if "tool_call" in event else
                "tool_error" if event.get("role") == "tool" and "error" in event else
                "tool_result" if event.get("role") == "tool" else
                "final" if event.get("role") == "assistant" else "input"
            )
            event_sink({
                "step": len(trace) - 1,
                "event_type": event_type,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "elapsed_ms": round((perf_counter() - started) * 1000, 3),
                "message": dict(event),
            })

    record({"role": "user", "content": prompt})
    for _ in range(max_steps):
        try:
            decision = model.next(trace)
        except StopIteration:
            return RunResult("model_exhausted", None, trace)
        if not isinstance(decision, dict):
            return RunResult("invalid_model_output", None, trace)
        if decision.get("type") == "final" and isinstance(decision.get("answer"), str):
            record({"role": "assistant", "content": decision["answer"]})
            return RunResult("completed", decision["answer"], trace)
        if decision.get("type") != "tool_call":
            return RunResult("invalid_model_output", None, trace)
        name, args = decision.get("name"), decision.get("args")
        record({"role": "assistant", "tool_call": {"name": name, "args": args}})
        retries: list[int] = []
        try:
            output = run_tool(
                name, args, timeout=tool_timeout, allowed_tools=allowed_tools,
                max_retries=max_tool_retries, retry_backoff=retry_backoff,
                on_retry=lambda attempt, _error: retries.append(attempt),
            )
        except ToolError as exc:
            error_event = {"role": "tool", "name": name, "error": str(exc)}
            if retries:
                error_event["attempts"] = len(retries) + 1
            record(error_event)
            return RunResult(exc.status, None, trace)
        result_event = {"role": "tool", "name": name, "content": output}
        if retries:
            result_event["attempts"] = len(retries) + 1
        record(result_event)
    return RunResult("max_steps", None, trace)
