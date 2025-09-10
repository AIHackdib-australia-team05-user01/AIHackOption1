from autogen_ext.tools.mcp import McpWorkbench, StreamableHttpServerParams
import asyncio
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv()

# Define a model client. You can use other model client that implements
# the `ChatCompletionClient` interface.
model_client = AzureOpenAIChatCompletionClient(
    model="gpt-4.1",
    api_version="2024-12-01-preview",
    azure_endpoint="https://extractionagentaihack.cognitiveservices.azure.com/",
    api_key=os.getenv("EXTRACTION_AGENT_API_KEY"),
)

# Get the fetch tool from mcp-server-fetch.
fetch_mcp_server = StreamableHttpServerParams(url="http://20.28.170.141:8002/mcp")
workbench = McpWorkbench(fetch_mcp_server)

# Define an AssistantAgent with the model, tool, system message, and reflection enabled.
# The system message instructs the agent via natural language.
f = open("system_prompt.txt", "r", encoding="utf-8")
system_prompt = f.read()
f.close()

f = open("user_prompt.txt", "r", encoding="utf-8")
user_prompt = f.read()
f.close()

agent = AssistantAgent(
    name="data_extraction_agent",
    model_client=model_client,
    workbench=workbench,
    #tools=[get_all_documents, get_schema, output_table_as_csv],
    system_message=system_prompt,
    reflect_on_tool_use=True,
    model_client_stream=True,  # Enable streaming tokens from the model client.
)


# Run the agent and stream the messages to the console.
async def main() -> None:
    await Console(agent.run_stream(task=user_prompt))
    # Close the connection to the model client.
    await model_client.close()


# NOTE: if running this inside a Python script you'll need to use asyncio.run(main()).
if __name__ == "__main__":
    asyncio.run(main())
