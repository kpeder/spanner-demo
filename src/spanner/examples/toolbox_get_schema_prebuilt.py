from spanner.toolbox import load_tool
from toolbox_core import ToolboxClient
from toolbox_core.protocol import Protocol

import argparse
import asyncio
import logging


logger = logging.getLogger('spanner.examples.toolbox_get_schema_prebuilt')


async def main():
    """Main function to parse arguments and use prebuilt tools from a toolbox server to fetch database schema information."""

    parser = argparse.ArgumentParser(description="Fetch spanner schema information from a prebuilt toolbox server.")
    parser.add_argument("--url", required=True, help="The URL of the toolbox server.")
    parser.add_argument("--tables", default="", help="A comma-separated list of tables to fetch.")
    parser.add_argument("--simple", action="store_true", help="Fetch the table information only.")

    args = parser.parse_args()

    if args.simple:
        mode = "simple"
    else:
        mode = "detailed"

    protocol = Protocol.MCP_v20251125
    tables = args.tables
    url = args.url

    try:
        logger.info("Initializing toolbox client for server with URL %s", url)
        async with ToolboxClient(url=url, protocol=protocol) as toolbox:

            logger.info("Fetching available tools from toolbox server.")
            tools = await toolbox.load_toolset()
            for tool in tools:
                logger.info("Found tool '%s' with description '%s'", tool._name, tool._description)

            logger.info("Found %d tools.", len(tools))

            logger.info("Loading tools...")
            fetch_tables = await load_tool("list_tables", toolbox)

            if fetch_tables is not None:
                schema_info = await fetch_tables(mode, tables)
                print(schema_info)

    except Exception as e:
        logger.error("An error occurred while fetching tools: %s", e, exc_info=True)
        return None


if __name__ == '__main__':
    asyncio.run(main())
    logging.shutdown()
