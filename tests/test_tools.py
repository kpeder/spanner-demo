from spanner.tools import exec_query, fetch_schema

import json


def test_exec_query_success(toolbox_config, spanner_config):
    """Tests successfully executing a query."""
    table_name = spanner_config['fixtures']['columns'][0]['tables'][0]
    query = "SELECT table_name FROM information_schema.tables WHERE table_name = '{}';".format(table_name)

    result = exec_query(query=query, url=toolbox_config["url"])
    assert result is not None

    data = json.loads(result)
    assert isinstance(data, object)
    assert data['table_name'] == table_name


def test_exec_query_invalid_query(toolbox_config):
    """Tests executing an invalid query."""
    result = exec_query(query="SELECT * FROM NonExistentTable;", url=toolbox_config["url"])
    assert result is not None
    assert isinstance(result, str)


def test_exec_query_client_exception():
    """Tests exec_query when the ToolboxSyncClient raises an exception."""
    result = exec_query(query="SELECT 1", url="http://localhost:9999")  # Non-existent server
    assert result is None


def test_fetch_schema_success(toolbox_config, spanner_config):
    """Tests successfully fetching a detailed schema."""
    # Assuming the toolbox server is connected to the spanner instance from config
    table_name = spanner_config['fixtures']['columns'][0]['tables'][0]

    result = fetch_schema(filter=table_name, url=toolbox_config["url"])
    assert result is not None

    schema = json.loads(result)
    assert isinstance(schema, list)
    assert len(schema) > 0

    # Check that the fetched schema has the expected structure
    table_info = schema[0]
    assert table_info["TABLE_NAME"] == table_name
    assert "COLUMNS" in table_info
    assert "KEYS" in table_info
    assert "INDEXES" in table_info
    assert isinstance(table_info["COLUMNS"], list)


def test_fetch_schema_no_tables_found(toolbox_config):
    """Tests fetch_schema when no tables match the filter."""
    result = fetch_schema(filter="NonExistentTable", url=toolbox_config["url"])
    assert result is None


def test_fetch_schema_client_exception():
    """Tests fetch_schema when the ToolboxSyncClient raises an exception."""
    result = fetch_schema(url="http://localhost:9999")  # Non-existent server
    assert result is None
