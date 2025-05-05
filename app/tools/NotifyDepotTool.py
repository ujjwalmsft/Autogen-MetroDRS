"""
NotifyDepotTool.py

This tool simulates notifying the depot team to prepare 10 standby buses
in response to a service disruption.
"""

from typing import Annotated


def notify_depot(
    operation: Annotated[str, "Brief description of the disruption or location requiring bus dispatch."]
) -> str:
    """
    Simulates a request to the depot to prepare standby buses.

    Args:
        operation (str): The reason or context for the bus preparation request.

    Returns:
        str: Confirmation message.
    """
    return f"🛠️ Depot has been notified to prepare 10 standby buses for: {operation}."
