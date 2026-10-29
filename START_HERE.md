# 从这里开始：Harness² AI Agent 工程学习工作区（最终版 v3.0）

目标交付：**官方 Harness² 复现 + 一个公开 Coding Benchmark + 自研评测与回归测试系统**，同时掌握 Python/Agent Runtime/Trace/LLM Judge/优化闭环/Reflection 与长期记忆，能独立参加工程面试。

## 你现在拿到的是什么
这是一套**学习流程、评测系统开发规格与进度管理工作区**，不是已经复现完成的项目代码。`upstream/harness2/`、Benchmark、API 运行结果都需要在你自己的环境里逐步完成。初始状态全部为未完成。

## 使用步骤
1. 将**本文件夹内容**复制到一个专用工作目录根部，在 Codex 中打开该目录。`AGENTS.md` 必须位于当前项目根目录以便后续会话读取。
2. 不要删除 `learning/`。优先把整个工作目录纳入你自己的 Git 仓库；请勿提交密钥、第三方数据的限制性内容或大型运行输出。
3. 给 Codex 发送 `CODEX_START_PROMPT.md` 中的提示词；先做阶段 00，不自动跳到后续阶段。
4. Codex 每次对话开始先执行 `python scripts/resume.py`；结束时更新所有状态文件，再执行 `python scripts/check_workspace.py`。
5. 若需要切换机器，复制整个工作区或提交记录（需排除密钥、私有资源、大型实验输出）；**聊天历史不是项目进度的替代品**。

**分工：** Codex 负责代码、环境、测试、调试、Git/GitHub 和实验记录；用户负责理解代码与方案、分析真实 Trace/故障、回答面试问题并验收。每个重要功能实现后，Codex 必须结合真实输入输出讲清场景、架构位置、函数与数据流、错误和修复，再进行不预告答案的考核。用户无需手写 Python 或自行配置环境。

## 官方资料（任务实施时以本地 checkout 的版本为准）
- Harness²：https://github.com/google-research/harness2
- Harness² 论文：https://arxiv.org/abs/2610.14224
- SWE-bench：https://github.com/SWE-bench/SWE-bench
- Multi-SWE-bench：https://github.com/multi-swe-bench/multi-swe-bench
- DeepSWE：https://github.com/datacurve-ai/deep-swe

## 本工作区的关键文件
- `AGENTS.md`：Codex 强制操作/教学/通关/记录约束
- `MASTER_PLAN.md`：14 个阶段的完整学习、代码实验、Benchmark、面试要求
- `CODEX_START_PROMPT.md`：第一轮与之后新会话的启动提示词
- `learning/PROGRESS.md`：**先读它**，确定真实当前阶段
- `learning/stage_status.json`：机器可读的状态，不等同实际掌握
- `learning/gates/`：每个阶段的问答/实操考核记录
- `learning/MASTERY_MATRIX.md`：知识点是否能在无提示下说明
- `learning/SESSION_LOG.md`：每轮做了什么、没做什么、下一步
- `learning/MISTAKES.md`：错误、纠正和变式复测结果
- `experiments/manifests/`：实验可复现配置样板
- `learning/OFFICIAL_EVAL_AUDIT.md`：必须先核实官方已有 Evaluator/Judge/Report/测试，避免重复开发
- `EVALUATION_SYSTEM_SPEC.md`：个人评测、Trajectory、Bad Case、Regression Gate 的具体实现标准
- `PROJECT_DELIVERABLES.md`：三个必交付 + 面试项目证据清单

注意：Codex 编程助手和 Harness² 被测的 Codex Executor 不是一回事。没有预算或网络时也能继续源码/单元测试学习，但不能假装已完成真实模型 Benchmark。

## 重要区分
ZIP 中有**14 阶段任务、代码规格、题目记录模板和离线校验脚本**；尚未包含 Google 官方仓库，也**没有假装已经实现评测器或跑出论文成绩**。Codex 按计划逐步开发，用户逐阶段理解并验收。
