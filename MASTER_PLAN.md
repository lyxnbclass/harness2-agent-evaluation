# Harness² 官方复现 + 公开 Coding Benchmark + Agent 评测与回归 + 面试通关计划（开发者负责实现版 v3.1）

> 最终可验证项目：**Harness²: Evaluation-Driven Self-Improving Coding Agent**。
> 源码复现基于 Google Research Harness²；第三方公开 Coding Benchmark 优先 SWE-bench；个人代码补上评测器、数据/Trace 统计、Regression Gate 和长期记忆实验。
> 本计划从旧版 12 个阶段演进为 14 个阶段；阶段编号 00–13。**这不是用户已经完成的项目**，实际完成状态必须以 `learning/PROGRESS.md` + Git/日志证据为准。
> 建议 12–16 周，每周 8–12 小时，仅是自主安排参考。**按通过率而非时间推进**。资料地址见 `START_HERE.md`。

## A. 最终目标 / 五个必须会回答的问题

**三个必须真正完成的交付：**

1. **官方 Harness² 复现：** 官方本地 Demo + 有凭证/安全环境时单任务真实 Benchmark；读懂 Agent Runtime → Propose → Probe → Compose → Reflect → Judge/Report 的具体入口及真实数据流。没有 API 环境则标注真实 Benchmark 阻塞，不伪造。
2. **公开 Coding Benchmark：** 优先 SWE-bench（可用其他公开集，但必须写明取舍），Codex 独立跑通原生 evaluator，并实现小规模 Harness²↔Benchmark Adapter，再以相同固定任务比较 Baseline 和优化 Harness。不要混淆 Harness² 原生支持的 JobBench/LAB/WorkBuddy-Bench 与第三方接入。
3. **项目自研的 Python 评测与回归系统：** Codex 负责编写任务调度、Patch/结果采集、规则评分与可选 LLM Judge、Trajectory 校验、Bad Case 库、质量门禁、成本统计和报告；用户负责理解与验收。

**贯穿的五个面试核心题：**
- 为什么选择这个 Benchmark，适用边界是什么？
- Evaluator 如何隔离运行、应用 Patch、决定 resolved/failed/infra_error？
- 如何从 trajectory 定位失败，并把根因归于 model/prompt/tool/runtime/environment/judge？
- 怎样证明 Harness 修改真的有效？如何做成对比、消融、回归？
- 如何防止答案泄漏、开发集过拟合与现有能力退化？

**核心理论：** Agent Loop/Runtime/Harness/Executor、Tool Schema、FakeModel、Success Rate、Pass@k/Pass@1、Trajectory Evaluation、LLM-as-a-Judge、Bad Case、Ground Truth、PPC、Parallel/Sequential、Reflection、Memory Retrieval/Conflict/Staleness/Poisoning、Retry/Idempotency/Timeout、CI、Docker/Sandbox/Cost。

## B. 工作方式：固定循环

每个阶段必须执行 **Trace → Implement → Inject Failure → Test → Teach → Interview Gate → Record**：

1. **Trace：** Codex 在已 checkout 的官方源码中定位入口、函数、参数、返回、异常；记录 `commit SHA:path:function`。没有源码就标记 NOT_VERIFIED。
2. **Implement：** Codex 编写/修改当前阶段的核心逻辑，配置环境并运行命令；用户负责阅读、理解、分析和验收，记录真实代码作者与用户的独立分析贡献。
3. **Inject Failure：** Codex 安全地制造或选择一个失败，保存 trace；用户根据证据解释首次偏离、根因和可证伪假设，Codex 完成修复和验证。
4. **Test：** Codex 保存命令、真实 exit code、日志路径、样本数量、PASS/FAIL/BLOCKED 结果。
5. **Teach：** 每完成一个重要功能，Codex 分块讲清问题场景、架构位置、真实函数/参数/返回/变量/调用与数据流、设计取舍、真实输入输出、错误与修复，并给一段准确的面试口述示范；用户不懂时先用简单案例再回到项目代码。
6. **Interview Gate：** 至少 5 道新原理题、两道深入追问、一题真实代码阅读或 Trace 分析、一题故障定位或工程设计；分批提问，**该题在用户独立回答前不透露答案**，不要求用户手写完整程序。
7. **Record：** 写进 `learning/gates/NN.md`、`MASTERY_MATRIX.md`、`MISTAKES.md`、`SESSION_LOG.md`、`PROGRESS.md`、`stage_status.json`；未经同意不开始下一阶段。

