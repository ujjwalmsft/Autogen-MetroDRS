"""
LogIncidentTool.py

Defines the log_incident function used by TrainBreakdownAgent
to register a train disruption. Wrapped using Function.from_function().
"""

from typing import Annotated


def log_incident(
    location: Annotated[str, "The location (e.g., station or line) where the train breakdown occurred."]
) -> str:
    """
    Simulates logging a metro disruption incident.

    Args:
        location (str): Name of the station or area impacted.

    Returns:
        str: Acknowledgment message.
    """
    return f"🚨 Disruption recorded successfully at: {location}. Further response steps initiated."
