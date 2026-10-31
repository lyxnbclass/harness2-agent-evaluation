# 独立知识掌握记录（与工程进度分开）

此文件按**完整工程链路和高频机制**记录教学与用户独立证据；`learning/MASTERY_MATRIX.md` 只做汇总。当前使用 `未讲 / 已讲待验证 / 已理解 / 需补充` 的定性状态，不做数字评分或 L1–L5 微评级。**Codex 讲解、运行或测试通过不自动证明用户已理解。**

每项记录：官方 SHA/源码位置、术语定义与作用、ASCII 架构/数据流、关键源码、真实演示、工程权衡、代表性问答与关键误区、待复习点和定性理解状态。普通细节遗漏补讲后继续主线，不以一道路径题阻断完整链路。以下旧条目保留历史回答证据；旧 L1/U 文字在本次规则调整后不再作为当前状态使用，以矩阵和本文件新状态为准。

## 2026-10-30 教学节奏调整：Stage 00 当前链路

### 2026-10-31 完整 Demo 链路复核与教学

- 官方 SHA：`1cfe254e8d25b15f37048c3730134686abe60335`。复核 `harness2/cli/demo.py:main` → `harness2/core/schedule.py:run_domain/run_task/_run_one_mode` → `harness2/core/recursion.py:run_parallel/run_sequential` → `harness2/demo.py:DemoAdapter.execute/DemoProposer.call` → `harness2/core/selection.py:trivial_selection/reflect_adoption` → `harness2/core/library.py:Library.add`。
- 本轮真实复核：`experiments/raw_runs/stage00_demo_k1/demo.json` 为 2 done/0 failed/14 executions/16 scripted editor calls；`ledger-1` 基线和 `agg1` 答案为 105.25/85.15；`selection/agg1/selection.json` 标记 `trivial=true`、`chosen_label=agg1`；经验文件存在于 `library/k1/agg/accounting/harnesses/ledger-1/EXPERIENCE.md`。
- 本轮讲解范围：命令参数传递、Adapter 供任务与执行、Scheduler 跑任务、固定规则 Proposer 修改脚本、产物生成、`k=1` 直接选择、Reflection/Library 和最终 `demo.json`；解释 Demo `ok` 与独立 Benchmark 判分的边界。没有重新运行 Demo 或模型。
- 用户独立回答：局部回答及待补充点见下节；完整链路状态保持 `已讲待验证`。Stage 00 正式 Gate 未考。

#### 2026-10-31 集中理解题反馈与超时故障演示

- 用户 Q1 原回答：`task_id` 选 CSV、`harness_dir` 选执行脚本、`run_id` 决定产物目录；三项均正确。Q2 原回答：基线漏负数，修改后删除过滤条件；方向正确，将 `if amount > 0` 误称为 `domain>0`，已纠正术语。
- 用户 Q3：猜测“选择了新的脚本执行”，同时指出只能证明有生成结果，主动要求解释。待补充的关键点：本次 `k=1` 选择的是已经执行且交付产物的唯一 final `agg1`，不是选择后才执行；`delivered` 检查文件存在，不是独立判分。用户 Q4 表示不知道超时如何定位，待教学后用新场景验证。
- OBSERVED 故障注入：Docker Python 3.12、`--network none`、官方源码只读挂载、隔离输出目录 `/out/raw_runs/stage00_timeout_probe_20261031`，直接调用 `DemoAdapter.execute('ledger-1', None, 'timeout-probe', timeout=1e-9)`；捕获 `TimeoutExpired`，执行目录存在，`answer.txt` 和 `trajectory.md` 均不存在。异常由探针代码捕获，所以容器最终退出 0；这不代表该 `execute()` 成功。源码路径：`demo.py:86–105`，调度层失败包装在 `core/recursion.py:_roll` 或 `core/schedule.py:_roll_bases`。
- 当前定性：Adapter 三参数与基线结果差异 `已理解`；选择/评测边界和超时定位 `需补充`；完整 Demo 链路 `已讲待验证`。正式 Gate 未考。

#### 2026-10-31 应用户要求讲解两个待答题，并推进 Scheduler 链路

