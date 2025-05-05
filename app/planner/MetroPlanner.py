import asyncio
import re
import traceback
from typing import List, Dict, Any
from dotenv import load_dotenv
from config.llm_config import get_llm_config

# Import the agents
from agents.TrainBreakdownAgent import TrainBreakdownAgent
from agents.DriverCoordinationAgent import DriverCoordinationAgent
from agents.DepotMaintenanceAgent import DepotMaintenanceAgent
from agents.PublicCommunicationAgent import PublicCommunicationAgent
from agents.IncidentResolutionAgent import IncidentResolutionAgent
from agents.InternalNotificationAgent import InternalNotificationAgent
from agents.PublicUpdateAgent import PublicUpdateAgent

# Import the group chat from autogen
from autogen_agentchat.agents import UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat

load_dotenv()

class MetroPlanner:
    
    async def run(self, incident_description: str) -> dict:
        """
        Runs the metro disruption response team on an incident.
        
        Args:
            incident_description (str): Description of the metro incident
            
        Returns:
            dict: Response with status and steps
        """
        print(f"Running team with input: {incident_description}")
        
        try:
            # Filter out None agents
            agents_list = [
                a for a in [
                    UserProxyAgent(
                        name="UserProxyAgent",
                        is_termination_msg=lambda x: True  ,
                        code_execution_config=False,
                        description="You represent the operations control center submitting an incident report.",
                    ),
                    TrainBreakdownAgent,
                    DriverCoordinationAgent, 
                    DepotMaintenanceAgent,
                    PublicCommunicationAgent,
                    IncidentResolutionAgent,
                    InternalNotificationAgent,
                    PublicUpdateAgent
                ] if a is not None
            ]
            
            # Check if we have enough valid agents to proceed
            if len(agents_list) < 3:  # UserProxy + at least 2 agents
                print(f"Not enough valid agents to create a group chat ({len(agents_list)}), using fallback")
                return {
                    "status": "error",
                    "message": "Not enough valid agents to create group chat",
                    "steps": self._generate_fallback_steps(incident_description)
                }
                
            # Create the group chat with all agents in the specified order
            try:
                # If all agents are valid, try to run the full system
                group_chat = RoundRobinGroupChat(
                    participants=agents_list,
                    # max_round=7
                )
                
                # Start the group chat with the incident description
                result = await group_chat.run(task=incident_description)
                print(f"Group chat completed with status: {result.status}")
                print(f"Group chat result: {result}")
                
                # Process messages and format responses here
                steps = []
                for msg in result.messages:
                    # Only include messages from our agents (not the user proxy)
                    if hasattr(msg, "source") and msg.source != "UserProxyAgent":
                        # Format the content
                        agent_name = msg.source
                        content = msg.content
                        
                        # Process by agent type and add emoji prefixes
                        formatted_name = self._format_agent_name(agent_name)
                        content = self._format_content_with_emoji(agent_name, content)
                        
                        # Add to steps
                        steps.append({
                            "name": formatted_name,
                            "content": content
                        })
                
                return {
                    "status": "completed",
                    "steps": steps
                }
                
            except Exception as e:
                print(f"Error running group chat: {e}")
                print(traceback.format_exc())
                return {
                    "status": "error",
                    "message": f"Group chat error: {str(e)}",
                    "steps": self._generate_fallback_steps(incident_description)
                }
                
        except Exception as e:
            print(f"Error running team: {e}")
            print(traceback.format_exc())
            
            # Fall back to debug/mock data for frontend testing
            return {
                "status": "error",
                "message": str(e),
                "steps": self._generate_fallback_steps(incident_description)
            }
    
    def _format_agent_name(self, name: str) -> str:
        """Extract the clean agent name from potentially longer qualified names"""
        if "TrainBreakdownAgent" in name:
            return "TrainBreakdownAgent"
        elif "DriverCoordinationAgent" in name:
            return "DriverCoordinationAgent"
        elif "DepotMaintenanceAgent" in name:
            return "DepotMaintenanceAgent"  
        elif "PublicCommunicationAgent" in name:
            return "PublicCommunicationAgent"
        elif "IncidentResolutionAgent" in name:
            return "IncidentResolutionAgent"
        elif "InternalNotificationAgent" in name:
            return "InternalNotificationAgent"
        elif "PublicUpdateAgent" in name:
            return "PublicUpdateAgent"
        else:
            return name
    
    def _format_content_with_emoji(self, agent_name: str, content: str) -> str:
        """Add appropriate emoji prefix to agent messages if not already present"""
        if "TrainBreakdownAgent" in agent_name:
            if not content.startswith("🚨"):
                content = f"🚨 {content}"
        elif "DriverCoordinationAgent" in agent_name:
            if not content.startswith("📣"):
                content = f"📣 {content}"
        elif "DepotMaintenanceAgent" in agent_name:
            if not content.startswith("🚍"):
                content = f"🚍 {content}"
        elif "PublicCommunicationAgent" in agent_name:
            if not content.startswith("⚠️"):
                content = f"⚠️ {content}"
        elif "IncidentResolutionAgent" in agent_name:
            if not content.startswith("✅"):
                content = f"✅ {content}"
        elif "InternalNotificationAgent" in agent_name:
            if not content.startswith("📨"):
                content = f"📨 {content}"
        elif "PublicUpdateAgent" in agent_name:
            if not content.startswith("📢"):
                content = f"📢 {content}"
        
        return content
    
    def _generate_fallback_steps(self, incident_text: str) -> List[Dict[str, str]]:
        """Generates fallback response steps when the real system fails"""
        # Extract location from incident text if possible
        location_match = re.search(r'(?:at|near|in)\s+([A-Za-z\s]+)', incident_text)
        location = location_match.group(1) if location_match else "Downtown station"
        
        # Generate fallback steps
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
                "content": f"⚠️ Draft social media post: 'Service disruption on the affected line at {location}. Shuttle buses are being arranged. We apologize for the inconvenience.'"
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