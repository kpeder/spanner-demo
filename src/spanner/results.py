import pandas as pd
import json
import logging


logger = logging.getLogger(__name__)


def render_results_as_table(json_results: str) -> None:
    """
    Parses a JSON string of query results and prints them in a tabular format using pandas.

    Args:
        json_results: A JSON string representing the query results.
    """
    if not json_results:
        print("No results to display.")
        return

    try:
        data = json.loads(json_results)
        if not data:
            print("Query returned no data.")
            return

        if not isinstance(data, list):
            data = [data]

        df = pd.DataFrame(data)
        print("Query Results:")
        print(df.to_string())

    except (json.JSONDecodeError, TypeError):
        logger.warning("Results are not in JSON format.")
        print("Could not render the results as a table. Raw results:")
        print(json_results)

    except Exception as e:
        logger.error("An error occurred while rendering the results: %s", e, exc_info=True)
        print("Could not render the results as a table. Raw results:")
        print(json_results)
