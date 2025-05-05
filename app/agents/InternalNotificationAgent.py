"""
InternalNotificationAgent.py

This agent sends a resolution update to internal stakeholders
(Control Room, Depot Ops, Bus Coordination) once the issue is resolved.
Built using AutoGen v0.5.6 using AssistantAgent and FunctionTool.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from tools.SendInternalNotificationTool import send_internal_notification
from dotenv import load_dotenv
from config.llm_config import get_llm_config
import os

load_dotenv()

# Define system behavior for the agent
SYSTEM_MESSAGE = """You are the Internal Notification Agent in the metro disruption response system.

Responsibilities:
- Send clear notifications to internal stakeholders about incident resolution
- Include all relevant details about the resolution status
- Ensure proper distribution to Control Room, Depot Operations, and Bus Coordination teams

Use only the registered tool. Be clear, concise, and factual.
"""

# Initialize the AutoGen-compatible Function wrapper
send_internal_notification_tool = FunctionTool(
    send_internal_notification,
    name="send_internal_notification",
    description="Sends notification to internal metro operations teams about incident resolution."
)

def create_internal_notification_agent(llm_config=None):
    """
    Creates and returns an InternalNotificationAgent instance configured with appropriate tools.
    
    Args:
        llm_config (dict, optional): Configuration for the language model. Defaults to None.
    
    Returns:
        AssistantAgent: The configured InternalNotificationAgent.
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
        name="InternalNotificationAgent",
        system_message=SYSTEM_MESSAGE,
        model_client=model_client,
        tools=[send_internal_notification_tool]
    )

# Create the agent instance for direct import
InternalNotificationAgent = create_internal_notification_agent()