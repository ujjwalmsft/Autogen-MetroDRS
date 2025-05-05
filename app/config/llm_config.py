"""
llm_config.py

Centralized utility to load LLM configuration for AutoGen agents
using Azure OpenAI settings from environment variables.
"""

import os
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

def get_llm_config() -> dict:
    """
    Returns a config_list compatible with AutoGen.

    Required ENV variables:
    - AZURE_OPENAI_API_KEY
    - AZURE_OPENAI_ENDPOINT
    - AZURE_OPENAI_DEPLOYMENT_NAME
    - AZURE_OPENAI_API_VERSION (optional, defaults to 2023-07-01-preview)

    Returns:
        dict: Configuration to be used by AutoGen LLM agents
    """
    return {
        "config_list": [
            {
                "model": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),  # e.g., "gpt-35-turbo"
                "api_type": "azure",
                "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
                "api_base": os.getenv("AZURE_OPENAI_ENDPOINT"),
                "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2023-07-01-preview")
            }
        ]
    }
