"""
DriverCoordinationAgent.py

This agent is responsible for coordinating standby bus drivers.
Tasks:
- Notify 10 standby drivers to report to the depot
- Confirm that all drivers have acknowledged the request
Built using AutoGen v0.5.6 using AssistantAgent and FunctionTool.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from tools.NotifyDriverTool import notify_driver
from tools.ConfirmDriverAckTool import confirm_driver_ack
from dotenv import load_dotenv
from config.llm_config import get_llm_config
import os

load_dotenv()

# Define system behavior for the agent
SYSTEM_MESSAGE = """You are the Driver Coordination Agent in the metro disruption response system.

Responsibilities:
- Notify 10 standby drivers to report to the depot.
- Confirm all 10 have acknowledged.

Use only the registered tools. Be direct and procedural.
"""

# Initialize the AutoGen-compatible Function wrappers
notify_driver_tool = FunctionTool(
    notify_driver,
    name="notify_driver",
    description="Sends a dispatch message to 10 standby bus drivers."
)

confirm_driver_ack_tool = FunctionTool(
    confirm_driver_ack,
    name="confirm_driver_ack",
    description="Checks how many drivers have acknowledged the request."
)

def create_driver_coordination_agent(llm_config=None):
    """
    Creates and returns a DriverCoordinationAgent instance configured with appropriate tools.
    
    Args:
        llm_config (dict, optional): Configuration for the language model. Defaults to None.
    
    Returns:
        AssistantAgent: The configured DriverCoordinationAgent.
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
        name="DriverCoordinationAgent",
        system_message=SYSTEM_MESSAGE,
        model_client=model_client,
        tools=[notify_driver_tool, confirm_driver_ack_tool]
    )

# Create the agent instance for direct import
DriverCoordinationAgent = create_driver_coordination_agent()