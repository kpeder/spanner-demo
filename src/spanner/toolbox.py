from toolbox_core import ToolboxSyncClient
from toolbox_core.tool import ToolboxTool

import logging


logger = logging.getLogger(__name__)


def load_tool(name: str,
              toolbox: ToolboxSyncClient) -> ToolboxTool | None:
    """
    Loads a specific tool from the toolbox server.

    Args:
        name: The name of the tool to load.
        toolbox: The toolbox instance to use.

    Returns:
        A ToolboxTool instance, or None if an error occurs.
    """
    try:
        logger.info("Loading the %s tool from the toolbox.", name)
        tool = toolbox.load_tool(name=name)

        return tool

    except Exception as e:
        logger.error("An error occurred while loading the tool: %s", e, exc_info=True)
        return None
