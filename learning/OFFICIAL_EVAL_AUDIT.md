# 官方 Harness² 评测系统源码审计（不可凭猜测填写）

> 初始状态：**NOT_VERIFIED**。这里是学习时逐步核实的模板，不是已经验证的结论。
> 依赖：先克隆官方仓库到 `upstream/harness2`，记录 commit SHA；不同版本/CLI 功能可能不同。

## 1. 元数据
- 官方 repo：`https://github.com/google-research/harness2`
- 本地 checkout 路径：NOT_CLONED
- commit SHA：UNKNOWN
- 日期 / 操作人：未开始
- 官方 README/文档版本：UNKNOWN

## 2. 能力审计矩阵

| 模块 | 状态 VERIFIED/UNKNOWN/NOT_FOUND | 真实路径/函数或 CLI | 输入/输出格式 | 单测路径 | 运行证据 | 与自研模块的边界 |
|---|---|---|---|---|---|---|
| Task runner | UNKNOWN | | | | | 负责执行原生任务 |
| Benchmark evaluator / judge | UNKNOWN | | | | | 官方/原生 verdict 优先 |
| Baseline/base judge | UNKNOWN | | | | | 自研负责逐任务比较 |
| Report generation | UNKNOWN | | | | | 自研跨版本+回归报告 |
| Trajectory artifact/log | UNKNOWN | | | | | 自研 trace validator |
| Official unit/integration tests | UNKNOWN | | | | | 与个人 regression suite 不同 |
| Failure diagnostics | UNKNOWN | | | | | 自研 Bad Case 库 |
| Automatic regression rejection | UNKNOWN | | | | | 若官方已实现，先复用/扩展 |

## 3. 源码定位证据
- 运行的命令（原样复制）：
- 退出码与日志路径：
- `commit SHA:path:function`：
- 一条任务的 `task_id → run_id → trajectory → verdict → report` 实际数据链：
- 哪些功能不必重写：
- 哪些功能是个人原创扩展：

## 4. 必须解释给面试官的问题
1. 哪个组件真正决定 `resolved/failed`？由哪项程序化证据支持？
2. `base` 与 `optimized` 的结果如何对齐同一个 task_id？
3. 官方 unit tests 和对 Agent 能力的 regression evaluation 有何区别？
4. 候选 Harness 在线行为比较与最终公开 Benchmark 的 judge 有何区别？
5. 如何避免将官方原有模块描述为自己的开发成果？
