from __future__ import annotations

from .tools import VehicleDataStore


def build_server():
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError(
            "尚未安装可选 MCP SDK。请运行：pip install -r requirements-optional.txt"
        ) from exc

    store = VehicleDataStore()
    server = FastMCP("vehicle-data-lab", json_response=True)

    @server.tool()
    def get_vehicle_status(vehicle_id: str) -> dict:
        """查询课程模拟车辆的综合状态。"""
        return store.get_vehicle_status(vehicle_id)

    @server.tool()
    def get_energy_summary(vehicle_id: str) -> dict:
        """查询课程模拟车辆的电量、续航和能耗。"""
        return store.get_energy_summary(vehicle_id)

    @server.tool()
    def get_tire_pressure(vehicle_id: str) -> dict:
        """查询课程模拟车辆的胎压。"""
        return store.get_tire_pressure(vehicle_id)

    @server.tool()
    def explain_fault_code(code: str) -> dict:
        """解释课程模拟故障码。"""
        return store.explain_fault_code(code)

    return server


def main() -> None:
    build_server().run()


if __name__ == "__main__":
    main()
