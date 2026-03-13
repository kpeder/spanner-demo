import logging
import argparse

from spanner.query import query_database

logger = logging.getLogger('spanner.examples.spannner_query')


def main():
    """Main function to parse arguments and query Spanner."""

    parser = argparse.ArgumentParser(description="Query a Google Cloud Spanner database.")
    parser.add_argument("--project-id", required=True, help="Your Google Cloud project ID.")
    parser.add_argument("--instance-id", required=True, help="The ID of the Spanner instance.")
    parser.add_argument("--database-id", required=True, help="The ID of the Spanner database.")
    parser.add_argument("--query-string", required=True, help="The SQL query string to execute.")
    parser.add_argument("--timeout", type=float, default=60.0, help="The query timeout in seconds. Ignored if partitioned is true.")
    parser.add_argument("--partitioned", action="store_true", help="Execute as a partitioned query.")

    args = parser.parse_args()

    logger.info(f"Running Query on {args.project_id}")

    try:
        results = query_database(
            project=args.project_id,
            instance_id=args.instance_id,
            database_id=args.database_id,
            query_string=args.query_string,
            query_timeout=args.timeout,
            is_partitioned=args.partitioned,
        )

        if results is not None:
            if isinstance(results, list):
                print("Query Results:")
                for row in results:
                    print(row)
            elif isinstance(results, int):
                print(f"DML statement affected {results} rows.")
        else:
            print("Query executed, but returned no results or an error occurred.")

    except Exception as e:
        print(f"An error occurred during the example run: {e}")


if __name__ == '__main__':
    main()
    logging.shutdown()
