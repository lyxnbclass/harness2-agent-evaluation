# 自研评测与回归测试系统：实施规格（必须逐阶段实现）

> **注意：这是需求规格，不是已实现代码。** Codex 按 Stage 02/03/04/09/10 分步实现、测试并讲解；用户通过真实代码阅读、Trace 分析、故障诊断和面试考核验收，不承担手写程序或环境配置。
> 官方评分器或 SWE-bench 原生评测器决定任务是否通过；我们的系统汇总、诊断、比较并控制是否采纳优化，**不得利用测试答案反向给 Agent 提示**。

## 架构与数据流

```text
Harness² Baseline / Improved Harness
           |
           v
   Benchmark Task + Agent Executor
           |   (Trace / Patch / Usage)
           v
   Native Benchmark Evaluator  ---------------------> task verdict
           |                                               |
           +--------------> Result Normalizer <------------+
                                        |
                      +-----------------+------------------+
                      |                 |                  |
                      v                 v                  v
                    Metrics      Trajectory/BadCase    Paired Compare
                                           |                 |
                                           +--------+--------+
                                                    v
                                             Regression Gate
                                                    |
                                                    v
                                            Report + Artifacts
```

## 模块清单与所在阶段

| 模块（目标路径） | 阶段 | 自己需要写出的最小功能 | 禁止混淆的官方职责 |
|---|---|---|---|
| `experiments/evaluators/metrics.py` | 02,10 | 计算 resolved / attempted / infra_error / unscored，约定分母并解释 | 不替代 native judge |
| `experiments/evaluators/trace_validator.py` | 03,10 | event/schema 校验、tool error、重试/超限/顺序 | 不把轨迹分数等同最终成功 |
| `experiments/evaluators/bad_case_registry.py` | 03,10 | 从 trace + verdict 汇总错误及证据，支持人工核查 | 不凭 LLM 随意决定真值 |
| `experiments/evaluators/judge.py` | 04 | 可选 rule-based/LLM judge 校准，校验结构化输出 | 不覆盖 SWE-bench 原生测试结果 |
| `experiments/adapters/` | 09 | task/repo/commit/patch 映射，调用原生 evaluator | 不假装 Harness² 原生支持 SWE-bench |
| `experiments/evaluators/compare_runs.py` | 10 | task_id 成对对齐，计算新增成功、旧成功退化、差异表 | 不混用不同任务/模型版本 |
| `experiments/evaluators/regression_gate.py` | 10,12 | FAIL/REVIEW/PASS 决策，关键回归禁止自动采纳 | 不因总分上升自动采纳 |
| `experiments/evaluators/report_generator.py` | 10 | Markdown/JSON 报告，引用 manifest、trace、native verdict | 不编造缺失指标 |

## 数据契约（拟议格式；必须根据本地官方产物验证并映射）

### run_manifest.json
- `run_id`、`kind`（baseline|optimized）、`harness_sha`、`upstream_sha`、`adapter_sha`
- `benchmark`、`benchmark_commit`、`task_ids`、`model_id`、`model_settings`
- `executor`、`environment`、`network_restrictions`、`budget`、`timestamp`
- 产物路径：`trace_path`、`native_verdict_path`、`patch_path`；若字段不可观测则记录 `null/unknown`

### normalized_results.jsonl（一行一个 task_id）
- `run_id`, `task_id`, `outcome`：`resolved | failed | infra_error | unscored`
- `verdict_source`：原生评测器名称/版本/原始文件引用
- `patch_path`, `trace_path`, `tokens`, `latency_sec`, `cost`（未知写 `null`）

### paired_comparison.jsonl
- `task_id`, `base_outcome`, `new_outcome`, `transition`：
  - resolved→resolved: stable_success
  - failed→resolved: newly_solved
  - resolved→failed: regression
  - failed→failed: stable_failure
  - 任何 infra_error/unscored: incomparable（不能强行算成回归或改善）
- 每条包含证据链接与两个 run_id。必须保证两次评测的同一组 task_id/环境/模型配置可比。

## Regression Gate（教学起步策略，阈值应有理由和审核）

- `FAIL`：硬安全约束被违反、明确关键回归、超过已批准的硬成本预算（如果这些条件有可信证据）。
- `REVIEW`：基础设施错误/未评分、新旧 task 集不一致、证据不足、普通回归、样本量过小或统计波动不确定。
- `PASS`：不存在硬约束失效；可比任务集合充分、阈值符合事先写好的 policy；依然需要显式记录与人工审核/用户批准（根据部署场景）。
- **默认 fail-closed：Gate 不得把 UNKNOWN 解释为 PASS。** Gate 只是项目自己的策略，不是 Google 官方 Harness² 论文默认算法。

## 至少应验证的单元/集成测试

1. 同一 task_id 新旧均成功：stable_success。
2. failed→resolved：newly_solved。
3. resolved→failed：regression；关键回归应 FAIL。
4. 某侧 infra_error：incomparable + REVIEW。
5. 某侧 unscored：incomparable + REVIEW。
6. 两次 task_id 列表不一致：REVIEW，禁止直接比较成功率。
7. patch 无法应用或基 commit 不符：按原生 evaluator 结果分类并保留原因。
8. 工具超时、重复调用、违反权限：trace validator 标记，保留 trace step。
9. 报告引用可存在的日志路径，不泄露 API key。
10. 一组分数总体提高但有已知关键 regression：必须禁止自动采用。
11. 成本超过已批准预算：FAIL 或阻止自动采用。
12. 同一个 benchmark任务重复运行导致随机波动：保留重复试验，不能用单个观察推断统计显著。

## 必须交付的演示与面试回答

- 最少一条 task 的 `Issue → Agent Trace → Patch → Native Verdict → Paired Comparison → Gate Decision → Report` 完整证据链。
- 一个总成功率提升但仍触发 Regression Gate 的反例。
- 一个看似失败实为 infra_error 的反例；解释为什么不能据此得出模型变差。
- 用自己的语言解释哪些是“Google 原版复现”、哪些是“原生 Benchmark”、哪些是“本人开发扩展”。
