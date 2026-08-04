from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from common.tools import JsonlAuditLog

from .models import UIAction
from .vlm_adapter import MockVLM


class CockpitUIAgent:
    """VLM -> contract validation -> policy gate -> simulated executor."""

    def __init__(
        self,
        vlm: Any | None = None,
        ui_path: str | Path | None = None,
        audit_path: str | Path = Path("runtime") / "lab03_ui_actions.jsonl",
    ) -> None:
        path = Path(ui_path) if ui_path else Path(__file__).parent / "data" / "sample_ui.json"
        ui = json.loads(path.read_text(encoding="utf-8"))
        self.elements = {element["id"]: element for element in ui["elements"]}
        self.vlm = vlm or MockVLM(path)
        self.audit = JsonlAuditLog(audit_path)

    def plan(self, image_path: str | Path, instruction: str) -> UIAction:
        return self.vlm.analyze(image_path, instruction)

    def validate(self, plan: UIAction) -> tuple[bool, str]:
        if plan.action == "none" or plan.target_id not in self.elements:
            return False, "未识别到受信任的可操作控件"
        element = self.elements[plan.target_id]
        if plan.action not in element["allowed_actions"]:
            return False, f"动作 {plan.action} 不在控件允许列表中"
        if plan.bounds != element["bounds"]:
            return False, "控件坐标与受信任 UI 清单不一致"
        if plan.confidence < 0.75:
            return False, "识别置信度低于 0.75"
        if element["critical"] and not plan.requires_confirmation:
            return False, "高风险控件必须声明需要人工确认"
        return True, "验证通过"

    def simulate(
        self,
        image_path: str | Path,
        instruction: str,
        confirmed: bool = False,
    ) -> dict[str, Any]:
        plan = self.plan(image_path, instruction)
        valid, validation_message = self.validate(plan)
        if not valid:
            status = "refused"
        elif plan.requires_confirmation and not confirmed:
            status = "confirmation_required"
        else:
            status = "simulated"

        event = {
            "instruction": instruction,
            "status": status,
            "validation": validation_message,
            "plan": plan.to_dict(),
            "note": "教学模拟：未向真实车辆或真实 UI 发送操作。",
        }
        self.audit.append(event)
        return event