### 评分制度（每阶段相同）

| 维度 | 满分 | 必须有的证据 |
|---|---:|---|
| 概念准确性与原理理解 | 40 | ≥5 道无提示问答，能说出条件与反例 |
| 代码与 Trace 理解 | 35 | 当场阅读真实函数、解释调用链和数据流，分析给定 Trace；Codex 执行代码与测试 |
| 故障诊断与设计权衡 | 15 | 失败定位 → 方案 → 副作用 → 验证 |
| 表达与面试沟通 | 10 | 独立解释项目动机、选择、证据与限制 |

**通过门槛：** 总分 ≥80；概念≥30/40；代码/Trace 理解≥28/35；没有关键的安全/数据泄漏/评分误区；必做代码和实验产物有可核验证据。答错题要用**变式题**复测。用户须依据真实代码/Trace 独立解释，不能只复述教学示范；手写代码与亲自配置环境不是门槛。

通过后写入 `PASSED_AWAITING_USER` 并问用户是否批准进入下一阶段。只有获得“进入下一阶段”的明确指令，更新为 `COMPLETED` 并解锁下一阶段。未通过不得自动解锁；`BLOCKED` 表示受环境/授权约束，**不等于通过**。

> 每次面试题的具体题目应根据真实源码和用户近期错误动态生成。每阶段列出的示例题是范围提示，**不是事先发给用户的标准答案**。

### GitHub 阶段交付

Codex 负责本地 Git 初始化、远程仓库关联、每阶段独立 branch、必要时的 Commit/Push 和阶段 PR；用户检查 PR 与阶段成果。仓库名和可见性在首次创建前由用户确认。每阶段原则上一个面向 `main` 的正式完成 PR，须在本阶段代码/实验与面试 Gate 通过后创建；不自动 Merge。进入下一阶段前，核实 PR 已合并、目标分支含本阶段提交，并取得用户明确批准。每轮记录 branch、重要 commit、PR 链接/状态、测试与考核证据。GitHub 认证或网络失败应记录为 BLOCKED，不得声称已 Push 或已建 PR。

## C. 阶段计划（00–13，必做）

### Stage 00｜开发环境、仓库溯源与官方 Demo（基础）
**目标：** 划清官方 Harness²、模型、Harness、Executor、Benchmark、Evaluator 的职责。

**知识：** Git commit、Python 虚拟环境/包、Linux/WSL2、uv、Docker/Node 基本概念；可复现实验为什么要冻结版本。

**执行任务：**
- [ ] 盘点本机 OS、Python、Git、uv、Docker、Node、云端/本地模型权限；不能一上来就要求用户购买 API。
- [ ] 检查是否已有官方 checkout；如无，经过适当确认后在 `upstream/harness2/` 克隆 Google 源码；记下 commit SHA、tree 状态与远程地址。
- [ ] 实际阅读本地 README/pyproject/docs，定位 CLI entry points / Demo；记录真实源码入口，不预设不存在的函数名。
- [ ] 按当前 README 核对命令后，运行无需模型凭证的 `harness2-demo`，分别观察 parallel/sequential 的真实输出；若环境不支持，写 BLOCKED + 最小环境解决步骤。
- [ ] 画图解释 `CLI → Harness → Executor → task → artifact`，说明为什么跑通 Demo 不等于论文级复现。

