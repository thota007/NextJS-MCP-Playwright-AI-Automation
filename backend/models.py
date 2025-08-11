from pydantic import BaseModel, EmailStr
from typing import Literal, List, Optional
from enum import Enum

class MHMDPreference(str, Enum):
    OPT_IN = "OPT_IN"
    OPT_OUT = "OPT_OUT"

class UserData(BaseModel):
    name: str
    email: EmailStr
    mhmd_preference: MHMDPreference

class UserResponse(BaseModel):
    success: bool
    data: UserData = None
    message: str = ""

class UserUpdateRequest(BaseModel):
    name: str = None
    email: EmailStr = None
    mhmd_preference: MHMDPreference = None

class AICommandRequest(BaseModel):
    command: str

class MHMDWorkflowInput(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    preference: Optional[MHMDPreference] = None

class AICommandResponse(BaseModel):
    success: bool
    message: str
    workflow_steps: List[str] = []
    screenshot: Optional[str] = None
    final_preference: Optional[str] = None
    database_verification: Optional[dict] = None
    error: Optional[str] = None

class MCPCallRequest(BaseModel):
    method: str
    params: Optional[dict] = None

class MCPResponse(BaseModel):
    success: bool
    data: Optional[List[dict]] = None
    error: Optional[str] = None
