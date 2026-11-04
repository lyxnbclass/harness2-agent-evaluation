# 章节理解矩阵（按实际回答更新）

当前章节：Stage 01「最小 Agent Runtime 与 Tool Calling」。定性状态：`未讲 / 已讲待验证 / 已理解 / 需补充`。不评分。用户已明确选择进入 Stage 01；Stage 00 的局部理解证据保留，完整五题由 Codex 讲解，仍不记为用户独立回答。历史细节见 `learning/KNOWLEDGE_MASTERY.md`。

| 知识点 | 对应阶段 | 当前理解状态 | 最近回答/证据 | 关键薄弱点/后续复习 |
|---|---|---|---|---|
| CSV 输入、答案文件与简化 Trajectory | 00 | 已理解 | 用户独立区分输入、`answer.txt` 与过程记录；详见 `KNOWLEDGE_MASTERY.md` | 后续在完整 Demo 链路中复用 |
| 官方 Demo 完整代码与执行链 | 00 | 已讲待验证 | 2026-10-31 用户正确解释 `task_id`/`harness_dir`/`run_id` 和基线漏算负数；尚无独立全链路解释 | 结合选择、异常与报告边界串起整条链 |
| Demo 脚本候选的校验与回退 | 00 | 已讲待验证 | 用户回答“记录错误并回退”；已补充先重试一次的边界 | 结合完整链路解释候选验证，不单独拦截 |
| Demo CLI/`argparse` 参数与退出码 | 00 | 已讲待验证 | 有效/无效参数已真实运行；参数变式由 Codex 讲解 | 在完整链路中复习参数到调度的传递 |
| DemoAdapter 任务、Harness 选择与产物 | 00 | 已理解 | 2026-10-31 用户独立说明 `task_id` 选 CSV、`harness_dir` 选脚本、`run_id` 决定产物目录；并解释负数过滤导致结果差异 | 继续用于完整链路分析；`if amount > 0` 表述已纠正 |
| Python 函数、字典、异常、测试 | 01 | 已讲待验证 | Stage 01 章节讲了 `run_agent`/`run_tool` 的分支、字典及异常；用户尚未独立解释代码或单测 | 随具体失败单测定点复习 |
| Agent Loop / Runtime / Executor | 00–01 | 需补充 | 2026-11-04 用户正确描述工具调用与结果回传；误把 `max_steps=1` 后的工具结果当成最终答案 | 区分工具完成、模型 final、步数耗尽；官方 substrate 边界待解释 |
| Tool Call / Tool Result / Schema | 01–03 | 需补充 | 用户正确指出 Tool Call 来自模型、结果经 Runtime 回传；把第二轮可见消息数说成 4，并笼统归因为“大模型没办法校验” | 第二轮只有 user/call/result 三条；程序强制执行 Schema 校验 |
| Mock / FakeModel / 单元测试 | 01 | 需补充 | 用户知道 FakeModel 使用预设决策步骤，但尚未说明最终回答并非由工具结果推理得出 | 对比脚本决策与真实模型推理；阅读结果回传单测 |
| Dataset / Splits / Evaluation Leakage | 02、08 | 未讲 | 尚未教学与验证 | 待验证 |
| Success Rate / Pass@k / 未评分样本 | 02、10 | 未讲 | 尚未教学与验证 | 待验证 |
| Trace / Trajectory Evaluation | 03 | 未讲 | 尚未教学与验证 | 待验证 |
| Bad Case / Root Cause | 03、05 | 未讲 | 尚未教学与验证 | 待验证 |
| LLM-as-a-Judge / 校准 | 04 | 未讲 | 尚未教学与验证 | 待验证 |
| Prompt / Tool Schema / Retry / Runtime 优化 | 05 | 未讲 | 尚未教学与验证 | 待验证 |
| Harness² PPC、Parallel/Sequential | 00、06 | 已讲待验证 | Stage 00 已结合官方 `run_parallel/run_sequential` 和真实 Demo 产物讲解两模式；PPC 深入留在 06 | 用户尚未独立解释两模式与选择时序 |
| Harness² Reflection / 经验复用 | 06、11 | 未讲 | 尚未教学与验证 | 待验证 |
| 官方 Benchmark Run/Judge/Report | 07 | 未讲 | 尚未教学与验证 | 待验证 |
| SWE-bench 任务/原生 Evaluator | 08 | 未讲 | 尚未教学与验证 | 待验证 |
| Coding Agent Benchmark Adapter | 09 | 未讲 | 尚未教学与验证 | 待验证 |
| 官方评测器源码审计 / 复用边界 | 00、06–07 | 未讲 | 尚未教学与验证 | 待验证 |
| Paired Comparison / Regression Gate | 10、12 | 未讲 | 尚未教学与验证 | 待验证 |
| Baseline / Ablation / Regression / Cost | 10 | 未讲 | 尚未教学与验证 | 待验证 |
| Memory Retrieval / Conflict / Staleness | 11 | 未讲 | 尚未教学与验证 | 待验证 |
| 自主工程贡献 / Design Tradeoffs | 12 | 未讲 | 尚未教学与验证 | 待验证 |
| 结构化技术面试表达 | 00–13 | 未讲 | 尚未教学与验证 | 待验证 |
