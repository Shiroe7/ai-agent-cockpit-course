import tempfile
import unittest
from pathlib import Path

from lab02_vehicle_tools.agent import VehicleToolAgent
from lab02_vehicle_tools.registry import build_registry


class VehicleToolTests(unittest.TestCase):
    def test_tire_tool_selection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            agent = VehicleToolAgent(
                audit_path=Path(directory) / "audit.jsonl"
            )
            event = agent.run("查询 CQ-AI-002 的胎压")
            self.assertEqual(event["status"], "success")
            self.assertEqual(event["plan"]["tool_name"], "get_tire_pressure")
            self.assertIn(
                "rear_left",
                event["result"]["data"]["low_pressure_positions"],
            )

    def test_schema_rejects_missing_parameter(self) -> None:
        result = build_registry().invoke("get_vehicle_status", {})
        self.assertFalse(result.ok)
        self.assertIn("缺少必填参数", result.error or "")

    def test_unknown_vehicle_is_safe_error(self) -> None:
        result = build_registry().invoke(
            "get_vehicle_status",
            {"vehicle_id": "CQ-AI-999"},
        )
        self.assertFalse(result.ok)
        self.assertIn("未找到车辆", result.error or "")


if __name__ == "__main__":
    unittest.main()
