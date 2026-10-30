# 官方源码索引（真实定位后才填写）

- 官方项目：https://github.com/google-research/harness2
- 官方站点：https://harness2.github.io/（由官方 README 链接，本文源码结论仍以本地 commit 为准）
- 本地检出目录：`upstream/harness2/`（Git submodule，已验证）
- Commit SHA：`1cfe254e8d25b15f37048c3730134686abe60335`
- 运行环境：源码尚未执行；本机 Docker Linux daemon 与 `python:3.12-slim-trixie` 镜像已核实，Demo 运行待验证

| 主题 | 已验证源码路径 | 函数/类 | 调用者 → 被调用方 | commit SHA | 证据与测试 |
|---|---|---|---|---|---|
| CLI → Run | `pyproject.toml:26–32`; `harness2/cli/demo.py:27` | `main(argv=None)` | `harness2-demo` → `main()` → `run_domain()` | `1cfe254e` | 源码核实；未运行 |
| Demo | `harness2/cli/demo.py:27–54`; `harness2/core/schedule.py:669`; `harness2/demo.py:41,67,86,123` | `main`, `run_domain`, `DemoAdapter.tasks/execute`, `DemoProposer.call` | CLI 构造 adapter/proposer → domain 调度 → 本地 Python 执行 → `answer.txt`/`trajectory.md` → `demo.json` | `1cfe254e` | 源码核实；产物路径为源码声明，实际产物未验证 |
| Agent Executor | NOT_VERIFIED（真实模型执行器未审计） | | Demo 仅使用 `DemoAdapter.execute` 的本地子进程 | | 不得把本地 Demo 称为模型执行 |
| Propose | NOT_VERIFIED | | | | |
| Probe | NOT_VERIFIED | | | | |
| Compose | NOT_VERIFIED | | | | |
| Reflect | NOT_VERIFIED | | | | |
| Benchmark Adapter | NOT_VERIFIED | | | | |
| Judge / Report | NOT_VERIFIED | | | | |

> 未检查本地代码禁止填入猜测的路径、函数名或行号。
