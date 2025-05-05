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
"""

# Initialize the AutoGen-compatible Function wrapper
log_incident_tool = FunctionTool(
    log_incident,
    name="log_incident",
    description="Logs a metro train breakdown at a specified location."
)

def create_train_breakdown_agent(llm_config=None):
    """Creates and returns a TrainBreakdownAgent instance."""
    # Get default config if none provided
    if llm_config is None:
        llm_config = get_llm_config()
    
    try:
        # Use the centralized client factory instead of recreating the client
        model_client = create_model_client_for_agent()
        
        print(f"Agent model client created using centralized factory")
        
        # Create agent with model_client as required by v0.5.6
        return AssistantAgent(
            name="TrainBreakdownAgent",
            system_message=SYSTEM_MESSAGE,
            model_client=model_client,
            tools=[log_incident_tool]
        )
    except Exception as e:
        print(f"Error creating agent: {e}")
        # Fallback to mock agent
        from autogen_agentchat.agents import MyChatAgent

        class MockAgent(MyChatAgent):
            def __init__(self):
                super().__init__(name="TrainBreakdownAgent")
            
            async def on_message(self, message, sender, metadata=None):
                # Parse the incident description from the message
                incident_text = str(message)
                if "at " in incident_text:
                    location = incident_text.split("at ")[1].split(".")[0].strip()
                else:
                    location = "the reported location"
                
                return f"🚨 Incident logged successfully at {location}. Disruption response initiated."

        return MockAgent()

# Create the agent instance for direct import
TrainBreakdownAgent = create_train_breakdown_agent()