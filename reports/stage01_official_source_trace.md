# Stage 01 — official execution and tool-event source trace

Date: 2026-11-04 (Asia/Shanghai). Google Harness² submodule SHA: `1cfe254e8d25b15f37048c3730134686abe60335`.

This is a source audit plus a synthetic event-rendering probe. It is **not** a model-backed JobBench run or a benchmark result. The Agent's actual tool execution occurs inside an externally launched OpenCode process, not inside our project-owned `experiments/toy_agent/runtime.py`.

## Verified boundary and types

| Hop | Official source | Input → output | Failure boundary |
|---|---|---|---|
| Benchmark adapter | `harness2/benchmarks/jobbench.py:JobBenchAdapter.execute` (717) | `task_id: str`, `harness_dir: Path | None`, `run_id: str`, optional `timeout: int` → one run directory `Path` | Staging directory removed in `finally`; completion marker written only after substrate execution returns |
| Substrate contract | `harness2/substrate/base.py:RunRequest` (35), `Substrate.execute` (63), `Launcher` (44) | `RunRequest(task_ref: str, run_ids: tuple[str, ...], timeout: int)` + `Install` → `list[Path]` | Interface defines the boundary; it does not implement an Agent loop |
| OpenCode substrate | `harness2/substrate/opencode.py:OpencodeSubstrate.execute` (287) | Converts `run_ids: list[str]` to a `RunRequest`, calls benchmark-provided `_launcher`, returns `list[Path]` | Missing launcher raises `RuntimeError` before execution |
| JobBench launcher | `harness2/benchmarks/jobbench.py:_launch_opencode` (786), `_run_runner` (832), `_require_artifacts` (851) | One `RunRequest` → packaged runner + artifacts → `list[Path]` | Runner wall-timeout becomes `RuntimeError`; missing deliverables remain unmarked, even if JSONL events exist |
| OpenCode runner | `harness2/benchmarks/jb_opencode_runner.py:_attempt` (174), `run_one` (211), `main` (263) | OpenCode subprocess stdout → filtered JSONL `Path`; final deliverables → output directory | Retry resets task workspace; no final deliverable returns false and `main` exits nonzero |
| Trajectory rendering | `harness2/benchmarks/jobbench.py:trajectory` (869) → `OpencodeSubstrate.read_trajectory` (300) → `render_events` (334) | JSONL `Path` → rendered `str` | Unreadable file returns an error string; malformed JSON lines are skipped; empty parse returns a fallback string |

In `render_events`, a parsed tool event with `state.input` and `state.output` becomes `[ACTION]` and `[OBSERVATION]`. If `state.status == "error"`, it becomes `[ACTION]` and `[OBSERVATION ERROR]`. This is **trajectory text**, not the benchmark's final task verdict. The exact model-side Tool Call generation and tool execution were not audited here.

The pinned source also includes `third_party/lab_runner/opencode/session.py:parse` (line 28) and `to_transcript` (line 75). For a `part.type == "tool"` event, `parse` appends a dict with `name`, `input`, `output`, and `status` to `tool_calls: list[dict]`; `to_transcript` writes a `role="tool"` JSONL record with those fields. Both accept `state.status == "error"` as a recorded tool event. This is a second source-level view of one Tool Call's return structure and error state. It still reads events emitted by the external OpenCode process; it does not implement the model's tool decision or execute the tool itself.

## Observed synthetic renderer probe

The following command uses artificial JSONL events only. It imports the pinned official `render_events`, writes a temporary file, asserts the exact output, and deletes the file on exit. No model, benchmark task, network call, or paid API runs.

```powershell
@'
import json
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, "upstream/harness2")
from harness2.substrate.opencode import render_events

events = [
    {"type": "tool_call", "part": {"type": "tool_call", "name": "read_file", "state": {"input": {"path": "README.md"}, "output": "ok"}}},
    {"type": "tool_call", "part": {"type": "tool_call", "name": "read_file", "state": {"status": "error", "input": {"path": "missing.txt"}, "error": "not found"}}},
]
with tempfile.TemporaryDirectory() as temp_dir:
    path = Path(temp_dir) / "events.jsonl"
    path.write_text("\n".join(json.dumps(event) for event in events), encoding="utf-8")
    actual = render_events(path, obs_trunc=200, max_chars=2000)
expected = '[ACTION] read_file({"path": "README.md"})\n[OBSERVATION] ok\n[ACTION] read_file({"path": "missing.txt"})\n[OBSERVATION ERROR] not found'
assert actual == expected, repr(actual)
print(actual)
print("synthetic render_events probe: PASS")
'@ | python -
```

OBSERVED on 2026-11-04: exit 0; output:

```text
[ACTION] read_file({"path": "README.md"})
[OBSERVATION] ok
[ACTION] read_file({"path": "missing.txt"})
[OBSERVATION ERROR] not found
synthetic render_events probe: PASS
```

This verifies the renderer for two artificial event shapes. It does not verify that a live OpenCode process emits those exact shapes, that JobBench successfully runs, or that a task is solved.
