"""
DraftSocialPostTool.py

Simulates creating a short, public-facing message about the metro disruption.
The message is designed to fit within 280 characters (e.g., for X/Twitter).
"""
#
# from autogen_agentchat.function_calling_tool import FunctionCallingTool
from typing import Annotated


def draft_social_post(
    disruption_info: Annotated[str, "Summary of the disruption including location, delay, and shuttle availability."]
) -> str:
    """
    Generates a public-facing disruption update message.

    Args:
        disruption_info (str): Short description of what commuters should know.

    Returns:
        str: A message under 280 characters for public posting.
    """
    base_message = (
        f"⚠️ Service Alert: {disruption_info}. "
        "Shuttle buses have been deployed. We apologize for the inconvenience. #MetroUpdate"
    )

    return base_message if len(base_message) <= 280 else base_message[:277] + "..."


# draft_social_post_tool = FunctionCallingTool(
#     name="draft_social_post",
#     description="Creates a 280-character message about the metro disruption for public posting.",
#     func=draft_social_post
# )
