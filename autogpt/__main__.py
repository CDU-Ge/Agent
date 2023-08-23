"""Auto-GPT: A GPT powered AI Assistant"""
import os
import pathlib

import dotenv
import openai

import autogpt.app.cli


def setup():
    env = pathlib.Path(__file__).parent.parent / ".env"
    if not env.exists():
        raise RuntimeError
    dotenv.load_dotenv(env)
    if openai_proxy := os.environ.get("OPENAI_PROXY", None):
        openai.proxy = openai_proxy
    if openai_key := os.environ.get("OPENAI_API_KEY", None):
        openai.api_key = openai_key


if __name__ == "__main__":
    setup()
    autogpt.app.cli.main()
