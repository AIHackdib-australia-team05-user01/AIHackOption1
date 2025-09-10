from fastapi import FastAPI, Request
import sys
import os
from db_connect import DBConnect

# Add the project root to the python path to allow importing db_connect
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.mock_tool import mock_run
from tools.pdf_extractor_tool import extract_pdf

app = FastAPI()

try:
    db = DBConnect()
    print("Database connection established successfully.")
except Exception as e:
    db = None
    print(f"Failed to connect to the database: {e}")


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

@app.get("/db-check")
async def check_db_connection():
    if db:
        try:
            vendors = db.get_all_vendors()
            return {"status": "connected", "vendors": vendors}
        except Exception as e:
            return {"status": "connection_error", "error": str(e)}
    else:
        return {"status": "disconnected"}
