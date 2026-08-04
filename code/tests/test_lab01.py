import tempfile
import unittest
from pathlib import Path

from lab01_memory_chat.agent import MemoryChatAgent
from lab01_memory_chat.memory import SQLiteConversationMemory


class MemoryChatTests(unittest.TestCase):
    def test_persistence_and_session_isolation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "memory.sqlite3"
            agent = MemoryChatAgent(SQLiteConversationMemory(path))
            agent.respond("s1", "我叫小刘")
            self.assertIn("小刘", agent.respond("s1", "我叫什么？")["answer"])

            new_agent = MemoryChatAgent(SQLiteConversationMemory(path))
            self.assertIn("小刘", new_agent.respond("s1", "我的名字是什么？")["answer"])
            self.assertIn("还没有记录", new_agent.respond("s2", "我叫什么？")["answer"])

    def test_fact_update(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            agent = MemoryChatAgent(
                SQLiteConversationMemory(Path(directory) / "memory.sqlite3")
            )
            agent.respond("s1", "我喜欢安静的座舱")
            agent.respond("s1", "我喜欢轻音乐")
            self.assertIn("轻音乐", agent.respond("s1", "我喜欢什么？")["answer"])


if __name__ == "__main__":
    unittest.main()
