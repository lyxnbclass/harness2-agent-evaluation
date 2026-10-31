# Harness² 官方复现 + 公开 Coding Benchmark + Agent 评测与回归 + 面试学习计划（v4.0）

> 最终可验证项目：**Harness²: Evaluation-Driven Self-Improving Coding Agent**。
> 源码复现基于 Google Research Harness²；第三方公开 Coding Benchmark 优先 SWE-bench；个人代码补上评测器、数据/Trace 统计、Regression Gate 和长期记忆实验。
> 本计划从旧版 12 个阶段演进为 14 个阶段；阶段编号 00–13。**这不是用户已经完成的项目**，实际完成状态必须以 `learning/PROGRESS.md` + Git/日志证据为准。
> 时间仅作自主安排参考。**按真实工程证据、完整链路理解与定性阶段验收推进**，避免在普通细节上停滞。资料地址见 `START_HERE.md`。

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

## B. 工程与教学循环

每个阶段完成 **Trace → Implement → Inject Failure → Test → Teach → Review → Record**，相邻章节如重复可合并讲解，但必做工程任务不删：

1. **Trace：** Codex 在已 checkout 的官方源码中定位入口、函数、参数、返回、异常；记录 `commit SHA:path:function`。没有源码就标记 NOT_VERIFIED。
2. **Implement：** Codex 编写/修改当前阶段的核心逻辑，配置环境并运行命令；用户负责阅读、理解、分析和验收，记录真实代码作者与用户的独立分析贡献。
3. **Inject Failure：** Codex 安全地制造或选择一个失败，保存 trace；用户根据证据解释首次偏离、根因和可证伪假设，Codex 完成修复和验证。
4. **Test：** Codex 保存命令、真实 exit code、日志路径、样本数量、PASS/FAIL/BLOCKED 结果。
5. **Teach：** 按 `AGENTS.md` 的七部分结构，一轮讲清当前章节的定义、作用、链路、ASCII 图、1–3 段关键源码、面试表达和 3–5 道集中思考题。基础语法即时解释；没有实测就标 `PROPOSED` 或 `BLOCKED`。
6. **Review：** 用户集中回答后，Codex 定点反馈并改进面试表达；用户判断自己是否理解。章节继续不靠分数或固定追问。阶段收尾核对核心理解、工程必做项和 PR，等待用户明确确认进入下一 Stage。
7. **Record：** 优先更新 `PROGRESS.md`、`MASTERY_MATRIX.md`、`stage_status.json`，必要时追加 `SESSION_LOG.md` 与实际工程证据；历史 Gate 文件保留，不再维护旧评分流程。

### 阶段验收（无分数）

| 维度 | 定性通过证据 |
|---|---|
| 概念与原理 | 独立解释核心术语、适用条件和重要反例 |
| 代码与 Trace | 当场追踪真实入口、关键参数/返回、数据流和产物，解释一次执行行为 |
| 故障与设计 | 指出首次偏离、根因假设、验证办法及方案权衡 |
| 面试表达 | 清楚说明项目动机、自己的真实贡献、运行证据和限制 |

上述维度用于指导反馈，不设固定题量或逐项达标分数。用户确认理解、必做代码/测试/实验有证据且关键安全或评测误解已澄清后，可准备阶段 PR。只有用户明确说“进入下一阶段”、阶段 PR 已核实合并后，才标记当前阶段 `COMPLETED` 并开启下一阶段。`BLOCKED` 不等于工程完成；历史 Gate 状态仅供查询。

### GitHub 阶段交付

Codex 负责本地 Git 初始化、远程仓库关联、每阶段独立 branch、必要时的 Commit/Push 和阶段 PR；用户检查 PR 与阶段成果。仓库名和可见性在首次创建前由用户确认。每阶段原则上一个面向 `main` 的正式完成 PR，须在本阶段代码/实验与面试 Gate 通过后创建；不自动 Merge。进入下一阶段前，核实 PR 已合并、目标分支含本阶段提交，并取得用户明确批准。每轮记录 branch、重要 commit、PR 链接/状态、测试与考核证据。GitHub 认证或网络失败应记录为 BLOCKED，不得声称已 Push 或已建 PR。

