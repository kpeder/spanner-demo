from google.cloud import spanner_v1
from google.api_core import exceptions

import logging


logger = logging.getLogger(__name__)


def query_database(project: str,
                   instance_id: str,
                   database_id: str,
                   query_string: str,
                   query_timeout: float = 30.0,
                   is_partitioned: bool = False) -> list | None:
    """
    Executes a query against a Google Cloud Spanner database.

    Args:
        project: The Google Cloud project ID.
        instance_id: The ID of the Spanner instance.
        database_id: The ID of the Spanner database.
        query_string: The SQL query string to execute.
        query_timeout: The timeout for the query in seconds.
        is_partitioned: A flag to indicate if this is a partitioned query.

    Returns:
        For SELECT queries, a list of rows as dictionaries.
        For DML queries, logs an error and returns None.
        Returns None if an error occurs.
    """
    try:
        logger.info(
            "Initializing Spanner client for project '%s' and instance '%s'",
            project,
            instance_id,
        )
        spanner_client = spanner_v1.Client(project=project, disable_builtin_metrics=True)
        instance = spanner_client.instance(instance_id)
        database = instance.database(database_id)

        if is_partitioned:
            logger.info("Executing partitioned read query on database '%s'", database_id)
            # Use a batch snapshot to get strong read consistency.
            with database.batch_snapshot() as snapshot:
                logger.info("Executing partitioned SQL query...")
                results = snapshot.run_partitioned_query(
                    query_string
                )
                if results.stats and results.stats.row_count_exact:
                    logger.info("DML statement affected %d rows.", results.stats.row_count_exact)
                    return results.stats.row_count_exact

                rows = [row for row in results]
                logger.info("Query returned %d rows.", len(rows))
                return rows

        else:
            # Use a snapshot to get strong read consistency.
            with database.snapshot() as snapshot:
                logger.info("Executing standard SQL query...")
                results = snapshot.execute_sql(
                    query_string,
                    timeout=query_timeout
                )
                if results.stats and results.stats.row_count_exact:
                    logger.info("DML statement affected %d rows.", results.stats.row_count_exact)
                    return results.stats.row_count_exact

                rows = [row for row in results]
                logger.info("Query returned %d rows.", len(rows))
                return rows

    except exceptions.GoogleAPICallError as e:
        logger.error("An API error occurred while querying Spanner: %s", e, exc_info=True)
        return None
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e, exc_info=True)
        return None


def update_database(project: str,
                    instance_id: str,
                    database_id: str,
                    dml_string: str,
                    transaction_timeout: float = 30.0,
                    is_partitioned: bool = False) -> int | None:
    """
    Executes an update against a Google Cloud Spanner database.

    Args:
        project: The Google Cloud project ID.
        instance_id: The ID of the Spanner instance.
        database_id: The ID of the Spanner database.
        dml_string: The SQL DML string to execute.
        transaction_timeout: The timeout for the transaction in seconds.
        is_partitioned: A flag to indicate if this is a partitioned DML statement.

    Returns:
        The number of modified rows if the statement executes successfully.
        Returns None if an error occurs.
    """
    try:
        logger.info(
            "Initializing Spanner client for project '%s' and instance '%s'",
            project,
            instance_id,
        )
        spanner_client = spanner_v1.Client(project=project, disable_builtin_metrics=True)
        instance = spanner_client.instance(instance_id)
        database = instance.database(database_id)

        if is_partitioned:
            logger.info("Executing partitioned DML on database '%s'", database_id)
            row_count = database.execute_partitioned_dml(dml_string)
            logger.info("Partitioned DML statement affected %d rows.", row_count)
            return row_count

        else:

            def _update_in_transaction(transaction):
                row_count = transaction.execute_update(
                    dml_string
                )
                return row_count

            logger.info("Executing standard DML on database '%s'", database_id)
            row_count = database.run_in_transaction(_update_in_transaction, timeout_secs=transaction_timeout)
            logger.info("Standard DML statement affected %d rows.", row_count)
            return row_count

    except exceptions.GoogleAPICallError as e:
        logger.error("An API error occurred while updating Spanner: %s", e, exc_info=True)
        return None
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e, exc_info=True)
        return None
