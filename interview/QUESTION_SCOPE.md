# 面试考核题库范围（只列主题，不预填答案）

每个 Stage 面试官须根据实际写过的代码、这次发现的错误、最近两次掌握状态，动态生成 ≥5 个新题，并设置至少 2 个追问、1 个现场代码或 Trace 题。题目必须先问用户，不得把标准答案和评分同时展示。

1. Runtime / Harness / Agent Loop / Tool schema：让用户画出调用路径，解释失败处理。
2. Dataset / metrics：给出 solved / failed / unscored / infra_error 的一组新数字，让用户手算并讲分母。
3. Trajectory / Bad Case：给一条实际 trace，问哪个步骤第一次偏离、证据是什么。
4. LLM Judge：针对 Judge 错判、位置偏差、rubric 泄漏设计校准。
5. PPC/Reflection：看官方源码实际执行与改动采纳决策，不可只背名词。
6. SWE-bench 原生评测：随机选一项任务解释 issue/repo/base commit/patch/test/verdict。
7. Adapter：现场解释 map 过程，修复一个故障（空 Patch / commit 冲突 / 超时）。
8. Regression：给 before/after 每任务结果，找新增失败和真实代价。
9. Memory：举出过时、冲突和恶意信息，解释何时不采用。
10. 贡献归属：为什么做这项改动、哪些代码由 Codex 编写、用户独立完成了哪些设计/审查/验收、证据和已知限制。

每次 Gate 评分按 `MASTER_PLAN.md` 40/35/15/10 标准，记录在 `learning/gates/NN.md`。题型要变，不允许简单复制题库拿满分。
