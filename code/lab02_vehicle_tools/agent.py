from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from common.tools import JsonlAuditLog, ToolRegistry

from .registry import build_registry


class VehicleToolAgent:
    """Observable tool-selection loop for teaching and offline testing."""

    VEHICLE_PATTERN = re.compile(r"CQ-AI-\d{3}", re.IGNORECASE)
    CODE_PATTERN = re.compile(r"[A-Z]{2,8}_\d{3}", re.IGNORECASE)

    def __init__(
        self,
        registry: ToolRegistry | None = None,
        audit_path: str | Path = Path("runtime") / "lab02_tool_calls.jsonl",
    ) -> None:
        self.registry = registry or build_registry()
        self.audit = JsonlAuditLog(audit_path)

    def plan(self, query: str, default_vehicle_id: str | None = None) -> dict[str, Any]:
        vehicle_match = self.VEHICLE_PATTERN.search(query)
        vehicle_id = (
            vehicle_match.group(0).upper()
            if vehicle_match
            else default_vehicle_id
        )

        if "故障" in query or self.CODE_PATTERN.search(query):
            code_match = self.CODE_PATTERN.search(query)
            if not code_match:
                raise ValueError("请提供要解释的故障码")
            return {
                "tool_name": "explain_fault_code",
                "arguments": {"code": code_match.group(0).upper()},
                "reason": "问题要求解释故障码",
            }

        if not vehicle_id:
            raise ValueError("请提供车辆编号，例如 CQ-AI-001")
        if "胎压" in query or "轮胎" in query:
            tool_name = "get_tire_pressure"
            reason = "问题涉及轮胎或胎压"
        elif any(keyword in query for keyword in ("电量", "续航", "能耗", "电池")):
            tool_name = "get_energy_summary"
            reason = "问题涉及车辆能源状态"
        else:
            tool_name = "get_vehicle_status"
            reason = "使用综合状态工具回答一般车辆状态问题"
        return {
            "tool_name": tool_name,
            "arguments": {"vehicle_id": vehicle_id.upper()},
            "reason": reason,
        }

    def run(self, query: str, default_vehicle_id: str | None = None) -> dict[str, Any]:
        try:
            plan = self.plan(query, default_vehicle_id)
        except ValueError as exc:
            event = {"query": query, "status": "planning_error", "error": str(exc)}
            self.audit.append(event)
            return event

        result = self.registry.invoke(plan["tool_name"], plan["arguments"])
        event = {
            "query": query,
            "status": "success" if result.ok else "tool_error",
            "plan": plan,
            "result": result.to_dict(),
        }
        self.audit.append(event)
        return event
