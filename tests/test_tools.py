import json
from spanner.tools import fetch_schema


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
