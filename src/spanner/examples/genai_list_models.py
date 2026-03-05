from google import genai

import argparse
import logging


logger = logging.getLogger('spanner.examples.genai_get_schema_tool')


def main():
    """An example script that loads a Gemini model, creates a chat session, and registers the fetch_schema tool for the model to use."""

    parser = argparse.ArgumentParser(description="A Spanner query agent using Gemini and Vertex AI.")
    parser.add_argument("--location", required=True, help="The Google Cloud location (e.g., 'us-central1').")
    parser.add_argument("--project", required=True, help="The Google Cloud project ID.")
    parser.add_argument("--stable-api", action="store_true", help="Use the stable instead of the beta API.")

    args = parser.parse_args()

    if args.stable_api:
        http_options = genai.types.HttpOptions(api_version='v1')
    else:
        http_options = None

    with genai.Client(vertexai=True, project=args.project, location=args.location, http_options=http_options) as client:

        logger.info("Listing available models...")
        for model in client.models.list():
            print(model.name)


if __name__ == '__main__':
    main()
    logging.shutdown()
