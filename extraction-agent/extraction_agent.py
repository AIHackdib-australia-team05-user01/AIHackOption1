import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from file_utils import read_file_to_text

# Define a model client. You can use other model client that implements
# the `ChatCompletionClient` interface.
model_client = AzureOpenAIChatCompletionClient(
    model="gpt-4.1",
    api_version="2024-12-01-preview",
    azure_endpoint="https://extractionagentaihack.cognitiveservices.azure.com/",
    api_key="API_KEY",
)


async def get_all_documents() -> str:
    """Gets all the rfp and executive summary documents from storage"""
    vendor1_exec_summary = read_file_to_text("docs/Vendor 1 Executive Summary.docx")
    vendor1_rfp = read_file_to_text("docs/Vendor 1 RFP.xlsx")
    vendor2_exec_summary = read_file_to_text("docs/Vendor 2 Executive Summary.docx")
    vendor2_rfp = read_file_to_text("docs/Vendor 2 RFP.xlsx")
    vendor3_exec_summary = read_file_to_text("docs/Vendor 3 Executive Summary.docx")
    vendor3_rfp = read_file_to_text("docs/Vendor 3 RFP.xlsx")
    
    return f"""The executive summary for vendor 1 is: {vendor1_exec_summary}
    The RFP for vendor 1 is: {vendor1_rfp}
    The executive summary for vendor 2 is: {vendor2_exec_summary}
    The RFP for vendor 2 is: {vendor2_rfp}
    The executive summary for vendor 3 is: {vendor3_exec_summary}
    The RFP for vendor 3 is: {vendor3_rfp}
    """

async def get_schema() -> str:
    """Gets the json schema that reflects what the database schema is"""
    with open("database.schema.json", "r", encoding="utf-8") as f:
        return f.read()


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
    tools=[get_all_documents, get_schema],
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