根目录英文 `README.md` 是正式 GitHub 项目介绍。Stage PR 合并后，Codex 必须核实 `main` 并同步 README 的完成阶段、真实功能/代码路径、测试与运行命令、实验结果和限制；未实现项继续标 `Planned` / `In progress`。详见 `AGENTS.md` 的 README 持续维护规则。

## C. 阶段计划（00–13，必做）

### 连贯的章节顺序

阶段编号继续对应独立 Branch 和 PR；章节是教学单元，可以在同一 Stage 内连续讲解，也可把相邻重复内容合并讲。

| 顺序 | 章节主线 | 对应 Stage | 面试落点 |
|---|---|---|---|
| 1 | 官方 Demo：输入、候选、执行、选择、经验与产物 | 00 | Harness 与 Runtime 的边界；Demo 不能证明 Benchmark 提升 |
| 2 | 最小 Agent Runtime 与 Tool Calling | 01 | 状态循环、工具协议、异常与测试 |
| 3 | 评测数据、Metrics、Trajectory 与 Bad Case | 02–03 | 分母、未评分、失败定位 |
| 4 | Judge 可靠性与评测驱动优化 | 04–05 | 校准、Baseline、Ablation、回归与成本 |
| 5 | 官方 PPC、Parallel/Sequential、Reflection 与评测审计 | 06–07 | 固定 SHA 的源码链路及真实官方判分边界 |
| 6 | 公开 Coding Benchmark 原生评测与 Adapter | 08–09 | 隔离、Patch、评分权威和泄漏 |
| 7 | 对照实验、回归门禁与报告 | 10、12 | 成对比较、退化、基础设施失败 |
| 8 | 长期记忆与跨任务经验复用 | 11 | 检索、冲突、过期、污染及记忆评测 |
| 9 | 项目复盘与技术面试 | 13 | 架构、真实贡献、证据与局限 |

Stage 12 的工程扩展仍在 Stage 11 之后实施；表中的 Stage 10、12 仅表示知识关联，不改变阶段执行顺序。

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
**教学顺序：** 按七部分结构一次贯通 `harness2-demo → main → DemoAdapter → run_domain/run_task → Proposer → execute/Trajectory → 选择/经验库 → demo.json`，结合真实输入、产物和源码；后续再按需深入高频机制，不按单个路径细节拆成多次考核。
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

### Stage 12｜项目原创工程扩展（用户理解与验收）
**任务：** 选一个并完整交付：
- [ ] A. 具备 trace 证据链接的 Failure Classifier/Bad Case dashboard；或
- [ ] B. Regression Gate（当改进版造成关键回归时自动拒绝采纳，**优先推荐**）；或
- [ ] C. Cost-aware Propose/Probe 策略（质量/成本/延迟）；或
- [ ] D. Memory provenance / conflict resolver。

**做法：** Codex 用 1 页 spec 说明问题、目标、输入输出、设计替代方案、测试、风险、假设，亲自实现核心部分并运行 unit/integration、反例、对照实验；展示 README 与 commit diff，注明官方代码、Codex 实现和用户独立设计/验收的真实边界。
**用户验收任务：** 阅读该模块的一处边界条件和测试，说明预期修改思路与验证方法；实际修改和运行由 Codex 完成。
**证据：** `reports/my_contribution.md`、ADR、Codex 代码 commit、用户独立分析/验收记录、`learning/stages/12.md`。
**通关方向：** 为什么选择这个改进？收益/副作用？相对官方有什么新贡献？如何验证不会伤害其他任务？

