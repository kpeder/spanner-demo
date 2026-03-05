# Spanner Client and AI Toolbox
This project contains a demo package that enables AI interactions with a Spanner database using MCP integration made available via the GenAI Toolbox, published by Google.

Alternative MCP Server implementations include [Developer Knowledge](https://developers.google.com/knowledge/mcp) and [Spanner](https://docs.cloud.google.com/spanner/docs/use-spanner-mcp) Managed MCP Servers. These implementations are enterprise ready but may incur additional costs. This package does not yet support these implementations.

## Compatibility
This demo is tested on Ubuntu Linux 24.04 (x86_64). It's expected to work on compatible versions of MacOS.

## Getting Started

1. If necessary, install Astral uv, instructions [here](https://docs.astral.sh/uv/getting-started/installation/).
1. Clone this repository:

    ```git clone git@github.com:kpeder/spanner-demo.git```

    ```$ cd spanner-demo```

1. Set up a virtual environment and install the required packages:

    ```uv venv --system-site-packages --python 3.12```

    ```$ uv sync```

1. If necessary, install gcloud, instructions [here](https://cloud.google.com/sdk/docs/install).
1. Get authenticated and configure your project:

    ```$ gcloud auth application-default login```

    ```$ gcloud auth application-default set-quota-project [your-project-id]```

    ```$ gcloud config set project [your-project-id]```

    ```$ gcloud services enable aiplatform.googleapis.com logging.googleapis.com spanner.googleapis.com```

1. Create a Spanner instance:

    ```$ gcloud spanner instances create spanner --config=regional-northamerica-northeast1 --edition=ENTERPRISE --processing-units=100```

1. Create a database and load test data using the [UI](https://console.cloud.google.com/spanner/instances/spanner/details/databases). Click the `Explore datasets` link, select `Retail`, and click the `Create database` button.

1. Install the GenAI Toolbox, instructions [here](https://googleapis.github.io/genai-toolbox/getting-started/local_quickstart/).
1. Start a toolbox server with your configuration:

    ```$ toolbox --tools-file toolbox/tools.yaml &```

    Example configurations are found in the toolbox directory. In particular, the spanner project must be updated.

1. Run the main module:

    ```$ uv run python3 -m spanner --project vertex-ai-experiments-448517 --location us-east1 --model gemini-2.5-flash```

    This command will prompt you to ask a question about the dataset, generate a GoogleSQL query, and offer to run it for you against the database.
