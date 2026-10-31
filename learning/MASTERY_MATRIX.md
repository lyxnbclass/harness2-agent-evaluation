# 章节理解矩阵（按实际回答更新）

当前章节：Stage 00「官方无模型 Demo 完整执行链路」。定性状态：`未讲 / 已讲待验证 / 已理解 / 需补充`。不评分。Codex 的讲解和运行通过不等于用户已理解；用户的局部正确回答也不等于整章确认。历史细节见 `learning/KNOWLEDGE_MASTERY.md`，本章后续集中回答见 `learning/PROGRESS.md`。

| 知识点 | 对应阶段 | 当前理解状态 | 最近回答/证据 | 关键薄弱点/后续复习 |
|---|---|---|---|---|
| CSV 输入、答案文件与简化 Trajectory | 00 | 已理解 | 用户独立区分输入、`answer.txt` 与过程记录；详见 `KNOWLEDGE_MASTERY.md` | 后续在完整 Demo 链路中复用 |
| 官方 Demo 完整代码与执行链 | 00 | 已讲待验证 | 2026-10-31 用户正确解释 `task_id`/`harness_dir`/`run_id` 和基线漏算负数；尚无独立全链路解释 | 结合选择、异常与报告边界串起整条链 |
| Demo 脚本候选的校验与回退 | 00 | 已讲待验证 | 用户回答“记录错误并回退”；已补充先重试一次的边界 | 结合完整链路解释候选验证，不单独拦截 |
| Demo CLI/`argparse` 参数与退出码 | 00 | 已讲待验证 | 有效/无效参数已真实运行；参数变式由 Codex 讲解 | 在完整链路中复习参数到调度的传递 |
| DemoAdapter 任务、Harness 选择与产物 | 00 | 已理解 | 2026-10-31 用户独立说明 `task_id` 选 CSV、`harness_dir` 选脚本、`run_id` 决定产物目录；并解释负数过滤导致结果差异 | 继续用于完整链路分析；`if amount > 0` 表述已纠正 |
| Python 函数、字典、异常、测试 | 01 | 未讲 | 尚未教学与验证 | 待验证 |
| Agent Loop / Runtime / Executor | 00–01 | 未讲 | 尚未教学与验证 | 待验证 |
| Tool Call / Tool Result / Schema | 01–03 | 未讲 | 尚未教学与验证 | 待验证 |
| Mock / FakeModel / 单元测试 | 01 | 未讲 | 尚未教学与验证 | 待验证 |
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
