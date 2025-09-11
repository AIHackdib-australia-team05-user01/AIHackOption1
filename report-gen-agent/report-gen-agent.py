import asyncio
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from db_connect import DBConnect
from dotenv import load_dotenv

load_dotenv()

# Define a model client. You can use other model client that implements
# the `ChatCompletionClient` interface.
model_client = AzureOpenAIChatCompletionClient(
    model="gpt-5-chat",
    api_version="2025-01-01-preview",
    azure_endpoint="https://aihac-mfc0kjaa-eastus2.cognitiveservices.azure.com/",
    api_key="API",
    model_info={"vision":False,"function_calling":True,"json_output":True,"family":"gpt-5","structured_output":True,"multiple_system_messages":True}
)

db=DBConnect(True)

async def get_all_vendors() -> dict:
    """A tool function to get all vendors from the database."""
    return db.get_all_vendors()

async def get_all_criteria_categories() -> dict:
    """A tool function to get all criteria categories from the database."""
    return db.get_all_criteria_categories()

async def get_all_criteria() -> dict:
    """A tool function to get all criteria from the database."""
    return db.get_all_criteria()

async def get_all_responses() -> dict:
    """A tool function to get all responses from the database."""
    return db.get_all_responses()

async def get_all_costs() -> dict:
    """A tool function to get all costs from the database."""
    return db.get_all_costs()

async def create_report(filename: str, content: str) -> None:
    """A tool to write content to a report file in the output directory"""
    print("jacob said to do this")
    output_dir = "output"
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content + "\n")  # Appends content to the file
    return None


# Define an AssistantAgent with the model, tool, system message, and reflection enabled.
# The system message instructs the agent via natural language.
f = open("system_prompt.txt", "r", encoding="utf-8")
system_prompt = f.read()
f.close()

f = open("user_prompt.txt", "r", encoding="utf-8")
user_prompt = f.read()
f.close()

agent = AssistantAgent(
    name="report_gen_agent",
    model_client=model_client,
    tools=[get_all_vendors, get_all_criteria_categories, get_all_criteria, get_all_responses, get_all_costs, create_report],
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
