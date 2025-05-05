"""
PublicCommunicationAgent.py

This file defines the PublicCommunicationAgent, which is responsible for
generating a public announcement in the event of train disruptions.
Built using AutoGen v0.5.6 using AssistantAgent and FunctionTool.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from tools.DraftSocialPostTool import draft_social_post
from dotenv import load_dotenv
from config.llm_config import get_llm_config
import os

load_dotenv()

# Define system behavior for the agent
SYSTEM_MESSAGE = """You are the Public Communication Agent in the metro disruption response system.

Responsibilities:
- Draft clear and concise social media posts about service disruptions
- Ensure messages contain essential information (location, alternative routes, estimated duration)
- Use a professional but reassuring tone suitable for social media platforms
- Keep messages concise while including all critical details

Use only the registered tools. Be direct and informative.
"""

# Initialize the AutoGen-compatible Function wrapper
draft_social_post_tool = FunctionTool(
    draft_social_post,
    name="draft_social_post",
    description="Creates a social media post about train service disruptions."
)

def create_public_communication_agent(llm_config=None):
    """
    Creates and returns a PublicCommunicationAgent instance configured with appropriate tools.
    
    Args:
        llm_config (dict, optional): Configuration for the language model. Defaults to None.
    
    Returns:
        AssistantAgent: The configured PublicCommunicationAgent.
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
        name="PublicCommunicationAgent",
        system_message=SYSTEM_MESSAGE,
        model_client=model_client,
        tools=[draft_social_post_tool]
    )

# Create the agent instance for direct import
PublicCommunicationAgent = create_public_communication_agent()