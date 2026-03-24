from spanner.prompts import get_system_prompt, SYSTEM_PROMPT
from spanner.tools import exec_query, fetch_schema
from spanner.results import render_results_as_table

from google import genai

import argparse
import asyncio
import logging


logger = logging.getLogger('spanner.examples.genai_nlp_to_sql')


async def main():
    """A script that fetches schema info, loads a Gemini model, and one shot prompts the model."""

    parser = argparse.ArgumentParser(description="A Spanner query agent using Gemini and Vertex AI.")
    parser.add_argument("--filter", default="%", help="A string filter to match against table names. Uses the '%' wildcard.")
    parser.add_argument("--location", required=True, help="The Vertex AI API location (e.g., 'us-central1').")
    parser.add_argument("--model", default="gemini-2.5-flash-lite", help="The name of the Gemini model to use.")
    parser.add_argument("--project", required=True, help="The Google Cloud project ID where the Gemini models are hosted.")
    parser.add_argument("--prompt", help="The prompt to send to the model.")
    parser.add_argument("--schema", default="", help="A specific schema to fetch schema elements from.")
    parser.add_argument("--stable-api", action="store_true", help="Use the stable instead of the beta API.")
    parser.add_argument("--toolbox-url", help="The URL of the toolbox server.")
    parser.add_argument("--no-table", action="store_true", help="Disable rendering query results as a table.")

    args = parser.parse_args()

    if args.stable_api:
        http_options = genai.types.HttpOptions(api_version='v1')
    else:
        http_options = None

    if args.prompt:
        user_prompt = args.prompt
    else:
        user_prompt = input("Enter your question: ")

    fetch_schema_opts = {"filter": args.filter, "schema": args.schema}
    if args.toolbox_url:
        fetch_schema_opts["url"] = args.toolbox_url

    system_instruction = get_system_prompt(SYSTEM_PROMPT['NLP_to_SQL'], [fetch_schema(**fetch_schema_opts)])

    with genai.Client(vertexai=True, project=args.project, location=args.location, http_options=http_options) as client:

        response = client.models.generate_content(
            model=args.model,
            contents=[
                genai.types.Part.from_text(text=user_prompt)
            ],
            config=genai.types.GenerateContentConfig(
                temperature=0.0,
                top_p=0.3,
                top_k=6,
                max_output_tokens=1024,
                system_instruction=[system_instruction]
            )
        )

        generated_sql = response.text
        print("Generated SQL:")
        print(generated_sql)

        run_query = input("Would you like to run this query? (y/N): ").lower().strip()
        if run_query == 'y':
            query_opts = {"query": generated_sql}
            if args.toolbox_url:
                query_opts["url"] = args.toolbox_url
            print("Executing query...")
            results = exec_query(**query_opts)
            if not args.no_table:
                render_results_as_table(results)
            else:
                print("Query Results (raw):")
                print(results)


if __name__ == '__main__':
    asyncio.run(main())
    logging.shutdown()
