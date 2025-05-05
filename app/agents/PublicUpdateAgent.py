"""
PublicUpdateAgent.py

This agent is responsible for posting a final resolution update to the public,
informing them that normal service has been restored.
Built using AutoGen v0.5.6 using AssistantAgent and FunctionTool.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from tools.PostPublicUpdateTool import post_public_update
from dotenv import load_dotenv
from config.llm_config import get_llm_config
import os

load_dotenv()

# Define system behavior for the agent
SYSTEM_MESSAGE = """You are the Public Update Agent in the metro disruption response system.

Responsibilities:
- Create and post a final update to inform the public that normal service has been restored
- Keep the message positive, clear, and concise
- Include the lines/stations affected and confirmation that they are now operational
- Thank the public for their patience

Use only the registered tool. Be professional and customer-focused.
"""

# Initialize the AutoGen-compatible Function wrapper
post_public_update_tool = FunctionTool(
    post_public_update,
    name="post_public_update",
    description="Posts a final status update informing the public that normal service has been restored."
)

def create_public_update_agent(llm_config=None):
    """
    Creates and returns a PublicUpdateAgent instance configured with appropriate tools.
    
    Args:
        llm_config (dict, optional): Configuration for the language model. Defaults to None.
    
    Returns:
        AssistantAgent: The configured PublicUpdateAgent.
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
        name="PublicUpdateAgent",
        system_message=SYSTEM_MESSAGE,
        model_client=model_client,
        tools=[post_public_update_tool]
    )

# Create the agent instance for direct import
PublicUpdateAgent = create_public_update_agent()