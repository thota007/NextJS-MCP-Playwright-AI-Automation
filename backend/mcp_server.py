#!/usr/bin/env python3
"""
Enhanced MCP Server that orchestrates both simple tools and AI browser automation.
This server provides a unified interface for all tool interactions.
"""

import asyncio
import json
import os
import platform
from typing import Any, Dict, List, Optional

# Global reference to the automation service (will be injected from main.py)
_automation_service = None

def set_automation_service(service):
    """Set the automation service instance for AI tools"""
    global _automation_service
    _automation_service = service

async def list_tools() -> List[Dict[str, Any]]:
    """List available AI automation tools"""
    tools = [
        # AI Browser Automation tools
        {
            "name": "ai_browser_automation",
            "description": "Execute complex browser automation tasks using natural language commands. Can navigate pages, fill forms, toggle preferences, take screenshots, and more.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Natural language command describing the browser automation task to perform"
                    },
                    "base_url": {
                        "type": "string",
                        "description": "Base URL to navigate to (defaults to http://localhost:3000)",
                        "default": "http://localhost:3000"
                    }
                },
                "required": ["command"]
            }
        },
        {
            "name": "mhmd_toggle_workflow",
            "description": "Execute the specific MHMD (My Health My Data) preference toggle workflow. Navigates to preferences, toggles MHMD setting, saves to database, and captures screenshot.",
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
                        "description": "MHMD preference to set (optional - will toggle current if not specified)"
                    },
                    "base_url": {
                        "type": "string",
                        "description": "Base URL to navigate to (defaults to http://localhost:3000)",
                        "default": "http://localhost:3000"
                    }
                },
                "required": []
            }
        },
        {
            "name": "take_screenshot",
            "description": "Navigate to a specific page and capture a screenshot",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to navigate to and screenshot"
                    },
                    "wait_for": {
                        "type": "string",
                        "description": "CSS selector to wait for before taking screenshot (optional)"
                    }
                },
                "required": ["url"]
            }
        },
        {
            "name": "swagger_api_test_workflow",
            "description": "Execute the Swagger UI API testing workflow: creates a test user with random MHMD preference and verifies it through Swagger UI docs by testing the GET /api/user endpoint",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "base_url": {
                        "type": "string",
                        "description": "Base URL for the API server (defaults to http://localhost:8000)",
                        "default": "http://localhost:8000"
                    }
                },
                "required": []
            }
        }
    ]
    
    return tools

