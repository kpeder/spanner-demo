from spanner.results import render_results_as_table
from unittest.mock import patch

import json


def test_render_results_as_table_success(capsys):
    """Tests rendering valid JSON results as a table."""
    json_input = json.dumps([
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ])
    render_results_as_table(json_input)
    captured = capsys.readouterr()

    assert "Query Results:" in captured.out
    assert "id" in captured.out
    assert "name" in captured.out
    assert "Alice" in captured.out
    assert "Bob" in captured.out
    assert "Raw results" not in captured.out


def test_render_results_as_table_no_results_input(capsys):
    """Tests rendering with no results input (empty string)."""
    render_results_as_table("")
    captured = capsys.readouterr()
    assert "No results to display." in captured.out


def test_render_results_as_table_empty_data(capsys):
    """Tests rendering with JSON representing an empty list."""
    render_results_as_table("[]")
    captured = capsys.readouterr()
    assert "Query returned no data." in captured.out


def test_render_results_as_table_scalar_json(capsys):
    """Tests rendering a scalar JSON object as a table."""
    json_input = json.dumps({"id": 1, "name": "Alice"})
    render_results_as_table(json_input)
    captured = capsys.readouterr()

    assert "Query Results:" in captured.out
    assert "id" in captured.out
    assert "name" in captured.out
    assert "Alice" in captured.out
    assert "1" in captured.out
    assert "Raw results" not in captured.out


def test_render_results_as_table_invalid_json(capsys, caplog):
    """Tests rendering with an invalid JSON string."""
    invalid_json = '{"key": "value"'
    render_results_as_table(invalid_json)
    captured = capsys.readouterr()

    assert "Results are not in JSON format." in caplog.text
    assert "Could not render the results as a table. Raw results:" in captured.out
    assert invalid_json in captured.out


def test_render_results_as_table_type_error(capsys, caplog):
    """Tests rendering with a non-string input that would cause a TypeError."""
    # json.loads() expects a string, bytes, or bytearray.
    # Passing it an integer will raise a TypeError.
    non_string_input = 123
    render_results_as_table(non_string_input)
    captured = capsys.readouterr()

    assert "Results are not in JSON format." in caplog.text
    assert "Could not render the results as a table. Raw results:" in captured.out
    assert str(non_string_input) in captured.out


@patch('pandas.DataFrame')
def test_render_results_as_table_unexpected_exception(mock_dataframe, capsys, caplog):
    """Tests the catch-all exception handler during rendering."""
    error_message = "Pandas internal error"
    mock_dataframe.side_effect = Exception(error_message)

    json_input = json.dumps([{"id": 1, "name": "Alice"}])
    render_results_as_table(json_input)
    captured = capsys.readouterr()

    assert "An error occurred while rendering the results" in caplog.text
    assert error_message in caplog.text
    assert "Could not render the results as a table. Raw results:" in captured.out
    assert json_input in captured.out