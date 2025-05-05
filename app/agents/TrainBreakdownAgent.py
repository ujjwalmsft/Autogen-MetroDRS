"""
TrainBreakdownAgent.py

This agent handles the first step in the metro disruption response flow:
logging a reported train breakdown using a structured tool call.

Built for AutoGen v0.5.6 using AssistantAgent and FunctionTool.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from tools.LogIncidentTool import log_incident
from dotenv import load_dotenv
from config.llm_config import get_llm_config
import os

load_dotenv()
# Define system behavior for the agent
SYSTEM_MESSAGE = """You are the Train Breakdown Agent.

Your job is to:
- Receive a description of a metro disruption (e.g., station, line, or area).
- Use the log_incident tool to register the event.
- Acknowledge the incident using only tool output. Do not invent facts.
"""

# Initialize the AutoGen-compatible Function wrapper
log_incident_tool = FunctionTool(
    log_incident,
    name="log_incident",
    description="Logs a metro train breakdown at a specified location."
)

def create_train_breakdown_agent(llm_config=None):
    """
    Creates and returns a TrainBreakdownAgent instance configured with appropriate tools.
    
    Args:
        llm_config (dict, optional): Configuration for the language model. Defaults to None.
    
    Returns:
        AssistantAgent: The configured TrainBreakdownAgent.
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
        model=llm_config.get('deployment_name'),  # This is needed for GitHub Models
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
        name="TrainBreakdownAgent",
        system_message=SYSTEM_MESSAGE,
        model_client=model_client,
        tools=[log_incident_tool]
    )

# Create the agent instance for direct import
TrainBreakdownAgent = create_train_breakdown_agent()