**用户验收任务：** 阅读 Codex 定位的一次 Demo 入口和一个真实输出文件，独立解释它们如何关联；源码定位和命令运行由 Codex 完成。
**故障注入：** 故意给错误的输出路径/依赖，读取异常并定位环境问题（不可删除用户文件）。
**证据：** `learning/stages/00.md`、`learning/SOURCE_INDEX.md`、命令输出、git SHA、Demo 产物路径。
**通关提问方向：** Harness vs Runtime；Codex 对话助手 vs Codex Executor；Demo vs model-backed run；Git SHA 的意义；环境失败和任务失败如何区分。

### Stage 01｜Python 基础 + 最小 Agent Runtime（基础）
**知识：** 函数、dict/list、类、JSON/JSONL、异常、pytest、Mock/Fake、同步/异步、状态机。
**任务：**
- [ ] Codex 用 20–50 行实现本地 Agent Loop：`FakeModel → tool_call → tool_result → FakeModel → final`，用户逐段阅读并解释。
- [ ] 设计 `run_tool(name,args)` 分发至少 3 个本地工具；输入输出 Schema 校验。
- [ ] 添加 `max_steps` 防死循环，注入超时/未知工具/错误参数，并用单元测试证明被正确处理。
- [ ] 定位官方相关源代码中的一次工具调用、异常处理及返回结构，记录函数名与数据类型。
**用户验收任务：** 阅读 Codex 实现的工具路由函数和一个失败单测，解释参数、返回、分支与失败原因；Codex 负责修改与运行。
**证据：** `experiments/toy_agent/`、测试日志、`learning/stages/01.md`。
**通关方向：** 谁决定工具调用？tool call/result 如何进消息？为何用 FakeModel？retry 的副作用？`max_steps` 何时触发？

### Stage 02｜评测集、成功率与指标实现（评测基础）
**知识：** task/outcome/trajectory、Pass@1 vs pass@k、denominator、infra_error、unscored、切分、置信区间、评测污染。
**任务：**
- [ ] 自建 **20–30 个小型多工具案例，仅用于学习**；标注 normal/boundary/error/permission/attack 与唯一 `case_id`。
- [ ] 用 JSONL 定义 `case_id, input, split, expected_outcome, tool_constraints, tags`；dev/validation/local-held-out 分离。
- [ ] Codex 实现 `success_rate`、`tool_schema_valid_rate`、`unsafe_tool_rate`、`median_latency`；错误/未评分单列，加入至少 6 个单测；用户解释分母和边界。
- [ ] 用一份反例解释“最终答案正确但调用工具过程违规”的情形。
**用户验收任务：** 阅读 `metrics.py` 的失败情况处理，独立手算 5 个样本验证分母并解释边界；Codex 负责代码与测试。
**证据：** `experiments/evaluators/metrics.py`、JSONL、tests、`learning/stages/02.md`。
**通关方向：** 为何 Success Rate 不够？pass@1与pass@k？infra_error/failed 分别如何统计？如何拆分 dev/test？样本少能否报提升？

### Stage 03｜Trajectory Evaluation、Trace 记录与 Bad Case 库（工程诊断）
**知识：** event trace、tool args、state transitions、trace replay、错误分类和根因证据链。
**任务：**
- [ ] 记录 `run_id, task_id, stage, model_id, harness_sha, tool_call, tool_result, timestamp, latency, error, final`（脱敏）。
- [ ] 实现 `trace_validator.py`：检查越权调用、参数错、工具重试、循环超限、必要工具遗漏。
- [ ] 保存至少 8 个经分析的 bad cases（每例：Expected/Actual/Trace step/Root Cause/Change hypothesis/Regression case）。
- [ ] 提供按 `run_id` 打印事件的回放 CLI；拿一条“结果正确但轨迹非法”的案例说明差异。
**用户验收任务：** 独立定位 1 个 Bad Case 的首次偏离步骤，附证据而不是猜测；Codex 负责工具和运行。
**证据：** `experiments/evaluators/trace_validator.py`、`reports/bad_cases.md`、trace、`learning/stages/03.md`。
**通关方向：** Trace 和 log 有何区别？Outcome/Trajectory 何时不一致？错误是 Prompt 还是 Tool Schema？如何防止日志泄露机密？

