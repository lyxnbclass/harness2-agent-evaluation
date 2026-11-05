# 学习进度 — 当前状态

> 更新：2026-11-05。当前状态以本轮 Git、源码及测试核实为准；Stage 00–01 的历史细节见 `learning/stages/00.md`、`learning/stages/01.md` 和 `learning/SESSION_LOG.md`。

- 当前阶段：02
- 当前章节：评测任务、结果状态与指标实现
- 状态：IN_PROGRESS
- 阶段入口证据：Stage 01 [PR #2](https://github.com/lyxnbclass/harness2-agent-evaluation/pull/2) 于 2026-11-04 合并到 `main`，merge commit `0b08058e22b6462941bb6781fc85c92c3012bc21` 已核实为远端 `main` 的祖先；合并后 README 收尾 `d02562c` 已 Push，远端 `main` 已核实。用户此前明确要求进入 Stage 02，且本轮明确要求创建 Stage 02 PR。
- Stage 00 已验证工程：Google 官方源码固定 SHA `1cfe254e8d25b15f37048c3730134686abe60335`；隔离无模型 Demo 两题 `ok`，5 个官方测试通过，错误输出路径按预期失败。无模型 Benchmark、SWE-bench 或性能提升结论。
- 学习情况：Stage 00 的 CSV、答案、Trajectory、Adapter 三参数和基线差异有用户局部独立回答；完整五题由 Codex 直接讲解，未获得完整独立作答。用户决定进入 Stage 01，此限制保留，不写成独立面试掌握。
- Stage 01 理解：七部分章节已讲，用户已回答五道思考题并继续解释一步预算。正确指出 Tool Call 来自模型、工具结果回传，以及 `max_steps=1` 时无法进行第二次模型决策；仍把“不能再校验 Tool Result”与“不能再生成最终 answer”混为一谈，已获定点纠正。官方 substrate 边界和失败单测尚无无提示独立解释；用户于 2026-11-04 明确选择推进 Stage 02，欠项保留后续复习，不写成全面掌握。
- Stage 01 工程：Codex 已在 `experiments/toy_agent/runtime.py` 实现本地 FakeModel → Tool Call → Tool Result → Final 的最小 Runtime、3 个本地工具、严格输入及输出类型 Schema 校验和 `max_steps`；`demo.py` 的真实轨迹见 `reports/stage01_toy_agent_demo.json`。2026-11-04 本机 Python 3.12 的 8 项 `unittest` 通过（0.132s），覆盖超时、未知工具、错误参数、非法输出、依赖失败、一步预算与结果回传；Demo 仍退出 0，见 `reports/stage01_runtime_contract_extension.md`。未运行真实模型。官方 JobBench adapter → substrate → launcher → JSONL renderer 的源码路径和数据类型已核实，人工合成事件的 renderer probe 通过；见 `reports/stage01_official_source_trace.md`。真实 OpenCode substrate 未运行。
- Stage 02 理解：用户正确手算有效评分成功率 `8/16=50%`、覆盖率 `16/20=80%`，能把判题器结论与 Runtime Trace 关联，并追问 SWE-bench Adapter、原生判题、Trace 采集与报告生成。已定点补充逐题回归和“Trace 不决定最终正确性”。本轮新代码尚未由用户独立阅读或按五个真实样本手算；不记为全面掌握。
- Stage 02 工程：Codex 在独立 `stage-02-metrics` 分支实现 24 条多工具教学案例、独立 FakeModel 决策 fixture、`experiments/evaluators/metrics.py`、本地案例 Runner 和 13 项测试。2026-11-05 Python 3.12.13 下测试 13 项通过；24 条本地脚本契约结果为 `resolved=19, failed=3, infra_error=1, unscored=1`。完整证据及限制见 `reports/stage02_metrics_smoke.md`；这些不是 SWE-bench 成绩。
- GitHub：当前 Stage 02 分支 `stage-02-metrics` 从远端 `main` 的 `d02562c` 建立。Stage 02 PR：NONE（本轮准备提交并创建）；不自动 Merge。Stage 00–01 PR 均已合并，历史提交/证据保留。
- 限制：无付费 API、真实模型或公开 Benchmark 运行；仅 FakeModel 与本地教学契约。Stage 03 Trace Validator 和 Stage 09 SWE-bench Adapter 尚未实现。
- 下次内容：审阅 Stage 02 PR 中 `metrics.py` 的分母和失败路径，按五条真实记录手算；用户判断是否理解。Stage 01 的官方 substrate 边界仍保留为面试复习项。
