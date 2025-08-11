# NextJS FastAPI MCP System Architecture

## Overview
This system implements a unified MCP (Model Context Protocol) server orchestration architecture where the frontend communicates exclusively with the MCP server, which acts as the single orchestration layer for all AI browser automation tools and workflows.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                 FRONTEND                                        │
│                              (NextJS React)                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐                                        │
│  │   Home Page     │  │  Preferences    │                                        │
│  │   (page.tsx)    │  │   (page.tsx)    │                                        │
│  └─────────────────┘  └─────────────────┘                                        │
│           │                     │                                                │
│  ┌─────────────────┐  ┌─────────────────┐                                        │
│  │   Navigation    │  │  AIAutomation   │                                        │
│  │  (Navigation.tsx)│  │(AIAutomation.tsx)│                                       │
│  └─────────────────┘  └─────────────────┘                                        │
│                                 │                                                │
│                                           │                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                        API Service Layer                                │  │
│  │                          (api.ts)                                       │  │
│  │                                                                         │  │
│  │  • callMCPMethod(request)                                              │  │
│  │  • executeAIAutomation(command, baseUrl)                              │  │
│  │  • executeMHMDWorkflow(name, email, preference)                       │  │
│  │  • EXCLUSIVE MCP communication                                         │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                           │
                                           │ HTTP/REST API
                                           │ (ONLY MCP endpoints)
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                  BACKEND                                        │
│                               (FastAPI Python)                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                           FastAPI Main Server                           │  │
│  │                              (main.py)                                  │  │
│  │                                                                         │  │
│  │  Endpoints:                                                             │  │
│  │  • GET  /mcp/tools     → List available MCP tools                      │  │
│  │  • POST /mcp/call      → Execute MCP tool calls                        │  │
│  │  • GET  /health        → Health check                                  │  │
│  │  • GET  /api/users     → User data management                          │  │
│  │                                                                         │  │
│  │  ❌ NO direct AI automation endpoints                                   │  │
│  │  ❌ NO /api/ai/execute or /api/ai/mhmd-toggle                          │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                           │                                    │
│                                           │ Internal routing                   │
│                                           ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                        MCP SERVER ORCHESTRATOR                          │  │
│  │                           (mcp_server.py)                               │  │
│  │                                                                         │  │
│  │  Available AI Automation Tools:                                        │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │  │
│  │  │ai_browser_auto  │  │mhmd_toggle_work │  │ take_screenshot │        │  │
│  │  │ (AI automation) │  │ (AI automation) │  │ (AI automation) │        │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │  │
│  │                                │                                       │  │
│  │                                │ Direct service calls                  │  │
│  │                                ▼                                       │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                           │                                    │
│                                           │                                    │
│                                           ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                    AI AUTOMATION SERVICE                                │  │
│  │                   (ai_automation_service.py)                           │  │
│  │                                                                         │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │  │
│  │  │   OpenAI GPT    │  │   Langchain     │  │   Playwright    │        │  │
│  │  │     4.1         │  │    Agent        │  │    Browser      │        │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │  │
│  │                                │                                       │  │
│  │  Core Methods:                 │                                       │  │
│  │  • process_natural_language_command()                                  │  │
│  │  • execute_mhmd_toggle_workflow()                                      │  │
│  │  • take_screenshot()                                                   │  │
│  │  • _save_screenshot_to_file()     ← NEW                               │  │
│  │  • _save_verification_to_file()   ← NEW                               │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                           │                                    │
│                                           │                                    │
│                                           ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                        DATA PERSISTENCE                                 │  │
│  │                                                                         │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │  │
│  │  │   JSON Data     │  │   Screenshot    │  │  Verification   │        │  │
│  │  │   Service       │  │     Files       │  │     Files       │        │  │
│  │  │(data_service.py)│  │    (.png)       │  │    (.json)      │        │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │  │
│  │           │                     │                     │                │  │
│  │           ▼                     ▼                     ▼                │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │  │
│  │  │  user_data.json │  │  screenshots/   │  │ verifications/  │        │  │
│  │  │                 │  │  *.png files    │  │  *.json files   │        │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. **Frontend → MCP Server Communication**
```
Frontend (TypeScript)
    ↓ HTTP POST /mcp/call
    ↓ { method: "mhmd_toggle_workflow", params: {} }
MCP Server (Python)
```

### 2. **MCP Server → AI Automation Orchestration**
```
MCP Server
    ↓ Direct function call
    ↓ await _automation_service.execute_mhmd_toggle_workflow()
AI Automation Service
```

### 3. **AI Automation → Browser Workflow**
```
AI Automation Service
    ↓ Playwright browser automation
    ↓ OpenAI GPT-4.1 natural language processing
    ↓ Langchain agent execution
Browser Workflow (localhost:3000)
    ↓ Navigate → Click → Fill → Save → Screenshot
    ↓ Database verification
File System
```

### 4. **Response & File Persistence**
```
AI Automation Service
    ↓ Generate detailed response
    ↓ Save screenshot as PNG file
    ↓ Save verification as JSON file
MCP Server
    ↓ Format comprehensive response
    ↓ Include file paths and detailed results
Frontend
```

## Key Components

### **Frontend (NextJS React + TypeScript)**
- **Pages**: Home, MCP Demo, Preferences
- **Components**: Navigation, MCPDemo, AIAutomation
- **API Layer**: Exclusive MCP communication via `api.ts`
- **Styling**: Tailwind CSS for modern UI

### **Backend (FastAPI Python)**
- **Main Server**: FastAPI with CORS, lifecycle management
- **MCP Server**: Simulated MCP with tool orchestration
- **AI Automation**: OpenAI GPT-4.1 + Langchain + Playwright
- **Data Service**: JSON-based user data persistence
- **Models**: Pydantic data validation

### **AI Automation Capabilities**
- **Natural Language Processing**: OpenAI GPT-4.1 command parsing
- **Browser Automation**: Playwright headless browser control
- **MHMD Workflow**: Preference toggle automation
- **Screenshot Capture**: Full-page PNG file generation
- **Database Verification**: JSON file persistence

### **File Storage Structure**
```
backend/
├── automation_results/
│   ├── screenshots/
│   │   └── mhmd_workflow_YYYYMMDD_HHMMSS.png
│   └── verifications/
│       └── mhmd_workflow_verification_YYYYMMDD_HHMMSS.json
├── user_data.json
└── [other backend files]
```

## Unified MCP Orchestration Benefits

1. **🎯 Single API Interface**: Frontend only communicates with MCP endpoints
2. **🔧 Centralized Orchestration**: All AI automation routed through MCP server
3. **📁 Persistent Storage**: Screenshots and verification data saved as files
4. **🔍 Detailed Responses**: Comprehensive workflow results with file paths
5. **🛡️ Robust Error Handling**: Error screenshots and verification saved
6. **🔄 Seamless Integration**: No direct AI automation API calls from frontend

This architecture ensures robust, detailed responses and seamless integration while maintaining the MCP server as the single orchestration layer for all AI browser automation tools and workflows.