### Stage 04｜LLM-as-a-Judge、评分器偏差与校准（评测可靠性）
**知识：** rule-based vs LLM judge、rubric、pairwise、偏差、judge hallucination、reference leakage、统计一致性。
**任务：**
- [ ] **先做确定性 Judge 和人工评分**，再申请授权使用真实模型；不要默认随意花钱。
- [ ] 为小型任务做 rubric，明确硬失败/评分维度；设计结构化输出与 schema 校验。
- [ ] 人工评分 15 个案例，再比较 Judge 输出；检查顺序偏差、冗长偏差、伪指令注入、Judge 失效/重试。
- [ ] 分析 3 个误判；能解释官方 PPC 在线对比不等于调用官方 benchmark 的 Judge 给答案。
**用户验收任务：** 阅读 Codex 实现的一项 Judge schema validation 与反例测试，解释输入、拒绝条件和误判风险。
**证据：** `experiments/evaluators/judge.py`、rubric、校准笔记、`learning/stages/04.md`。
**通关方向：** Judge 与 Ground Truth 的差别？如何发现位置偏差？判分不可靠怎么办？如何防 prompt injection？

### Stage 05｜评测驱动的优化闭环（Prompt/Schema/Retry/Runtime）（工程迭代）
**知识：** 单变量、因果假设、A/B、幂等性、指数退避、timeout、Regression Test、ADR。
**任务：**
- [ ] 从 Bad Case 中选择四类失败：Prompt、Tool Schema、Retry、Runtime；逐项写证据、假设、修改、预期收益、副作用。
- [ ] 每次只改变一个因素，保留可复现配置与测试日志。
- [ ] 写回归测试：至少 2 次有效改动、1 次看似提升但导致别的用例失败的案例。
- [ ] 对有副作用工具（退款/发消息）解释 idempotency/人工确认，不能盲重试。
**用户验收任务：** 根据 Codex 复现的错误与 before/after regression 证据，独立说明根因、修复思路和可能副作用；Codex 完成修复。
**证据：** `learning/decisions/ADR-001.md`、`reports/optimization_loop.md`、`learning/stages/05.md`。
**通关方向：** 如何定义一次合理的修改？如何归因？为何 retry 有风险？成功率上升仍然回滚的情况？

### Stage 06｜深入 Harness² 的 Propose–Probe–Compose 与 Reflection（源码理解）
**知识：** 任务级递归、候选生成、行为对比、Compose/Adoption、parallel/sequential、跨任务反思。
**任务：**
- [ ] 按当前 checkout 找到 CLI → candidate generation → probe runner → compare/compose → reflection persistence 的真实函数路径。
- [ ] 对比 k=1、k>1、parallel 和 sequential，分析候选数、执行次数、上下文依赖及成本。
- [ ] 从真实 Demo trace 还原一次候选修改前后行为；说明“不用 ground truth 优化”与“最终仍需独立 judge”并不冲突。
- [ ] 分析 8 类可编辑 Harness 组件与各自风险；至少给一个源代码边界/错误路径写可运行测试。
**用户验收任务：** 根据 Codex 提供的真实 PPC 调用图独立口述数据流，并回答任意一个函数的追问；Codex 负责源码定位与绘图。
**证据：** `learning/stages/06.md`、`learning/SOURCE_INDEX.md`、实际 trace 文件位置和 SHA。
**通关方向：** Compose 是否只是选最高分？如何在无标准答案时比较？什么是 Task-level vs Harness-level recursion？为何一个任务的经验可能伤害下一个？

