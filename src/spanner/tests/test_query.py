import yaml
import pytest
from google.cloud import spanner_v1
from google.api_core import exceptions

from spanner.query import query_database

TEST_TABLE = "TestTable"


@pytest.fixture(scope="session")
def spanner_config():
    """Reads the test configuration for Spanner."""
    with open("tests/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config["spanner"]


@pytest.fixture(scope="session")
def spanner_database(spanner_config):
    """
    Provides a Spanner database client and handles setup/teardown of the test table.
    """
    spanner_client = spanner_v1.Client(project=spanner_config["project_id"])
    instance = spanner_client.instance(spanner_config["instance_id"])
    database = instance.database(spanner_config["database_id"])

    # DDL to create the test table
    create_table_ddl = f"""
    CREATE TABLE {TEST_TABLE} (
        Id INT64 NOT NULL,
        Name STRING(1024),
    ) PRIMARY KEY (Id)
    """

    try:
        # Check if table exists
        database.run_in_transaction(lambda tx: tx.execute_sql(f"SELECT 1 FROM {TEST_TABLE} LIMIT 1"))
        print(f"Table {TEST_TABLE} already exists.")
    except exceptions.NotFound:
        print(f"Table {TEST_TABLE} not found, creating it...")
        operation = database.update_ddl([create_table_ddl])
        operation.result(timeout=300)
        print(f"Table {TEST_TABLE} created.")

    yield database

    # Teardown: Drop the test table
    drop_table_ddl = f"DROP TABLE {TEST_TABLE}"
    try:
        operation = database.update_ddl([drop_table_ddl])
        operation.result(timeout=300)
        print(f"Table {TEST_TABLE} dropped.")
    except exceptions.NotFound:
        print(f"Table {TEST_TABLE} was not found for dropping.")


@pytest.fixture(autouse=True)
def manage_test_data(spanner_database):
    """
    Manages test data for each test function.
    Inserts data before a test and cleans it up after.
    """
    # Setup: Insert test data
    def insert_data(transaction):
        transaction.execute_update(
            f"INSERT INTO {TEST_TABLE} (Id, Name) VALUES "
            "(1, 'Alice'), "
            "(2, 'Bob'), "
            "(3, 'Charlie')"
        )

    spanner_database.run_in_transaction(insert_data)

    yield

    # Teardown: Clean up test data
    def delete_data(transaction):
        transaction.execute_update(f"DELETE FROM {TEST_TABLE} WHERE true")

    spanner_database.run_in_transaction(delete_data)


def test_standard_select_query(spanner_config):
    """Tests a standard SELECT query."""
    results = query_database(
        project=spanner_config["project_id"],
        instance_id=spanner_config["instance_id"],
        database_id=spanner_config["database_id"],
        query_string=f"SELECT * FROM {TEST_TABLE} ORDER BY Id",
        query_timeout=30.0,
        is_partitioned=False,
    )
    assert results is not None
    assert len(results) == 3
    assert results[0][0] == 1 and results[0][1] == "Alice"
    assert results[1][0] == 2 and results[1][1] == "Bob"


def test_partitioned_select_query(spanner_config):
    """Tests a partitioned SELECT query."""
    results = query_database(
        project=spanner_config["project_id"],
        instance_id=spanner_config["instance_id"],
        database_id=spanner_config["database_id"],
        query_string=f"SELECT * FROM {TEST_TABLE}",
        query_timeout=30.0,
        is_partitioned=True,
    )
    assert results is not None
    # Order is not guaranteed in partitioned reads, so we sort for assertion
    sorted_results = sorted(results, key=lambda r: r[0])
    assert len(sorted_results) == 3
    assert sorted_results[0][0] == 1 and sorted_results[0][1] == "Alice"


def test_dml_statement(spanner_config):
    """Tests a DML statement (e.g., UPDATE)."""
    # This test runs inside a transaction implicitly created by query_database for DML
    # but since it's a separate call, it won't see the uncommitted data from the fixture easily.
    # For simplicity, we'll just insert and check the count.
    affected_rows = query_database(
        project=spanner_config["project_id"],
        instance_id=spanner_config["instance_id"],
        database_id=spanner_config["database_id"],
        query_string=f"UPDATE {TEST_TABLE} SET Name = 'Robert' WHERE Id = 2",
        query_timeout=30.0,
        is_partitioned=False,
    )
    assert affected_rows == 1
