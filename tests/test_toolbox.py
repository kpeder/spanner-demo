from spanner.toolbox import load_tool
from toolbox_core import ToolboxSyncClient
from toolbox_core.protocol import Protocol


def test_load_tool_success(toolbox_config):
    """Tests successfully loading a tool."""
    with ToolboxSyncClient(url=toolbox_config["url"], protocol=Protocol.MCP_v20251125) as toolbox:
        # Assuming 'get_tables' is a tool that exists on the server.
        tool = load_tool("get_tables", toolbox)
        assert tool is not None
        assert tool._name == "get_tables"


def test_load_tool_failure(toolbox_config):
    """Tests failure when loading a tool."""
    with ToolboxSyncClient(url=toolbox_config["url"], protocol=Protocol.MCP_v20251125) as toolbox:
        tool = load_tool("non_existent_tool", toolbox)
        assert tool is None
