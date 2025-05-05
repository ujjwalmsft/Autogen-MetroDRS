"""
PostPublicUpdateTool.py

Simulates posting a final public-facing message to confirm that metro train
service has been restored. Used by the PublicUpdateAgent.
"""

from typing import Annotated


def post_public_update(
    summary: Annotated[str, "Final public message confirming full service restoration."]
) -> str:
    """
    Simulates publicly announcing that service has resumed.

    Args:
        summary (str): Short, commuter-friendly message.

    Returns:
        str: Confirmation that the message was posted.
    """
    return f"📢 Public update posted: '{summary}'. Thank you for your patience. #MetroServiceResumed"
