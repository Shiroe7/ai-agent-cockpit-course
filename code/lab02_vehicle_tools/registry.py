from __future__ import annotations

from common.tools import ToolRegistry, ToolSpec

from .tools import VehicleDataStore


def build_registry(store: VehicleDataStore | None = None) -> ToolRegistry:
    store = store or VehicleDataStore()
    registry = ToolRegistry()
    vehicle_schema = {
        "type": "object",
        "properties": {
            "vehicle_id": {
                "type": "string",
                "description": "课程模拟车辆编号，例如 CQ-AI-001",
            }
        },
        "required": ["vehicle_id"],
        "additionalProperties": False,
    }
    registry.register(
        ToolSpec(
            "get_vehicle_status",
            "查询车辆在线状态、电量、续航、座舱温度和告警。",
            vehicle_schema,
            store.get_vehicle_status,
        )
    )
    registry.register(
        ToolSpec(
            "get_energy_summary",
            "查询车辆电量、预计续航和百公里能耗。",
            vehicle_schema,
            store.get_energy_summary,
        )
    )
    registry.register(
        ToolSpec(
            "get_tire_pressure",
            "查询四个轮胎的胎压并标记低压位置。",
            vehicle_schema,
            store.get_tire_pressure,
        )
    )
    registry.register(
        ToolSpec(
            "explain_fault_code",
            "解释课程模拟故障码的含义、等级和处理建议。",
            {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "故障码，例如 BMS_102 或 TPMS_201",
                    }
                },
                "required": ["code"],
                "additionalProperties": False,
            },
            store.explain_fault_code,
        )
    )
    return registry
