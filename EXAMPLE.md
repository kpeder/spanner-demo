# Spanner NLP Examples

## Core Module

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
## Chat Module

```
$ uv run python -m spanner.__chat__ --project vertex-ai-experiments-448517 --location us-east1 --model gemini-2.5-flash
2026-03-24 14:25:23,994 - spanner - INFO - Google Cloud Logging handler initialized.
2026-03-24 14:25:24,944 - spanner.tools - INFO - Initializing toolbox client for server with URL http://localhost:5000
2026-03-24 14:25:24,948 - spanner.tools - INFO - Fetching available tools from toolbox server.
2026-03-24 14:25:24,959 - spanner.tools - INFO - Found tool 'get_keys' with description 'Query the INFORMATION_SCHEMA for key constraints on a table.'
2026-03-24 14:25:24,959 - spanner.tools - INFO - Found tool 'get_indexes' with description 'Query the INFORMATION_SCHEMA for indexes on a table.'
2026-03-24 14:25:24,959 - spanner.tools - INFO - Found tool 'exec_query' with description 'Execute the supplied GoogleSQL query against the database.'
2026-03-24 14:25:24,959 - spanner.tools - INFO - Found tool 'get_tables' with description 'Query the INFORMATION_SCHEMA for tables in a schema.'
2026-03-24 14:25:24,959 - spanner.tools - INFO - Found tool 'get_columns' with description 'Query the INFORMATION_SCHEMA for columns in a table.'
2026-03-24 14:25:24,959 - spanner.tools - INFO - Found 5 tools.
2026-03-24 14:25:24,959 - spanner.tools - INFO - Loading tools...
2026-03-24 14:25:24,959 - spanner.toolbox - INFO - Loading the get_tables tool from the toolbox.
2026-03-24 14:25:24,964 - spanner.toolbox - INFO - Loading the get_columns tool from the toolbox.
2026-03-24 14:25:24,966 - spanner.toolbox - INFO - Loading the get_keys tool from the toolbox.
2026-03-24 14:25:24,968 - spanner.toolbox - INFO - Loading the get_indexes tool from the toolbox.
Spanner chat enabled. Type 'exit', 'quit' or 'stop' to quit.
Enter your question: What is the maximum number of items found on a single order?
Response:
SELECT
    MAX(TotalItems)
FROM
    (
        SELECT
            SUM(Quantity) AS TotalItems
        FROM
            OrderItems
        GROUP BY
            OrderID
    );
Would you like to run this query? (y/N): y
Executing query...
2026-03-24 14:26:02,018 - spanner.tools - INFO - Initializing toolbox client for server with URL http://localhost:5000
2026-03-24 14:26:02,019 - spanner.tools - INFO - Fetching available tools from toolbox server.
2026-03-24 14:26:02,028 - spanner.tools - INFO - Found tool 'get_keys' with description 'Query the INFORMATION_SCHEMA for key constraints on a table.'
2026-03-24 14:26:02,028 - spanner.tools - INFO - Found tool 'get_indexes' with description 'Query the INFORMATION_SCHEMA for indexes on a table.'
2026-03-24 14:26:02,028 - spanner.tools - INFO - Found tool 'exec_query' with description 'Execute the supplied GoogleSQL query against the database.'
2026-03-24 14:26:02,028 - spanner.tools - INFO - Found tool 'get_tables' with description 'Query the INFORMATION_SCHEMA for tables in a schema.'
2026-03-24 14:26:02,028 - spanner.tools - INFO - Found tool 'get_columns' with description 'Query the INFORMATION_SCHEMA for columns in a table.'
2026-03-24 14:26:02,028 - spanner.tools - INFO - Found 5 tools.
2026-03-24 14:26:02,028 - spanner.tools - INFO - Loading tools...
2026-03-24 14:26:02,028 - spanner.toolbox - INFO - Loading the exec_query tool from the toolbox.
2026-03-24 14:26:02,030 - spanner.tools - INFO - Executing query...
Query Results:

0  40
Enter your next question: stop
Waiting up to 5 seconds.
Sent all pending logs.
```

## Agent Module

