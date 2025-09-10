# agents/document_generation/mcp_server.py
import asyncio
from typing import Dict, List, Any
from doc_generation_agent import DocumentGenerationAgent
from db_manager import DatabaseManager, TenderData

class MCPDocumentGenerationServer:
    def __init__(self, doc_agent: DocumentGenerationAgent, db_manager: DatabaseManager):
        self.doc_agent = doc_agent
        self.db_manager = db_manager

    async def handle_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool calls from Manager Agent"""
        try:
            if tool_name == "generate_all_reports":
                tender_data = self.db_manager.get_evaluation_data()
                if tender_data:
                    reports = self.doc_agent.generate_all_reports(tender_data)
                    return {"status": "success", "reports": reports}
                else:
                    return {"status": "error", "message": "No tender data found"}
            
            elif tool_name == "generate_scoring_matrix":
                tender_data = self.db_manager.get_evaluation_data()
                if tender_data:
                    path = self.doc_agent.generate_scoring_matrix(tender_data)
                    return {"status": "success", "path": path}
                else:
                    return {"status": "error", "message": "No tender data found"}
            
            # Add more tool handlers as needed
            
            else:
                return {"status": "error", "message": f"Unknown tool: {tool_name}"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}

class MCPServerWrapper:
    """Wrapper for MCP server integration"""
    def __init__(self, server: MCPDocumentGenerationServer):
        self.server = server
    
    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return await self.server.handle_tool_call(tool_name, params)
