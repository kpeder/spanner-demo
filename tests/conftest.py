import yaml
import pytest


def pytest_addoption(parser):
    """Adds command-line options for integration tests."""
    parser.addoption(
        "--project", action="store", help="Global project for integration tests (overridable)."
    )
    parser.addoption(
        "--location", action="store", help="Global location for integration tests (overridable)."
    )
    parser.addoption(
        "--spanner-project", action="store", help="Spanner project for integration tests."
    )
    parser.addoption(
        "--spanner-instance", action="store", help="Spanner instance for integration tests."
    )
    parser.addoption(
        "--spanner-database", action="store", help="Spanner database for integration tests."
    )
    parser.addoption(
        "--vertexai-project", action="store", help="Vertex AI project for integration tests."
    )
    parser.addoption(
        "--vertexai-location", action="store", help="Vertex AI location for integration tests."
    )
    parser.addoption(
        "--vertexai-model-name", action="store", help="Vertex AI model name for integration tests."
    )
    parser.addoption(
        "--toolbox-url", action="store", help="Toolbox server URL for integration tests."
    )


@pytest.fixture(scope="session")
def config(request):
    """Reads the test configuration, allowing command-line overrides."""
    with open("tests/config.yaml", "r") as f:
        config_data = yaml.safe_load(f)

    if "spanner" not in config_data:
        config_data["spanner"] = {}
    if "vertexai" not in config_data:
        config_data["vertexai"] = {}
    if "toolbox" not in config_data:
        config_data["toolbox"] = {}

    # Override config file with command-line arguments if provided;
    # global arguments are overridable by service-specific arguments,
    # for example --spanner-project overrides --project
    if project_override := request.config.getoption("--project"):
        config_data["spanner"]["project"] = project_override
        config_data["vertexai"]["project"] = project_override

    if location_override := request.config.getoption("--location"):
        config_data["vertexai"]["location"] = location_override

    if spanner_project_override := request.config.getoption("--spanner-project"):
        config_data["spanner"]["project"] = spanner_project_override

    if spanner_instance_override := request.config.getoption("--spanner-instance"):
        config_data["spanner"]["instance"] = spanner_instance_override

    if spanner_database_override := request.config.getoption("--spanner-database"):
        config_data["spanner"]["database"] = spanner_database_override

    if vertexai_project_override := request.config.getoption("--vertexai-project"):
        config_data["vertexai"]["project"] = vertexai_project_override

    if vertexai_location_override := request.config.getoption("--vertexai-location"):
        config_data["vertexai"]["location"] = vertexai_location_override

    if vertexai_model_name_override := request.config.getoption("--vertexai-model-name"):
        config_data["vertexai"]["model_name"] = vertexai_model_name_override

    if toolbox_url_override := request.config.getoption("--toolbox-url"):
        config_data["toolbox"]["url"] = toolbox_url_override

    return config_data


@pytest.fixture(scope="session")
def spanner_config(config):
    """Returns the Spanner-specific configuration."""
    return config["spanner"]


@pytest.fixture(scope="session")
def vertexai_config(config):
    """Returns the Vertex AI-specific configuration."""
    return config["vertexai"]


@pytest.fixture(scope="session")
def toolbox_config(config):
    """Returns the Toolbox-specific configuration."""
    return config["toolbox"]
