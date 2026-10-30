# 官方 Harness² 评测系统源码审计（不可凭猜测填写）

> 状态：**源码 checkout 与 Demo 入口已验证；官方 benchmark evaluator/judge/report 审计仍 UNKNOWN**。这里是逐步核实的记录，不把存在的文件名当作已理解的评测能力。
> 不同版本/CLI 功能可能不同；以下只对锁定的本地 commit 有效。

## 1. 元数据
- 官方 repo：`https://github.com/google-research/harness2`
- 本地 checkout 路径：`upstream/harness2/`（Git submodule）
- commit SHA：`1cfe254e8d25b15f37048c3730134686abe60335`
- 日期 / 操作人：2026-10-30 / Codex
- 官方 README/文档版本：上述 commit；`README.md`、`pyproject.toml`、`docs/SETUP.md` 已读
- Git remote：`https://github.com/google-research/harness2.git`；checkout clean

## 2. 能力审计矩阵

| 模块 | 状态 VERIFIED/UNKNOWN/NOT_FOUND | 真实路径/函数或 CLI | 输入/输出格式 | 单测路径 | 运行证据 | 与自研模块的边界 |
|---|---|---|---|---|---|---|
| Task runner | UNKNOWN | | | | | 负责执行原生任务 |
| Benchmark evaluator / judge | UNKNOWN | | | | | 官方/原生 verdict 优先 |
| Baseline/base judge | UNKNOWN | | | | | 自研负责逐任务比较 |
| Report generation | UNKNOWN | | | | | 自研跨版本+回归报告 |
| Trajectory artifact/log | UNKNOWN | | | | | 自研 trace validator |
| Official unit/integration tests | UNKNOWN | | | | | 与个人 regression suite 不同 |
| Failure diagnostics | UNKNOWN | | | | | 自研 Bad Case 库 |
| Automatic regression rejection | UNKNOWN | | | | | 若官方已实现，先复用/扩展 |

## 3. 源码定位证据
- 运行的命令（原样复制）：`git ls-remote https://github.com/google-research/harness2.git HEAD`；`git submodule add https://github.com/google-research/harness2.git upstream/harness2`；`git -C upstream/harness2 rev-parse HEAD`。尚未执行官方程序。
- 退出码与日志路径：上述 Git 命令均 exit 0；命令输出记录于 `learning/stages/00.md`，未另存终端日志。
- `commit SHA:path:function`：`1cfe254e:harness2/cli/demo.py:main` → `1cfe254e:harness2/core/schedule.py:run_domain`；本地 `DemoAdapter.execute` 位于 `1cfe254e:harness2/demo.py`。入口脚本声明在 `pyproject.toml:32`。
- 一条任务的 `task_id → run_id → trajectory → verdict → report` 实际数据链：UNKNOWN（Demo 尚未运行；官方 benchmark evaluator 未审计）。
- 哪些功能不必重写：UNKNOWN（待 Stage 06–07 核对官方功能）。
- 哪些功能是项目原创扩展：目前仅有计划，尚无评测代码。

## 4. 必须解释给面试官的问题
1. 哪个组件真正决定 `resolved/failed`？由哪项程序化证据支持？
2. `base` 与 `optimized` 的结果如何对齐同一个 task_id？
3. 官方 unit tests 和对 Agent 能力的 regression evaluation 有何区别？
4. 候选 Harness 在线行为比较与最终公开 Benchmark 的 judge 有何区别？
5. 如何避免将官方原有模块描述为自己的开发成果？
