# 官方源码索引（真实定位后才填写）

- 官方项目：https://github.com/google-research/harness2
- 官方站点：https://harness2.github.io/（由官方 README 链接，本文源码结论仍以本地 commit 为准）
- 本地检出目录：`upstream/harness2/`（Git submodule，已验证）
- Commit SHA：`1cfe254e8d25b15f37048c3730134686abe60335`
- 运行环境：Docker Linux daemon + `python:3.12-slim-trixie`；无网络、只读源码挂载；官方无模型 Demo `--k 1 --mode both` 已退出 0，原始产物 `experiments/raw_runs/stage00_demo_k1/`

| 主题 | 已验证源码路径 | 函数/类 | 调用者 → 被调用方 | commit SHA | 证据与测试 |
|---|---|---|---|---|---|
| CLI → Run | `pyproject.toml:26–32`; `harness2/cli/demo.py:27` | `main(argv=None)` | `harness2-demo` → `main()` → `run_domain()` | `1cfe254e` | 源码核实；`python -m harness2.cli.demo --k 1 --mode both` 在隔离容器退出 0 |
| Demo | `harness2/cli/demo.py:27–54`; `harness2/core/schedule.py:669`; `harness2/demo.py:41,67,86,123` | `main`, `run_domain`, `DemoAdapter.tasks/execute`, `DemoProposer.call` | CLI 构造 adapter/proposer → domain 调度 → 本地 Python 执行 → `answer.txt`/`trajectory.md` → `demo.json` | `1cfe254e` | 源码与实际运行均核实；`experiments/raw_runs/stage00_demo_k1/demo.json` 2 ok / 0 failed，`ledger-1` base 105.25 → final 85.15 |
| Agent Executor | NOT_VERIFIED（真实模型执行器未审计） | | Demo 仅使用 `DemoAdapter.execute` 的本地子进程 | | 不得把本地 Demo 称为模型执行 |
| Substrate execution boundary | `harness2/substrate/base.py:RunRequest/Substrate.execute`; `harness2/substrate/opencode.py:OpencodeSubstrate.execute` | `RunRequest`, `Substrate.execute`, `OpencodeSubstrate.execute` | Benchmark adapter provides launcher; substrate passes task_ref/run_ids/timeout and staged Install to it | `1cfe254e` | 源码已定位；真实 OpenCode/模型未运行 |
| OpenCode tool-event rendering | `harness2/substrate/opencode.py:render_events` | `render_events` | 捕获的 `tool/tool_use/tool_call` 事件 → `[ACTION]` / `[OBSERVATION]`，错误 → `[OBSERVATION ERROR]` | `1cfe254e` | 源码已定位；本轮未运行真实 OpenCode 事件 |
| Propose | NOT_VERIFIED | | | | |
| Probe | NOT_VERIFIED | | | | |
| Compose | NOT_VERIFIED | | | | |
| Reflect | NOT_VERIFIED | | | | |
| Benchmark Adapter | NOT_VERIFIED | | | | |
| Judge / Report | NOT_VERIFIED | | | | |

> 未检查本地代码禁止填入猜测的路径、函数名或行号。
