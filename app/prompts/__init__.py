"""
__init__.py

Utility to load prompt templates from the /app/prompts directory.
"""

import os
def load_prompt(filename: str) -> str:
    """
    Loads a prompt template file from the prompts directory.

    Args:
        filename (str): Name of the prompt file (e.g., "TrainBreakdownAgent.txt").

    Returns:
        str: Contents of the prompt file.

    Raises:
        FileNotFoundError: If the prompt file does not exist.
    """
    prompt_dir = os.path.dirname(__file__)
    full_path = os.path.join(prompt_dir, filename)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Prompt file not found: {full_path}")

    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()