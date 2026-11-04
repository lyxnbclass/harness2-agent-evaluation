# Stage 01 — local Runtime tool contract extension

Date: 2026-11-04 (Asia/Shanghai). This is project-owned teaching code written by Codex, not a Google Harness² implementation or benchmark result.

## Contract

`SCHEMAS` now declares exact input fields/types and a `str` output type for `add`, `uppercase`, and `delay`. `run_tool()` rejects a non-string tool name as `invalid_args`; after `_execute_tool()`, it rejects a non-string result as `invalid_tool_result` before the result can enter `run_agent()`'s trace. This checks result **type**, not semantic truth. A string containing an incorrect answer could still pass.

`max_steps` counts model decisions. At `max_steps=1`, a valid first decision `add(2,3)` adds a Tool Result `"5"` to a three-message trace, then returns `RunResult(status="max_steps", answer=None, trace=...)`. A prewritten `final` decision is not read.

## Reproduction and observed results

```powershell
$python312 = uv python find 3.12
& $python312 -m unittest discover -s experiments/toy_agent -p test_runtime.py -v
& $python312 -m experiments.toy_agent.demo
```

OBSERVED on local Python 3.12: both commands exited 0; `Ran 8 tests in 0.132s`, `OK`. The Demo retained its original four messages and `status="completed"`, `answer="The sum is 5"`.

The new counterexamples inject an integer `add` output to verify `invalid_tool_result` and no second FakeModel decision, and exercise the one-step budget with a valid tool result but no final answer. The unknown-tool test also checks a list-valued tool name returns `invalid_args` rather than an uncaught `TypeError`.

These checks use FakeModel and local tools. They do not validate a real model, the official OpenCode substrate, or a coding benchmark outcome.
