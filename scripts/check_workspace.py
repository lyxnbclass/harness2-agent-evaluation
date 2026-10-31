#!/usr/bin/env python3
"""静态检查：文件、阶段状态与跨会话记录；不执行 Benchmark。"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
ALLOWED = {
    "LOCKED", "NOT_STARTED", "IN_PROGRESS", "BLOCKED",
    "READY_FOR_GATE", "PASSED_AWAITING_USER", "COMPLETED",
}
MANDATORY = [
    "AGENTS.md", "START_HERE.md", "MASTER_PLAN.md", "CODEX_START_PROMPT.md",
    "learning/PROGRESS.md", "learning/stage_status.json", "learning/KNOWLEDGE_MASTERY.md",
    "learning/MASTERY_MATRIX.md",
    "learning/SESSION_LOG.md", "learning/MISTAKES.md", "learning/SOURCE_INDEX.md",
]


def check() -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    for rel in MANDATORY:
        if not (ROOT / rel).is_file():
            errors.append(f"缺少必需文件：{rel}")
    path = ROOT / "learning/stage_status.json"
    if not path.is_file():
        return errors, warnings
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as ex:
        errors.append(f"无效 JSON：{ex}")
        return errors, warnings
    current = data.get("current_stage")
    stages = data.get("stages", {})
    if data.get("schema_version") != "4.0":
        errors.append("stage_status.json 需使用简化的 4.0 schema")
    required_ids = [f"{i:02}" for i in range(14)]
    if current not in required_ids:
        errors.append(f"current_stage 无效：{current}")
    for sid in required_ids:
        info = stages.get(sid)
        if not isinstance(info, dict):
            errors.append(f"没有阶段状态：{sid}")
            continue
        status = info.get("status")
        if status not in ALLOWED:
            errors.append(f"Stage {sid}: 无效 status={status}")
        for rel in (f"learning/stages/{sid}.md",):
            if not (ROOT / rel).is_file():
                errors.append(f"缺少阶段记录：{rel}")
        if status == "COMPLETED" and info.get("user_approved_next") is not True:
            errors.append(f"Stage {sid}: 未记录用户批准，却标为 COMPLETED")
        if current in required_ids and int(sid) < int(current) and status != "COMPLETED":
            errors.append(f"Stage {sid}: 当前已推进到 {current}，但上一阶段未完成")
        if current in required_ids and int(sid) > int(current) and status != "LOCKED":
            errors.append(f"Stage {sid}: 未来阶段没有锁定")
    if current in required_ids:
        progress = (ROOT / "learning/PROGRESS.md").read_text(encoding="utf-8") if (ROOT / "learning/PROGRESS.md").is_file() else ""
        expected = f"- 当前阶段：{current}"
        if expected not in progress:
            errors.append("PROGRESS.md 当前阶段与 JSON 不一致")
        current_status = stages.get(current, {}).get("status")
        if current_status and f"- 状态：{current_status}" not in progress:
            errors.append("PROGRESS.md 当前状态与 JSON 不一致")
    if not errors:
        warnings.append("静态检查通过不代表工程已复现或用户已理解；仍须核对真实代码、运行产物与用户反馈。")
    return errors, warnings


def main() -> int:
    errors, warnings = check()
    for err in errors:
        print("[ERROR]", err)
    for w in warnings:
        print("[INFO]", w)
    if errors:
        print(f"检查未通过：{len(errors)} 个问题")
        return 1
    print("工作区文件与阶段状态检查通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
