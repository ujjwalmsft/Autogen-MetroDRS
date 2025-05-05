from openai import AzureOpenAI
from autogen_ext.models.azure import AzureAIChatCompletionClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

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

def create_model_client_for_agent():
    """Creates a model client for AutoGen agents using working parameters"""
    # Use consistent parameters that work with your deployment
    return AzureAIChatCompletionClient(
        endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
        credential=AzureKeyCredential(os.getenv('AZURE_OPENAI_API_KEY')),
        model=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
        api_version="2024-02-15-preview",  # Try this specific API version
        model_info={
            "json_output": False,
            "function_calling": True,
            "vision": False,
            "family": "unknown", 
            "structured_output": False
        }
    )