# 学习进度 — 唯一的人类可读当前状态

> 最后更新：2026-10-30（Stage 00 官方无模型 Demo 实跑与六步教学协议）
> 操作纪律：**凡是“完成”必须有命令输出/代码路径/测试记录**。下一会话先读此文件。

- 当前阶段：00
- 当前阶段标题：开发环境、仓库溯源与官方 Demo
- 状态：IN_PROGRESS（官方源码已锁定，隔离的无模型 Demo 已运行；系统教学与 Gate 尚未完成）
- 官方 Harness² commit：`1cfe254e8d25b15f37048c3730134686abe60335`（Git submodule，remote 与 clean tree 已核实）
- 公开 Coding Benchmark：未选定（默认优先 SWE-bench，Stage 08 正式决策）
- 已验证完成的阶段：无
- 已验证的项目代码/实验：官方无模型 Demo `--k 1 --mode both` 在 Docker Linux/Python 3.12 退出 0；2 个账本任务 `ok`，详见 `learning/stages/00.md`。无自研 Agent 代码或模型实验。
- 最近一次考核：尚未开始
- 最近教学：2026-10-30 按用户最新要求建立六步教学协议与独立 `learning/KNOWLEDGE_MASTERY.md`，本轮开始从 Harness² 整体概念和已实跑 Demo 讲起；此前的 `--k 0` 问题撤回，尚无独立回答或评分。
- 已掌握的知识点（有无提示考核证据）：尚未评估
- 尚未掌握/待验证的知识点：全部待初测
- 阻塞：无模型调用需求；默认 Python 3.14.6 不满足上游 `<3.14` 要求，已用 Docker Python 3.12 完成无模型 Demo。官方 benchmark evaluator/judge/report 仍 UNKNOWN，真实模型运行未获批准。
- 用户明确批准下一阶段：否
- GitHub：公开仓库 `https://github.com/lyxnbclass/harness2-agent-evaluation`；当前 branch `stage-00-setup`；官方源码固定提交 `0b1902d` 已 Push；正式根目录 README 已在 `main` 的 `f7a0ae1` 发布并经 GitHub API 核实；Stage 00 PR `NONE`；当前 Stage 考核 `未考`。

## 当前唯一下一步
Codex 完成 Stage 00 整体概念与官方无模型 Demo 的系统讲解，在用户理解当前整体图后，下一小节深入 `harness2-demo` 入口与 `argparse`。**不要求用户手写脚本，不运行收费模型，不跳到 Stage 01**。

## 最近期真实证据
- 2026-10-30 `docker run` 以 `python:3.12-slim-trixie`、`--network none`、只读源码挂载、隔离输出挂载执行 `python -m harness2.cli.demo --output /out/raw_runs/stage00_demo_k1 --k 1 --mode both`，退出 0；终端显示两个任务 `ok`。`demo.json` 记录 `done=2`、`failed=0`、`execution_count=14`、`editor_calls=16`。`ledger-1` 基线 `Total: 105.25`，parallel final 和 sequential final 均 `Total: 85.15`。本地原始产物在 `experiments/raw_runs/stage00_demo_k1/`（忽略目录），证据摘要在 `learning/stages/00.md`；无付费模型、无真实 Benchmark 判分。
- `git ls-remote`、父仓库 Git submodule gitlink 与本地 checkout 均指向 `1cfe254e8d25b15f37048c3730134686abe60335`；官方 remote 为 `https://github.com/google-research/harness2.git`，checkout clean，保留官方 Apache 2.0 `LICENSE`。`pyproject.toml:32` 声明 `harness2-demo` 入口，`harness2/cli/demo.py:main` → `harness2/core/schedule.py:run_domain` → `harness2/demo.py:DemoAdapter.execute` 的源码路径与本轮无模型运行已核实。
- 根目录 `README.md` 已基于用户提供的英文素材建立并发布到 GitHub 默认 `main`，GitHub API 返回 `README.md`。本轮 Stage 00 分支中的 README 已补充 Demo 真实结果；公开 Benchmark 与自研评测模块未完成。`AGENTS.md` 已规定每阶段 PR 合并后的 README 同步维护。本文档工作不构成 Stage 00 技术 Gate 通过。
- `python scripts/resume.py` 与 `python scripts/check_workspace.py` 均退出 0；后者只说明记录完整性检查通过，不代表知识掌握。
- 用户已将分工调整为 Codex 负责实现与运行、用户负责理解与验收；上轮布置的用户手写环境脚本任务已取消，未据此评分。
- `git init -b main` 成功；检查拟提交文件和敏感凭证模式后，初始提交 `46ba3d2` 成功，创建 `stage-00-setup` 分支。公开仓库创建成功，`main` 与 Stage 00 分支均已 Push；`gh auth status` 复查退出 0。
- Windows 环境：Python 3.14.6、Git 2.41.0、uv 0.12.18、Docker CLI 29.8.0、Node v24.15.0；Docker 配置访问警告、WSL 状态查询被拒绝，运行能力仍待验证。
- 本工作区已有官方源码的固定版本 submodule，以及计划、规格、模板与离线校验脚本；**未运行 Demo/Benchmark，未测出任何性能提升**。

## 对下个新会话的提醒
1. 运行 `python scripts/resume.py`，读取当前阶段 Gate 文件、错误记录与知识矩阵。
2. 在实际证据出现前不要改写上述“尚未完成”状态。
3. 本轮结束更新此文件、`stage_status.json`、`SESSION_LOG.md`、相应 Gate 文件，并运行 `python scripts/check_workspace.py`。
