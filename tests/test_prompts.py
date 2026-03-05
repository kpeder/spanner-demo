from spanner.prompts import get_system_prompt


def test_get_system_prompt_success():
    """Tests successful rendering of a system prompt."""
    template = "This is a {} for {}."
    context = ["test", "prompts"]
    expected = "This is a test for prompts."
    result = get_system_prompt(template, context)
    assert result == expected


def test_get_system_prompt_no_context():
    """Tests rendering a system prompt with no context."""
    template = "This is a test."
    result = get_system_prompt(template)
    assert result == "This is a test."


def test_get_system_prompt_error():
    """Tests an error when rendering a system prompt with incorrect context."""
    template = "This is a {}."
    result = get_system_prompt(template, [])
    assert result is None
