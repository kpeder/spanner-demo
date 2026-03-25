from spanner.query import query_database, update_database
from google.api_core import exceptions
import pytest


def test_standard_select_query(spanner_config):
    """Tests a standard SELECT query."""
    for col in spanner_config['fixtures']['columns']:
        config = {'name': col['name'], 'type': col['type'], 'nullable': col['nullable'], 'tables': col['tables']}
        results = query_database(
            project=spanner_config["project"],
            instance_id=spanner_config["instance"],
            database_id=spanner_config["database"],
            query_string=f"""SELECT `table_name`, `column_name`, `spanner_type`, `is_nullable`
                             FROM `information_schema`.`columns`
                             WHERE `column_name` = '{config['name']}'
                             LIMIT {len(config['tables'])};""",
            query_timeout=3.0,
            is_partitioned=False,
        )
        assert len(results) == len(config['tables'])
        for result in results:
            assert result[0] in config['tables']
            assert result[1] == config['name']
            assert result[2] == config['type']
            assert result[3] == config['nullable']


def test_query_bad_config(caplog):
    """Tests that query_database returns None on an unexpected error."""

    result = query_database(
        project="notmy-project",
        instance_id="notmy-instance",
        database_id="notmy-db",
        query_string="SELECT 1",
        query_timeout=5.0,
        is_partitioned=False,
    )
    print(caplog.text)
    # There should be an exception in the logs.
    pytest.raises(exceptions.PermissionDenied)
    assert "An API error occurred while querying Spanner: 403 Operation denied by" in caplog.text
    # The function should return None.
    assert result is None


def test_dml_query(spanner_config, caplog):
    """Tests a standard DML query logs an error and returns None."""
    # This is a non-destructive update that will either affect 1 row or 0.
    result = query_database(
        project=spanner_config["project"],
        instance_id=spanner_config["instance"],
        database_id=spanner_config["database"],
        query_string="UPDATE Users SET Email = Email WHERE UserID = 456",
        query_timeout=30.0,
        is_partitioned=False,
    )
    # There should be an exception in the logs.
    pytest.raises(exceptions.InvalidArgument)
    assert "An API error occurred while querying Spanner: 400 DML statements may not be performed in single-use transactions, to avoid replay." in caplog.text
    # The function should return None.
    assert result is None


def test_partitioned_select_query(spanner_config):
    """Tests a partitioned SELECT query."""
    for col in spanner_config['fixtures']['columns']:
        config = {'name': col['name'], 'type': col['type'], 'nullable': col['nullable'], 'tables': col['tables']}
        results = query_database(
            project=spanner_config["project"],
            instance_id=spanner_config["instance"],
            database_id=spanner_config["database"],
            query_string=f"""SELECT `table_name`, `column_name`, `spanner_type`, `is_nullable`
                             FROM `information_schema`.`columns`
                             WHERE `column_name` = '{config['name']}';""",
            query_timeout=3.0,
            is_partitioned=True,
        )
        assert len(results) == len(config['tables'])
        for result in results:
            assert result[0] in config['tables']
            assert result[1] == config['name']
            assert result[2] == config['type']
            assert result[3] == config['nullable']


def test_standard_update(spanner_config):
    """Tests a standard DML update."""
    # This is a non-destructive update that will affect 1 row.
    result = update_database(
        project=spanner_config["project"],
        instance_id=spanner_config["instance"],
        database_id=spanner_config["database"],
        dml_string="UPDATE Users SET Email = Email WHERE UserID = 456",
        transaction_timeout=30.0,
        is_partitioned=False,
    )
    # The function should return the number of rows affected.
    assert isinstance(result, int)
    assert result == 1


def test_partitioned_update(spanner_config):
    """Tests a partitioned DML update."""
    # This is a non-destructive update that will affect all rows in the Users table.
    result = update_database(
        project=spanner_config["project"],
        instance_id=spanner_config["instance"],
        database_id=spanner_config["database"],
        dml_string="UPDATE Users SET Email = Email WHERE TRUE",
        transaction_timeout=60.0,
        is_partitioned=True,
    )
    # The function should return the number of rows affected.
    assert isinstance(result, int)
    assert result > 1


def test_update_bad_config(caplog):
    """Tests that update_database returns None on an unexpected error."""
    result = update_database(
        project="notmy-project",
        instance_id="notmy-instance",
        database_id="notmy-db",
        dml_string="UPDATE Users SET Email = Email WHERE UserID = 1",
        transaction_timeout=5.0,
        is_partitioned=False,
    )
    # There should be an exception in the logs.
    pytest.raises(exceptions.PermissionDenied)
    assert "An API error occurred while updating Spanner: 403 Operation denied by" in caplog.text
    # The function should return None.
    assert result is None


def test_select_query(spanner_config, caplog):
    """Tests a standard select query returns 0."""
    result = update_database(
        project=spanner_config["project"],
        instance_id=spanner_config["instance"],
        database_id=spanner_config["database"],
        dml_string="SELECT * FROM Users WHERE UserID = 456",
        transaction_timeout=30.0,
        is_partitioned=False,
    )
    assert result == 0
