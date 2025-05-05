"""
SendInternalNotificationTool.py

Simulates notifying internal teams (Control Room, Depot, Bus Operations)
that metro service has been restored after a disruption.
"""

from typing import Annotated


def send_internal_notification(
    summary: Annotated[str, "A brief resolution message for internal teams."]
) -> str:
    """
    Simulates sending a resolution update internally.

    Args:
        summary (str): A message indicating the issue is resolved.

    Returns:
        str: Confirmation message for internal teams.
    """
    return (
        f"📨 Internal notification sent: '{summary}'. "
        "Control Room, Depot, and Bus Operations teams have been informed."
    )
