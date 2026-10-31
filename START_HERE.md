# 从这里开始：Harness² AI Agent 工程学习工作区（章节教学 v4.0）

目标交付：**官方 Harness² 复现 + 一个公开 Coding Benchmark + 自研评测与回归测试系统**，同时掌握 Python/Agent Runtime/Trace/LLM Judge/优化闭环/Reflection 与长期记忆，能独立参加工程面试。

## 你现在拿到的是什么
这是一套**学习流程、评测系统开发规格与进度管理工作区**，不是已经复现完成的项目代码。`upstream/harness2/`、Benchmark、API 运行结果都需要在你自己的环境里逐步完成。初始状态全部为未完成。

## 使用步骤
1. 将**本文件夹内容**复制到一个专用工作目录根部，在 Codex 中打开该目录。`AGENTS.md` 必须位于当前项目根目录以便后续会话读取。
2. 不要删除 `learning/`。优先把整个工作目录纳入你自己的 Git 仓库；请勿提交密钥、第三方数据的限制性内容或大型运行输出。
3. 给 Codex 发送 `CODEX_START_PROMPT.md` 中的提示词；先做阶段 00，不自动跳到后续阶段。
4. Codex 每次新会话从 `learning/PROGRESS.md` 和 `learning/MASTERY_MATRIX.md` 恢复章节与疑问，核对实际证据；辅助脚本可检查记录一致性。
5. 若需要切换机器，复制整个工作区或提交记录（需排除密钥、私有资源、大型实验输出）；**聊天历史不是项目进度的替代品**。

**分工：** Codex 负责代码、环境、测试、调试、Git/GitHub 和实验记录；用户负责理解代码与方案、分析真实 Trace/故障、回答章节思考题并验收。每章按 `AGENTS.md` 七部分结构一次讲清，不评分；用户无需手写 Python 或自行配置环境。

## 官方资料（任务实施时以本地 checkout 的版本为准）
- Harness²：https://github.com/google-research/harness2
- Harness² 论文：https://arxiv.org/abs/2610.14224
- SWE-bench：https://github.com/SWE-bench/SWE-bench
- Multi-SWE-bench：https://github.com/multi-swe-bench/multi-swe-bench
- DeepSWE：https://github.com/datacurve-ai/deep-swe

## 本工作区的关键文件
- `AGENTS.md`：Codex 工程、七部分教学与阶段确认规则
- `README.md`：面向技术招聘人员的英文 GitHub 项目介绍；每个 Stage PR 合并后按证据更新
- `MASTER_PLAN.md`：14 个阶段的完整学习、代码实验、Benchmark、面试要求
- `CODEX_START_PROMPT.md`：第一轮与之后新会话的启动提示词
- `learning/PROGRESS.md`：**先读它**，确定真实当前阶段
- `learning/stage_status.json`：机器可读的状态，不等同实际掌握
- `learning/gates/`：历史阶段问答记录；不再运行旧评分流程
- `learning/MASTERY_MATRIX.md`：已讲、已确认理解与仍有疑问的章节/知识点
- `learning/KNOWLEDGE_MASTERY.md`：按完整工程链路记录官方源码/演示、用户独立理解与关键薄弱点；无数字评分或 L1–L5 微评级
- `learning/SESSION_LOG.md`：每轮做了什么、没做什么、下一步
- `learning/MISTAKES.md`：历史关键误区及必要的纠正
- `experiments/manifests/`：实验可复现配置样板
- `learning/OFFICIAL_EVAL_AUDIT.md`：必须先核实官方已有 Evaluator/Judge/Report/测试，避免重复开发
- `EVALUATION_SYSTEM_SPEC.md`：个人评测、Trajectory、Bad Case、Regression Gate 的具体实现标准
- `PROJECT_DELIVERABLES.md`：三个必交付 + 面试项目证据清单

注意：Codex 编程助手和 Harness² 被测的 Codex Executor 不是一回事。没有预算或网络时也能继续源码/单元测试学习，但不能假装已完成真实模型 Benchmark。

## 重要区分
本工作区有 **14 阶段任务、代码规格和离线检查脚本**。当前完成情况以 `learning/PROGRESS.md` 和真实 Git/运行证据为准；不能从模板推断官方复现、评测器或论文结果已完成。
