"""
Spawns the Curiosity Break MCP server as a subprocess and talks to it over stdio.

Run (from this folder):
    uv run python demo_client.py

That shows tools + sample outputs. Running `python server.py` alone stays "idle"
because no client is sending MCP messages on stdin yet.
"""

import asyncio
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent


async def main() -> None:
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "server.py"],
        cwd=str(ROOT),
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connected to curiosity_break MCP (stdio).\n")
            listed = await session.list_tools()
            print("Tools:")
            for t in listed.tools:
                print(f"  • {t.name}")
            print()

            for name, args in [
                ("xkcd_latest", {}),
                ("random_advice", {}),
                ("xkcd_by_number", {"comic_number": 303}),
            ]:
                result = await session.call_tool(name, arguments=args)
                text = result.content[0].text if result.content else str(result)
                print(f"--- {name} ---")
                print(text)
                print()


if __name__ == "__main__":
    asyncio.run(main())
