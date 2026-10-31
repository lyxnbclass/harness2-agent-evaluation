# Stage 00 — Official deterministic Demo smoke test

Date: 2026-10-31 (Asia/Shanghai)
Upstream: Google Research Harness², Git submodule SHA `1cfe254e8d25b15f37048c3730134686abe60335`
Attribution: official Demo and `tests/test_workflow.py` are Google upstream code; Codex ran and documented them. The project owner reviewed the explanations and requested the next Stage 00 engineering step.

## OBSERVED: isolated Demo

From the repository root, the pinned source was mounted read-only and the output was mounted separately. The image was already available locally; execution had no network or model credentials.

```powershell
docker run --rm --network none --read-only --tmpfs /tmp:rw,noexec,nosuid,size=64m --security-opt no-new-privileges --cap-drop ALL --mount "type=bind,source=$((Get-Location).Path)\upstream\harness2,target=/src,readonly" --mount "type=bind,source=$((Get-Location).Path)\experiments,target=/out" -w /src -e PYTHONPATH=/src python:3.12-slim-trixie python -m harness2.cli.demo --output /out/raw_runs/stage00_demo_k1 --k 1 --mode both
```

Exit 0. `experiments/raw_runs/stage00_demo_k1/demo.json`: 2 tasks done, 0 failed, 14 local executions, 16 scripted editor calls. For `ledger-1`, the base answer was `Total: 105.25`; parallel final `agg1` and sequential final `c1` each returned `Total: 85.15`. For `ledger-2`, the base was `35.50` and both finals were `20.25`. The raw directory is Git ignored; `learning/stages/00.md` records the original paths and evidence.

Verified local path through the pinned source:

```text
CLI main() -> DemoAdapter (task CSV + base harness) -> run_domain()
           -> run_task() -> shared base execution -> answer/trajectory
                         -> run_parallel() / run_sequential()
                         -> DemoProposer.call() -> candidate harness
                         -> DemoAdapter.execute() -> candidate answer/trajectory
                         -> final selection -> summary.json / experience library
           -> demo.json
```

`DemoAdapter.execute()` runs a local Python script. It is the Demo execution boundary here; no model-backed executor or native benchmark judge is exercised.

## OBSERVED: official tests

```powershell
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=256m --security-opt no-new-privileges --cap-drop ALL --mount "type=bind,source=$((Get-Location).Path)\upstream\harness2,target=/src,readonly" -w /src -e PYTHONPATH=/src python:3.12-slim-trixie python -m unittest discover -s tests -p test_workflow.py -v
```

Exit 0: `Ran 5 tests in 9.648s`, `OK`. The upstream tests cover execution budgets and resume behavior, failed selection, invalid proposal retry, and experience-library behavior. No project-owned Agent implementation is claimed at Stage 00.

## OBSERVED: output-path failure injection

```powershell
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=64m --security-opt no-new-privileges --cap-drop ALL --mount "type=bind,source=$((Get-Location).Path)\upstream\harness2,target=/src,readonly" -w /src -e PYTHONPATH=/src python:3.12-slim-trixie python -m harness2.cli.demo --output /src/stage00_unwritable --k 1 --mode both
```

Exit 1: `OSError: [Errno 30] Read-only file system: '/src/stage00_unwritable'`. The failure occurs while `DemoAdapter.__init__()` writes the base harness through `tree.write_tree()`, before `run_domain()` starts. A writable, isolated output mount resolves this configuration error. A separate timeout probe and invalid-`k` check are documented in `learning/stages/00.md`.

## Limits and next engineering boundary

This verifies a deterministic local workflow on two arithmetic tasks. Its `ok` status is not a native benchmark verdict or evidence of model improvement. No paid model, SWE-bench evaluator, baseline comparison, token cost, or latency experiment ran. The official benchmark judge/report flow remains `UNKNOWN` in `learning/OFFICIAL_EVAL_AUDIT.md` and must be audited before project evaluation extensions are built.
