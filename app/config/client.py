from openai import AzureOpenAI
from autogen_ext.models.azure import AzureAIChatCompletionClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
import asyncio
import json

load_dotenv()

def create_model_client_for_agent():
    """Creates a model client for AutoGen agents using the most reliable approach"""
    try:
        # First try the standard client approach
        return AzureAIChatCompletionClient(
            endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            credential=AzureKeyCredential(os.getenv('AZURE_OPENAI_API_KEY')),
            model=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
            api_version="2024-02-15-preview",
            model_info={
                "json_output": False,
                "function_calling": True,
                "vision": False,
                "family": "unknown", 
                "structured_output": False
            }
        )
    except Exception as e:
        print(f"Standard AzureAIChatCompletionClient failed: {e}")
        print("Falling back to MockModelClient")
        return MockModelClient()

class MockModelClient:
    """A mock model client that simulates responses without calling OpenAI"""
    
    def __init__(self):
        self.name = "MockModelClient"
    
    async def create(self, messages=None, **kwargs):
        """Simulate creating a completion response"""
        # Extract the last user message content
        user_message = "Unknown request"
        for msg in messages:
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
        
        # Generate a mock response based on the request
        if "capital of Germany" in user_message:
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "The capital of Germany is Berlin."
                        }
                    }
                ]
            }
        elif "tool" in user_message.lower() or "function" in user_message.lower():
            # If tools were provided and tool usage was requested, generate a tool call
            if kwargs.get("tools") and len(kwargs["tools"]) > 0:
                tool_name = kwargs["tools"][0]["function"]["name"]
                return {
                    "choices": [
                        {
                            "message": {
                                "role": "assistant",
                                "content": None,
                                "tool_calls": [
                                    {
                                        "id": "call_123",
                                        "type": "function",
                                        "function": {
                                            "name": tool_name,
                                            "arguments": json.dumps({"location": "Berlin"})
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
                
        # Default generic response
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "I'm a mock response since Azure OpenAI is unavailable."
                    }
                }
            ]
        }
    
    async def close(self):
        """Mock close method"""
        pass