### Stage 07｜官方真实模型单任务复现（官方 Benchmark）（官方可复现）
**知识：** solver/improver/judge 分工、模型路由、依赖、token/cost、沙箱与网络、官方原生 benchmark。
**任务：**
- [ ] 先选择官方 LAB 单任务或 WorkBuddy code 单任务；使用当前 checkout 的 `--help`、README/SETUP 核对真实命令。
- [ ] 在隔离环境中核对安全、认证、输出路径及成本；先 dry-run。官方 CLI `--bench`, `--k`, `--mode`, `--max-tasks`, `--dry-run` 的支持以本地版本为准。
- [ ] **仅经明确授权**执行一个真实模型任务及官方 judge/report；保存 baseline、adopted harness、trace、run manifest。
- [ ] 明确 run 和 judge 的模型/subset/task selection/seed、环境一致；失败/未评分分开。
- [ ] 无凭证时允许先完成此阶段的概念练习，但**真实复现必做要求留为 BLOCKED，不能以 Demo 代替真实结果**。
**用户验收任务：** 解释一次实际 run 的输入→输出文件关系与评分结果；如 blocked，解释阻塞与排障清单。
**证据：** `experiments/manifests/official_run_*.json`、`reports/official_one_task.md`、`learning/stages/07.md`。
**通关方向：** 为什么 judge 与 improver 隔离？为什么任务成功不代表模型稳定？什么信息属于泄漏？没有真实 run 能说完成到什么程度？

### Stage 08｜公开 Coding Benchmark：选择、独立安装与原生评测（新增必做）
**目的：** 学会独立判断一个公开数据集是否适合 Coding Agent，理解原生 Evaluator，而非只用别人的 score。
**默认选择：** SWE-bench（在其当前仓库内评估可运行任务及评测脚本）；可研究 DeepSWE/Multi-SWE-bench 做对比。由于部分公开基准存在污染/评测问题，**不能凭名字保证绝对公平**。
**任务：**
- [ ] 评估三个候选：任务类型/语言/原生 evaluator/隔离机制/数据访问/机器成本/许可证/时间/结果可信度；写 Benchmark Selection ADR，选择一个并解释为什么不选另外两个。
- [ ] 克隆选择的官方 Benchmark 仓库并锁 commit；读清 task instance、repo、base commit、patch、test/verifier 的字段和格式。
- [ ] **先验证 benchmark 自己的 evaluator**：在隔离容器/VM 中使用官方示例或最小样本，观察环境启动、应用 Patch、运行测试、产出 verdict 的全过程；区分 `resolved`, `failed`, `infra_error`, `unscored`。
- [ ] 设置不少于 2 个可运行任务作为 wiring smoke test；再策划 5–10 个固定验证任务（若成本允许），另保留不参与调参的本地测试任务；样本数有限时不能声称泛化提升。
- [ ] 避免把 gold patch / hidden verifier / rubric 传给被测 Agent；记录已知公共数据污染风险。
**用户验收任务：** 独立追踪一个实例 `issue → base commit → patch → evaluator → verdict`，解释何时判定通过；Codex 执行 Evaluator。
**证据：** `learning/decisions/ADR-benchmark-selection.md`、`learning/stages/08.md`、`reports/coding_benchmark_native_eval.md`、测试命令/原始输出。
**通关方向：** 为什么选 SWE-bench？Evaluator 是不是 LLM-as-a-Judge？为何不能把测试失败直接当模型失败？何为 patch 应用失败？如何降低数据泄漏？
**硬性要求：** 此阶段不能省略；如果机器资源不足，记录资源与阻塞并由用户决定更换公开 Benchmark；不能虚构已跑通。

