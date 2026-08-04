from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class VehicleDataStore:
    def __init__(self, data_path: str | Path | None = None) -> None:
        path = Path(data_path) if data_path else Path(__file__).parent / "data" / "vehicle_mock.json"
        self.data = json.loads(path.read_text(encoding="utf-8"))

    def _vehicle(self, vehicle_id: str) -> dict[str, Any]:
        try:
            return self.data["vehicles"][vehicle_id]
        except KeyError as exc:
            raise ValueError(f"未找到车辆：{vehicle_id}") from exc

    def get_vehicle_status(self, vehicle_id: str) -> dict[str, Any]:
        vehicle = self._vehicle(vehicle_id)
        return {
            "vehicle_id": vehicle_id,
            "online": vehicle["online"],
            "battery_pct": vehicle["battery_pct"],
            "estimated_range_km": vehicle["estimated_range_km"],
            "cabin_temp_c": vehicle["cabin_temp_c"],
            "warnings": vehicle["warnings"],
        }

    def get_energy_summary(self, vehicle_id: str) -> dict[str, Any]:
        vehicle = self._vehicle(vehicle_id)
        return {
            "vehicle_id": vehicle_id,
            "battery_pct": vehicle["battery_pct"],
            "estimated_range_km": vehicle["estimated_range_km"],
            "energy_kwh_per_100km": vehicle["energy_kwh_per_100km"],
        }

    def get_tire_pressure(self, vehicle_id: str) -> dict[str, Any]:
        vehicle = self._vehicle(vehicle_id)
        tires = vehicle["tires_kpa"]
        return {
            "vehicle_id": vehicle_id,
            "unit": "kPa",
            "tires": tires,
            "low_pressure_positions": [
                position for position, pressure in tires.items() if pressure < 220
            ],
        }

    def explain_fault_code(self, code: str) -> dict[str, Any]:
        normalized = code.upper()
        try:
            detail = self.data["fault_codes"][normalized]
        except KeyError as exc:
            raise ValueError(f"未知故障码：{normalized}") from exc
        return {"code": normalized, **detail}
