# 学习进度 — 当前状态

> 更新：2026-10-31。Stage 00 合并与用户进入 Stage 01 的明确指令已核实。历史工程细节见 `learning/stages/00.md`、`reports/stage00_demo_smoke.md` 和 `learning/SESSION_LOG.md`。

- 当前阶段：01
- 当前章节：最小 Agent Runtime 与 Tool Calling
- 状态：IN_PROGRESS
- 阶段入口证据：Stage 00 PR [#1](https://github.com/lyxnbclass/harness2-agent-evaluation/pull/1) 于 2026-10-31 合并；远端 `main` 为 `4b0a1effd5c0a1c355a1c39f326b7ef6e2cf556f`，包含 Stage 00 分支提交 `d67a64c`。用户本轮明确说“进入下一阶段”。
- Stage 00 已验证工程：Google 官方源码固定 SHA `1cfe254e8d25b15f37048c3730134686abe60335`；隔离无模型 Demo 两题 `ok`，5 个官方测试通过，错误输出路径按预期失败。无模型 Benchmark、SWE-bench 或性能提升结论。
- 学习情况：Stage 00 的 CSV、答案、Trajectory、Adapter 三参数和基线差异有用户局部独立回答；完整五题由 Codex 直接讲解，未获得完整独立作答。用户决定进入 Stage 01，此限制保留，不写成独立面试掌握。
- Stage 01 工程：按 `MASTER_PLAN.md` 实现本地 FakeModel → Tool Call → Tool Result → Final 的最小 Runtime、3 个本地工具、Schema 校验和 `max_steps`；注入超时/未知工具/错误参数并运行单测。先核实官方真实代码位置，不编造函数。
- GitHub：Stage 00 PR 已合并，README 合并后收尾正在提交；Stage 01 独立分支将在该 main 基础上创建，Stage 01 PR 暂为 NONE。
- 阻塞：无费用需求；当前 Stage 01 先用本地 FakeModel，不调用付费模型。公开 Benchmark 和官方真实模型运行仍未授权。
- 下次内容：完成 Stage 01 最小 Runtime 的实现与测试后，按七部分结构讲解其真实输入、数据流、失败边界及官方源码关联。
