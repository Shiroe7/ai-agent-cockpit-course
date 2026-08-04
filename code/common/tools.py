from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


class ToolValidationError(ValueError):
    """Raised when a tool call does not satisfy its input contract."""


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[..., Any]

    def public_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_schema,
            },
        }


@dataclass(frozen=True)
class ToolResult:
    ok: bool
    tool_name: str
    data: Any = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ToolRegistry:
    """Small, dependency-free registry used to teach tool contracts."""

    _TYPE_MAP = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "object": dict,
        "array": list,
    }

    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        if spec.name in self._tools:
            raise ValueError(f"工具已注册：{spec.name}")
        self._tools[spec.name] = spec

    def schemas(self) -> list[dict[str, Any]]:
        return [spec.public_schema() for spec in self._tools.values()]

    def invoke(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        spec = self._tools.get(name)
        if spec is None:
            return ToolResult(False, name, error=f"未知工具：{name}")
        try:
            self._validate(spec.input_schema, arguments)
            return ToolResult(True, name, data=spec.handler(**arguments))
        except (ToolValidationError, KeyError, ValueError) as exc:
            return ToolResult(False, name, error=str(exc))
        except Exception as exc:  # defensive boundary around external tools
            return ToolResult(False, name, error=f"工具执行失败：{type(exc).__name__}: {exc}")

    @classmethod
    def _validate(cls, schema: dict[str, Any], arguments: dict[str, Any]) -> None:
        if not isinstance(arguments, dict):
            raise ToolValidationError("工具参数必须是 JSON 对象")

        properties = schema.get("properties", {})
        required = schema.get("required", [])
        missing = [key for key in required if key not in arguments]
        if missing:
            raise ToolValidationError(f"缺少必填参数：{', '.join(missing)}")

        if schema.get("additionalProperties") is False:
            extra = sorted(set(arguments) - set(properties))
            if extra:
                raise ToolValidationError(f"存在未声明参数：{', '.join(extra)}")

        for key, value in arguments.items():
            expected_name = properties.get(key, {}).get("type")
            expected_type = cls._TYPE_MAP.get(expected_name)
            if expected_type and not isinstance(value, expected_type):
                raise ToolValidationError(
                    f"参数 {key} 类型错误：需要 {expected_name}，实际为 {type(value).__name__}"
                )


class JsonlAuditLog:
    """Append-only JSONL log for traceability and grading evidence."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: dict[str, Any]) -> None:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **event,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    def read_all(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return [
            json.loads(line)
            for line in self.path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