- 用户明确要求 Codex 直接讲解“已有错误答案文件”和“唯一 final 未交付”两题；因此这两题**没有用户独立回答证据**，不能据讲解更新为已理解。
- 官方 SHA `1cfe254e…`：`demo.py:107–108` 的 `delivered()` 仅检查 `answer.txt` 存在；`core/selection.py:_render_pool():120–132` 要求 `rv.ok`、`rv.delivered` 且答案文本非空；`trivial_selection():379–399` 在筛后为空时返回错误。Demo 的 `BenchSpec.state_deliverable` 取默认 `False`，所以不能用轨迹替代缺失的答案。已有文件但内容错误属于答案正确性问题（前提是新鲜的本次产物）；无交付的唯一 final 不能仅凭候选数量被采用。两者均不是原生 benchmark 真值判分。
- 下一步源码链：`core/schedule.py:run_domain():669–733` 创建每个模式的库、逐任务记录 `library_entries_before`、调用 `run_task()`、按状态累计 done/failed；`run_task():619–666` 共享基线后运行各模式并写每题 `summary.json`；`_run_one_mode():513–563` 建 finals-only 选择池、`k=1` 走 trivial selection、反思和入库；`_merged_status():265–279` 看各模式、选择与错误记录，不核验答案真值；`cli/demo.py:49–54` 补执行/编辑次数并写总 `demo.json`。
- OBSERVED：本地 `ledger-1` 和 `ledger-2` 的 `summary.json` 均 `status=ok`，两模式 final 为 `agg1`/`c1`；总 `demo.json` 为 2 done/0 failed，`library_entries_before` 对首题为 agg/seq 各 0、次题各 1。`ledger-2` 基线/agg final 答案为 35.50/20.25。经验条目确实存在；计数只证明可供后题读取，不证明它对 DemoProposer 的固定规则修改有因果效果。
- 用户对 Scheduler 数据流、状态汇总与上述两题变式的独立理解待验证；正式 Gate 仍未考。

#### 2026-10-31 再次由 Codex 讲题，并讲 parallel/sequential

- 用户要求 Codex直接讲解 Scheduler 的三道待答题并进入下一小节，没有独立作答。这三题不计入正式 Gate，也不能据此将 Scheduler 标记为用户已理解。
- 答案与边界：`library_entries_before=1` 证明前题经验条目已存在且传给后题的库上下文，不证明固定规则的 DemoProposer 因此得到更好结果；`summary.json status=ok` 由 `core/schedule.py:_merged_status` 根据模式、选择和错误记录决定，不核对真值；若 `run_task()` 返回 `partial`，`run_domain()` 走 `failed += 1`，CLI 最终 `return int(result["failed"] > 0)`，此反事实为源码推演，非本次运行观察。
- 新小节源码（官方 SHA `1cfe254e…`）：`core/recursion.py:run_mode():569–578` 将 `agg` 分派给 `run_parallel()`、`seq` 分派给 `run_sequential()`；`run_parallel():343–449` 从共享基线证据提出 `2k` 个 INV/DOM 候选并独立组合为 `agg1..aggk`；`run_sequential():452–566` 按 `t=1..k` 逐轮提出候选、组合为 `c1..ck`，每轮 `current_harness = comp.tree`。`core/selection.py:selection_pool():93–111` 仅把各模式 final 加入选择池。
- OBSERVED：`ledger-1` 的两个 `summary.json` 模式记录同一共享 `base1`，agg 的 final 为 `agg1`，seq 的 final 为 `c1`；真实答案均 `Total: 85.15`，两个 `selection.json` 均 `trivial=true`。每题 1 次共享基线 + agg 3 次 + seq 3 次 = 7 次本地执行，两题总 `execution_count=14`；这是实际 manifest/产物与源码的对照，不是模型 Benchmark 结果。`k>1` 的多轮差异只基于本地源码分析，尚未执行。
- 用户独立解释 parallel/sequential、共享基线计数及 Demo/Benchmark 边界仍待验证；正式 Gate 未考。