### Stage 09｜自主实现 Coding Benchmark ↔ Harness² Adapter（新增必做）
**目的：** 让官方优化流程在公开 Coding Benchmark 任务上运行，并且让该 Benchmark 原生 evaluator 保持评分权威。
**任务：**
- [ ] 从**已核实的官方代码**确认当前 Harness² benchmark task/runner/artifact 接口；不得写死虚构 API。
- [ ] 设计 `task adapter`（task id/repo/commit/issue）、`executor adapter`（working tree、timeout、patch capture）、`result adapter`（patch/artifact 路径）、`judge bridge`（调用 benchmark 原生 evaluator 并解释 verdict）。
- [ ] 先用 Fake Executor 验证映射和 Patch 收集，再用隔离执行器跑 1–2 个真实任务 smoke test。
- [ ] 对空 patch、错误 base commit、patch 冲突、环境超时、测试不通过、tool crash 分别写测试。
- [ ] 为每个任务保留原生 task_id，trace 与 patch 可追溯到 `run_id`；记录 adapter 的代码与官方原始代码区分。
- [ ] **优先外置 adapter**，若必须改官方源码需建立个人分支、小改动、单测和 diff。
**用户验收任务：** 阅读 Codex 实现的最小 mapping 函数，解释由谁执行 Patch、由谁判决 resolved，并指出一处可能的映射错误。
**证据：** `experiments/adapters/`、`tests/`、`reports/adapter_smoke_test.md`、`learning/stages/09.md`。
**通关方向：** 为什么 task adapter 和 evaluator 不应混为一体？什么是 verifier isolation？如何处理基础 commit 不一致？如何做 adapter 单测？

### Stage 10｜可信对照、回归、消融与成本分析（新增必做）
**目的：** 从“跑通”跨到“证明效果”。
**任务：**
- [ ] 固定 model、任务 ID 集合、base commit、运行环境、工具权限、max steps、budget、官方框架 SHA、evaluator 版本、seeds（若支持）。
- [ ] 用相同 Coding Benchmark 的开发/验证任务对比 Base Harness vs Harness² refinement；按任务记录 resolved/failed/infra_error/unscored，不把仅成功几题包装成代表性提升。
- [ ] 创建独立 regression suite：在修改没参与调参的案例上复测，统计新增成功与由成功变失败的任务。
- [ ] Ablation：关闭一个组件（如 reflection / guardrail / retry），确认差异与成本，避免结论过度归因。
- [ ] 记录 token、API费用、wall-time、模型调用数、重试与工具错误；做 paired comparison，并清楚标注随机波动和样本规模局限。
- [ ] 设计 `regression gate`：若安全硬约束失效/关键回归或成本超预算，禁止自动采用新的 Harness。
**用户验收任务：** 给定 before/after 的逐任务结果，独立分析 paired delta、回归任务和未评分任务；Codex 实现比较代码与报告。
**证据：** `reports/coding_benchmark_comparison.md`、`experiments/manifests/`、regression test、`learning/stages/10.md`。
**通关方向：** 任务成功率改善是否证明因果？怎样比较基线公平？为什么 unscored 不应该混入 failed？什么是过拟合和回归门槛？

### Stage 11｜Reflection 与长期记忆的独立扩展（核心学习）
**知识：** 官方跨任务经验 vs 通用 Memory、provenance、retrieval precision/recall、冲突、staleness、忘记/归档、污染。
**任务：**
- [ ] 在当前官方代码真实定位 Reflection 的写入/读取和经验跨任务使用路径；记录经验与证据如何被保留。
- [ ] **独立实现**简单记忆存储结构（`memory_id`, `fact`, `source`, `valid_from`, `confidence`, `status`）；支持检索、更新、冲突处理、失效、归档。
- [ ] 自建约 30 个含真值的记忆测试，覆盖准确召回、跨会话、时间冲突、相似噪声、错误信息注入、旧记忆污染。
- [ ] 对照 Memory ON/OFF 及 no-conflict-resolution，报告 retrieval precision@k/recall@k、stale_use、false_adoption、latency/cost。
- [ ] 严格区分个人新实现与 Google 官方 Harness² 的实验结果。
**用户验收任务：** 阅读 Codex 实现的 resolver，从新旧冲突记录中解释选择保留/失效的证据及一项反例。
**证据：** `experiments/memory_lab/`、`reports/memory_eval.md`、`learning/stages/11.md`。
**通关方向：** Memory vs RAG？为什么不能只用 Redis 存全部历史？新旧记忆冲突怎么办？怎么识别污染？

