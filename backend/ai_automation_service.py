import asyncio
import base64
import io
import json
import logging
import os
import random
import string
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, SystemMessage
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from playwright.async_api import async_playwright, Browser, Page
from PIL import Image
from pydantic import BaseModel

from data_service import JSONDataService
from models import (
    AICommandRequest,
    AICommandResponse,
    MHMDPreference,
    MHMDWorkflowInput,
    UserData,
    UserResponse,
    UserUpdateRequest,
)

logger = logging.getLogger(__name__)

class MHMDWorkflowTool(BaseTool):
    name = "mhmd_workflow_tool"
    description = "Executes the MHMD preference workflow. Use this to toggle, opt-in, or opt-out a user. You can optionally provide a name and email. If an email is not provided but is required, a random one will be generated."
    args_schema: type[BaseModel] = MHMDWorkflowInput
    service: 'BrowserAutomationService'

    def _run(self, *args, **kwargs):
        raise NotImplementedError("Use arun for asynchronous execution")

    async def _arun(self, name: Optional[str] = None, email: Optional[str] = None, preference: Optional[MHMDPreference] = None) -> Dict[str, Any]:
        """Use the tool asynchronously."""
        workflow_input = MHMDWorkflowInput(name=name, email=email, preference=preference)
        return await self.service.execute_mhmd_toggle_workflow(workflow_input)

