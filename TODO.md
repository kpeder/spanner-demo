# TODO List

Here is a list of potential features and improvements for the Spanner Client and AI Toolbox project.

- [ ] **Transform `main` into a `genai` chat interface:** Convert the current one-shot prompt/response script into an interactive chat session, allowing for conversational follow-up questions while maintaining context.
- [ ] **Add support for Spanner Managed MCP Server:** Extend the `tools.py` module to support communication with the Spanner Managed MCP Server, in addition to the locally hosted GenAI Toolbox.
- [ ] **Create alternative prompts:** Extend the prompt module to include other generative features, such as the ability to answer questions about the schema, consult product documentation, or to support alternative dialects (PostgreSQL).
- [ ] **Add support for DML statements:** Enhance the toolset to support DML (`INSERT`, `UPDATE`, `DELETE`) and return the number of affected rows.
- [ ] **Add options to save output:** Include local and cloud-storage output options, such as to a GCS bucket or a Google Drive folder.
- [ ] **Add an option to truncate output:** Since database queries can return a great deal of data, set a default maximum for output to the console.
- [ ] **Add flexible output formats:** Extend the results handling to allow saving output to different formats, such as CSV or JSON, controlled by a command-line flag (e.g., `--output-format csv`).
- [ ] **Improve configuration management:** Introduce a configuration file (e.g., `config.yaml`) to manage settings like project ID, location, and model name, reducing reliance on command-line arguments.
