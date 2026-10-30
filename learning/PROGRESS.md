# 学习进度 — 唯一的人类可读当前状态

> 最后更新：2026-10-30（Stage 00 官方源码溯源）
> 操作纪律：**凡是“完成”必须有命令输出/代码路径/测试记录**。下一会话先读此文件。

- 当前阶段：00
- 当前阶段标题：开发环境、仓库溯源与官方 Demo
- 状态：IN_PROGRESS（官方源码已锁定并追踪 Demo 入口，Demo 尚未运行）
- 官方 Harness² commit：`1cfe254e8d25b15f37048c3730134686abe60335`（Git submodule，remote 与 clean tree 已核实）
- 公开 Coding Benchmark：未选定（默认优先 SWE-bench，Stage 08 正式决策）
- 已验证完成的阶段：无
- 已验证的项目代码/实验：无
- 最近一次考核：尚未开始
- 已掌握的知识点（有无提示考核证据）：尚未评估
- 尚未掌握/待验证的知识点：全部待初测
- 阻塞：无模型调用需求；官方 Demo 尚未在隔离环境中执行。默认 Python 3.14.6 不满足上游 `<3.14` 要求；可用的 Docker Linux daemon 和本地 `python:3.12-slim-trixie` 镜像已核实。官方 benchmark evaluator/judge/report 仍 UNKNOWN。
- 用户明确批准下一阶段：否
- GitHub：公开仓库 `https://github.com/lyxnbclass/harness2-agent-evaluation`；当前 branch `stage-00-setup` 已 Push；正式根目录 README 已在 `main` 的 `f7a0ae1` 发布并经 GitHub API 核实，分支文档提交 `7f5d5e1` 已同步；Stage 00 PR `NONE`；当前 Stage 考核 `未考`。

## 当前唯一下一步
Codex 在隔离的 Python 3.12 Linux 容器中运行无需模型凭证的官方 Demo，并核对 `demo.json`、`answer.txt`、`trajectory.md` 的真实数据流；随后让用户解释入口与产物关系。**不要求用户手写脚本，不运行收费模型，不跳到 Stage 01**。

## 最近期真实证据
- `git ls-remote`、父仓库 Git submodule gitlink 与本地 checkout 均指向 `1cfe254e8d25b15f37048c3730134686abe60335`；官方 remote 为 `https://github.com/google-research/harness2.git`，checkout clean，保留官方 Apache 2.0 `LICENSE`。`pyproject.toml:32` 声明 `harness2-demo` 入口，`harness2/cli/demo.py:main` → `harness2/core/schedule.py:run_domain` → `harness2/demo.py:DemoAdapter.execute` 的源码路径已核实，未执行官方代码。
- 根目录 `README.md` 已基于用户提供的英文素材建立并发布到 GitHub 默认 `main`，GitHub API 返回 `README.md`。内容对照当前文件树与 Stage 00 记录：官方源码、Demo、公开 Benchmark 和自研评测模块均未完成；`AGENTS.md` 已规定每阶段 PR 合并后的 README 同步维护。本文档工作不构成 Stage 00 技术 Gate 通过。
- `python scripts/resume.py` 与 `python scripts/check_workspace.py` 均退出 0；后者只说明记录完整性检查通过，不代表知识掌握。
- 用户已将分工调整为 Codex 负责实现与运行、用户负责理解与验收；上轮布置的用户手写环境脚本任务已取消，未据此评分。
- `git init -b main` 成功；检查拟提交文件和敏感凭证模式后，初始提交 `46ba3d2` 成功，创建 `stage-00-setup` 分支。公开仓库创建成功，`main` 与 Stage 00 分支均已 Push；`gh auth status` 复查退出 0。
- Windows 环境：Python 3.14.6、Git 2.41.0、uv 0.12.18、Docker CLI 29.8.0、Node v24.15.0；Docker 配置访问警告、WSL 状态查询被拒绝，运行能力仍待验证。
- 本工作区已有官方源码的固定版本 submodule，以及计划、规格、模板与离线校验脚本；**未运行 Demo/Benchmark，未测出任何性能提升**。

## 对下个新会话的提醒
1. 运行 `python scripts/resume.py`，读取当前阶段 Gate 文件、错误记录与知识矩阵。
2. 在实际证据出现前不要改写上述“尚未完成”状态。
3. 本轮结束更新此文件、`stage_status.json`、`SESSION_LOG.md`、相应 Gate 文件，并运行 `python scripts/check_workspace.py`。
