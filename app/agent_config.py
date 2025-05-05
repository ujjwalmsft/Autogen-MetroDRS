"""
agent_config.py
 
Centralized agent registration and configuration module
for the metro train disruption multi-agent response system.
"""
 
from agents.TrainBreakdownAgent import TrainBreakdownAgent
from agents.DriverCoordinationAgent import DriverCoordinationAgent
from agents.DepotMaintenanceAgent import DepotMaintenanceAgent
from agents.PublicCommunicationAgent import PublicCommunicationAgent
from agents.IncidentResolutionAgent import IncidentResolutionAgent
from agents.InternalNotificationAgent import InternalNotificationAgent
from agents.PublicUpdateAgent import PublicUpdateAgent
 
# Global list of initialized agents
# (In practice, these can be managed by a planner or passed to an orchestrator)
agents = {
    "TrainBreakdownAgent": TrainBreakdownAgent(),
    "DriverCoordinationAgent": DriverCoordinationAgent(),
    "DepotMaintenanceAgent": DepotMaintenanceAgent(),
    "PublicCommunicationAgent": PublicCommunicationAgent(),
    "IncidentResolutionAgent": IncidentResolutionAgent(),
    "InternalNotificationAgent": InternalNotificationAgent(),
    "PublicUpdateAgent": PublicUpdateAgent()
}
 
def get_agent(name: str):
    """
    Retrieve an agent by its name.
 
    Args:
        name (str): Name of the registered agent.
 
    Returns:
        ConversableAgent: Instance of the agent.
 
    Raises:
        ValueError: If the agent name is not registered.
    """
    if name not in agents:
        raise ValueError(f"Agent '{name}' is not registered.")
    return agents[name]
 
def list_agents():
    """
    Returns a list of all registered agent names.
    """
    return list(agents.keys())