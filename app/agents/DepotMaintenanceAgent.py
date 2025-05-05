"""
DepotMaintenanceAgent.py

This agent handles coordination with the depot to prepare and confirm
standby bus availability. Built using AutoGen v0.5.6.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from tools.NotifyDepotTool import notify_depot
from tools.ConfirmBusReadinessTool import confirm_bus_readiness
from dotenv import load_dotenv
from config.llm_config import get_llm_config
import os

load_dotenv()

# Define system behavior for the agent
SYSTEM_MESSAGE = """You are the Depot Maintenance Agent in the metro disruption response system.

Responsibilities:
- Notify the depot to prepare 10 standby buses
- Confirm all 10 buses are ready for deployment

Use only the registered tools. Be direct and procedural.
"""

# Initialize the AutoGen-compatible Function wrappers
notify_depot_tool = FunctionTool(
    notify_depot,
    name="notify_depot",
    description="Notifies the depot to prepare 10 standby buses."
)

confirm_bus_readiness_tool = FunctionTool(
    confirm_bus_readiness,
    name="confirm_bus_readiness",
    description="Checks if all 10 standby buses are ready for deployment."
)

def create_depot_maintenance_agent(llm_config=None):
    """
    Creates and returns a DepotMaintenanceAgent instance configured with appropriate tools.
    
    Args:
        llm_config (dict, optional): Configuration for the language model. Defaults to None.
    
    Returns:
        AssistantAgent: The configured DepotMaintenanceAgent.
    """
    # Get default config if none provided
    if llm_config is None:
        llm_config = get_llm_config()
    
    # Create a model client using the Azure configuration
    from autogen_ext.models.azure import AzureAIChatCompletionClient
    from azure.core.credentials import AzureKeyCredential
    
    model_client = AzureAIChatCompletionClient(
        endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
        credential=AzureKeyCredential(os.getenv('AZURE_OPENAI_API_KEY')),
        model=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),  # This is needed for GitHub Models
        model_info={
            "json_output": False,
            "function_calling": True,  # Enable function calling for tools
            "vision": False,
            "family": "unknown",
            "structured_output": False
        }
    )
    
    # Return the configured agent with the model_client
    return AssistantAgent(
        name="DepotMaintenanceAgent",
        system_message=SYSTEM_MESSAGE,
        model_client=model_client,
        tools=[notify_depot_tool, confirm_bus_readiness_tool]
    )

# Create the agent instance for direct import
DepotMaintenanceAgent = create_depot_maintenance_agent()