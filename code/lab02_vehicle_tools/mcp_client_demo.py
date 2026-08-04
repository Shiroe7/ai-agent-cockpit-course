from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run(vehicle_id: str) -> None:
    code_dir = Path(__file__).resolve().parents[1]
    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "lab02_vehicle_tools.mcp_server"],
        cwd=code_dir,
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("MCP 工具：", ", ".join(tool.name for tool in tools.tools))

            result = await session.call_tool(
                "get_vehicle_status",
                {"vehicle_id": vehicle_id},
            )
            print("调用结果：")
            if result.structuredContent is not None:
                print(json.dumps(result.structuredContent, ensure_ascii=False, indent=2))
            else:
                for item in result.content:
                    text = getattr(item, "text", None)
                    print(text if text is not None else item.model_dump_json(indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="最小 MCP 客户端演示")
    parser.add_argument("--vehicle", default="CQ-AI-001", help="课程模拟车辆编号")
    args = parser.parse_args()
    asyncio.run(run(args.vehicle))


if __name__ == "__main__":
    main()