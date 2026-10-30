# 独立知识掌握记录（与工程进度分开）

此文件按**知识点**记录六步教学和用户独立证据；`learning/MASTERY_MATRIX.md` 只做汇总。等级：`U` 无独立证据；`L1` 理解概念；`L2` 理解源码；`L3` 理解完整执行；`L4` 能分析工程设计与故障；`L5` 能独立应对深入面试。**Codex 讲解、运行或测试通过不自动提高用户等级。**

每项记录：官方 SHA/源码位置、为什么学、架构/数据流、源码讲解、真实演示路径、工程权衡、提问/用户原答摘要/错误、尚未掌握与补课、最近考核与等级。未完成的教学步骤写待讲，不预填掌握。

## Stage 00 · Harness² 概念与官方无模型 Demo

- 官方版本：`1cfe254e8d25b15f37048c3730134686abe60335`。
- 源码位置：`upstream/harness2/README.md` 的项目定义；`pyproject.toml:32`；`harness2/cli/demo.py:main`；`harness2/demo.py:DemoAdapter` / `DemoProposer`；`harness2/core/schedule.py:run_domain` / `run_task`。详细源码教学按小节逐步展开。
- 为什么学：辨认模型、Harness、执行器、调度和评测的边界；正确解释无模型 Demo 能证明什么。
- 架构/数据流：`CLI → DemoAdapter 提供任务和初始 Harness → run_domain/run_task → 本地 Python 执行与预设修改 → 轨迹/答案 → summary.json → demo.json`。正式逐函数教学待继续。
- 已讲内容：过去讲过 CLI 与 Demo 源码数据流；2026-10-30 曾重新组织整体概念教学并加入真实运行结果。用户再次指出该讲解缺少关键代码、参数/返回值和 ASCII 调用图，因此**这部分不能标记教学完成**；本轮补充逐段代码与实际值对应。原 `--k 0` 问题已撤回，不计分。
- 真实演示：2026-10-30 Docker Linux/Python 3.12、无网络、只读源码、无凭证，`--k 1 --mode both` 退出 0；产物在 `experiments/raw_runs/stage00_demo_k1/`（忽略的大型原始运行目录）。`demo.json`：2 个任务 `ok`、0 failed、14 次本地执行、16 次预设编辑器调用；`ledger-1` 基线 `105.25`、修改后 `85.15`。这不是模型 Benchmark 或用户掌握证据。
- 工程分析：`k=1` 每模式只有一个 final，源码走 trivial selection；预设 `DemoProposer` 不是 LLM；本地 `delivered()` 仅检查 `answer.txt` 存在，不能等同独立 evaluator 判分。详细替代方案、故障与权衡待逐节教学。
- 理解检查/用户回答：尚无独立技术回答；最近一次考核：未考；等级：`U`。
- 错误/未掌握：没有用户技术错误证据；概念、源码、执行和设计均待独立验证。
- 基础补课（2026-10-30）：用户主动询问 `Trajectory` 和 `CSV` 的含义，说明此前解释默认了尚未建立的数据格式与轨迹概念；这不是答题错误。已核对真实 `ledger-1/ledger.csv` 与基线/修改后 `trajectory.md`，本轮从这两个文件及 `csv.DictReader`、`DemoAdapter.execute()` 的写入代码补讲。用户掌握仍为 `U`，待独立解释验证。
- 下一补课/小节：待用户确认代码贯穿的整体 Demo 讲解可理解后，再单独深入 `harness2-demo` 入口与 `argparse` 的真实调用、异常与参数变式。

## Stage 00 · CSV 与简化 Trajectory（基础子知识点）

