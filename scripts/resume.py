#!/usr/bin/env python3
"""离线显示下一次 Codex 会话必须读取的真实本地进度；不调用模型/网络。"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    state_path = ROOT / "learning/stage_status.json"
    progress_path = ROOT / "learning/PROGRESS.md"
    if not state_path.exists() or not progress_path.exists():
        print("[ERROR] 状态文件缺失，请检查工作区是否完整。")
        return 1
    data = json.loads(state_path.read_text(encoding="utf-8"))
    sid = data.get("current_stage")
    stage = data.get("stages", {}).get(sid)
    if not stage:
        print("[ERROR] 当前阶段无效：", sid)
        return 1
    print(f"当前阶段：{sid} | {stage['status']}")
    print("状态更新时间：", data.get("last_updated"))
    print("用户明确允许进入下一阶段：", stage.get("user_approved_next"))
    print("\n必读文件：")
    for rel in [
        "AGENTS.md", "MASTER_PLAN.md", "learning/PROGRESS.md",
        "learning/MASTERY_MATRIX.md", "learning/MISTAKES.md", "learning/SESSION_LOG.md",
        f"learning/stages/{sid}.md", f"learning/gates/{sid}.md",
    ]:
        print(" -", rel, "[存在]" if (ROOT/rel).is_file() else "[缺失]")
    print("\n进度摘要（以真实证据为准）：")
    lines = progress_path.read_text(encoding="utf-8").splitlines()
    for line in lines:
        if line.startswith(("- 当前阶段：", "- 当前阶段标题：", "- 状态：", "- 最近一次考核：", "- 阻塞：")):
            print(line)
    print("\n提示：新会话应先复习上次薄弱项；如果是 PASSED_AWAITING_USER，必须等待用户明确批准后才能推进。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
