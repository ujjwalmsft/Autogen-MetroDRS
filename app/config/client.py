from openai import AzureOpenAI
from autogen_ext.models.azure import AzureAIChatCompletionClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
from typing import Dict, List, Optional, Union, Any
import asyncio

load_dotenv()

# Cache the test client that works
_azure_client = None

def get_working_azure_client():
    """Returns a working Azure OpenAI client instance (cached)"""
    global _azure_client
    
    if _azure_client is None:
        _azure_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
            api_version="2024-02-15-preview",  # Try a different, more stable API version
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT") 
        )
        
        # Test the client
        try:
            response = _azure_client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            print(f"Azure client test: {response.choices[0].message.content}")
        except Exception as e:
            print(f"Azure client test failed: {e}")
            _azure_client = None
            raise
            
    return _azure_client

class DirectAzureClientWrapper:
    """
    A custom model client for AutoGen that uses the direct AzureOpenAI client internally.
    This provides the interface AutoGen expects while using the client we know works.
    """
    def __init__(self):
        self.client = get_working_azure_client()
        self.model = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    async def create(self, 
                     messages: List[Dict],
                     stream: bool = False,
                     temperature: Optional[float] = None,
                     max_tokens: Optional[int] = None,
                     tools: Optional[List] = None,
                     tool_choice: Optional[Union[str, Dict]] = None,
                     **kwargs) -> Dict[str, Any]:
        """
        Create a chat completion using the working AzureOpenAI client.
        This mimics the interface of AzureAIChatCompletionClient.
        """
        try:
            # Convert from AutoGen's expected format to what the OpenAI client expects
            params = {
                "model": self.model,
                "messages": messages,
                "stream": stream,
                "temperature": temperature if temperature is not None else 0.7,
                "max_tokens": max_tokens if max_tokens is not None else 1000,
            }
            
            # Add tools if provided
            if tools:
                params["tools"] = tools
            if tool_choice:
                params["tool_choice"] = tool_choice
                
            # Add any additional kwargs
            for key, value in kwargs.items():
                if value is not None:
                    params[key] = value
            
            # Run in a thread to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: self.client.chat.completions.create(**params)
            )
            
            # Convert the response to the format AutoGen expects
            result = {
                "choices": [
                    {
                        "message": {
                            "role": response.choices[0].message.role,
                            "content": response.choices[0].message.content,
                        }
                    }
                ]
            }
            
            # Handle tool calls if present
            if hasattr(response.choices[0].message, "tool_calls") and response.choices[0].message.tool_calls:
                tool_calls = []
                for tool_call in response.choices[0].message.tool_calls:
                    tool_calls.append({
                        "id": tool_call.id,
                        "type": tool_call.type,
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        }
                    })
                result["choices"][0]["message"]["tool_calls"] = tool_calls
            
            return result
        
        except Exception as e:
            print(f"Error in DirectAzureClientWrapper: {e}")
            raise

def create_model_client_for_agent():
    """Creates a model client for AutoGen agents using a known working approach"""
    
    # Create and return our custom client wrapper instead of the standard AzureAIChatCompletionClient
    return DirectAzureClientWrapper()