- 当前主线：`CLI → Adapter → Scheduler → Proposer → execute → Trajectory/产物 → 选择/经验库 → demo.json`，用官方 SHA `1cfe254e…` 的源码和已运行 Demo 产物贯通。
- 已有证据：官方本地 Demo 2 个账本任务均 `ok`，无模型调用；用户已能区分 CSV、答案文件与简化 Trajectory，并知道未通过校验的候选不能直接执行。完整调度、选择、经验库与 Demo/Benchmark 边界待集中教学和问答。
- 当前理解状态：`已讲待验证`（针对完整链路），无阶段 Gate 结论。原 `review-b` 路径变式取消为必答门槛，路径拼接作为面试前可选复习点。
- 下一教学任务：完整 Demo 链路已在 2026-10-31 贯通讲解；等待用户回答集中理解题，再按关键缺口补讲。

## Stage 00 · Harness² 概念与官方无模型 Demo

- 官方版本：`1cfe254e8d25b15f37048c3730134686abe60335`。
- 源码位置：`upstream/harness2/README.md` 的项目定义；`pyproject.toml:32`；`harness2/cli/demo.py:main`；`harness2/demo.py:DemoAdapter` / `DemoProposer`；`harness2/core/schedule.py:run_domain` / `run_task`。详细源码教学按小节逐步展开。
- 为什么学：辨认模型、Harness、执行器、调度和评测的边界；正确解释无模型 Demo 能证明什么。
- 架构/数据流：`CLI → DemoAdapter 提供任务和初始 Harness → run_domain/run_task → 本地 Python 执行与预设修改 → 轨迹/答案 → summary.json → demo.json`。正式逐函数教学待继续。
- 已讲内容：过去讲过 CLI 与 Demo 源码数据流；2026-10-30 曾重新组织整体概念教学并加入真实运行结果。用户再次指出该讲解缺少关键代码、参数/返回值和 ASCII 调用图，因此**这部分不能标记教学完成**；本轮补充逐段代码与实际值对应。原 `--k 0` 问题已撤回，不计分。
- 真实演示：2026-10-30 Docker Linux/Python 3.12、无网络、只读源码、无凭证，`--k 1 --mode both` 退出 0；产物在 `experiments/raw_runs/stage00_demo_k1/`（忽略的大型原始运行目录）。`demo.json`：2 个任务 `ok`、0 failed、14 次本地执行、16 次预设编辑器调用；`ledger-1` 基线 `105.25`、修改后 `85.15`。这不是模型 Benchmark 或用户掌握证据。
- 工程分析：`k=1` 每模式只有一个 final，源码走 trivial selection；预设 `DemoProposer` 不是 LLM；本地 `delivered()` 仅检查 `answer.txt` 存在，不能等同独立 evaluator 判分。详细替代方案、故障与权衡待逐节教学。
- 理解检查/用户回答：针对完整 Demo 链路尚无独立技术回答；阶段 Gate 未考；状态：`已讲待验证`。
- 错误/未掌握：没有用户技术错误证据；概念、源码、执行和设计均待独立验证。
- 基础补课（2026-10-30）：用户主动询问 `Trajectory` 和 `CSV` 的含义，说明此前解释默认了尚未建立的数据格式与轨迹概念；这不是答题错误。已核对真实 `ledger-1/ledger.csv` 与基线/修改后 `trajectory.md`，并从 `csv.DictReader`、`DemoAdapter.execute()` 的写入代码补讲。完整链路仍待验证。
- 下一补课/小节：待用户确认代码贯穿的整体 Demo 讲解可理解后，再单独深入 `harness2-demo` 入口与 `argparse` 的真实调用、异常与参数变式。

## Stage 00 · CSV 与简化 Trajectory（基础子知识点）

