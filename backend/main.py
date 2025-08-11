from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import asyncio
import logging

# Configure logging
logger = logging.getLogger("uvicorn")
import os
import platform
from dotenv import load_dotenv
from models import UserData, UserResponse, UserUpdateRequest, MHMDPreference, AICommandRequest, AICommandResponse, MCPCallRequest, MCPResponse
from data_service import JSONDataService
from ai_automation_service import BrowserAutomationService
from playwright.async_api import async_playwright
import mcp_server

# Load environment variables
load_dotenv()

# State dictionary to hold the automation service instance
state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the Playwright and AI Automation Service lifecycle."""
    async with async_playwright() as p:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")

        # Pass the playwright instance to the service
        automation_service = BrowserAutomationService(p, openai_api_key)
        await automation_service.initialize_browser()
        state["automation_service"] = automation_service
        
        # Inject the automation service into the MCP server
        mcp_server.set_automation_service(automation_service)
        print("BrowserAutomationService initialized and injected into MCP server.")
        
        yield
        
        await state["automation_service"].shutdown_browser()
        print("BrowserAutomationService shut down.")

app = FastAPI(
    title="NextJS FastAPI MCP Server", 
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for NextJS frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # NextJS default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class MCPRequest(BaseModel):
    method: str
    params: Optional[Dict[str, Any]] = None

class MCPResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    message: str

# Enhanced MCP tools including AI browser automation
MCP_TOOLS = [
    {
        "name": "echo",
        "description": "Echo back the input message",
        "inputSchema": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Message to echo back"
                }
            },
            "required": ["message"]
        }
    },
    {
        "name": "calculate",
        "description": "Perform basic arithmetic calculations",
        "inputSchema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "Arithmetic operation to perform"
                },
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["operation", "a", "b"]
        }
    },
    {
        "name": "get_system_info",
        "description": "Get basic system information",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    },
    {
        "name": "ai_browser_automation",
        "description": "Execute complex browser automation tasks using natural language commands",
        "inputSchema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Natural language command describing the browser automation task"
                },
                "base_url": {
                    "type": "string",
                    "description": "Base URL to navigate to (defaults to http://localhost:3000)"
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "mhmd_toggle_workflow",
        "description": "Execute the MHMD preference toggle workflow with database persistence",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "User name (optional)"
                },
                "email": {
                    "type": "string",
                    "description": "User email (optional)"
                },
                "preference": {
                    "type": "string",
                    "enum": ["OPT_IN", "OPT_OUT"],
                    "description": "MHMD preference (optional - will toggle if not specified)"
                },
                "base_url": {
                    "type": "string",
                    "description": "Base URL to navigate to (defaults to http://localhost:3000)"
                }
            },
            "required": []
        }
    },
    {
        "name": "take_screenshot",
        "description": "Navigate to a page and capture a screenshot",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to navigate to and screenshot"
                },
                "wait_for": {
                    "type": "string",
                    "description": "CSS selector to wait for before screenshot (optional)"
                }
            },
            "required": ["url"]
        }
    }
]

# Simulated MCP session status
mcp_connected = True

# Initialize JSON data service
data_service = JSONDataService()



@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="NextJS FastAPI MCP Server is running"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check including MCP status"""
    mcp_status = "connected" if mcp_connected else "disconnected"
    return HealthResponse(
        status="healthy",
        message=f"Server is running. MCP status: {mcp_status}"
    )

@app.post("/mcp/call", response_model=MCPResponse)
async def call_mcp_method(request: MCPRequest):
    """Call an MCP method through the unified MCP server"""
    if not mcp_connected:
        raise HTTPException(
            status_code=503,
            detail="MCP client not initialized"
        )
    
    try:
        # Route all tool calls through the enhanced MCP server
        method = request.method
        params = request.params or {}
        
        # Call the MCP server's call_tool function directly
        mcp_result = await mcp_server.call_tool(method, params)
        
        # Convert MCP result to our API format
        if mcp_result and len(mcp_result) > 0:
            # Combine all text content from MCP response (mcp_result is list of dicts)
            combined_text = "\n".join([content.get('text', '') for content in mcp_result if content.get('type') == 'text'])
            result = [{"type": "text", "text": combined_text}]
        else:
            result = [{"type": "text", "text": "No result returned from MCP server"}]
        
        return MCPResponse(
            success=True,
            data=result
        )
    except Exception as e:
        logger.error(f"MCP call failed: {e}", exc_info=True)
        return MCPResponse(
            success=False,
            error=str(e)
        )

@app.get("/mcp/tools")
async def list_mcp_tools():
    """List available MCP tools"""
    try:
        # Get tools from the simulated MCP server
        tools = await mcp_server.list_tools()
        return MCPResponse(
            success=True,
            data=tools
        )
    except Exception as e:
        return MCPResponse(
            success=False,
            error=str(e)
        )



@app.get("/api/example")
async def example_endpoint():
    """Example API endpoint for NextJS frontend"""
    return {
        "message": "Hello from FastAPI!",
        "timestamp": "2025-01-07T00:17:59-05:00",
        "data": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"}
        ]
    }

# User Data API Endpoints
@app.get("/api/user", response_model=UserResponse)
async def get_user_data():
    """Get user data"""
    try:
        user_data = data_service.get_user_data()
        if user_data:
            return UserResponse(
                success=True,
                data=user_data,
                message="User data retrieved successfully"
            )
        else:
            return UserResponse(
                success=False,
                message="No user data found"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user", response_model=UserResponse)
async def create_user_data(user_data: UserData):
    """Create or update user data"""
    try:
        success = data_service.save_user_data(user_data)
        if success:
            return UserResponse(
                success=True,
                data=user_data,
                message="User data saved successfully"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to save user data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/api/user", response_model=UserResponse)
async def update_user_data(update_request: UserUpdateRequest):
    """Update specific fields of user data"""
    try:
        # Convert update request to dict, excluding None values
        update_data = {k: v for k, v in update_request.dict().items() if v is not None}
        
        updated_user = data_service.update_user_data(**update_data)
        if updated_user:
            return UserResponse(
                success=True,
                data=updated_user,
                message="User data updated successfully"
            )
        else:
            return UserResponse(
                success=False,
                message="Failed to update user data or incomplete data"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/user", response_model=UserResponse)
async def delete_user_data():
    """Delete user data (reset to defaults)"""
    try:
        success = data_service.delete_user_data()
        if success:
            return UserResponse(
                success=True,
                message="User data deleted successfully"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to delete user data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Note: AI Automation is now handled exclusively through the MCP server
# Frontend communicates only with MCP endpoints:
# - /mcp/tools: List available tools
# - /mcp/call: Execute tool calls (including AI automation)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
