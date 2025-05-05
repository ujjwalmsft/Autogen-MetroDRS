"""
IncidentResolutionAgent.py

This agent verifies whether the reported train disruption has been resolved.
It uses a tool to query and confirm operational status.
Built using AutoGen v0.5.6 using AssistantAgent and FunctionTool.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from tools.CheckIncidentStatusTool import check_incident_status
from dotenv import load_dotenv
from config.llm_config import get_llm_config
import os

load_dotenv()

# Define system behavior for the agent
SYSTEM_MESSAGE = """You are the Incident Resolution Agent in the metro disruption response system.

Responsibilities:
- Verify whether the reported train disruption has been fully resolved
- Confirm that normal operations have been restored
- Report the verification results clearly

Use only the registered tool. Be direct and factual. Do not guess or invent information.
"""

# Initialize the AutoGen-compatible Function wrapper
check_incident_status_tool = FunctionTool(
    check_incident_status,
    name="check_incident_status",
    description="Verifies whether a reported metro disruption has been resolved."
)

def create_incident_resolution_agent(llm_config=None):
    """
    Creates and returns an IncidentResolutionAgent instance configured with appropriate tools.
    
    Args:
        llm_config (dict, optional): Configuration for the language model. Defaults to None.
    
    Returns:
        AssistantAgent: The configured IncidentResolutionAgent.
    """
    # Get default config if none provided
    if llm_config is None:
        llm_config = get_llm_config()
    
    # Create a model client using the Azure configuration
    from autogen_ext.models.azure import AzureAIChatCompletionClient
    from azure.core.credentials import AzureKeyCredential
    print(os.getenv('AZURE_OPENAI_ENDPOINT'))
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
        name="IncidentResolutionAgent",
        system_message=SYSTEM_MESSAGE,
        model_client=model_client,
        tools=[check_incident_status_tool]
    )

# Create the agent instance for direct import
IncidentResolutionAgent = create_incident_resolution_agent()