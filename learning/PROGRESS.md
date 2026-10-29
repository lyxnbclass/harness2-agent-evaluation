# 学习进度 — 唯一的人类可读当前状态

> 最后更新：2026-10-29（Stage 00 开发/教学分工调整与 Git 初始化）
> 操作纪律：**凡是“完成”必须有命令输出/代码路径/测试记录**。下一会话先读此文件。

- 当前阶段：00
- 当前阶段标题：开发环境、仓库溯源与官方 Demo
- 状态：IN_PROGRESS（仅完成首轮离线盘点，未运行官方 Demo）
- 官方 Harness² commit：UNKNOWN（尚未克隆/验证）
- 公开 Coding Benchmark：未选定（默认优先 SWE-bench，Stage 08 正式决策）
- 已验证完成的阶段：无
- 已验证的项目代码/实验：无
- 最近一次考核：尚未开始
- 已掌握的知识点（有无提示考核证据）：尚未评估
- 尚未掌握/待验证的知识点：全部待初测
- 阻塞：`upstream/harness2/` 仍不存在，官方源码 commit 和 Demo 尚未核实；Docker daemon/WSL 可运行性未知。`gh auth status` 曾报凭证无效，但本轮仓库创建与 Git Push 实际成功，应以具体操作结果为准。
- 用户明确批准下一阶段：否
- GitHub：用户确认仓库名 `harness2-agent-evaluation`、可见性 `public`；当前 branch `stage-00-setup`；main 初始 commit `46ba3d2` 已 Push；remote `https://github.com/lyxnbclass/harness2-agent-evaluation.git`；Stage 00 PR `NONE`；当前 Stage 考核 `未考`。

## 当前唯一下一步
Codex 检出官方 Harness² 源码到 `upstream/harness2/`，记录真实 commit、remote、tree 状态并阅读 README 确定 Demo 入口；随后分块讲解并安排用户代码/Trace 阅读题。**不要求用户手写脚本，不运行收费模型，不跳到 Stage 01**。

## 最近期真实证据
- `python scripts/resume.py` 与 `python scripts/check_workspace.py` 均退出 0；后者只说明记录完整性检查通过，不代表知识掌握。
- 用户已将分工调整为 Codex 负责实现与运行、用户负责理解与验收；上轮布置的用户手写环境脚本任务已取消，未据此评分。
- `git init -b main` 成功；检查拟提交文件和敏感凭证模式后，初始提交 `46ba3d2` 成功，创建 `stage-00-setup` 分支。公开仓库创建成功且 `main` 已 Push；Stage 00 分支待本轮记录提交后 Push。
- Windows 环境：Python 3.14.6、Git 2.41.0、uv 0.12.18、Docker CLI 29.8.0、Node v24.15.0；Docker 配置访问警告、WSL 状态查询被拒绝，运行能力仍待验证。
- 本工作区只有计划、规格、模板与离线校验脚本；**未克隆官方源码，未运行 Demo/Benchmark，未测出任何性能提升**。

## 对下个新会话的提醒
1. 运行 `python scripts/resume.py`，读取当前阶段 Gate 文件、错误记录与知识矩阵。
2. 在实际证据出现前不要改写上述“尚未完成”状态。
3. 本轮结束更新此文件、`stage_status.json`、`SESSION_LOG.md`、相应 Gate 文件，并运行 `python scripts/check_workspace.py`。
