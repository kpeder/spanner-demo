from spanner.prompts import get_system_prompt, SYSTEM_PROMPT
from spanner.tools import fetch_schema

from google import genai

import argparse
import asyncio
import logging


logger = logging.getLogger('spanner.examples.genai_nlp_to_sql')


async def main():
    """An example script that fetches schema info, loads a Gemini model, and one shot prompts the model."""

    parser = argparse.ArgumentParser(description="A Spanner query agent using Gemini and Vertex AI.")
    parser.add_argument("--filter", default="%", help="A string filter to match against table names. Uses the '%' wildcard.")
    parser.add_argument("--location", required=True, help="The Vertex AI API location (e.g., 'us-central1').")
    parser.add_argument("--model", default="gemini-2.5-flash-lite", help="The name of the Gemini model to use.")
    parser.add_argument("--project", required=True, help="The Google Cloud project ID where the Gemini models are hosted.")
    parser.add_argument("--prompt", required=True, help="The prompt to send to the model.")
    parser.add_argument("--stable-api", action="store_true", help="Use the stable instead of the beta API.")

    args = parser.parse_args()

    if args.stable_api:
        http_options = genai.types.HttpOptions(api_version='v1')
    else:
        http_options = None

    system_instruction = get_system_prompt(SYSTEM_PROMPT['NLP_to_SQL'], [fetch_schema(filter=args.filter)])

    with genai.Client(vertexai=True, project=args.project, location=args.location, http_options=http_options) as client:

        response = client.models.generate_content(
            model=args.model,
                contents=
                    [
                        genai.types.Part.from_text(text=args.prompt)
                    ],
                config=genai.types.GenerateContentConfig(
                    temperature=0.0,
                    top_p=0.3,
                    top_k=6,
                    max_output_tokens=1024,
                    system_instruction=[system_instruction]
                )
        )

        print(response.text)


if __name__ == '__main__':
    asyncio.run(main())
    logging.shutdown()
