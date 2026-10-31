"""Print one reproducible FakeModel → tool → final trace as JSON."""

from dataclasses import asdict
import json

from experiments.toy_agent.runtime import FakeModel, run_agent


def main() -> None:
    model = FakeModel([
        {"type": "tool_call", "name": "add", "args": {"a": 2, "b": 3}},
        {"type": "final", "answer": "The sum is 5"},
    ])
    result = run_agent("Add 2 and 3", model)
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
