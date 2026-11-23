import asyncio
import os

from servicenow_mcp.server import ServiceNowMCP
from servicenow_mcp.utils.config import (
    AuthConfig,
    AuthType,
    BasicAuthConfig,
    ServerConfig,
)


def test_full_package_tool_registration():
    os.environ["MCP_TOOL_PACKAGE"] = "full"

    config = ServerConfig(
        instance_url="https://example.service-now.com",
        auth=AuthConfig(
            type=AuthType.BASIC,
            basic=BasicAuthConfig(
                username="test-user",
                password="test-password",
            ),
        ),
    )

    server = ServiceNowMCP(config)

    assert server.current_package_name == "full"
    assert len(server.enabled_tool_names) == 93

    tools = asyncio.run(server._list_tools_impl())
    actual_names = {tool.name for tool in tools}
    expected_names = set(server.enabled_tool_names)

    missing = sorted(expected_names - actual_names)

    print("\nMissing MCP tools:")
    for name in missing:
        print(f"  - {name}")

    assert not missing, f"{len(missing)} configured tools were not exposed: {missing}"
