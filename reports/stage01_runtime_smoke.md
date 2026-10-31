# Stage 01 — deterministic local Agent Runtime smoke test

Date: 2026-10-31 (Asia/Shanghai). The implementation is project-owned code written by Codex for teaching and testing; the project owner has not yet reviewed the Stage 01 code or answered its chapter questions. No paid model or external tool was used.

## Contract and run

`experiments/toy_agent/runtime.py:run_agent(prompt, model, max_steps, tool_timeout)` returns `RunResult(status, answer, trace)`. `FakeModel` supplies scripted decisions. `run_tool()` accepts only `add(a:int,b:int)`, `uppercase(text:str)`, and `delay(seconds:int)` with exactly the declared keys and types. `max_steps` counts model decisions, including a final answer. The trace carries the user input, assistant tool call, tool result or error, and final assistant answer if reached.

```powershell
$python312 = uv python find 3.12
& $python312 -m experiments.toy_agent.demo
& $python312 -m unittest discover -s experiments/toy_agent -p test_runtime.py -v
```

Both exited 0. `reports/stage01_toy_agent_demo.json` records `Add 2 and 3` → `add(2,3)` → tool result `5` → final `The sum is 5`; status `completed`. The test command reported `Ran 6 tests in 0.157s`, `OK` on the repeat run.

## Failure counterexamples

- A one-second local `delay` run with a 0.01-second timeout returns `tool_timeout`, a tool error trace item, and no answer. This is an actual subprocess timeout in the local test.
- `delete_all` returns `unknown_tool` and is never invoked.
- Wrong argument types or extra fields return `invalid_args`. In particular, `True` is rejected where an `int` is required, despite Python treating `bool` as an `int` subtype.
- A missing final decision returns `model_exhausted`; repeated tool calls stop at `max_steps`.

## Relationship to Google Harness²

At upstream SHA `1cfe254e8d25b15f37048c3730134686abe60335`, `harness2/substrate/base.py:RunRequest/Substrate.execute` defines the execution boundary, `harness2/substrate/opencode.py:OpencodeSubstrate.execute` delegates to a benchmark-supplied launcher, and its `render_events()` converts captured tool events into trajectory text. This Toy Runtime demonstrates the Agent loop *inside* that kind of execution conceptually. It does not run Harness²'s model-backed substrate, validate its launcher, or measure benchmark performance.