- 官方 SHA/源码：`1cfe254e…`；`upstream/harness2/harness2/demo.py:30–37` 的 CSV 读取，以及 `DemoAdapter.execute():86–105` 的答案与轨迹写入。
- 已教学：真实 `ledger-1/ledger.csv` 是输入表；`csv.DictReader` 将 `amount` 列读成字典；`answer.txt` 存 stdout；这个 Demo 的 `trajectory.md` 用固定 `[ACTION]`/`[OBSERVATION]` 模板记录一次执行，不是完整 LLM Agent Trace。
- 真实演示：`experiments/raw_runs/stage00_demo_k1/sources/ledger-1/ledger.csv`、`executions/demo-oc-agg1/ledger-1/base1/trajectory.md` 与 `agg1/trajectory.md` 均已核对。
- 用户原回答（2026-10-30，非正式理解检查）：CSV“属于输入”；执行后“到 answer.txt 中查看”；“Trajectory 中记录了执行过程”。三点正确。未独立解释 `csv.DictReader`、`subprocess` 或轨迹写入代码。
- 错误/补课：此题未见错误；下一步补“脚本版本如何复制、修改、验证和执行”的代码链路。该基础子知识点暂记 `L1`（仅概念），整条 Demo 与正式 Gate 仍未评估。

## Stage 00 · Demo 脚本版本替换与校验（子知识点）

- 官方 SHA/源码：`1cfe254e…`；`core/context.py:build` 复制可编辑工作副本；`core/recursion.py:_run_stage/_accept_tree/_roll` 提议、校验、物化与执行；`harness2/demo.py:DemoProposer.call/DemoAdapter.execute` 执行确定性修改和本地脚本。
- 已教学：ASCII 文件树及 `base → context/inv1/harness → harnesses/inv1 → executions/inv1` 链；相同 CSV 下基线脚本过滤负数得到 `105.25`，候选脚本删除过滤条件得到 `85.15`；组合阶段另行生成 `agg1`，不把它误说成机械复制 `inv1`。
- 真实演示：本地 `experiments/raw_runs/stage00_demo_k1/` 中 `base/`、`context/inv1/harness/`、`harnesses/inv1/`、`harnesses/agg1/` 的 `scripts/summarize.py` 内容和基线/候选 `answer.txt` 已核对；本小节未重新运行 Demo。
- 用户原回答（2026-10-30，非正式理解检查）：对“工作副本修改后校验失败应否直接执行”的回答为“记录错误并回退”。方向正确。补充精确源码边界：`_run_stage()` 最多再尝试一次；仍失败才返回 `fell_back=True` 和错误，未通过校验的工作副本不直接执行。
- 最近结果与等级：该校验边界有一次正确概念回答，暂记 `L1`；完整源码路径和执行过程尚无用户独立复述证据，不升级 L2/L3。正式 Stage 00 Gate 未考。
- 下一补课/任务：单独讲 CLI/`argparse` 的参数进入、转换、校验与退出码，再用新输入做 Trace 分析。

## Stage 00 · Demo CLI 参数与退出码（当前教学小节）

- 官方 SHA/源码：`1cfe254e…`；`upstream/harness2/pyproject.toml:32` 声明 `harness2-demo` 入口；`upstream/harness2/harness2/cli/demo.py:27–58` 的 `main(argv=None) -> int`；`core/schedule.py:48–55` 的 `mode_token()` 与 `:669–733` 的 `run_domain()`。
- 为什么学：看清用户命令如何变成 Python 类型和调度参数，区分参数错误与任务执行错误；联系前节的脚本版本替换与结果文件。
- ASCII/源码教学：本轮按 `命令 → __main__/入口 → parse_args → k 校验 → Path/模式转换 → adapter/proposer → run_domain → demo.json/exit code` 逐段解释。真实代码片段与各值在本轮回复展示；用户独立理解待检查。
- 有效运行证据：之前 `--output /out/raw_runs/stage00_demo_k1 --k 1 --mode both` 在隔离 Docker/Python 3.12 容器退出 0；`demo.json` 记录 2 done、0 failed、14 executions、16 scripted editor calls。参数值由源码解析规则推得，不是 CLI 单独打印出的内部变量。
- 新故障演示（2026-10-30）：同一容器、安全参数和官方源码，执行 `python -m harness2.cli.demo --output /tmp/invalid_k_demo --k 0 --mode both`；真实 stderr 为 `demo.py: error: --k must be positive`，捕获容器进程退出码 `2`。校验位于 `DemoAdapter(root)` 之前，因而此调用未进入任务调度。外层 PowerShell 在打印 `DEMO_EXIT_CODE=2` 后返回 0；二者不可混淆。
- 工程分析：`argparse` 负责类型/choices 与帮助信息，`main()` 补充 `k >= 1` 语义校验；参数错误通过 `parser.error()` 抛出 `SystemExit(2)`，有效任务的汇总结果走 `return int(result["failed"] > 0)`。`--k 0` 是 CLI 参数坏例，不能替代 Stage 00 计划中的错误输出路径/依赖故障注入。
- 用户回答与最近考核：用户要求直接讲解 `--k 1 --mode parallel` 题并进入 Stage 00 下一小节，未独立作答；由源码可推 `k=1`、`modes=("agg",)`、任务由 `adapter.tasks()` 提供，不计分。等级 `U`；正式 Stage 00 Gate 未考。之后用不同参数再检查。