### Stage 13｜最终技术面试、README 与简历证据（终验收）
**任务：**
- [ ] 准备 30 秒概述、2 分钟架构讲解、5 分钟 Trace/Bad Case 分析，以及 10 分钟现场代码追踪。
- [ ] 从真实报告填入：选用 Benchmark/样本数/Base vs Optimized/Regression/Unscored/运行成本/环境限制；没有证据的指标不能写简历。
- [ ] 整理 30 道技术题及 10 道项目追问：Runtime/Harness/Tool/MCP、fake/model mocks、数据集/metrics、trajectory/Judge、PPC、评测泄漏、Retry、ablation、memory、个性化工程贡献。
- [ ] 围绕基础概念、代码/调试、系统设计/项目深挖完成模拟面试；按实际回答记录关键反馈，不设固定轮数或分数。
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
README.md                      # 面向招聘人员的英文 GitHub 项目介绍，随已合并 Stage 更新
MASTER_PLAN.md                 # 本计划，原始要求不可随意弱化
CODEX_START_PROMPT.md          # 新会话引导
learning/PROGRESS.md           # 人类可读的当前进度与下一唯一动作
learning/stage_status.json     # 结构化阶段状态与用户批准
learning/MASTERY_MATRIX.md     # 关键链路的定性理解状态及证据
learning/SESSION_LOG.md        # 会话事实日志（追加，不替换）
learning/MISTAKES.md           # 历史关键误区与必要的纠正
learning/SOURCE_INDEX.md       # 官方仓库 commit:path:function 真实定位
learning/OFFICIAL_EVAL_AUDIT.md # 源码级盘点官方已有评测/回归能力
learning/gates/NN.md           # 历史 Gate 记录，必要时补充阶段验收证据
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

新会话优先读取进度和矩阵，再用实际 Git、代码与日志核对；`python scripts/resume.py`、`python scripts/check_workspace.py` 可辅助检查记录，不能替代理解或运行证据。

**会话结束最少记录：** 日期、当前章节与阶段、实际工程改动和验证、已讲/已确认理解/仍有疑问、Branch/PR、下次内容及待用户确认事项。重要命令和结果保留在工程记录或简短 Session Log；不重复抄写所有文件。

**状态流：** `LOCKED → NOT_STARTED → IN_PROGRESS → COMPLETED`，另有 `BLOCKED`。历史 `READY_FOR_GATE` / `PASSED_AWAITING_USER` 可读但不再作为强制步骤；下一阶段仅在用户明确确认且上一阶段 PR 已核实合并后开启。

**记录每次 Benchmark run 的最小 manifest：** upstream commit，adapter commit，benchmark commit/dataset version，任务 ID/筛选规则，模型 ID/温度（若可控），substrate/executor，harness diff，环境/网络限制，工具权限，seed，时间，token/成本/延迟，`resolved/failed/infra_error/unscored`，结果路径与完整命令，允许其他人复算。**不保存 API key**。

## E. 新会话与章节收尾

开场简述当前章节/Stage、上次已验证证据、用户已确认理解与疑问、下一内容。每章按 `AGENTS.md` 七部分讲解并集中给 3–5 道无提示思考题。用户回答后定点反馈；无需数字评分、固定追问或强制补考。收尾写入真实工程与学习状态。阶段结束仍等待用户确认，不自动进入下一阶段。

## F. 防止简历夸大的明确边界

- 只完成 Stage 00–06：只能写“源码分析与官方 Demo 复现”，不可写真实 LLM 优化成绩。
- Stage 07：最多写“官方单任务真实模型复现”，不代表论文所有 Benchmark 复现。
- Stage 08：只表示公开 Coding Benchmark 的原生评测已跑通，**不代表 Harness² 能跑此集**。
- Stage 09：能够说“自研 Adapter 连接公开 Coding Benchmark”，但 smoke test 不代表通用性能提升。
- Stage 10：有对照数据才写量化结果，注明样本量和是否重复执行；无效/未评分单列。
- Stage 11–12：属于项目原创扩展，不能冒充官方新增功能；记录由 Codex 编写的代码和用户独立完成的设计/审查/验收。
- Stage 13：实际已交付/已验证的才进入简历；不得把 Codex 编写的代码声称为用户亲手实现。
