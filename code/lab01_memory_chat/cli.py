from __future__ import annotations

import argparse
from pathlib import Path

from .agent import MemoryChatAgent
from .memory import SQLiteConversationMemory


def main() -> None:
    parser = argparse.ArgumentParser(description="多轮对话记忆实验")
    parser.add_argument("--session", default="demo", help="会话 ID")
    parser.add_argument(
        "--db",
        default=str(Path("runtime") / "lab01_memory.sqlite3"),
        help="SQLite 文件路径",
    )
    args = parser.parse_args()

    agent = MemoryChatAgent(SQLiteConversationMemory(args.db))
    print(f"会话 {args.session} 已启动。输入 exit 退出，输入 clear 清空当前会话。")
    while True:
        text = input("你：").strip()
        if text.lower() in {"exit", "quit"}:
            break
        if text.lower() == "clear":
            agent.memory.clear(args.session)
            print("系统：当前会话已清空。")
            continue
        try:
            result = agent.respond(args.session, text)
            print(f"智能体：{result['answer']}")
        except ValueError as exc:
            print(f"系统：{exc}")


if __name__ == "__main__":
    main()
