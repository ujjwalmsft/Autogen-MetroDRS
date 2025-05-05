import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

load_dotenv()

# Print environment variables (with API key partially masked)
api_key = os.getenv('AZURE_OPENAI_API_KEY')
masked_key = api_key[:5] + "..." + api_key[-5:] if api_key else "Not set"

print(f"AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
print(f"AZURE_OPENAI_API_KEY: {masked_key}")
print(f"AZURE_OPENAI_DEPLOYMENT_NAME: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')}")
print(f"AZURE_OPENAI_API_VERSION: {os.getenv('AZURE_OPENAI_API_VERSION', '2023-07-01-preview')}")

# Try to create a client and make a simple call
try:
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-07-01-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT") 
    )
    
    # Try a simple completion
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=[{"role": "user", "content": "Hello, Azure OpenAI!"}],
        max_tokens=10
    )
    
    print("\nSuccessful connection to Azure OpenAI!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"\nError connecting to Azure OpenAI: {e}")