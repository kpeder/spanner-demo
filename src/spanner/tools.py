from spanner.toolbox import load_tool

from toolbox_core import ToolboxSyncClient
from toolbox_core.protocol import Protocol

import json
import logging


logger = logging.getLogger(__name__)


def fetch_schema(filter: str = "%",
                 protocol: Protocol = Protocol.MCP_v20251125,
                 schema: str = "",
                 url: str = "http://localhost:5000") -> list | None:
    """
    Fetches detailed Spanner schema information from a toolbox server.

    This function connects to a specified toolbox server, fetches table
    information matching a filter, and then retrieves columns, keys, and
    indexes for each table.

    Args:
        filter: A filter to match against table names, uses SQL LIKE syntax (i.e., the '%' wildcard).
        protocol: The toolbox communication protocol to use.
        schema: The specific schema to fetch elements from. An empty string indicates the Default schema.
        url: The URL of the toolbox server, including protocol and port.

    Returns:
        A JSON string representing the detailed schema information,
        or None if no results are returned or an error occurs.
    """

    try:
        logger.info("Initializing toolbox client for server with URL %s", url)
        with ToolboxSyncClient(url=url, protocol=protocol) as toolbox:

            logger.info("Fetching available tools from toolbox server.")
            tools = toolbox.load_toolset()
            for tool in tools:
                logger.info("Found tool '%s' with description '%s'", tool._name, tool._description)

            logger.info("Found %d tools.", len(tools))

            logger.info("Loading tools...")
            fetch_tables = load_tool("get_tables", toolbox)
            fetch_columns = load_tool("get_columns", toolbox)
            fetch_keys = load_tool("get_keys", toolbox)
            fetch_indexes = load_tool("get_indexes", toolbox)

            if fetch_tables is not None:
                t = fetch_tables(filter, schema)
                tables = json.loads(t)
                if tables is not None:
                    if not isinstance(tables, list):
                        tables = [tables]
                        
                    if fetch_columns is not None:
                        for table in tables:
                            c = fetch_columns(schema, table['TABLE_NAME'])
                            columns = json.loads(c)
                            table['COLUMNS'] = columns
                    if fetch_keys is not None:
                        for table in tables:
                            k = fetch_keys(schema, table['TABLE_NAME'])
                            keys = json.loads(k)
                            table['KEYS'] = keys
                    if fetch_indexes is not None:
                        for table in tables:
                            i = fetch_indexes(schema, table['TABLE_NAME'])
                            indexes = json.loads(i)
                            table['INDEXES'] = indexes
                    return json.dumps(tables)
            else:
                return None

    except Exception as e:
        logger.error("An error occurred while fetching tools: %s", e, exc_info=True)
        return None   
