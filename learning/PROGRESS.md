# 学习进度 — 唯一的人类可读当前状态

> 最后更新：2026-10-29（Stage 00 首次环境盘点）
> 操作纪律：**凡是“完成”必须有命令输出/代码路径/测试记录**。下一会话先读此文件。

- 当前阶段：00
- 当前阶段标题：开发环境、仓库溯源与官方 Demo
- 状态：IN_PROGRESS（仅完成首轮离线盘点，未运行官方 Demo）
- 官方 Harness² commit：UNKNOWN（尚未克隆/验证）
- 公开 Coding Benchmark：未选定（默认优先 SWE-bench，Stage 08 正式决策）
- 已验证完成的阶段：无
- 已验证的项目代码/实验：无
- 最近一次考核：尚未开始
- 已掌握的知识点（有无提示考核证据）：尚未评估
- 尚未掌握/待验证的知识点：全部待初测
- 阻塞：当前目录没有 `.git`，`upstream/harness2/` 不存在；`gh auth status` 报登录凭证无效。GitHub 仓库名称与可见性待用户确认；官方源码克隆尚未获本轮授权。
- 用户明确批准下一阶段：否
- GitHub：branch `NONE`；重要 commit `NONE`；remote `NONE`；PR `NONE`；当前 Stage 考核 `未考`。

## 当前唯一下一步
用户亲手完成 Stage 00 第一小节的环境检查小练习，并回答两个无提示诊断问题；Codex 根据回答复核。**不要直接运行收费模型或跳到 Stage 01**。

## 最近期真实证据
- `python scripts/resume.py` 与 `python scripts/check_workspace.py` 均退出 0；后者只说明记录完整性检查通过，不代表知识掌握。
- Windows 环境：Python 3.14.6、Git 2.41.0、uv 0.12.18、Docker CLI 29.8.0、Node v24.15.0；Docker 配置访问警告、WSL 状态查询被拒绝，运行能力仍待验证。
- 本工作区只有计划、规格、模板与离线校验脚本；**未克隆官方源码，未运行 Demo/Benchmark，未测出任何性能提升**。

## 对下个新会话的提醒
1. 运行 `python scripts/resume.py`，读取当前阶段 Gate 文件、错误记录与知识矩阵。
2. 在实际证据出现前不要改写上述“尚未完成”状态。
3. 本轮结束更新此文件、`stage_status.json`、`SESSION_LOG.md`、相应 Gate 文件，并运行 `python scripts/check_workspace.py`。
