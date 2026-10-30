# 错题与误区追踪（追加日志）

> 初始为空。禁止预填“你已经掌握”或“已纠正”。回答中错误要被记录，但不能通过记录敏感资料来证明学习。

| 日期 | Stage/题号 | 我的原回答摘要 | 错在哪里 | 正确推理要点 | 变式复测问题 | 复测结果 | 证据链接 |
|---|---|---|---|---|---|---|---|
| 2026-10-30 | 00 / DemoAdapter 路径理解检查 | “选择一开始错误的脚本，读取一开始的CSV。answer.txt” | 前两点正确；第三点仅说文件名，未指出 `run_id='trial-a'` 决定 `executions/trial-a/` 目录 | `run_dir = self.root / 'executions' / run_id`；答案路径为 `run_dir / 'answer.txt'`；`task_id` 选 CSV，`harness_dir` 选脚本 | 将 `task_id` 换为 `ledger-2`、`run_id` 换为 `review-b`，指出脚本、CSV、产物目录 | 待答，不计正式 Gate | `upstream/harness2/harness2/demo.py:76–105`；`learning/KNOWLEDGE_MASTERY.md` |

## 复习要求
- 每个新会话：先抽查上一会话最弱 1–2 项；过往未过关概念必须重新追问。
- 不提前提供答案；新变式复测不是复述刚看到的答案。
- 复测未过不得将对应能力标为 L3/L4，也不能把该 Stage 评为 PASS。