```
$ uv run python -m spanner.__agent__ --project vertex-ai-experiments-448517 --location us-east1 --model gemini-2.5-flash
2026-03-24 14:26:55,960 - spanner - INFO - Google Cloud Logging handler initialized.
Spanner agent enabled. Type 'exit', 'quit' or 'stop' to quit.
spanner_user: hello
spanner_nlp_agent: Hello! I'm a natural language processor that can help you with Google SQL for Spanner databases. I can translate your questions into SQL statements and help you execute them.

What can I do for you today?
spanner_user: can you tell me about my schema? please summarize the details for me.
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
2026-03-24 14:27:46,726 - spanner.tools - INFO - Initializing toolbox client for server with URL http://localhost:5000
2026-03-24 14:27:46,730 - spanner.tools - INFO - Fetching available tools from toolbox server.
2026-03-24 14:27:46,737 - spanner.tools - INFO - Found tool 'get_keys' with description 'Query the INFORMATION_SCHEMA for key constraints on a table.'
2026-03-24 14:27:46,738 - spanner.tools - INFO - Found tool 'get_indexes' with description 'Query the INFORMATION_SCHEMA for indexes on a table.'
2026-03-24 14:27:46,738 - spanner.tools - INFO - Found tool 'exec_query' with description 'Execute the supplied GoogleSQL query against the database.'
2026-03-24 14:27:46,738 - spanner.tools - INFO - Found tool 'get_tables' with description 'Query the INFORMATION_SCHEMA for tables in a schema.'
2026-03-24 14:27:46,738 - spanner.tools - INFO - Found tool 'get_columns' with description 'Query the INFORMATION_SCHEMA for columns in a table.'
2026-03-24 14:27:46,738 - spanner.tools - INFO - Found 5 tools.
2026-03-24 14:27:46,738 - spanner.tools - INFO - Loading tools...
2026-03-24 14:27:46,738 - spanner.toolbox - INFO - Loading the get_tables tool from the toolbox.
2026-03-24 14:27:46,740 - spanner.toolbox - INFO - Loading the get_columns tool from the toolbox.
2026-03-24 14:27:46,742 - spanner.toolbox - INFO - Loading the get_keys tool from the toolbox.
2026-03-24 14:27:46,745 - spanner.toolbox - INFO - Loading the get_indexes tool from the toolbox.
spanner_nlp_agent: Your schema contains the following tables:

*   **Products**: Stores product information.
    *   **Columns**: `ProductID` (INT64, Primary Key), `Name` (STRING), `Description` (STRING), `ImageURL` (STRING), `PriceUSD` (NUMERIC), `Category` (STRING), `ProductEmbedding` (ARRAY<FLOAT64>), `Name_Tokens` (TOKENLIST), `Description_Tokens` (TOKENLIST).
    *   **Indexes**: `ProductID` (Primary Key), `Description_Tokens` (SEARCH), `Name_Tokens` (SEARCH), `ProductEmbedding` (VECTOR).

*   **Payments**: Records payment transactions.
    *   **Columns**: `PaymentID` (INT64, Primary Key), `OrderID` (INT64), `UserID` (INT64), `PaymentDate` (TIMESTAMP), `PaymentMethod` (STRING), `TransactionID` (STRING), `AmountUSD` (NUMERIC), `Status` (STRING), `PaymentMethod_Tokens` (TOKENLIST), `Status_Tokens` (TOKENLIST).
    *   **Indexes**: `PaymentMethod_Tokens` (SEARCH), `Status_Tokens` (SEARCH), `PaymentID` (Primary Key).

*   **ShoppingCarts**: Details items in users' shopping carts.
    *   **Columns**: `UserID` (INT64, Primary Key), `ProductID` (INT64, Primary Key), `Quantity` (INT64), `AddedDate` (TIMESTAMP).
    *   **Foreign Keys**: `ProductID` references `Products`, `UserID` references `Users`.
    *   **Indexes**: `ProductID` (Index), `UserID` (Primary Key), `ProductID` (Primary Key).

*   **Addresses**: Stores user address information.
    *   **Columns**: `AddressID` (INT64, Primary Key), `UserID` (INT64, Primary Key), `StreetAddress` (STRING), `City` (STRING), `State` (STRING), `Country` (STRING), `ZipCode` (STRING).
    *   **Foreign Keys**: `UserID` references `Users`.
    *   **Indexes**: `AddressID` (Index), `UserID` (Primary Key), `AddressID` (Primary Key).

*   **Orders**: Contains order details.
    *   **Columns**: `OrderID` (INT64, Primary Key), `UserID` (INT64), `OrderDate` (TIMESTAMP), `ShippingAddressID` (INT64), `PaymentID` (INT64), `TotalAmountUSD` (NUMERIC), `OrderStatus` (STRING), `OrderStatus_Tokens` (TOKENLIST).
    *   **Foreign Keys**: `ShippingAddressID` references `Addresses`, `PaymentID` references `Payments`, `UserID` references `Users`.
    *   **Indexes**: `PaymentID` (Index), `ShippingAddressID` (Index), `UserID` (Index), `OrderStatus_Tokens` (SEARCH), `OrderID` (Primary Key).

*   **Users**: Stores user account information.
    *   **Columns**: `UserID` (INT64, Primary Key), `Email` (STRING).
    *   **Indexes**: `UserID` (Primary Key).

*   **OrderItems**: Lists individual items within orders.
    *   **Columns**: `OrderItemID` (INT64, Primary Key), `OrderID` (INT64, Primary Key), `ProductID` (INT64), `Quantity` (INT64), `PriceAtOrderUSD` (NUMERIC).
    *   **Foreign Keys**: `OrderID` references `Orders`, `ProductID` references `Products`.
    *   **Indexes**: `ProductID` (Index), `OrderID` (Primary Key), `OrderItemID` (Primary Key).
spanner_user: can you distill this information to a few lines?
spanner_nlp_agent: Your database schema consists of seven tables:

*   **Products**: Stores product details (ID, name, price, category).
*   **Payments**: Records payment transactions (ID, order, user, amount, status).
*   **ShoppingCarts**: Manages items in user shopping carts (user ID, product ID, quantity).
*   **Addresses**: Holds user address information (ID, user, street, city).
*   **Orders**: Contains order specifics (ID, user, date, total amount, status).
*   **Users**: Stores user account information (ID, email).
*   **OrderItems**: Details individual items within orders (ID, order, product, quantity).
spanner_user: great. I wonder how many users have open shopping carts?
spanner_nlp_agent: SELECT
    COUNT(DISTINCT UserID)
  FROM
    ShoppingCarts;

spanner_user: could you run this query for me?
2026-03-24 14:29:21,400 - spanner.tools - INFO - Initializing toolbox client for server with URL http://localhost:5000
2026-03-24 14:29:21,402 - spanner.tools - INFO - Fetching available tools from toolbox server.
2026-03-24 14:29:21,410 - spanner.tools - INFO - Found tool 'get_keys' with description 'Query the INFORMATION_SCHEMA for key constraints on a table.'
2026-03-24 14:29:21,410 - spanner.tools - INFO - Found tool 'get_indexes' with description 'Query the INFORMATION_SCHEMA for indexes on a table.'
2026-03-24 14:29:21,410 - spanner.tools - INFO - Found tool 'exec_query' with description 'Execute the supplied GoogleSQL query against the database.'
2026-03-24 14:29:21,410 - spanner.tools - INFO - Found tool 'get_tables' with description 'Query the INFORMATION_SCHEMA for tables in a schema.'
2026-03-24 14:29:21,411 - spanner.tools - INFO - Found tool 'get_columns' with description 'Query the INFORMATION_SCHEMA for columns in a table.'
2026-03-24 14:29:21,411 - spanner.tools - INFO - Found 5 tools.
2026-03-24 14:29:21,411 - spanner.tools - INFO - Loading tools...
2026-03-24 14:29:21,411 - spanner.toolbox - INFO - Loading the exec_query tool from the toolbox.
2026-03-24 14:29:21,414 - spanner.tools - INFO - Executing query...
Query Results:

0  44
spanner_nlp_agent: There are 44 users with open shopping carts.
spanner_user: excellent. please ask me whether I would like to run the query each time that you generate one. how many users have open shopping carts as a percentage of total users?
spanner_nlp_agent: SELECT
    CAST(COUNT(DISTINCT sc.UserID) AS FLOAT64) / COUNT(DISTINCT u.UserID) * 100
  FROM
    ShoppingCarts AS sc,
    Users AS u;
Would you like to execute the returned query?
spanner_user: yes!
2026-03-24 14:30:42,348 - spanner.tools - INFO - Initializing toolbox client for server with URL http://localhost:5000
2026-03-24 14:30:42,351 - spanner.tools - INFO - Fetching available tools from toolbox server.
2026-03-24 14:30:42,357 - spanner.tools - INFO - Found tool 'get_keys' with description 'Query the INFORMATION_SCHEMA for key constraints on a table.'
2026-03-24 14:30:42,357 - spanner.tools - INFO - Found tool 'get_indexes' with description 'Query the INFORMATION_SCHEMA for indexes on a table.'
2026-03-24 14:30:42,358 - spanner.tools - INFO - Found tool 'exec_query' with description 'Execute the supplied GoogleSQL query against the database.'
2026-03-24 14:30:42,359 - spanner.tools - INFO - Found tool 'get_tables' with description 'Query the INFORMATION_SCHEMA for tables in a schema.'
2026-03-24 14:30:42,359 - spanner.tools - INFO - Found tool 'get_columns' with description 'Query the INFORMATION_SCHEMA for columns in a table.'
2026-03-24 14:30:42,359 - spanner.tools - INFO - Found 5 tools.
2026-03-24 14:30:42,359 - spanner.tools - INFO - Loading tools...
2026-03-24 14:30:42,359 - spanner.toolbox - INFO - Loading the exec_query tool from the toolbox.
2026-03-24 14:30:42,363 - spanner.tools - INFO - Executing query...
Query Results:

0  88
spanner_nlp_agent: 88.0% of the total users have open shopping carts.
spanner_user: stop
Waiting up to 5 seconds.
Sent all pending logs.
```
