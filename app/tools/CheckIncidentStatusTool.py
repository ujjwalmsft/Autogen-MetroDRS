"""
CheckIncidentStatusTool.py

Simulates querying metro operational systems to confirm whether
a reported disruption has been resolved. Used by IncidentResolutionAgent.
"""

from typing import Annotated


def check_incident_status(
    location: Annotated[str, "The affected station or location to check for resolution status."]
) -> dict:
    """
    Simulates checking if train service has resumed at a specific location.

    Args:
        location (str): Name of the disrupted station or metro line.

    Returns:
        dict: Contains resolution status and a human-readable message.
    """
    # Simulated fixed response
    resolved = True
    return {
        "resolved": resolved,
        "message": f"✅ Normal train service has resumed at {location}."
    }
