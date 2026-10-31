"""A deterministic local Agent loop for studying tool calls, without a model API."""

from dataclasses import dataclass
import subprocess
import sys


class ToolError(Exception):
    def __init__(self, status: str, message: str):
        super().__init__(message)
        self.status = status


SCHEMAS = {
    "add": {"a": int, "b": int},
    "uppercase": {"text": str},
    "delay": {"seconds": int},
}


def run_tool(name: str, args: dict, *, timeout: float = 1.0) -> str:
    schema = SCHEMAS.get(name)
    if schema is None:
        raise ToolError("unknown_tool", f"unknown tool: {name}")
    if not isinstance(args, dict) or set(args) != set(schema):
        raise ToolError("invalid_args", f"{name} expects {sorted(schema)}")
    if any(type(args[key]) is not kind for key, kind in schema.items()):
        raise ToolError("invalid_args", f"{name} argument types do not match schema")
    if name == "add":
        return str(args["a"] + args["b"])
    if name == "uppercase":
        return args["text"].upper()
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
    prompt: str, model: FakeModel, *, max_steps: int = 5, tool_timeout: float = 1.0
) -> RunResult:
    if type(max_steps) is not int or max_steps < 1 or tool_timeout <= 0:
        raise ValueError("max_steps and tool_timeout must be positive")
    trace: list[dict] = [{"role": "user", "content": prompt}]
    for _ in range(max_steps):
        try:
            decision = model.next(trace)
        except StopIteration:
            return RunResult("model_exhausted", None, trace)
        if not isinstance(decision, dict):
            return RunResult("invalid_model_output", None, trace)
        if decision.get("type") == "final" and isinstance(decision.get("answer"), str):
            trace.append({"role": "assistant", "content": decision["answer"]})
            return RunResult("completed", decision["answer"], trace)
        if decision.get("type") != "tool_call":
            return RunResult("invalid_model_output", None, trace)
        name, args = decision.get("name"), decision.get("args")
        trace.append({"role": "assistant", "tool_call": {"name": name, "args": args}})
        try:
            output = run_tool(name, args, timeout=tool_timeout)
        except ToolError as exc:
            trace.append({"role": "tool", "name": name, "error": str(exc)})
            return RunResult(exc.status, None, trace)
        trace.append({"role": "tool", "name": name, "content": output})
    return RunResult("max_steps", None, trace)
