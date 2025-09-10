from fastapi import FastAPI, Request
from tools.mock_tool import mock_run
from tools.pdf_extractor_tool import extract_pdf

app = FastAPI()

@app.post("/tools/mock")
async def call_mock_tool(request: Request):
    params = await request.json()
    result = mock_run(params)
    return result

@app.post("/tools/pdf_extractor")
async def call_pdf_extractor(request: Request):
    params = await request.json()
    result = extract_pdf(params)
    return result
