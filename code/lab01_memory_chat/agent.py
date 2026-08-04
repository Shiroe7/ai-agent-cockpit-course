from __future__ import annotations

import re
from typing import Any

from .memory import SQLiteConversationMemory


class MemoryChatAgent:
    """Deterministic teaching agent that makes memory behavior observable."""

    FACT_PATTERNS = (
        ("name", re.compile(r"我叫(?P<value>[\u4e00-\u9fffA-Za-z0-9_-]{1,20})")),
        ("preference", re.compile(r"我喜欢(?P<value>[^，。！？\n]{1,40})")),
        (
            "temperature",
            re.compile(r"(?:座舱|空调).*?(?:偏好|设为|设置为)?(?P<value>\d{2})\s*度"),
        ),
    )

    def __init__(self, memory: SQLiteConversationMemory) -> None:
        self.memory = memory

    def respond(self, session_id: str, user_text: str) -> dict[str, Any]:
        if not session_id.strip():
            raise ValueError("session_id 不能为空")
        if not user_text.strip():
            raise ValueError("输入不能为空")

        self.memory.add_message(session_id, "user", user_text)
        changed: dict[str, str] = {}
        is_question = any(mark in user_text for mark in ("什么", "多少", "吗", "？", "?"))
        if not is_question:
            for key, pattern in self.FACT_PATTERNS:
                match = pattern.search(user_text)
                if match:
                    value = match.group("value").strip(" ，。！？")
                    self.memory.upsert_fact(session_id, key, value)
                    changed[key] = value

        facts = self.memory.facts(session_id)
        answer = self._answer(user_text, facts, changed)
        self.memory.add_message(session_id, "assistant", answer)
        return {
            "session_id": session_id,
            "answer": answer,
            "facts": facts,
            "history": self.memory.history(session_id),
        }

    @staticmethod
    def _answer(
        user_text: str,
        facts: dict[str, str],
        changed: dict[str, str],
    ) -> str:
        if "我叫什么" in user_text or "我的名字" in user_text:
            return (
                f"你之前告诉我，你叫{facts['name']}。"
                if "name" in facts
                else "当前会话中还没有记录你的名字。"
            )
        if "我喜欢什么" in user_text or "我的偏好" in user_text:
            return (
                f"当前记录的偏好是：{facts['preference']}。"
                if "preference" in facts
                else "当前会话中还没有记录偏好。"
            )
        if "温度偏好" in user_text or "几度" in user_text:
            return (
                f"当前记录的座舱温度偏好是 {facts['temperature']} 度。"
                if "temperature" in facts
                else "当前会话中还没有记录座舱温度偏好。"
            )
        if changed:
            labels = {
                "name": "姓名",
                "preference": "偏好",
                "temperature": "座舱温度",
            }
            summary = "；".join(f"{labels[key]}={value}" for key, value in changed.items())
            return f"已写入当前会话记忆：{summary}。"
        return "我已记录本轮对话。你可以继续补充信息，或询问我刚才记住了什么。"
