from spanner.query import query_database


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
