from autogen_ext.tools.mcp import McpWorkbench, StreamableHttpServerParams
import asyncio
import os
import sys
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from aioconsole import ainput
from dotenv import load_dotenv

load_dotenv()

async def write_stdout(chunk: str):
    data = chunk.encode()
    fd = sys.stdout.fileno()
    pos = 0
    while pos < len(data):
        try:
            pos += os.write(fd, data[pos:])
        except BlockingIOError:
            await asyncio.sleep(0.01)

# --- event filter: print only human-facing text ---
def is_printable_event(ev) -> bool:
    # Prefer explicit type names if available
    name = type(ev).__name__
    etype = getattr(ev, "type", None)

    # 1) Never print internal/verbose containers or chain-of-thought
    if name in {
        "ThoughtEvent",
        "TraceEvent",
        "RunResult",
        "Result"}:
        return False
    if hasattr(ev, "messages") or hasattr(ev, "documents"):
        # containers like "...messages=[TextMessage(...)]"
        return False

    # 2) Only allow assistant/user text deltas / messages
    printable_types = {
        "TextDelta", "AssistantMessage", "UserMessage", "ToolOutput",
        "ModelOutput", "TextEvent", "Token"
    }
    if name in printable_types or etype in {"text-delta", "assistant_message", "tool-output"}:
        return True

    # 3) If it exposes to_text(), treat non-empty text as printable
    if hasattr(ev, "to_text"):
        try:
            txt = ev.to_text()
            # Guard against repr-like dumps
            if txt and not txt.strip().startswith(("documents.messages=", "detail.messages=")):
                return True
        except Exception:
            return False

    return isinstance(ev, str)

async def run_once(prompt: str):
    async for ev in agent.run_stream(task=prompt):
        if not is_printable_event(ev):
            continue
        text = ev.to_text() if hasattr(ev, "to_text") else (
            ev if isinstance(ev, str) else "")
        if text:
            await write_stdout(text)
    await write_stdout("\n")  # newline at end of message

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

# Run the agent continuously taking user prompts from stdio until the user quits
async def main():
    tools = await workbench.list_tools()
    print(f"Available tools from MCP Server: {[t['name'] for t in tools]}")
    try:
        while True:
            user_prompt = (await ainput("You> ")).strip()
            if user_prompt.lower() in {"exit", "quit", ":q"}:
                break
            if not user_prompt:
                continue
            await run_once(user_prompt)
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        # graceful shutdown to avoid RuntimeWarning at exit
        await model_client.close()
        await workbench.stop()

if __name__ == "__main__":
    asyncio.run(main())
