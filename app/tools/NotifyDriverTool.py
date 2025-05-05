"""
NotifyDriverTool.py

Defines a tool function that simulates sending a dispatch message
to 10 standby bus drivers. This function is registered via
Function.from_function() in the DriverCoordinationAgent.
"""

from typing import Annotated


def notify_driver(
    message: Annotated[str, "The dispatch message to be sent to 10 standby drivers."]
) -> str:
    """
    Simulates notifying drivers of a dispatch order.

    Args:
        message (str): Content of the message to be sent to drivers.

    Returns:
        str: Confirmation that the message was delivered.
    """
    return f"📣 Notification sent to 10 standby drivers: '{message}'. Awaiting acknowledgments."