## Stage 00 · DemoAdapter 的任务与执行边界（当前教学小节）

- 官方 SHA/源码：`1cfe254e…`；`upstream/harness2/harness2/demo.py:41–117` 的 `DemoAdapter`；`core/spec.py:200–249` 的 `BenchmarkAdapter` Protocol；调用者 `cli/demo.py:36–47`、`core/schedule.py:465,617,669`。
- 为什么学：Adapter 将通用任务调度与账本 CSV、脚本执行、产物格式隔开；联系前节 CLI 如何创建 Adapter、候选 Harness 如何由 `harness_dir` 切换。
- 已教学准备：本轮会以 ASCII 图解释 `DemoAdapter(root)` 初始化源文件与 base Harness、`tasks/task_prompt/task_files` 提供输入、`execute(task_id,harness_dir,run_id)` 执行、`delivered/trajectory/deliverable_text` 读取产物。`score` 在通用 Protocol 中声明，但 DemoAdapter 没有实现，不能把它说成真实 benchmark judge。
- 独立直接演示（2026-10-30）：隔离 Docker Python 3.12、无网络、官方只读源、输出挂 `experiments/`，直接创建 `DemoAdapter('/out/raw_runs/stage00_adapter_direct')`，`tasks()` 返回 `['ledger-1','ledger-2']`，`task_prompt('ledger-1')` 返回签名求和任务说明；`execute('ledger-1',None,'direct-base')` 的 `answer` 为 `Total: 105.25`，`delivered=True`，Trajectory 含固定 ACTION/OBSERVATION，`execution_count=1`，容器退出码 0。再在 `stage00_adapter_compare` 用同一输入分别执行 `harness_dir=None` 和已有 `harnesses/inv1`：输出 `105.25` 与 `85.15`，`execution_count=2`，容器退出码 0。两个原始输出目录均在忽略的 `experiments/raw_runs/` 下。
- 工程权衡/限制：同一 `execute()` 通过 Harness 路径参数切换脚本，调度器无须读 CSV；Demo 用 `subprocess.run(check=True,timeout=10)` 和简化轨迹，`delivered()` 仅检查文件存在，不代表真值评分。错误时 `execute()` 可能抛异常，调度层记录失败。
- 用户回答与等级：此小节尚无独立回答，`U`；Stage 00 正式 Gate 未考。下次在已教源码上做一题参数与产物 Trace。

## 后续知识点模板

每开始一个新知识点复制以下字段，不预填等级：

- 名称、Stage、官方 SHA/源码：
- 为什么学/与前一知识点关联：
- 架构图、组件边界、数据流：
- 已分段讲解的函数/参数/返回/分支/异常：
- Codex 真实运行命令、退出码、输入/Trace/产物：
- 工程设计、替代方案、故障、成本/可靠性：
- 面试口述示范已讲解：是/否；独立题在作答前不附答案。
- 用户原回答摘要、正确点、错误和复测：
- 最近考核、等级（默认 U）、下一补课：
