from spanner.toolbox import load_tool
from toolbox_core import ToolboxClient
from toolbox_core.protocol import Protocol

import argparse
import asyncio
import json
import logging


logger = logging.getLogger('spanner.examples.toolbox_get_schema_custom')


async def main():
    """Main function to parse arguments and use custom tools from a toolbox server to fetch database schema information."""

    parser = argparse.ArgumentParser(description="Fetch spanner schema information from a custom toolbox server.")
    parser.add_argument("--filter", default="%", help="A string filter to match against table names.")
    parser.add_argument("--schema", default="", help="A specific schema to fetch schema elements from.")
    parser.add_argument("--url", required=True, help="The URL of the toolbox server.")

    args = parser.parse_args()

    filter = args.filter
    protocol = Protocol.MCP_v20251125
    schema = args.schema
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
            fetch_tables = await load_tool("get_tables", toolbox)
            fetch_columns = await load_tool("get_columns", toolbox)
            fetch_keys = await load_tool("get_keys", toolbox)
            fetch_indexes = await load_tool("get_indexes", toolbox)

            if fetch_tables is not None:
                t = await fetch_tables(filter, schema)
                tables = json.loads(t)
                if tables is not None:
                    if not isinstance(tables, list):
                        tables = [tables]

                    if fetch_columns is not None:
                        for table in tables:
                            c = await fetch_columns(schema, table['TABLE_NAME'])
                            columns = json.loads(c)
                            table['COLUMNS'] = columns
                    if fetch_keys is not None:
                        for table in tables:
                            k = await fetch_keys(schema, table['TABLE_NAME'])
                            keys = json.loads(k)
                            table['KEYS'] = keys
                    if fetch_indexes is not None:
                        for table in tables:
                            i = await fetch_indexes(schema, table['TABLE_NAME'])
                            indexes = json.loads(i)
                            table['INDEXES'] = indexes
                    print(json.dumps(tables, indent=2))

    except Exception as e:
        logger.error("An error occurred while fetching tools: %s", e, exc_info=True)
        return None


if __name__ == '__main__':
    asyncio.run(main())
    logging.shutdown()
