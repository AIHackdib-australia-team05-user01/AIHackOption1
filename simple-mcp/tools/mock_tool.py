def mock_run(params: dict) -> dict:
    name = params.get("name", "Guest")
    return {"message": f"Hello, {name}! This is a mock MCP tool."}
