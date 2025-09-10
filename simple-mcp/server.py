# server.py
from fastmcp import FastMCP
from tools.text_to_string import read_file_to_text

mcp = FastMCP("rfp-mcp")

@mcp.tool
def get_all_documents() -> str:
    """Gets all the rfp and executive summary documents from storage"""
    vendor1_exec_summary = read_file_to_text("tender_docs/Vendor 1 Executive Summary.docx")
    vendor1_rfp = read_file_to_text("tender_docs/Vendor 1 RFP.xlsx")
    vendor2_exec_summary = read_file_to_text("tender_docs/Vendor 2 Executive Summary.docx")
    vendor2_rfp = read_file_to_text("tender_docs/Vendor 2 RFP.xlsx")
    vendor3_exec_summary = read_file_to_text("tender_docs/Vendor 3 Executive Summary.docx")
    vendor3_rfp = read_file_to_text("tender_docs/Vendor 3 RFP.xlsx")
    
    return f"""The executive summary for vendor 1 is: {vendor1_exec_summary}
    The RFP for vendor 1 is: {vendor1_rfp}
    The executive summary for vendor 2 is: {vendor2_exec_summary}
    The RFP for vendor 2 is: {vendor2_rfp}
    The executive summary for vendor 3 is: {vendor3_exec_summary}
    The RFP for vendor 3 is: {vendor3_rfp}
    """

@mcp.tool
def get_schema() -> str:
    """Gets the json schema that reflects what the database schema is"""
    with open("database.schema.json", "r", encoding="utf-8") as f:
        return f.read()