- 官方 SHA/源码：`1cfe254e…`；`upstream/harness2/harness2/demo.py:30–37` 的 CSV 读取，以及 `DemoAdapter.execute():86–105` 的答案与轨迹写入。
- 已教学：真实 `ledger-1/ledger.csv` 是输入表；`csv.DictReader` 将 `amount` 列读成字典；`answer.txt` 存 stdout；这个 Demo 的 `trajectory.md` 用固定 `[ACTION]`/`[OBSERVATION]` 模板记录一次执行，不是完整 LLM Agent Trace。
- 真实演示：`experiments/raw_runs/stage00_demo_k1/sources/ledger-1/ledger.csv`、`executions/demo-oc-agg1/ledger-1/base1/trajectory.md` 与 `agg1/trajectory.md` 均已核对。
- 用户原回答（2026-10-30，非正式理解检查）：CSV“属于输入”；执行后“到 answer.txt 中查看”；“Trajectory 中记录了执行过程”。三点正确。未独立解释 `csv.DictReader`、`subprocess` 或轨迹写入代码。
- 错误/补课：此题未见错误；基础概念已能区分，脚本版本替换与完整 Demo 链路尚待集中验证。正式 Gate 未进行。

## Stage 00 · Demo 脚本版本替换与校验（子知识点）

- 官方 SHA/源码：`1cfe254e…`；`core/context.py:build` 复制可编辑工作副本；`core/recursion.py:_run_stage/_accept_tree/_roll` 提议、校验、物化与执行；`harness2/demo.py:DemoProposer.call/DemoAdapter.execute` 执行确定性修改和本地脚本。
- 已教学：ASCII 文件树及 `base → context/inv1/harness → harnesses/inv1 → executions/inv1` 链；相同 CSV 下基线脚本过滤负数得到 `105.25`，候选脚本删除过滤条件得到 `85.15`；组合阶段另行生成 `agg1`，不把它误说成机械复制 `inv1`。
- 真实演示：本地 `experiments/raw_runs/stage00_demo_k1/` 中 `base/`、`context/inv1/harness/`、`harnesses/inv1/`、`harnesses/agg1/` 的 `scripts/summarize.py` 内容和基线/候选 `answer.txt` 已核对；本小节未重新运行 Demo。
- 用户原回答（2026-10-30，非正式理解检查）：对“工作副本修改后校验失败应否直接执行”的回答为“记录错误并回退”。方向正确。补充精确源码边界：`_run_stage()` 最多再尝试一次；仍失败才返回 `fell_back=True` 和错误，未通过校验的工作副本不直接执行。
- 最近结果：该校验边界有一次正确概念回答；完整源码路径和执行过程尚无用户独立复述证据。正式 Stage 00 Gate 未考。
- 下一补课/任务：单独讲 CLI/`argparse` 的参数进入、转换、校验与退出码，再用新输入做 Trace 分析。

## Stage 00 · Demo CLI 参数与退出码（当前教学小节）

- 官方 SHA/源码：`1cfe254e…`；`upstream/harness2/pyproject.toml:32` 声明 `harness2-demo` 入口；`upstream/harness2/harness2/cli/demo.py:27–58` 的 `main(argv=None) -> int`；`core/schedule.py:48–55` 的 `mode_token()` 与 `:669–733` 的 `run_domain()`。
- 为什么学：看清用户命令如何变成 Python 类型和调度参数，区分参数错误与任务执行错误；联系前节的脚本版本替换与结果文件。
- ASCII/源码教学：本轮按 `命令 → __main__/入口 → parse_args → k 校验 → Path/模式转换 → adapter/proposer → run_domain → demo.json/exit code` 逐段解释。真实代码片段与各值在本轮回复展示；用户独立理解待检查。
- 有效运行证据：之前 `--output /out/raw_runs/stage00_demo_k1 --k 1 --mode both` 在隔离 Docker/Python 3.12 容器退出 0；`demo.json` 记录 2 done、0 failed、14 executions、16 scripted editor calls。参数值由源码解析规则推得，不是 CLI 单独打印出的内部变量。
- 新故障演示（2026-10-30）：同一容器、安全参数和官方源码，执行 `python -m harness2.cli.demo --output /tmp/invalid_k_demo --k 0 --mode both`；真实 stderr 为 `demo.py: error: --k must be positive`，捕获容器进程退出码 `2`。校验位于 `DemoAdapter(root)` 之前，因而此调用未进入任务调度。外层 PowerShell 在打印 `DEMO_EXIT_CODE=2` 后返回 0；二者不可混淆。
- 工程分析：`argparse` 负责类型/choices 与帮助信息，`main()` 补充 `k >= 1` 语义校验；参数错误通过 `parser.error()` 抛出 `SystemExit(2)`，有效任务的汇总结果走 `return int(result["failed"] > 0)`。`--k 0` 是 CLI 参数坏例，不能替代 Stage 00 计划中的错误输出路径/依赖故障注入。
- 用户回答与最近考核：用户要求直接讲解 `--k 1 --mode parallel` 题并进入 Stage 00 下一小节，未独立作答；由源码可推 `k=1`、`modes=("agg",)`、任务由 `adapter.tasks()` 提供。状态 `已讲待验证`；正式 Stage 00 Gate 未考。

