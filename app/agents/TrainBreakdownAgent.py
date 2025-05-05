"""
TrainBreakdownAgent.py

This agent detects and triggers response to train breakdown events.
Built using AutoGen v0.5.6.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from tools.LogIncidentTool import log_incident
from dotenv import load_dotenv
from config.llm_config import get_llm_config
import os

# Import your client factory
from agents.client import create_model_client_for_agent

load_dotenv()

# Define system behavior for the agent
SYSTEM_MESSAGE = """You are the Train Breakdown Agent.

Your job is to:
- Receive a description of a metro disruption (e.g., station, line, or area).
- Use the log_incident tool to register the event.
- Acknowledge the incident using only tool output. Do not invent facts.

Format your response with "🚨 " at the beginning to indicate it's a critical incident response.
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
    try:
        # Use the centralized client factory
        model_client = create_model_client_for_agent()
        
        print(f"TrainBreakdownAgent model client created using centralized factory")
        
        # Create agent with model_client as required by v0.5.6
        return AssistantAgent(
            name="TrainBreakdownAgent",
            system_message=SYSTEM_MESSAGE,
            model_client=model_client,
            tools=[log_incident_tool]
        )
    except Exception as e:
        print(f"Error creating TrainBreakdownAgent: {e}")
        # Just use the fallback in MetroPlanner instead, so return None
        return None

# Create the agent instance for direct import
TrainBreakdownAgent = create_train_breakdown_agent()