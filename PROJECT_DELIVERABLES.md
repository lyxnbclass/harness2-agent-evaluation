# 最终项目交付与简历证据清单

> 所有状态默认为未完成。请 Codex 随实际实验更新，但不得替用户勾选尚未完成内容。
> 贡献归属必须真实：Codex 编写的项目自研代码记录为 Codex 实现；用户独立完成的方案选择、代码审查、故障分析和验收分别记录证据。简历不得把 Codex 编写的代码表述成用户亲手编写。

## 1. Google Harness² 官方复现
- [ ] 记录官方仓库 SHA、依赖与环境
- [ ] 官方 Demo 无模型执行（含真实日志）
- [ ] Propose–Probe–Compose/Reflection 源码路径与调用图
- [ ] 原生 Benchmark 单任务真实模型运行（需授权；受环境限制可 BLOCKED，但不能标完成）
- [ ] 官方 Judge/Report/Baseline 源码审计：`learning/OFFICIAL_EVAL_AUDIT.md`

## 2. 公开 Coding Benchmark（必须，不只是选个名字）
- [ ] SWE-bench/其他公开集的选型 ADR 与版本锁定
- [ ] 其原生 Evaluator 独立运行，保留日志和 verdict
- [ ] 小规模 task/patch/evaluator 冒烟测试
- [ ] 自己的 Harness²↔Benchmark Adapter（含单测）
- [ ] 隔离环境、安全控制与禁止 gold patch 泄漏

## 3. 自研 Agent 评测与 Regression System（必须）
- [ ] Metrics 与计数分母约定
- [ ] Trace Validator + Trace replay
- [ ] Bad Case Registry（有证据指向）
- [ ] Judge 校准与偏差实验（真实模型须授权）
- [ ] Paired Comparison + 回归四象限
- [ ] Regression Gate（PASS/REVIEW/FAIL， fail-closed）
- [ ] 可复现报告 + Run manifest + 成本/Token 统计（不具备则留空）
- [ ] 至少 10 项可执行单元测试与反例

## 4. 长期记忆与个人工程改进
- [ ] 官方跨任务 Reflection 与通用 Memory 的边界分析
- [ ] Memory Retrieval / Conflict / Staleness / Poisoning 独立实验
- [ ] 一个原创扩展模块和可审计代码差异
- [ ] Regression/消融验证与局限说明

## 5. 面试准备与进度管理
- [ ] 14 阶段的工程证据与用户确认记录；历史 `learning/gates/` 保留供查阅
- [ ] 对关键误区的针对性纠正记录 (`learning/MISTAKES.md`)
- [ ] 每轮记录真实产出和下一唯一任务 (`learning/SESSION_LOG.md`)
- [ ] 最终 30 秒/2 分钟/5 分钟讲解，以及基础、代码/调试和系统设计模拟面试
- [ ] README & 简历项目描述仅使用有证据的完成项

**适合简历的结构（完成后再写）：** Google Harness² Reproduction + Public Coding Benchmark Adapter + Evaluation/Trajectory/Regression System + Measured Experiments + Original Engineering Contribution。