class BrowserAutomationService:
    def __init__(self, playwright, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.llm = ChatOpenAI(
            model="gpt-4-1106-preview",  # GPT-4 Turbo
            api_key=openai_api_key,
            temperature=0.1
        )
        self.data_service = JSONDataService()
        self.playwright = playwright
        self.browser: Optional[Browser] = None
        
        # Initialize the tool
        mhmd_tool = MHMDWorkflowTool(service=self)
        tools = [mhmd_tool]
        
        # Create the agent
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that executes web automation workflows."),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        agent = create_openai_tools_agent(self.llm, tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
        
    async def initialize_browser(self):
        """Launches the browser."""
        if not self.browser:
            self.browser = await self.playwright.chromium.launch(headless=True)
        logger.info("Browser initialized.")

    async def shutdown_browser(self):
        """Closes the browser."""
        if self.browser:
            await self.browser.close()
        logger.info("Browser shut down.")

    async def take_screenshot(self, page: Page) -> str:
        """Take a screenshot and return base64 encoded image"""
        if not page or page.is_closed():
            raise Exception("Page not available or closed")
        
        screenshot_bytes = await page.screenshot(full_page=True)
        return base64.b64encode(screenshot_bytes).decode()
    
    def _save_screenshot_to_file(self, screenshot_b64: str, workflow_type: str = "automation") -> str:
        """Save base64 screenshot to a PNG file and return the file path"""
        try:
            # Create automation_results directory if it doesn't exist
            screenshots_dir = Path("automation_results/screenshots")
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate timestamp-based filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{workflow_type}_{timestamp}.png"
            file_path = screenshots_dir / filename
            
            # Decode base64 and save as PNG
            screenshot_bytes = base64.b64decode(screenshot_b64)
            with open(file_path, "wb") as f:
                f.write(screenshot_bytes)
            
            logger.info(f"Screenshot saved to: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Failed to save screenshot: {e}")
            return ""
    
    def _save_verification_to_file(self, verification_data: Dict[str, Any], workflow_type: str = "automation") -> str:
        """Save database verification results to a JSON file and return the file path"""
        try:
            # Create automation_results directory if it doesn't exist
            verifications_dir = Path("automation_results/verifications")
            verifications_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate timestamp-based filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{workflow_type}_verification_{timestamp}.json"
            file_path = verifications_dir / filename
            
            # Add timestamp to verification data
            verification_with_timestamp = {
                "timestamp": timestamp,
                "workflow_type": workflow_type,
                "verification_data": verification_data
            }
            
            # Save as JSON
            with open(file_path, "w") as f:
                json.dump(verification_with_timestamp, f, indent=2)
            
            logger.info(f"Verification data saved to: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Failed to save verification data: {e}")
            return ""
    
    async def navigate_to_url(self, page: Page, url: str) -> Dict[str, Any]:
        """Navigate to a specific URL"""
        try:
            await page.goto(url, wait_until="networkidle")
            return {
                "success": True,
                "message": f"Successfully navigated to {url}",
                "current_url": page.url,
                "title": await page.title()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to navigate to {url}: {str(e)}"
            }
    
    async def find_and_click_element(self, page: Page, selector: str, text_content: Optional[str] = None) -> Dict[str, Any]:
        """Find and click an element by selector or text content"""
        try:
            if text_content:
                # Find element by text content
                await page.get_by_text(text_content).first.click(timeout=5000)
            elif selector:
                await page.locator(selector).first.click(timeout=5000)
            else:
                return {"success": False, "message": "Either selector or text must be provided"}
            
            return {"success": True, "message": f"Successfully clicked element {selector or text_content}"}
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to click element {selector or text_content}: {str(e)}"
            }
    
    async def toggle_radio_button(self, page: Page, value: str) -> Dict[str, Any]:
        """Toggle a radio button by value"""
        try:
            radio_selector = f'input[type="radio"][value="{value}"]'
            await page.click(radio_selector)
            return {
                "success": True,
                "message": f"Successfully selected radio button with value: {value}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to toggle radio button {value}: {str(e)}"
            }
    
    async def fill_input_field(self, page: Page, selector: str, value: str) -> Dict[str, Any]:
        """Fill an input field with a value"""
        try:
            await page.fill(selector, value)
            return {
                "success": True,
                "message": f"Successfully filled input field {selector} with value: {value}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to fill input field {selector}: {str(e)}"
            }
    
    async def click_save_button(self, page: Page) -> Dict[str, Any]:
        """Click the save button"""
        try:
            # Try multiple possible save button selectors
            save_selectors = [
                'button:has-text("Save Preferences")',
                'button:has-text("Save")',
                'input[type="submit"]',
                'button[type="submit"]'
            ]
            
            for selector in save_selectors:
                try:
                    await page.click(selector, timeout=2000)
                    return {
                        "success": True,
                        "message": "Successfully clicked save button"
                    }
                except:
                    continue
            
            return {
                "success": False,
                "message": "Could not find save button"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to click save button: {str(e)}"
            }
    
    async def wait_for_success_message(self, page: Page) -> Dict[str, Any]:
        """Wait for success message to appear"""
        try:
            # Wait for success message
            await page.wait_for_selector('.bg-green-50', timeout=5000)
            success_text = await page.locator('.bg-green-50 .text-green-800').text_content()
            return {
                "success": True,
                "message": f"Success message appeared: {success_text}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"No success message found: {str(e)}"
            }
    
    async def get_current_mhmd_preference(self) -> Dict[str, Any]:
        """Get the current MHMD preference from the database"""
        try:
            user_data = self.data_service.get_user_data()
            if user_data:
                return {
                    "success": True,
                    "current_preference": user_data.mhmd_preference.value,
                    "user_data": {
                        "name": user_data.name,
                        "email": user_data.email,
                        "mhmd_preference": user_data.mhmd_preference.value
                    }
                }
            else:
                return {
                    "success": False,
                    "message": "No user data found in database"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to get current MHMD preference: {str(e)}"
            }
    
    async def execute_mhmd_toggle_workflow(self, workflow_input: MHMDWorkflowInput, base_url: str = "http://localhost:3000") -> Dict[str, Any]:
        """Execute the complete MHMD toggle workflow using dynamic inputs."""
        workflow_results = []
        screenshot_b64 = None
        page = None
        try:
            if not self.browser or not self.browser.is_connected():
                raise Exception("Browser not initialized or closed. Please ensure the service is running.")

            page = await self.browser.new_page()
            await page.set_viewport_size({"width": 1280, "height": 720})

            # Navigate to the base URL
            await page.goto(base_url, wait_until="networkidle")
            workflow_results.append(f"📍 Navigated to: {base_url}")

            # Step 2: Find and click Preferences link
            prefs_result = await self.find_and_click_element(page, None, "Preferences")
            workflow_results.append(f"🔗 Preferences click: {prefs_result['message']}")
            if not prefs_result['success']:
                raise Exception("Failed to click Preferences link")

            await asyncio.sleep(2)

            # Step 3: Determine target preference
            if workflow_input.preference:
                new_pref = workflow_input.preference.value
                workflow_results.append(f"🎯 Target preference specified: {new_pref}")
            else:
                current_pref_result = await self.get_current_mhmd_preference()
                current_pref = current_pref_result.get('current_preference', 'OPT_OUT')
                new_pref = "OPT_IN" if current_pref == "OPT_OUT" else "OPT_OUT"
                workflow_results.append(f"🔄 No preference specified, toggling to: {new_pref}")

            # Step 4: Toggle MHMD preference
            toggle_result = await self.toggle_radio_button(page, new_pref)
            workflow_results.append(f"🎛️ Toggle result: {toggle_result['message']}")
            if not toggle_result['success']:
                raise Exception("Failed to toggle MHMD preference")

            # Step 5: Fill in required fields
            try:
                user_name = workflow_input.name or "Test User"
                await self.fill_input_field(page, 'input[type="text"]', user_name)
                workflow_results.append(f"📝 Filled name field with: {user_name}")

                user_email = workflow_input.email
                if not user_email or user_email == 'random':
                    user_email = f"testuser_{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}@example.com"
                    workflow_results.append(f"📧 Generated random email: {user_email}")
                
                await self.fill_input_field(page, 'input[type="email"]', user_email)
                workflow_results.append(f"📧 Filled email field with: {user_email}")

            except Exception as e:
                workflow_results.append(f"⚠️ Field filling failed: {str(e)}")

            # Step 6: Click Save button
            save_result = await self.click_save_button(page)
            workflow_results.append(f"💾 Save result: {save_result['message']}")
            if not save_result['success']:
                raise Exception("Failed to click save button")

            # Step 7: Wait for success message
            success_msg_result = await self.wait_for_success_message(page)
            workflow_results.append(f"✅ Success message: {success_msg_result['message']}")

            # Step 8: Take screenshot
            screenshot_b64 = await self.take_screenshot(page)
            workflow_results.append("📸 Screenshot captured")

            # Step 9: Verify data in database
            final_pref_result = await self.get_current_mhmd_preference()
            workflow_results.append(f"🗄️ Final DB state: {final_pref_result}")

            # Step 10: Save screenshot to file
            screenshot_file_path = ""
            if screenshot_b64:
                screenshot_file_path = self._save_screenshot_to_file(screenshot_b64, "mhmd_workflow")
                if screenshot_file_path:
                    workflow_results.append(f"💾 Screenshot saved to: {screenshot_file_path}")
                else:
                    workflow_results.append("⚠️ Failed to save screenshot to file")

            # Step 11: Save database verification to file
            verification_file_path = ""
            if final_pref_result:
                verification_file_path = self._save_verification_to_file(final_pref_result, "mhmd_workflow")
                if verification_file_path:
                    workflow_results.append(f"💾 Verification data saved to: {verification_file_path}")
                else:
                    workflow_results.append("⚠️ Failed to save verification data to file")

            return {
                "success": True,
                "message": "MHMD preference toggle workflow completed successfully",
                "workflow_steps": workflow_results,
                "screenshot": screenshot_b64,
                "screenshot_file_path": screenshot_file_path,
                "final_preference": new_pref,
                "database_verification": final_pref_result,
                "verification_file_path": verification_file_path
            }

        except Exception as e:
            workflow_results.append(f"❌ Error: {str(e)}")
            screenshot_file_path = ""
            verification_file_path = ""
            
            if page and not page.is_closed():
                try:
                    screenshot_b64 = await self.take_screenshot(page)
                    workflow_results.append("📸 Screenshot captured on error")
                    
                    # Save error screenshot to file
                    screenshot_file_path = self._save_screenshot_to_file(screenshot_b64, "mhmd_workflow_error")
                    if screenshot_file_path:
                        workflow_results.append(f"💾 Error screenshot saved to: {screenshot_file_path}")
                        
                except Exception as screen_e:
                    workflow_results.append(f"📸 Screenshot failed on error: {screen_e}")
            
            # Save error verification data
            error_verification = {
                "success": False,
                "error": str(e),
                "workflow_steps": workflow_results
            }
            verification_file_path = self._save_verification_to_file(error_verification, "mhmd_workflow_error")
            if verification_file_path:
                workflow_results.append(f"💾 Error verification saved to: {verification_file_path}")
            
            return {
                "success": False,
                "message": f"MHMD preference toggle workflow failed: {str(e)}",
                "workflow_steps": workflow_results,
                "screenshot": screenshot_b64,
                "screenshot_file_path": screenshot_file_path,
                "verification_file_path": verification_file_path,
                "error": str(e)
            }
        finally:
            if page and not page.is_closed():
                await page.close()
    
    async def process_natural_language_command(self, command: str, base_url: str = "http://localhost:3000") -> Dict[str, Any]:
        """Process a natural language command using the Langchain agent or direct execution."""
        try:
            logger.info(f"Processing command: {command}")
            logger.info(f"Using base URL: {base_url}")
            
            # Use a simpler approach to avoid template formatting issues
            system_message = """You are an expert at parsing natural language commands for a web automation tool. 
Extract the parameters for the MHMD toggle workflow and respond with ONLY a valid JSON object.

The JSON should contain:
- name: string or null (user's name if specified, null if not)
- email: string or null (user's email if specified, null if not specified or if random is requested)
- preference: string or null (OPT_IN or OPT_OUT if specified, null if not)

Examples:
- Visit preferences add John with random email and opt him in -> return JSON with name John, email null, preference OPT_IN
- Toggle MHMD to opt out -> return JSON with name null, email null, preference OPT_OUT
- Visit preference test page send screenshot -> return JSON with name null, email null, preference null

CRITICAL: Respond ONLY with valid JSON. No explanations, no markdown, no extra text."""

            user_message = f"Command: {command}"
            
            # Create messages manually to avoid template formatting issues
            from langchain_core.messages import SystemMessage, HumanMessage
            messages = [SystemMessage(content=system_message), HumanMessage(content=user_message)]
            
            response = await self.llm.ainvoke(messages)
            logger.info(f"OpenAI response: {response.content}")
            
            # Parse the JSON response with improved error handling
            import json
            import re
            
            try:
                # Clean the response content to extract JSON
                content = response.content.strip()
                logger.info(f"Cleaned content: {content}")
                
                # Try to extract JSON from the response if it's wrapped in markdown or other text
                json_match = re.search(r'\{[^{}]*\}', content)
                if json_match:
                    content = json_match.group(0)
                    logger.info(f"Extracted JSON: {content}")
                
                parsed_data = json.loads(content)
                logger.info(f"Parsed data: {parsed_data}")
                
                # Validate the parsed data structure
                if not isinstance(parsed_data, dict):
                    raise ValueError("Response is not a JSON object")
                
                workflow_input = MHMDWorkflowInput(
                    name=parsed_data.get("name"),
                    email=parsed_data.get("email"),
                    preference=MHMDPreference(parsed_data["preference"]) if parsed_data.get("preference") else None
                )
                logger.info(f"Created workflow input: {workflow_input}")
                
            except (json.JSONDecodeError, ValueError, KeyError) as parse_error:
                logger.warning(f"Failed to parse OpenAI response: {parse_error}")
                logger.warning(f"Raw response content: {response.content}")
                
                # Provide user-friendly error message with the actual AI response
                return {
                    "success": False,
                    "message": f"I couldn't parse the AI response properly. The AI returned: '{response.content}'. This seems to be a JSON parsing issue. Please try a simpler command like 'Visit preferences and take screenshot'",
                    "error": f"JSON parsing failed: {str(parse_error)}",
                    "raw_ai_response": response.content
                }

            # Execute the workflow with the parsed, structured input
            workflow_result = await self.execute_mhmd_toggle_workflow(workflow_input, base_url)
            return workflow_result

        except Exception as e:
            logger.error(f"Error processing command: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"An error occurred while processing your command: {str(e)}. Please check that the frontend is running on the correct port and try again.",
                "error": str(e)
            }

# Resolve the forward reference for the service field in MHMDWorkflowTool
MHMDWorkflowTool.update_forward_refs(BrowserAutomationService=BrowserAutomationService)