### Stage 12｜个人工程贡献（项目亮点）
**任务：** 选一个并完整交付：
- [ ] A. 具备 trace 证据链接的 Failure Classifier/Bad Case dashboard；或
- [ ] B. Regression Gate（当改进版造成关键回归时自动拒绝采纳，**优先推荐**）；或
- [ ] C. Cost-aware Propose/Probe 策略（质量/成本/延迟）；或
- [ ] D. Memory provenance / conflict resolver。

**做法：** Codex 用 1 页 spec 说明问题、目标、输入输出、设计替代方案、测试、风险、假设，亲自实现核心部分并运行 unit/integration、反例、对照实验；展示 README 与 commit diff，注明官方代码、Codex 实现和用户独立设计/验收的真实边界。
**用户验收任务：** 阅读该模块的一处边界条件和测试，说明预期修改思路与验证方法；实际修改和运行由 Codex 完成。
**证据：** `reports/my_contribution.md`、ADR、个人 commit、`learning/stages/12.md`。
**通关方向：** 为什么选择这个改进？收益/副作用？相对官方有什么新贡献？如何验证不会伤害其他任务？

### Stage 13｜最终技术面试、README 与简历证据（终验收）
**任务：**
- [ ] 准备 30 秒概述、2 分钟架构讲解、5 分钟 Trace/Bad Case 分析，以及 10 分钟现场代码追踪。
- [ ] 从真实报告填入：选用 Benchmark/样本数/Base vs Optimized/Regression/Unscored/运行成本/环境限制；没有证据的指标不能写简历。
- [ ] 整理 30 道技术题及 10 道项目追问：Runtime/Harness/Tool/MCP、fake/model mocks、数据集/metrics、trajectory/Judge、PPC、评测泄漏、Retry、ablation、memory、个性化工程贡献。
- [ ] 完成 **三轮独立面试**：基础概念、代码/调试、系统设计/项目深挖；每轮记录原回答、追问、得分和变式复测。
- [ ] 对真实未解决的问题、数据集污染风险和项目局限做独立说明；最终 README 清晰区分 official replication / adapter / original contribution。
**用户验收任务：** 在不查当前考题答案的情况下独立讲解架构，并定位评测器一个 bug、说明修复与验证思路；Codex 执行修改和测试。
**证据：** `interview/`、最终 README（由用户与 Codex 实际生成）、`reports/final_report.md`、`learning/stages/13.md`。
**通关方向：** 五个核心题全部无提示解释；能随机定位任一关键函数；能客观解释为什么结果可信、哪里还不可信。

## C.1 关于自研评测系统的最终实施边界

请额外阅读 `EVALUATION_SYSTEM_SPEC.md` 与 `PROJECT_DELIVERABLES.md`。官方 Judge/Benchmark Evaluator、个人 Metrics/Trace/Bad Case/Regression Gate 和公开 Coding Benchmark 的 Native Evaluator 属于不同层，不得互相冒充。具体自研文件名是**计划中的交付目标**，并非 ZIP 已实现代码。

## D. 跨会话进度与证据存储标准

**必须文件：**

