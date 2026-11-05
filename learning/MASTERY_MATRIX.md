# 章节理解矩阵（按实际回答更新）

当前章节：Stage 02「评测任务、结果状态与指标实现」。定性状态：`未讲 / 已讲待验证 / 已理解 / 需补充`。不评分。Stage 01 PR 已合并、README 收尾已推送；用户此前明确要求进入 Stage 02。Stage 00–01 的局部理解与未完全独立解释项保留，历史细节见 `learning/KNOWLEDGE_MASTERY.md`、`learning/stages/01.md`。

| 知识点 | 对应阶段 | 当前理解状态 | 最近回答/证据 | 关键薄弱点/后续复习 |
|---|---|---|---|---|
| CSV 输入、答案文件与简化 Trajectory | 00 | 已理解 | 用户独立区分输入、`answer.txt` 与过程记录；详见 `KNOWLEDGE_MASTERY.md` | 后续在完整 Demo 链路中复用 |
| 官方 Demo 完整代码与执行链 | 00 | 已讲待验证 | 2026-10-31 用户正确解释 `task_id`/`harness_dir`/`run_id` 和基线漏算负数；尚无独立全链路解释 | 结合选择、异常与报告边界串起整条链 |
| Demo 脚本候选的校验与回退 | 00 | 已讲待验证 | 用户回答“记录错误并回退”；已补充先重试一次的边界 | 结合完整链路解释候选验证，不单独拦截 |
| Demo CLI/`argparse` 参数与退出码 | 00 | 已讲待验证 | 有效/无效参数已真实运行；参数变式由 Codex 讲解 | 在完整链路中复习参数到调度的传递 |
| DemoAdapter 任务、Harness 选择与产物 | 00 | 已理解 | 2026-10-31 用户独立说明 `task_id` 选 CSV、`harness_dir` 选脚本、`run_id` 决定产物目录；并解释负数过滤导致结果差异 | 继续用于完整链路分析；`if amount > 0` 表述已纠正 |
| Python 函数、字典、异常、测试 | 01 | 已讲待验证 | Stage 01 章节讲了 `run_agent`/`run_tool` 的分支、字典及异常；用户尚未独立解释代码或单测 | 随具体失败单测定点复习 |
| Agent Loop / Runtime / Executor | 00–01 | 需补充 | 2026-11-04 用户进一步正确指出一步预算用尽后没有第二次模型决策；仍误以为 Runtime 因此不能校验 Tool Result | 工具输出已校验并写入 Trace；缺少的是模型 `final`，官方 substrate 边界待解释 |
| Tool Call / Tool Result / Schema | 01–03 | 需补充 | 用户正确指出 Tool Call 来自模型、结果经 Runtime 回传；一步预算解释中混淆了输出校验与最终回答生成 | `run_tool()` 先校验输出，`run_agent()` 再写 Trace；仅下一轮模型决策因预算耗尽而未发生 |
| Mock / FakeModel / 单元测试 | 01 | 需补充 | 用户知道 FakeModel 使用预设决策步骤，但尚未说明最终回答并非由工具结果推理得出 | 对比脚本决策与真实模型推理；阅读结果回传单测 |
| Dataset / Splits / Evaluation Leakage | 02、08 | 已讲待验证 | 2026-11-05 已讲 dev/validation/local-held-out、公开集训练泄漏风险；24 条本地案例已建立 | 用户未独立解释数据切分与本地 held-out 被观察后的限制 |
| Success Rate / Pass@k / 未评分样本 | 02、10 | 已讲待验证 | 用户正确手算 `8/(8+8)=50%`、覆盖率 `16/20=80%`，并指出各状态需单列；`metrics.py` 与 12 项测试已完成 | 本轮代码分母和真实五样本手算未独立验证；pass@k 未实测 |
| Trace / Trajectory Evaluation | 03 | 未讲 | 尚未教学与验证 | 待验证 |
| Bad Case / Root Cause | 03、05 | 未讲 | 尚未教学与验证 | 待验证 |
| LLM-as-a-Judge / 校准 | 04 | 未讲 | 尚未教学与验证 | 待验证 |
| Prompt / Tool Schema / Retry / Runtime 优化 | 05 | 未讲 | 尚未教学与验证 | 待验证 |
| Harness² PPC、Parallel/Sequential | 00、06 | 已讲待验证 | Stage 00 已结合官方 `run_parallel/run_sequential` 和真实 Demo 产物讲解两模式；PPC 深入留在 06 | 用户尚未独立解释两模式与选择时序 |
| Harness² Reflection / 经验复用 | 06、11 | 未讲 | 尚未教学与验证 | 待验证 |
| 官方 Benchmark Run/Judge/Report | 07 | 未讲 | 尚未教学与验证 | 待验证 |
| SWE-bench 任务/原生 Evaluator | 08 | 已讲待验证 | 用户已追问任务、补丁、原生判题与程序化接入；已解释原生判题保留真值、我们读取判题结果和 Runtime Trace | 尚未接入真实 SWE-bench 或核实其固定版本接口；Stage 08–09 实做后再验证 |
| Coding Agent Benchmark Adapter | 09 | 未讲 | 尚未教学与验证 | 待验证 |
| 官方评测器源码审计 / 复用边界 | 00、06–07 | 未讲 | 尚未教学与验证 | 待验证 |
| Paired Comparison / Regression Gate | 10、12 | 未讲 | 尚未教学与验证 | 待验证 |
| Baseline / Ablation / Regression / Cost | 10 | 未讲 | 尚未教学与验证 | 待验证 |
| Memory Retrieval / Conflict / Staleness | 11 | 未讲 | 尚未教学与验证 | 待验证 |
| 自主工程贡献 / Design Tradeoffs | 12 | 未讲 | 尚未教学与验证 | 待验证 |
| 结构化技术面试表达 | 00–13 | 未讲 | 尚未教学与验证 | 待验证 |
