```
$  uv run python3 -m spanner --project vertex-ai-experiments-448517 --location us-east1 --model gemini-2.5-flash
2026-03-06 10:42:36,389 - spanner - INFO - Google Cloud Logging handler initialized.
Enter your question: What are the top 3 most popular products?
2026-03-06 10:43:06,647 - spanner.tools - INFO - Initializing toolbox client for server with URL http://localhost:5000
2026-03-06 10:43:06,650 - spanner.tools - INFO - Fetching available tools from toolbox server.
2026-03-06 10:43:06,659 - spanner.tools - INFO - Found tool 'get_keys' with description 'Query the INFORMATION_SCHEMA for key constraints on a table.'
2026-03-06 10:43:06,659 - spanner.tools - INFO - Found tool 'get_indexes' with description 'Query the INFORMATION_SCHEMA for indexes on a table.'
2026-03-06 10:43:06,660 - spanner.tools - INFO - Found tool 'exec_query' with description 'Execute the supplied GoogleSQL query against the database.'
2026-03-06 10:43:06,660 - spanner.tools - INFO - Found tool 'get_tables' with description 'Query the INFORMATION_SCHEMA for tables in a schema.'
2026-03-06 10:43:06,660 - spanner.tools - INFO - Found tool 'get_columns' with description 'Query the INFORMATION_SCHEMA for columns in a table.'
2026-03-06 10:43:06,660 - spanner.tools - INFO - Found 5 tools.
2026-03-06 10:43:06,661 - spanner.tools - INFO - Loading tools...
2026-03-06 10:43:06,661 - spanner.toolbox - INFO - Loading the get_tables tool from the toolbox.
2026-03-06 10:43:06,663 - spanner.toolbox - INFO - Loading the get_columns tool from the toolbox.
2026-03-06 10:43:06,664 - spanner.toolbox - INFO - Loading the get_keys tool from the toolbox.
2026-03-06 10:43:06,666 - spanner.toolbox - INFO - Loading the get_indexes tool from the toolbox.
Generated SQL:
SELECT
    p.Name
FROM
    OrderItems AS oi
JOIN
    Products AS p
ON
    oi.ProductID = p.ProductID
GROUP BY
    p.Name
ORDER BY
    COUNT(oi.ProductID) DESC
LIMIT 3;
Would you like to run this query? (y/N): y
Executing query...
2026-03-06 10:43:17,961 - spanner.tools - INFO - Initializing toolbox client for server with URL http://localhost:5000
2026-03-06 10:43:17,963 - spanner.tools - INFO - Fetching available tools from toolbox server.
2026-03-06 10:43:17,978 - spanner.tools - INFO - Found tool 'get_keys' with description 'Query the INFORMATION_SCHEMA for key constraints on a table.'
2026-03-06 10:43:17,978 - spanner.tools - INFO - Found tool 'get_indexes' with description 'Query the INFORMATION_SCHEMA for indexes on a table.'
2026-03-06 10:43:17,978 - spanner.tools - INFO - Found tool 'exec_query' with description 'Execute the supplied GoogleSQL query against the database.'
2026-03-06 10:43:17,978 - spanner.tools - INFO - Found tool 'get_tables' with description 'Query the INFORMATION_SCHEMA for tables in a schema.'
2026-03-06 10:43:17,978 - spanner.tools - INFO - Found tool 'get_columns' with description 'Query the INFORMATION_SCHEMA for columns in a table.'
2026-03-06 10:43:17,978 - spanner.tools - INFO - Found 5 tools.
2026-03-06 10:43:17,978 - spanner.tools - INFO - Loading tools...
2026-03-06 10:43:17,978 - spanner.toolbox - INFO - Loading the exec_query tool from the toolbox.
2026-03-06 10:43:17,980 - spanner.tools - INFO - Executing query...
Query Results:
                            Name
0  Gonzalez Classic Hiking Boots
1             Roy, Camping Chair
2        Mclean-Wilkerson Cooler
Waiting up to 5 seconds.
Sent all pending logs.
```