```
AGENTS.md                      # 持久导师协议，每次优先读取
MASTER_PLAN.md                 # 本计划，原始要求不可随意弱化
CODEX_START_PROMPT.md          # 新会话引导
learning/PROGRESS.md           # 人类可读的当前进度与下一唯一动作
learning/stage_status.json     # 结构化阶段状态、审批与 gate 信息
learning/MASTERY_MATRIX.md     # 关键能力掌握等级及证据
learning/SESSION_LOG.md        # 会话事实日志（追加，不替换）
learning/MISTAKES.md           # 错误、改进、变式复测
learning/SOURCE_INDEX.md       # 官方仓库 commit:path:function 真实定位
learning/OFFICIAL_EVAL_AUDIT.md # 源码级盘点官方已有评测/回归能力
learning/gates/NN.md           # 单阶段问题、用户回答、评分、补救、审批
learning/stages/NN.md          # 单阶段教学笔记与动手实践
learning/decisions/ADR-*.md    # 方案选择与证据
experiments/adapters/          # 公开 Benchmark Adapter（个人实现）
experiments/evaluators/        # 自动评测与 trace/judge/指标
experiments/manifests/         # 模型版本、任务集、预算、运行设置
experiments/memory_lab/        # 独立 Memory 扩展
reports/                        # 基准结果、回归、个人贡献
interview/                      # 练习与问答记录
scripts/                        # 不花钱的本地状态检查工具
upstream/harness2/              # 官方代码 checkout（后续完成）
```

每次会话前 `python scripts/resume.py`，结束时 `python scripts/check_workspace.py`。新会话不依赖“你应该记得”；从**保存的文件 + 实际 git/日志证据**恢复。

**会话结束最少要写入：** 日期、当前阶段/status、做了的任务、Codex 代码与用户独立分析/验收的归属、测试命令与 PASS/FAIL/BLOCKED 结果、面试原回答摘要、掌握/薄弱点、变式复测需求、下次一个唯一动作、待用户批准事项。

**状态流：** `NOT_STARTED → IN_PROGRESS → READY_FOR_GATE → PASSED_AWAITING_USER → COMPLETED`，另有 `BLOCKED`。下一阶段从 `LOCKED → NOT_STARTED` 仅由用户明确批准后执行。

**记录每次 Benchmark run 的最小 manifest：** upstream commit，adapter commit，benchmark commit/dataset version，任务 ID/筛选规则，模型 ID/温度（若可控），substrate/executor，harness diff，环境/网络限制，工具权限，seed，时间，token/成本/延迟，`resolved/failed/infra_error/unscored`，结果路径与完整命令，允许其他人复算。**不保存 API key**。

## E. 新会话开场和阶段收尾协议（固定格式）

**开场报告（6 行内）：**
- 当前 Stage / 状态：
- 上次已验证的结果（文件/命令）：
- 已掌握 / 未掌握：
- 当前阻塞或需要确认的成本：
- 本次唯一工程任务与用户验收点：
- 本轮第一道复习问题：

**考核前：** 根据当前 stage 和用户常错点生成 ≥5 道**新**原理题，分批提问，用户没回答当前题之前不透露该题答案；至少两道追问、一道真实代码/Trace 题、一道故障定位/设计题。必须记录 score 和证据。不能因为用户说“懂了”就给 PASS，也不要求用户手写完整程序。

**收尾：** 本阶段实际状态 + 哪些真实代码/运行结果支持 + 问答成绩/未考 + 新发现的错误 + 写入了哪些文件 + 下次唯一动作。若已通过，**停止并等待批准**，绝不自动进入下一阶段。

## F. 防止简历夸大的明确边界

- 只完成 Stage 00–06：只能写“源码分析与官方 Demo 复现”，不可写真实 LLM 优化成绩。
- Stage 07：最多写“官方单任务真实模型复现”，不代表论文所有 Benchmark 复现。
- Stage 08：只表示公开 Coding Benchmark 的原生评测已跑通，**不代表 Harness² 能跑此集**。
- Stage 09：能够说“自研 Adapter 连接公开 Coding Benchmark”，但 smoke test 不代表通用性能提升。
- Stage 10：有对照数据才写量化结果，注明样本量和是否重复执行；无效/未评分单列。
- Stage 11–12：属于个人扩展，不能冒充官方新增功能。
- Stage 13：实际已交付/已验证的才进入简历。
