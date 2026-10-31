# 学习进度 — 当前状态

> 更新：2026-10-31。完成教学规范重构；阶段编号与既有工程证据保留。历史会话见 `learning/SESSION_LOG.md`，Stage 00 运行细节见 `learning/stages/00.md`。

- 当前阶段：00
- 当前章节：官方无模型 Demo 的完整执行链路
- 状态：IN_PROGRESS
- 已讲解：CSV/Trajectory、候选脚本校验、CLI 参数、DemoAdapter、Scheduler、parallel/sequential、选择与经验传递；本轮按新七部分结构系统重讲完整链路。
- 已确认理解：用户独立区分 CSV 输入、`answer.txt` 输出、Trajectory 过程；能解释 `task_id` 选任务数据、`harness_dir` 选脚本、`run_id` 决定产物目录，以及基线漏算负数。此证据只覆盖局部，不代表整章已确认理解。
- 仍有疑问/待确认：完整调用与数据流、`k=1` 的选择时序、异常与产物关系、Demo 状态和真实 Benchmark 评分边界。新章节思考题尚待用户回答。
- 实际代码与测试：官方子模块固定在 `1cfe254e8d25b15f37048c3730134686abe60335`，未修改上游。2026-10-30 隔离 Docker Python 3.12、无网络的 Demo `--k 1 --mode both` 退出 0，`demo.json` 为 2 done / 0 failed / 14 executions / 16 scripted editor calls；ledger-1 基线 105.25、两个 final 均 85.15。DemoAdapter 直接调用和 CLI `--k 0` 故障、超时故障均有记录。原始产物在忽略目录 `experiments/raw_runs/`，摘要见 `learning/stages/00.md`。无付费模型或真实 Benchmark 结果；自研评测模块尚未实现。
- 工程待办：Stage 00 计划中的自研代码与必要测试仍未完成；阶段完成 PR 尚未创建。官方评测审计后续继续，未知项保持 UNKNOWN。
- GitHub：`stage-00-setup`，追踪 `origin/stage-00-setup`；本轮开始时 HEAD `039dc45`，教学重构提交 `e53e417` 已 Push。其余既存未提交改动保留。`gh auth status` 有效；`gh pr list --head stage-00-setup --state all` 返回 `[]`。PR：NONE。用户尚未批准进入 Stage 01。
- 阻塞：本机默认 Python 3.14.6 不满足上游 `<3.14`，已用 Docker Python 3.12 完成无模型 Demo。真实模型调用未经批准，成本 UNKNOWN。
- 下次内容：等待用户集中回答本章思考题，针对性反馈；随后在 Stage 00 内完成剩余工程证据与阶段验收。

## 证据边界

`demo.json` 的 `ok` 是官方本地演示的工作流状态，不是独立 Coding Benchmark 的 solved 或模型通过率。已有讲解和 Codex 执行成功不能自动写成用户理解。历史记录中出现的 L1、旧 Gate、未运行 Demo 等说法仅反映当时状态，以较新的实际产物和本页当前状态为准。
