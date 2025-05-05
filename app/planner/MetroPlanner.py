"""
MetroPlanner.py

Main orchestrator for the metro disruption response using AutoGen v0.5.6.
Uses RoundRobinGroupChat to run a full, automated workflow that follows
the sequence specified in the metro disruption response workflow.
"""

# Import concrete implementations instead of abstract base classes
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.agents import UserProxyAgent, AssistantAgent
from autogen_core import CancellationToken

# Import system messages and tools instead of agent instances
from agents.TrainBreakdownAgent import SYSTEM_MESSAGE as TRAIN_SYSTEM_MESSAGE, log_incident_tool
from agents.DriverCoordinationAgent import SYSTEM_MESSAGE as DRIVER_SYSTEM_MESSAGE, notify_driver_tool, confirm_driver_ack_tool
from agents.DepotMaintenanceAgent import SYSTEM_MESSAGE as DEPOT_SYSTEM_MESSAGE, notify_depot_tool, confirm_bus_readiness_tool
from agents.PublicCommunicationAgent import SYSTEM_MESSAGE as PUBLIC_COMM_SYSTEM_MESSAGE, draft_social_post_tool
from agents.IncidentResolutionAgent import SYSTEM_MESSAGE as INCIDENT_SYSTEM_MESSAGE, check_incident_status_tool
from agents.InternalNotificationAgent import SYSTEM_MESSAGE as INTERNAL_SYSTEM_MESSAGE, send_internal_notification_tool
from agents.PublicUpdateAgent import SYSTEM_MESSAGE as PUBLIC_UPDATE_SYSTEM_MESSAGE, post_public_update_tool

from config.llm_config import get_llm_config
import os

# Import the client factory that actually works
from agents.client import create_model_client_for_agent, get_working_azure_client


