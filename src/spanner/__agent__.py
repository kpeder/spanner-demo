from google.adk.agents.llm_agent import Agent
from google.adk.runners import InMemoryRunner
from google import genai

from spanner.prompts import get_system_prompt, SYSTEM_PROMPT
from spanner.tools import exec_query, fetch_schema

import argparse
import asyncio
import logging
import os


logger = logging.getLogger('spanner.__agent__')


APP_NAME = "spanner_nlp_agent"
USER_PROMPT = "spanner_user"


async def main():
    """A script that initializes an NLP agent with function tools."""

    parser = argparse.ArgumentParser(description="A Spanner query agent using Gemini and Vertex AI.")
    parser.add_argument("--location", required=True, help="The Vertex AI API location (e.g., 'us-central1').")
    parser.add_argument("--model", default="gemini-2.5-flash-lite", help="The name of the Gemini model to use.")
    parser.add_argument("--project", required=True, help="The Google Cloud project ID where the Gemini models are hosted.")
    parser.add_argument("--schema", default="", help="A specific schema to fetch schema elements from.")
    parser.add_argument("--toolbox-url", help="The URL of the toolbox server.")
    parser.add_argument("--no-table", action="store_true", help="Disable rendering query results as a table.")

    args = parser.parse_args()

    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
    os.environ["GOOGLE_GENAI_PROJECT"] = args.project
    os.environ["GOOGLE_GENAI_LOCATION"] = args.location

    system_instruction = get_system_prompt(SYSTEM_PROMPT['NLP_Agent'])

    try:
        agent = Agent(
            model=args.model,
            name=APP_NAME,
            description="A natural language processing agent for Spanner databases.",
            instruction=system_instruction,
            tools=[exec_query, fetch_schema]
        )
    except Exception as e:
        logger.error("An error occurred while creating the agent: %s", e, exc_info=True)

    user = 'spanner_user'

    runner = InMemoryRunner(agent=agent,
                            app_name=APP_NAME)

    session = await runner.session_service.create_session(app_name=APP_NAME, user_id=user)

    print("Spanner agent enabled. Type 'exit', 'quit' or 'stop' to quit.")
    user_prompt = input(f"{USER_PROMPT}: ")

    while user_prompt.lower() not in ['exit', 'quit', 'stop']:
        async for event in runner.run_async(user_id=user,
                                            session_id=session.id,
                                            new_message=genai.types.Content(
                                                role="user",
                                                parts=[
                                                    genai.types.Part(text=user_prompt)
                                                ])):

            if event.content:
                for p in range(len(event.content.parts)):
                    if event.content.parts[p].text:
                        print(f'{event.author}: {event.content.parts[p].text}')

        user_prompt = input(f"{USER_PROMPT}: ")

if __name__ == '__main__':
    asyncio.run(main())
    logging.shutdown()
