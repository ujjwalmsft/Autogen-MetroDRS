import asyncio
import sys
from client import DirectAzureClientWrapper, get_working_azure_client
from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from llm_config import get_llm_config
import asyncio
import os
from typing import Annotated
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from dotenv import load_dotenv
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load env vars (AZURE_OPENAI_* keys)
load_dotenv()

# Define your tool function
def test_function(
    location: Annotated[str, "The name of the station or location where the incident occurred."]
) -> str:
    return f"✅ Tool successfully executed with location: {location}"

# Wrap tool using FunctionTool
test_tool = FunctionTool(
    name="test_function",
    description="Returns a message confirming tool was used with the given location.",
    func=test_function,
)

# Create AzureOpenAI model client using .env values
model_client = AzureOpenAIChatCompletionClient(
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    model=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2023-07-01-preview'),
    azure_deployment=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
)

async def main():
    print("🚀 Testing AssistantAgent with Azure OpenAI and FunctionTool...\n")

    # Step 1: Create agent
    agent = AssistantAgent(
        name="TestAgent",
        model_client=model_client,
        system_message="You are a helpful assistant. Always respond concisely.",
        tools=[test_tool],
    )

    # Step 2: Ask a normal question
    print("🔍 Asking LLM: What is the capital of Germany?")
    reply_1 = await agent.a_generate_reply([
        {"role": "user", "content": "What is the capital of Germany?"}
    ])
    print("🧠 LLM Response:", reply_1)

    # Step 3: Trigger tool via prompt
    print("\n🛠️ Asking LLM to invoke the tool...")
    reply_2 = await agent.a_generate_reply([
        {"role": "user", "content": "Use the test function with location 'Berlin'"}
    ])
    print("🛠️ Tool Invocation Response:", reply_2)

    print("\n✅ All tests completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())