## Stage 00 · DemoAdapter 的任务与执行边界（当前教学小节）

- 官方 SHA/源码：`1cfe254e…`；`upstream/harness2/harness2/demo.py:41–117` 的 `DemoAdapter`；`core/spec.py:200–249` 的 `BenchmarkAdapter` Protocol；调用者 `cli/demo.py:36–47`、`core/schedule.py:465,617,669`。
- 为什么学：Adapter 将通用任务调度与账本 CSV、脚本执行、产物格式隔开；联系前节 CLI 如何创建 Adapter、候选 Harness 如何由 `harness_dir` 切换。
- 已教学准备：本轮会以 ASCII 图解释 `DemoAdapter(root)` 初始化源文件与 base Harness、`tasks/task_prompt/task_files` 提供输入、`execute(task_id,harness_dir,run_id)` 执行、`delivered/trajectory/deliverable_text` 读取产物。`score` 在通用 Protocol 中声明，但 DemoAdapter 没有实现，不能把它说成真实 benchmark judge。
- 独立直接演示（2026-10-30）：隔离 Docker Python 3.12、无网络、官方只读源、输出挂 `experiments/`，直接创建 `DemoAdapter('/out/raw_runs/stage00_adapter_direct')`，`tasks()` 返回 `['ledger-1','ledger-2']`，`task_prompt('ledger-1')` 返回签名求和任务说明；`execute('ledger-1',None,'direct-base')` 的 `answer` 为 `Total: 105.25`，`delivered=True`，Trajectory 含固定 ACTION/OBSERVATION，`execution_count=1`，容器退出码 0。再在 `stage00_adapter_compare` 用同一输入分别执行 `harness_dir=None` 和已有 `harnesses/inv1`：输出 `105.25` 与 `85.15`，`execution_count=2`，容器退出码 0。两个原始输出目录均在忽略的 `experiments/raw_runs/` 下。
- 工程权衡/限制：同一 `execute()` 通过 Harness 路径参数切换脚本，调度器无须读 CSV；Demo 用 `subprocess.run(check=True,timeout=10)` 和简化轨迹，`delivered()` 仅检查文件存在，不代表真值评分。错误时 `execute()` 可能抛异常，调度层记录失败。
- 用户回答与状态：2026-10-30 用户答“选择一开始错误的脚本，读取一开始的CSV。answer.txt”。脚本和输入判断正确；答案只给文件名，遗漏 `run_id` 对应目录。已补讲 `run_dir = self.root / 'executions' / run_id` 与 `run_dir / 'answer.txt'`；普通路径细节不阻断完整链路。状态 `已讲待验证`；Stage 00 正式 Gate 未考。

## 后续知识点模板

每开始一条新链路复制以下字段，不预填“已理解”：

- 名称、Stage、官方 SHA/源码：
- 为什么学/与前一知识点关联：
- 架构图、组件边界、数据流：
- 已分段讲解的函数/参数/返回/分支/异常：
- Codex 真实运行命令、退出码、输入/Trace/产物：
- 工程设计、替代方案、故障、成本/可靠性：
- 面试口述示范已讲解：是/否；独立题在作答前不附答案。
- 用户原回答摘要、正确点、错误和复测：
- 最近无分数问答、定性状态（默认未讲）、关键薄弱点：
