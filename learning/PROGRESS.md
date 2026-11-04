# 学习进度 — 当前状态

> 更新：2026-11-04。Stage 00 合并与用户进入 Stage 01 的明确指令已核实。历史工程细节见 `learning/stages/00.md`、`reports/stage00_demo_smoke.md` 和 `learning/SESSION_LOG.md`。

- 当前阶段：01
- 当前章节：最小 Agent Runtime 与 Tool Calling
- 状态：IN_PROGRESS
- 阶段入口证据：Stage 00 PR [#1](https://github.com/lyxnbclass/harness2-agent-evaluation/pull/1) 于 2026-10-31 合并；远端 `main` 为 `4b0a1effd5c0a1c355a1c39f326b7ef6e2cf556f`，包含 Stage 00 分支提交 `d67a64c`。用户本轮明确说“进入下一阶段”。
- Stage 00 已验证工程：Google 官方源码固定 SHA `1cfe254e8d25b15f37048c3730134686abe60335`；隔离无模型 Demo 两题 `ok`，5 个官方测试通过，错误输出路径按预期失败。无模型 Benchmark、SWE-bench 或性能提升结论。
- 学习情况：Stage 00 的 CSV、答案、Trajectory、Adapter 三参数和基线差异有用户局部独立回答；完整五题由 Codex 直接讲解，未获得完整独立作答。用户决定进入 Stage 01，此限制保留，不写成独立面试掌握。
- Stage 01 理解：七部分章节已讲，用户已回答五道思考题并继续解释一步预算。正确指出 Tool Call 来自模型、工具结果回传，以及 `max_steps=1` 时无法进行第二次模型决策；仍把“不能再校验 Tool Result”与“不能再生成最终 answer”混为一谈，已获定点纠正。官方 substrate 边界和失败单测尚无无提示独立解释；用户于 2026-11-04 明确选择推进 Stage 02，欠项保留后续复习，不写成全面掌握。
- Stage 01 工程：Codex 已在 `experiments/toy_agent/runtime.py` 实现本地 FakeModel → Tool Call → Tool Result → Final 的最小 Runtime、3 个本地工具、严格输入及输出类型 Schema 校验和 `max_steps`；`demo.py` 的真实轨迹见 `reports/stage01_toy_agent_demo.json`。2026-11-04 本机 Python 3.12 的 8 项 `unittest` 通过（0.132s），覆盖超时、未知工具、错误参数、非法输出、依赖失败、一步预算与结果回传；Demo 仍退出 0，见 `reports/stage01_runtime_contract_extension.md`。未运行真实模型。官方 JobBench adapter → substrate → launcher → JSONL renderer 的源码路径和数据类型已核实，人工合成事件的 renderer probe 通过；见 `reports/stage01_official_source_trace.md`。真实 OpenCode substrate 未运行。
- GitHub：Stage 00 PR 已合并，合并后 README 收尾提交 `470e357` 已 Push 且远端 README 已核实。当前独立分支 `stage-01-runtime` 从该 `main` 建立；Runtime 提交 `98ca15c`、`1e21f29` 及源码追踪提交 `622669a` 已 Push。2026-11-04 核查 Stage 01 PR 为 NONE。
- 阻塞：无费用需求；当前 Stage 01 先用本地 FakeModel，不调用付费模型。公开 Benchmark 和官方真实模型运行仍未授权。
- 下次内容：先完成 Stage 01 PR 的审阅与合并核实；用户已明确选择推进 Stage 02。核实合并提交与远端 README 收尾后，从合并后的 `main` 建立 Stage 02 独立分支，讲解评测集与成功率，并将 Stage 01 源码/边界疑点列为后续复习，不再用固定追问阻断推进。
