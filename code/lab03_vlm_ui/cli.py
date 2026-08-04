from __future__ import annotations

import json
from pathlib import Path

from .agent import CockpitUIAgent


def main() -> None:
    agent = CockpitUIAgent()
    image_path = Path(__file__).parent / "assets" / "sample_cockpit.svg"
    print("座舱 UI 安全模拟已启动。输入 exit 退出。")
    print("示例：打开空调、导航回家、切换运动模式。")
    while True:
        instruction = input("指令：").strip()
        if instruction.lower() in {"exit", "quit"}:
            break
        event = agent.simulate(image_path, instruction)
        print(json.dumps(event, ensure_ascii=False, indent=2))
        if event["status"] == "confirmation_required":
            answer = input("该操作需要确认，是否仅做模拟执行？[y/N] ").strip().lower()
            if answer == "y":
                confirmed = agent.simulate(image_path, instruction, confirmed=True)
                print(json.dumps(confirmed, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
