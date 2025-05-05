import os
import asyncio
from typing import Dict, Any
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

print(f"Azure OpenAI Configuration:")
print(f"  Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
print(f"  Deployment: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')}")
print(f"  Model: {os.getenv('AZURE_OPENAI_MODEL_NAME', 'gpt-4o')}")
print(f"  API Version: {os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-01')}")
print(f"  API Key: {os.getenv('AZURE_OPENAI_API_KEY')[:5]}...{os.getenv('AZURE_OPENAI_API_KEY')[-5:] if os.getenv('AZURE_OPENAI_API_KEY') else 'Not set'}")
# Create a shared client instance to reuse across all agents
_shared_client = None

def create_model_client_for_agent():
    """
    Creates an Azure OpenAI model client for AutoGen agents using the same approach 
    that worked in test_custom.py
    """
    global _shared_client
    
    # If we already created a client, return it (singleton pattern)
    if _shared_client is not None:
        return _shared_client
    
    # Always use MockModelClient for now to avoid Azure errors
    # This guarantees the app will work while you debug Azure issues
    _shared_client = MockModelClient()
    print("Using MockModelClient for all agents to ensure stability")
    return _shared_client
    
    # Check required environment variables
    required_vars = ['AZURE_OPENAI_ENDPOINT', 'AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_DEPLOYMENT_NAME']
    for var in required_vars:
        if not os.getenv(var):
            print(f"ERROR: Missing required environment variable {var}")
            return MockModelClient()
    
    try:
        # Try to create a real client with Azure OpenAI
        print(f"Using deployment: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')}")
        
        # Import just what we need
        from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
        
        # Instead of the client that didn't work, try the one from test_custom.py
        client = AzureOpenAIChatCompletionClient(
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            azure_deployment=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-01'),
            model=os.getenv('AZURE_OPENAI_MODEL_NAME', "gpt-4o"),
            model_info={
                "json_output": False,
                "function_calling": True,
                "vision": False,
                "family": "chat_completion", 
                "structured_output": False
            }
        )
        
        print("Created shared Azure OpenAI model client for all agents")
        _shared_client = client
        return client
        
    except Exception as e:
        print(f"Failed to create Azure client: {str(e)}")
        print("Falling back to MockModelClient")
        _shared_client = MockModelClient()
        return _shared_client

class MockModelClient:
    """A mock model client that simulates responses without calling OpenAI"""
    
    def __init__(self):
        self.name = "MockModelClient"
        # Add model_info attribute to fix the error
        self.model_info = {
            "json_output": False,
            "function_calling": True,
            "vision": False,
            "family": "chat_completion", 
            "structured_output": False
        }
    # Add this right after the load_dotenv() call

    async def create(self, messages=None, **kwargs):
        """Simulate creating a completion response"""
        # Extract the last user message content
        user_message = "Unknown request"
        for msg in messages:
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                
        # Log the request details for debugging
        print(f"MockModelClient received request: {user_message[:50]}...")
        
        # Generate a response based on keywords in the request
        if "breakdown" in user_message.lower() or "incident" in user_message.lower():
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "I need to log this incident immediately."
                        }
                    }
                ]
            }
        elif "driver" in user_message.lower() or "bus" in user_message.lower():
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "I'll coordinate with the bus drivers now."
                        }
                    }
                ]
            }
        elif "depot" in user_message.lower() or "maintenance" in user_message.lower():
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "I'll notify the maintenance team to prepare buses."
                        }
                    }
                ]
            }
        elif "communication" in user_message.lower() or "public" in user_message.lower():
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "I'll draft a public announcement for social media."
                        }
                    }
                ]
            }
            
        # If tools were provided and tool usage is needed, generate a tool call
        if kwargs.get("tools") and len(kwargs["tools"]) > 0:
            tool_name = kwargs["tools"][0]["function"]["name"]
            
            # Common arguments for different tools
            arguments = {}
            
            if "log_incident" in tool_name:
                arguments = {"location": "Downtown station"}
            elif "notify" in tool_name:
                arguments = {"message": "Reporting for duty"}
            elif "confirm" in tool_name:
                arguments = {"status": "confirmed"}
            elif "draft" in tool_name:
                arguments = {"message": "Service disruption announcement"}
            elif "post" in tool_name:
                arguments = {"channel": "all", "message": "Service update"}
            elif "check" in tool_name:
                arguments = {"id": "incident-123"}
            
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
                                        "arguments": json.dumps(arguments)
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
                        "content": "I'm handling this metro disruption situation."
                    }
                }
            ]
        }
    
    async def close(self):
        """Mock close method"""
        pass