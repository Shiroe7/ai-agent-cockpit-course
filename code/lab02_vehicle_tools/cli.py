from __future__ import annotations

import argparse
import json

from .agent import VehicleToolAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="车辆数据工具调用实验")
    parser.add_argument("--vehicle", default="CQ-AI-001", help="默认课程模拟车辆编号")
    args = parser.parse_args()
    agent = VehicleToolAgent()
    print("可询问车辆状态、电量/续航、胎压或故障码。输入 exit 退出。")
    while True:
        query = input("你：").strip()
        if query.lower() in {"exit", "quit"}:
            break
        event = agent.run(query, args.vehicle)
        print(json.dumps(event, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
