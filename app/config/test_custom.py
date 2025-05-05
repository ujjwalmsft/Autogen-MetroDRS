import os
import asyncio
from typing import Annotated
from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define your tool function
def test_function(
    location: Annotated[str, "The name of the station or location where the incident occurred."]
) -> str:
    return f"✅ Tool successfully executed with location: {location}"

# Wrap tool using FunctionTool
test_tool = FunctionTool(
    name="test_function",
    description="Returns a message confirming the tool was used with the given location.",
    func=test_function,
)

# Azure OpenAI client initialization
model_client = AzureOpenAIChatCompletionClient(
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    azure_deployment=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
    model=os.getenv('AZURE_OPENAI_MODEL_NAME', "gpt-4o"),
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-01'),
)

async def main():
    print("🚀 Testing AssistantAgent with Azure OpenAI and FunctionTool...\n")

    # Initialize AssistantAgent
    agent = AssistantAgent(
        name="TestAgent",
        model_client=model_client,
        system_message="You are a helpful assistant. Always respond concisely.",
        tools=[test_tool],
    )

    # Step 1: Correct async usage with await
    print("🔍 Asking LLM: What is the capital of Germany?")
    reply_1 = await agent.run(task="What is the capital of Germany?")
    print("🧠 LLM Response:", reply_1)

    # Step 2: Tool invocation explicitly via await
    print("\n🛠️ Asking LLM to invoke the tool...")
    reply_2 = await agent.run(task="Use the test function with location 'Berlin'")
    print("🛠️ Tool Invocation Response:", reply_2)

    # Close the model client properly with await
    await model_client.close()

    print("\n✅ All tests completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