class MetroPlanner:
    """
    Coordinates a metro incident response using RoundRobinGroupChat and AssistantAgents.
    Each agent is triggered in sequence to handle a specific part of the incident response.
    """

    def __init__(self, llm_config=None):
        self.llm_config = llm_config or get_llm_config()
        
        # Store incident description for non-interactive input
        self.incident_description = None

        # First verify that the Azure OpenAI client works directly
        try:
            client = get_working_azure_client()
            print("Verified working Azure OpenAI client connection")
        except Exception as e:
            print(f"Warning: Azure OpenAI direct client failed: {e}")
        
        # Create a shared model client for all agents
        try:
            # Get a shared model client to use for all agents
            model_client = create_model_client_for_agent()
            print(f"Created shared model client for all agents")
            
            # System initiator with corrected parameters
            self.user_proxy = UserProxyAgent(
                name="UserProxyAgent",
                description="A system user initiating the metro disruption response.",
                input_func=self._non_interactive_input  # Use a non-interactive input function
            )
            
            # Create all agents with the same model client
            self.train_breakdown_agent = AssistantAgent(
                name="TrainBreakdownAgent",
                system_message=TRAIN_SYSTEM_MESSAGE,
                model_client=model_client,
                tools=[log_incident_tool]
            )
            
            self.driver_coordination_agent = AssistantAgent(
                name="DriverCoordinationAgent",
                system_message=DRIVER_SYSTEM_MESSAGE,
                model_client=model_client,
                tools=[notify_driver_tool, confirm_driver_ack_tool]
            )
            
            self.depot_maintenance_agent = AssistantAgent(
                name="DepotMaintenanceAgent",
                system_message=DEPOT_SYSTEM_MESSAGE,
                model_client=model_client,
                tools=[notify_depot_tool, confirm_bus_readiness_tool]
            )
            
            self.public_communication_agent = AssistantAgent(
                name="PublicCommunicationAgent",
                system_message=PUBLIC_COMM_SYSTEM_MESSAGE,
                model_client=model_client,
                tools=[draft_social_post_tool]
            )
            
            self.incident_resolution_agent = AssistantAgent(
                name="IncidentResolutionAgent",
                system_message=INCIDENT_SYSTEM_MESSAGE,
                model_client=model_client,
                tools=[check_incident_status_tool]
            )
            
            self.internal_notification_agent = AssistantAgent(
                name="InternalNotificationAgent",
                system_message=INTERNAL_SYSTEM_MESSAGE,
                model_client=model_client,
                tools=[send_internal_notification_tool]
            )
            
            self.public_update_agent = AssistantAgent(
                name="PublicUpdateAgent",
                system_message=PUBLIC_UPDATE_SYSTEM_MESSAGE,
                model_client=model_client,
                tools=[post_public_update_tool]
            )
            
            # List of all agents - order matters for RoundRobinGroupChat
            self.agents = [
                self.user_proxy,
                self.train_breakdown_agent,
                self.driver_coordination_agent,
                self.depot_maintenance_agent,
                self.public_communication_agent,
                self.incident_resolution_agent,
                self.internal_notification_agent,
                self.public_update_agent
            ]
            
            # Use RoundRobinGroupChat for ordered execution
            self.team = RoundRobinGroupChat(
                participants=self.agents,
                max_turns=20  # Setting the maximum number of turns
            )
        
        except Exception as e:
            import traceback
            print(f"Error setting up agents: {e}")
            print(traceback.format_exc())
            raise

    # Add a non-interactive input function that returns the incident description
    async def _non_interactive_input(self, prompt, cancellation_token=None):
        """Non-interactive input function that returns the stored incident description."""
        return self.incident_description

    async def run(self, incident_description: str) -> dict:
        """
        Executes the multi-agent workflow with the given disruption input.
        Returns a formatted response that matches the workflow specification.

        Args:
            incident_description (str): Description of the train disruption

        Returns:
            dict: Formatted response with status and steps
        """
        # Store the incident description for the input function
        self.incident_description = incident_description
        
        try:
            # Use the team's run method directly
            print(f"Running team with input: {incident_description}")
            result = await self.team.run(task=incident_description)
            
            # Process the messages from the result with enhanced formatting
            steps = []
            
            for msg in result.messages:
                # Only include messages from our agents (not the user proxy)
                if hasattr(msg, "source") and msg.source != "UserProxyAgent":
                    # Format the content based on agent type
                    agent_name = msg.source
                    content = msg.content
                    
                    # Add appropriate emoji prefixes based on agent type
                    if "TrainBreakdownAgent" in agent_name:
                        formatted_name = "TrainBreakdownAgent"
                        if not content.startswith("🚨"):
                            content = f"🚨 {content}"
                    
                    elif "DriverCoordinationAgent" in agent_name:
                        formatted_name = "DriverCoordinationAgent"
                        if not content.startswith("📣"):
                            content = f"📣 {content}"
                    
                    elif "DepotMaintenanceAgent" in agent_name:
                        formatted_name = "DepotMaintenanceAgent"
                        if not content.startswith("🚍"):
                            content = f"🚍 {content}"
                    
                    elif "PublicCommunicationAgent" in agent_name:
                        formatted_name = "PublicCommunicationAgent"
                        if not content.startswith("⚠️"):
                            content = f"⚠️ {content}"
                    
                    elif "IncidentResolutionAgent" in agent_name:
                        formatted_name = "IncidentResolutionAgent"
                        if not content.startswith("✅"):
                            content = f"✅ {content}"
                    
                    elif "InternalNotificationAgent" in agent_name:
                        formatted_name = "InternalNotificationAgent"
                        if not content.startswith("📨"):
                            content = f"📨 {content}"
                    
                    elif "PublicUpdateAgent" in agent_name:
                        formatted_name = "PublicUpdateAgent"
                        if not content.startswith("📢"):
                            content = f"📢 {content}"
                    else:
                        formatted_name = agent_name
                    
                    # Add to steps with formatted name and content
                    steps.append({
                        "name": formatted_name,
                        "content": content
                    })
            
            # Return the final structured response
            return {
                "status": "completed",
                "steps": steps
            }
        except Exception as e:
            import traceback
            print(f"Error running team: {e}")
            print(traceback.format_exc())
            
            # Fall back to debug/mock data for frontend testing
            return {
                "status": "error",
                "message": str(e),
                "steps": self._generate_fallback_steps(incident_description)
            }
    
    def _generate_fallback_steps(self, incident_text):
        """Generates fallback response steps when the real system fails"""
        import re
        
        # Extract location if possible
        location_match = re.search(r'at\s+([A-Za-z\s]+(?:Station|Line|Terminal))', incident_text, re.IGNORECASE)
        if not location_match:
            location_match = re.search(r'near\s+([A-Za-z\s]+(?:Station|Line|Terminal))', incident_text, re.IGNORECASE)
        if not location_match:
            location_match = re.search(r'at\s+([A-Za-z\s]+)', incident_text, re.IGNORECASE)
        location = location_match.group(1) if location_match else "the reported location"
        
        # Extract line name if mentioned
        line_match = re.search(r'(Green|Red|Blue|Yellow|East-West|North-South)\s+Line', incident_text, re.IGNORECASE)
        line_name = line_match.group(0) if line_match else "the affected line"
        
        # Create steps with the extracted location and line name
        return [
            {
                "name": "TrainBreakdownAgent",
                "content": f"🚨 Incident logged successfully at {location}. Disruption response initiated."
            },
            {
                "name": "DriverCoordinationAgent",
                "content": "📣 Notification sent to 10 drivers. 8/10 confirmed. Still waiting on 2 responses..."
            },
            {
                "name": "DepotMaintenanceAgent",
                "content": "🚍 Maintenance team notified to prepare 10 buses. Depot confirmed all buses are ready for deployment."
            },
            {
                "name": "PublicCommunicationAgent", 
                "content": f"⚠️ Draft social media post: 'Service disruption on {line_name} at {location}. Shuttle buses are being arranged. We apologize for the inconvenience.'"
            },
            {
                "name": "IncidentResolutionAgent",
                "content": f"✅ System check complete. No remaining disruptions detected at {location}. Ready to proceed with clearance notification."
            },
            {
                "name": "InternalNotificationAgent",
                "content": "📨 All internal teams notified of incident resolution. Acknowledged by: Control Room, Bus Ops, Maintenance."
            },
            {
                "name": "PublicUpdateAgent",
                "content": f"📢 Public notice posted: 'Train services at {location} have resumed. Thank you for your patience.' Published on Twitter, Facebook, and IG."
            }
        ]