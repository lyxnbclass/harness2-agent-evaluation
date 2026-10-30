# 独立知识掌握记录（与工程进度分开）

此文件按**知识点**记录六步教学和用户独立证据；`learning/MASTERY_MATRIX.md` 只做汇总。等级：`U` 无独立证据；`L1` 理解概念；`L2` 理解源码；`L3` 理解完整执行；`L4` 能分析工程设计与故障；`L5` 能独立应对深入面试。**Codex 讲解、运行或测试通过不自动提高用户等级。**

每项记录：官方 SHA/源码位置、为什么学、架构/数据流、源码讲解、真实演示路径、工程权衡、提问/用户原答摘要/错误、尚未掌握与补课、最近考核与等级。未完成的教学步骤写待讲，不预填掌握。

## Stage 00 · Harness² 概念与官方无模型 Demo

- 官方版本：`1cfe254e8d25b15f37048c3730134686abe60335`。
- 源码位置：`upstream/harness2/README.md` 的项目定义；`pyproject.toml:32`；`harness2/cli/demo.py:main`；`harness2/demo.py:DemoAdapter` / `DemoProposer`；`harness2/core/schedule.py:run_domain` / `run_task`。详细源码教学按小节逐步展开。
- 为什么学：辨认模型、Harness、执行器、调度和评测的边界；正确解释无模型 Demo 能证明什么。
- 架构/数据流：`CLI → DemoAdapter 提供任务和初始 Harness → run_domain/run_task → 本地 Python 执行与预设修改 → 轨迹/答案 → summary.json → demo.json`。正式逐函数教学待继续。
- 已讲内容：过去讲过 CLI 与 Demo 源码数据流；2026-10-30 本次重新组织整体概念教学并加入真实运行结果。用户指出此前讲解深度不足，原 `--k 0` 问题已撤回，不计分。
- 真实演示：2026-10-30 Docker Linux/Python 3.12、无网络、只读源码、无凭证，`--k 1 --mode both` 退出 0；产物在 `experiments/raw_runs/stage00_demo_k1/`（忽略的大型原始运行目录）。`demo.json`：2 个任务 `ok`、0 failed、14 次本地执行、16 次预设编辑器调用；`ledger-1` 基线 `105.25`、修改后 `85.15`。这不是模型 Benchmark 或用户掌握证据。
- 工程分析：`k=1` 每模式只有一个 final，源码走 trivial selection；预设 `DemoProposer` 不是 LLM；本地 `delivered()` 仅检查 `answer.txt` 存在，不能等同独立 evaluator 判分。详细替代方案、故障与权衡待逐节教学。
- 理解检查/用户回答：尚无独立技术回答；最近一次考核：未考；等级：`U`。
- 错误/未掌握：没有用户技术错误证据；概念、源码、执行和设计均待独立验证。
- 下一补课/小节：先完成 Harness² 与无模型 Demo 的整体直观讲解和温和理解检查，再讲 `harness2-demo` 入口与 `argparse` 的真实调用。

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
