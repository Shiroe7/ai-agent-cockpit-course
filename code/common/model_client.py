from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Protocol


class ModelClient(Protocol):
    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        ...


@dataclass
class OpenAICompatibleClient:
    """Minimal standard-library client for OpenAI-compatible endpoints."""

    api_key: str
    base_url: str
    model: str
    timeout_seconds: int = 30

    @classmethod
    def from_env(cls, model_env: str = "CHAT_MODEL") -> "OpenAICompatibleClient":
        missing = [
            key
            for key in ("OPENAI_API_KEY", "OPENAI_BASE_URL", model_env)
            if not os.getenv(key)
        ]
        if missing:
            raise RuntimeError(f"缺少环境变量：{', '.join(missing)}")
        return cls(
            api_key=os.environ["OPENAI_API_KEY"],
            base_url=os.environ["OPENAI_BASE_URL"],
            model=os.environ[model_env],
            timeout_seconds=int(os.getenv("AGENT_TIMEOUT_SECONDS", "30")),
        )

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
        }
        if tools:
            payload["tools"] = tools

        request = urllib.request.Request(
            f"{self.base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"模型接口返回 HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"无法连接模型接口：{exc.reason}") from exc

        try:
            return body["choices"][0]["message"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"模型响应结构不符合预期：{body}") from exc
