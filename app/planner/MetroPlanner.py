"""
MetroPlanner.py

Main orchestrator for the metro disruption response using AutoGen v0.5.6.
Uses GroupChat and GroupChatManager to run a full, automated workflow.
"""

# from autogen import GroupChat, GroupChatManager
from autogen_agentchat.state import  BaseGroupChatManagerState
from autogen_agentchat.teams import BaseGroupChat
from autogen_agentchat.agents import UserProxyAgent

# Import updated AutoGen v0.5.6 agents

from agents.TrainBreakdownAgent import TrainBreakdownAgent
from agents.DriverCoordinationAgent import DriverCoordinationAgent
from agents.DepotMaintenanceAgent import DepotMaintenanceAgent
from agents.PublicCommunicationAgent import PublicCommunicationAgent
from agents.IncidentResolutionAgent import IncidentResolutionAgent
from agents.InternalNotificationAgent import InternalNotificationAgent
from agents.PublicUpdateAgent import PublicUpdateAgent
from config.llm_config import get_llm_config


class MetroPlanner:
    """
    Coordinates a metro incident response using GroupChatManager and AssistantAgents.
    """

    def __init__(self, llm_config=None):
        self.llm_config = llm_config or get_llm_config()

        # System initiator
        self.user_proxy = UserProxyAgent(
            name="UserProxyAgent",
            system_message="You are a system user initiating the metro disruption response.",
            human_input_mode="NEVER"
        )

        # List of all agents
        self.agents = [
            self.user_proxy,
            TrainBreakdownAgent,
            DriverCoordinationAgent,
            DepotMaintenanceAgent,
            PublicCommunicationAgent,
            IncidentResolutionAgent,
            InternalNotificationAgent,
            PublicUpdateAgent
        ]

        # Set up the group chat and manager
        self.groupchat = GroupChat(
            agents=self.agents,
            messages=[],
            max_round=20
        )

        self.manager = BaseGroupChatManager(
            groupchat=self.groupchat,
            llm_config=self.llm_config
        )

    async def run(self, incident_description: str) -> list:
        """
        Executes the multi-agent workflow with the given disruption input.

        Args:
            incident_description (str): Description of the train disruption

        Returns:
            list: List of assistant messages from all agents
        """
        await self.user_proxy.initiate_chat(
            manager=self.manager,
            message=incident_description
        )

        # Return all assistant messages only
        return [
            {
                "role": m.get("role"),
                "name": m.get("name", ""),
                "content": m.get("content")
            }
            for m in self.groupchat.chat_history
            if m["role"] == "assistant"
        ]
