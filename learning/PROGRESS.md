# 学习进度 — 当前状态

> 更新：2026-11-10。当前状态以本轮 Git、源码及测试核实为准；Stage 00–01 的历史细节见 `learning/stages/00.md`、`learning/stages/01.md` 和 `learning/SESSION_LOG.md`。

- 当前阶段：04
- 当前章节：Judge rubric、结构化输出校验与偏差校准
- 状态：IN_PROGRESS
- 阶段入口证据：Stage 03 [PR #4](https://github.com/lyxnbclass/harness2-agent-evaluation/pull/4) 已合并，merge commit `4358153ca47afbeb4d4da9fba399751ef4a02da7` 已核实位于远端 `main`；合并后 README 收尾 `c943544` 已 Push 并核实。用户明确说“当前stage03已合并，我们进入下一个stage”。
- Stage 00 已验证工程：Google 官方源码固定 SHA `1cfe254e8d25b15f37048c3730134686abe60335`；隔离无模型 Demo 两题 `ok`，5 个官方测试通过，错误输出路径按预期失败。无模型 Benchmark、SWE-bench 或性能提升结论。
- 学习情况：Stage 00 的 CSV、答案、Trajectory、Adapter 三参数和基线差异有用户局部独立回答；完整五题由 Codex 直接讲解，未获得完整独立作答。用户决定进入 Stage 01，此限制保留，不写成独立面试掌握。
- Stage 01 理解：七部分章节已讲，用户已回答五道思考题并继续解释一步预算。正确指出 Tool Call 来自模型、工具结果回传，以及 `max_steps=1` 时无法进行第二次模型决策；仍把“不能再校验 Tool Result”与“不能再生成最终 answer”混为一谈，已获定点纠正。官方 substrate 边界和失败单测尚无无提示独立解释；用户于 2026-11-04 明确选择推进 Stage 02，欠项保留后续复习，不写成全面掌握。
- Stage 01 工程：Codex 已在 `experiments/toy_agent/runtime.py` 实现本地 FakeModel → Tool Call → Tool Result → Final 的最小 Runtime、3 个本地工具、严格输入及输出类型 Schema 校验和 `max_steps`；`demo.py` 的真实轨迹见 `reports/stage01_toy_agent_demo.json`。2026-11-04 本机 Python 3.12 的 8 项 `unittest` 通过（0.132s），覆盖超时、未知工具、错误参数、非法输出、依赖失败、一步预算与结果回传；Demo 仍退出 0，见 `reports/stage01_runtime_contract_extension.md`。未运行真实模型。官方 JobBench adapter → substrate → launcher → JSONL renderer 的源码路径和数据类型已核实，人工合成事件的 renderer probe 通过；见 `reports/stage01_official_source_trace.md`。真实 OpenCode substrate 未运行。
- Stage 02 理解：用户正确手算有效评分成功率 `8/16=50%`、覆盖率 `16/20=80%`，能把判题器结论与 Runtime Trace 关联，并追问 SWE-bench Adapter、原生判题、Trace 采集与报告生成。已定点补充逐题回归和“Trace 不决定最终正确性”。本轮新代码尚未由用户独立阅读或按五个真实样本手算；不记为全面掌握。
- Stage 02 工程：Codex 在独立 `stage-02-metrics` 分支实现 24 条多工具教学案例、独立 FakeModel 决策 fixture、`experiments/evaluators/metrics.py`、本地案例 Runner 和 13 项测试。2026-11-05 Python 3.12.13 下测试 13 项通过；24 条本地脚本契约结果为 `resolved=19, failed=3, infra_error=1, unscored=1`。完整证据及限制见 `reports/stage02_metrics_smoke.md`；这些不是 SWE-bench 成绩。
- GitHub：Stage 03 [PR #4](https://github.com/lyxnbclass/harness2-agent-evaluation/pull/4) 已合并到 `main`，merge commit `4358153ca47afbeb4d4da9fba399751ef4a02da7` 经 `git merge-base --is-ancestor` 核实；合并后 README 收尾 `c9435448e73c704f1fd88375d20ac732a6d1af3d` 已 Push 且远端核实。用户明确要求进入下一阶段。当前独立分支 `stage-04-judge` 从此 `main` 建立；Stage 04 PR：NONE。
- Stage 03 理解：用户对 `dev-08` 首次越权步骤、`resolved` 与过程合规的区别、`val-04` 观察事实和 FakeModel 边界、`infra_error` 不判正误、结构化事件优于截断文本，均给出正确要点。第 5 题回答“是”混淆了 Trace replay 与重新执行；已定点补讲：replay 只展示已保存事件，重跑可能因模型采样、环境、工具状态、版本改变而得到不同轨迹。用户尚未确认已理解新代码。
- Stage 03 工程：Codex 新增运行时事件时间戳与累计耗时、脱敏持久化、`trace_validator.py`、`bad_case_registry.py`、按 `run_id` 回放 CLI、24 条结构化本地 Trace 和 8 条分析记录。2026-11-08 本地评测 19 项测试、Runtime 8 项回归测试、工作区检查均通过。证据见 `reports/stage03_fake_trace.jsonl`、`reports/stage03_bad_case_candidates.jsonl`、`reports/bad_cases.md`。这些是 FakeModel 教学案例，不是官方 Harness² 或 SWE-bench 成绩。
- Stage 04 工程：Codex 在已 Push 的 `stage-04-judge` 分支提交 `d859141`，实现确定性 `judge.py`、15 条合成案例及 Codex 人工参考标签、结构化输出 Schema 校验、有界失败重试、pairwise 顺序/冗长/伪指令反例和校准 Runner。2026-11-10 评测测试 25 项、Runtime 回归 8 项通过；本地 Judge 与参考标签一致 12/15，分歧 `j04/j08/j12`，详见 `reports/stage04_judge_calibration.md`。参考标签尚待用户审阅，不是独立人工标注或真实模型成绩。
- 限制：无付费 API、真实模型或公开 Benchmark 运行；仅本地确定性 Judge 与合成案例。Stage 03 的脱敏仍只覆盖常见凭据模式；Stage 09 SWE-bench Adapter 尚未实现。Stage 04 PR 尚未创建，不自动 Merge。
- Stage 04 理解：2026-11-11 用户已能解释 Judge 输出缺字段/内部矛盾需要拒绝，并指出单个顺序交换不足以证明 LLM 无偏差。需定点纠正 `j04/j08` 均为误拒、本地答案 Judge 不读取原生 verdict 或 Trace；用户追问证据是程序采集还是 LLM 判断，已针对 Stage 02–04 的不同来源说明。参考标签尚未由用户逐项审阅。
- 下一内容：按用户实际疑问定点补充 Judge 输入与证据来源、官方 selection/adapter.score 边界及偏差实验设计；等待用户审阅参考标签和阶段工程，再准备 Stage 04 PR。Stage 01 substrate 边界和 Stage 02 分母代码未独立解释项保留为面试复习。
