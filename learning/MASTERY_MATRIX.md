# 知识掌握矩阵（按实际回答更新）

掌握等级：`U=尚无独立证据`、`L1=理解概念`、`L2=理解真实源码`、`L3=理解完整执行过程`、`L4=能分析工程设计和故障原因`、`L5=能独立应对深入技术面试`。
每级都需用户独立回答的证据；六步教学的覆盖、官方 SHA/源码位置、真实演示、答题/错误、补课和最近考核详见 `learning/KNOWLEDGE_MASTERY.md`。只有用户独立作答、指向真实代码/Trace 的分析证据与变式复测才能升级。**Codex 编写的代码、测试通过和教学示范不算用户掌握。**

| 知识点 | 对应阶段 | 当前等级 | 最近考试/证据 | 常见误区/下次复习 |
|---|---|---|---|---|
| CSV 输入、答案文件与简化 Trajectory | 00 | L1 | 2026-10-30 用户独立区分输入、`answer.txt` 与过程记录；详见 `KNOWLEDGE_MASTERY.md` | 尚未独立追踪读取/写入代码及版本替换 |
| 官方 Demo 完整代码与执行链 | 00 | U | 已教学并真实运行，尚无用户独立源码/Trace 分析 | 先讲脚本复制、修改、校验和重跑 |
| Demo 脚本候选的校验与回退 | 00 | L1 | 2026-10-30 用户回答“记录错误并回退”；已补充先重试一次的源码边界 | 待独立追踪 `_run_stage` 的分支及 `fell_back` |
| Python 函数、字典、异常、测试 | 01 | U | 尚未考核 | 待验证 |
| Agent Loop / Runtime / Executor | 00–01 | U | 尚未考核 | 待验证 |
| Tool Call / Tool Result / Schema | 01–03 | U | 尚未考核 | 待验证 |
| Mock / FakeModel / 单元测试 | 01 | U | 尚未考核 | 待验证 |
| Dataset / Splits / Evaluation Leakage | 02、08 | U | 尚未考核 | 待验证 |
| Success Rate / Pass@k / 未评分样本 | 02、10 | U | 尚未考核 | 待验证 |
| Trace / Trajectory Evaluation | 03 | U | 尚未考核 | 待验证 |
| Bad Case / Root Cause | 03、05 | U | 尚未考核 | 待验证 |
| LLM-as-a-Judge / 校准 | 04 | U | 尚未考核 | 待验证 |
| Prompt / Tool Schema / Retry / Runtime 优化 | 05 | U | 尚未考核 | 待验证 |
| Harness² PPC、Parallel/Sequential | 06 | U | 尚未考核 | 待验证 |
| Harness² Reflection / 经验复用 | 06、11 | U | 尚未考核 | 待验证 |
| 官方 Benchmark Run/Judge/Report | 07 | U | 尚未考核 | 待验证 |
| SWE-bench 任务/原生 Evaluator | 08 | U | 尚未考核 | 待验证 |
| Coding Agent Benchmark Adapter | 09 | U | 尚未考核 | 待验证 |
| 官方评测器源码审计 / 复用边界 | 00、06–07 | U | 尚未考核 | 待验证 |
| Paired Comparison / Regression Gate | 10、12 | U | 尚未考核 | 待验证 |
| Baseline / Ablation / Regression / Cost | 10 | U | 尚未考核 | 待验证 |
| Memory Retrieval / Conflict / Staleness | 11 | U | 尚未考核 | 待验证 |
| 自主工程贡献 / Design Tradeoffs | 12 | U | 尚未考核 | 待验证 |
| 结构化技术面试表达 | 00–13 | U | 尚未考核 | 待验证 |