async def call_tool(name: str, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Handle AI automation tool calls"""
    
    # AI Browser Automation Tools - Direct service calls
    if name == "ai_browser_automation":
        if not _automation_service:
            return [{"type": "text", "text": "Error: AI automation service not available"}]
        
        try:
            command = arguments.get("command", "")
            base_url = arguments.get("base_url", "http://localhost:3000")
            
            # Call the automation service directly (no HTTP routing)
            result = await _automation_service.process_natural_language_command(command, base_url)
            
            # Format the result for MCP response
            if result.get("success"):
                response_text = f"✅ {result.get('message', 'Command executed successfully')}"
                if result.get("screenshot"):
                    response_text += f"\n📸 Screenshot captured"
                if result.get("workflow_steps"):
                    response_text += f"\n📋 Steps: {', '.join(result['workflow_steps'])}"
                return [{"type": "text", "text": response_text}]
            else:
                error_text = f"❌ {result.get('message', 'Command failed')}"
                if result.get("error"):
                    error_text += f"\n🔍 Details: {result['error']}"
                return [{"type": "text", "text": error_text}]
                
        except Exception as e:
            return [{"type": "text", "text": f"Error executing AI automation: {str(e)}"}]
    
    elif name == "mhmd_toggle_workflow":
        print(f"DEBUG: MHMD workflow called with arguments: {arguments}")
        
        if not _automation_service:
            print("DEBUG: Automation service not available")
            return [{"type": "text", "text": "Error: AI automation service not available"}]
        
        print(f"DEBUG: Automation service available: {type(_automation_service)}")
        
        try:
            from models import MHMDWorkflowInput, MHMDPreference
            
            # Extract parameters from arguments
            name_param = arguments.get("name")
            email = arguments.get("email")
            preference_str = arguments.get("preference")
            base_url = arguments.get("base_url", "http://localhost:3000")
            
            print(f"DEBUG: Creating workflow input with name={name_param}, email={email}, preference={preference_str}, base_url={base_url}")
            
            # Create workflow input
            preference = MHMDPreference(preference_str) if preference_str else None
            workflow_input = MHMDWorkflowInput(name=name_param, email=email, preference=preference)
            
            print(f"DEBUG: About to call execute_mhmd_toggle_workflow with input: {workflow_input}")
            
            # Call the automation service directly (no HTTP routing)
            result = await _automation_service.execute_mhmd_toggle_workflow(workflow_input, base_url)
            
            # Debug: Log the full result to see what we're getting
            print(f"DEBUG: MHMD workflow result: {result}")
            print(f"DEBUG: Result type: {type(result)}")
            print(f"DEBUG: Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
            
            # Format the result for MCP response - preserve ALL details
            if result.get("success"):
                response_text = f"✅ MHMD Workflow Completed Successfully!\n"
                response_text += f"📋 Message: {result.get('message', 'Workflow executed')}\n"
                
                if result.get("final_preference"):
                    response_text += f"🎯 Final MHMD Preference: {result['final_preference']}\n"
                
                if result.get("workflow_steps"):
                    response_text += f"📝 Workflow Steps:\n"
                    for i, step in enumerate(result['workflow_steps'], 1):
                        response_text += f"  {i}. {step}\n"
                
                if result.get("screenshot"):
                    response_text += f"📸 Screenshot: Captured successfully (length: {len(result['screenshot'])} chars)\n"
                
                if result.get("screenshot_file_path"):
                    response_text += f"🖼️ Screenshot File: {result['screenshot_file_path']}\n"
                
                if result.get("database_verification"):
                    response_text += f"💾 Database Verification: {result['database_verification']}\n"
                
                if result.get("verification_file_path"):
                    response_text += f"📄 Verification File: {result['verification_file_path']}\n"
                
                print(f"DEBUG: Final response_text: {response_text}")
                return [{"type": "text", "text": response_text.strip()}]
            else:
                error_text = f"❌ MHMD workflow failed: {result.get('message', 'Unknown error')}"
                if result.get("error"):
                    error_text += f"\n🔍 Error Details: {result['error']}"
                print(f"DEBUG: Error response: {error_text}")
                return [{"type": "text", "text": error_text}]
                
        except Exception as e:
            error_msg = f"Error executing MHMD workflow: {str(e)}"
            print(f"DEBUG: Exception occurred: {error_msg}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            return [{"type": "text", "text": error_msg}]
    
    elif name == "take_screenshot":
        if not _automation_service:
            return [{"type": "text", "text": "Error: AI automation service not available"}]
        
        try:
            url = arguments.get("url")
            wait_for = arguments.get("wait_for")
            
            if not _automation_service.browser:
                return [{"type": "text", "text": "Error: Browser not initialized"}]
            
            page = await _automation_service.browser.new_page()
            try:
                await page.goto(url, wait_until="networkidle")
                
                if wait_for:
                    await page.wait_for_selector(wait_for, timeout=5000)
                
                screenshot_b64 = await _automation_service.take_screenshot(page)
                
                return [{"type": "text", "text": f"✅ Screenshot captured from {url}\n📸 Base64 length: {len(screenshot_b64)} chars"}]
                
            finally:
                await page.close()
                
        except Exception as e:
            return [{"type": "text", "text": f"Error taking screenshot: {str(e)}"}]
    
    elif name == "swagger_api_test_workflow":
        if not _automation_service:
            return [{"type": "text", "text": "Error: AI automation service not available"}]
        
        try:
            base_url = arguments.get("base_url", "http://localhost:8000")
            
            # Call the automation service directly
            result = await _automation_service.execute_swagger_api_test_workflow(base_url)
            
            # Format the result for MCP response
            if result.get("success"):
                response_text = f"✅ Swagger API Test Workflow Completed Successfully!\n"
                response_text += f"📋 Message: {result.get('message', 'Workflow executed')}\n"
                
                if result.get("test_user_data"):
                    user_data = result["test_user_data"]["data"]
                    response_text += f"👤 Test User Created: {user_data['name']} ({user_data['email']}) with {user_data['mhmd_preference']} preference\n"
                
                if result.get("api_response_status"):
                    response_text += f"📊 API Response Status: {result['api_response_status']}\n"
                
                if result.get("workflow_steps"):
                    response_text += f"📝 Workflow Steps:\n"
                    for i, step in enumerate(result['workflow_steps'], 1):
                        response_text += f"  {i}. {step}\n"
                
                if result.get("screenshot"):
                    response_text += f"📸 Screenshot: Captured successfully (length: {len(result['screenshot'])} chars)\n"
                
                if result.get("screenshot_file_path"):
                    response_text += f"🖼️ Screenshot File: {result['screenshot_file_path']}\n"
                
                if result.get("database_verification"):
                    response_text += f"💾 Database Verification: {result['database_verification']}\n"
                
                if result.get("verification_file_path"):
                    response_text += f"📄 Verification File: {result['verification_file_path']}\n"
                
                return [{"type": "text", "text": response_text.strip()}]
            else:
                error_text = f"❌ Swagger API test workflow failed: {result.get('message', 'Unknown error')}"
                if result.get("error"):
                    error_text += f"\n🔍 Error Details: {result['error']}"
                return [{"type": "text", "text": error_text}]
                
        except Exception as e:
            return [{"type": "text", "text": f"Error executing Swagger API test workflow: {str(e)}"}]
    
    else:
        return [{"type": "text", "text": f"Error: Unknown tool {name}"}]
