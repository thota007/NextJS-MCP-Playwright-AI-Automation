# NextJS-MCP-Playwright-AI-Automation

🤖 **AI-Powered Browser Automation System** with unified MCP server orchestration, natural language command processing, and persistent file storage.

## 🚀 Overview

This project demonstrates a sophisticated integration of modern web technologies with AI-powered browser automation capabilities. The system uses a unified MCP (Model Context Protocol) server to orchestrate all AI automation workflows, providing a streamlined interface for natural language command processing and browser automation tasks.

## 📁 Project Structure

```
nextjs-fastapi-mcp/
├── frontend/                           # NextJS 15 React application
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx               # Home page
│   │   │   ├── preferences/page.tsx   # User preferences management
│   │   │   └── ai-automation/page.tsx # AI automation interface
│   │   ├── components/
│   │   │   ├── Layout.tsx             # Main layout wrapper
│   │   │   ├── Navigation.tsx         # Navigation bar
│   │   │   └── AIAutomation.tsx       # AI automation component
│   │   └── lib/
│   │       └── api.ts                 # API service layer
│   └── package.json
├── backend/                            # FastAPI + AI automation server
│   ├── main.py                        # FastAPI application with MCP endpoints
│   ├── mcp_server.py                  # Unified MCP server orchestration
│   ├── ai_automation_service.py       # AI automation with OpenAI + Playwright
│   ├── data_service.py                # JSON data persistence
│   ├── models.py                      # Pydantic data models
│   ├── requirements.txt               # Python dependencies
│   ├── automation_results/            # Generated screenshots and verification files
│   │   ├── screenshots/               # PNG screenshot files
│   │   └── verifications/             # JSON verification data
│   └── .env                           # Environment configuration
├── ARCHITECTURE.md                     # System architecture documentation
└── README.md
```

## ✨ Key Features

### 🎯 **AI-Powered Automation**
- **Natural Language Processing**: Execute browser automation using plain English commands
- **OpenAI GPT-4.1 Integration**: Advanced AI command interpretation and workflow generation
- **Playwright Browser Automation**: Headless browser control for web interactions
- **Custom NLP Commands**: Flexible command interface for complex automation tasks

### 🏗️ **Unified MCP Architecture**
- **Single Orchestration Layer**: All AI automation routed through unified MCP server
- **Streamlined Communication**: Frontend communicates exclusively with MCP endpoints
- **Tool Abstraction**: Complex automation logic abstracted behind simple MCP interface
- **Robust Error Handling**: Comprehensive error management and user feedback

### 💾 **Persistent File Storage**
- **Screenshot Capture**: Automatic PNG screenshot saving with timestamps
- **Verification Files**: JSON verification data persistence for audit trails
- **Organized Storage**: Timestamped folders for easy file management
- **File Path Tracking**: Complete file paths returned in automation responses

### 🎨 **Modern Frontend**
- **NextJS 15**: Latest React framework with TypeScript support
- **Tailwind CSS**: Modern, responsive UI design
- **Dedicated AI Page**: Focused interface for AI automation workflows
- **Real-time Feedback**: Live status updates and detailed result displays

## 🛠️ AI Automation Capabilities

### **Available Workflows**
1. **MHMD Preference Toggle**: Automated preference management with database verification
2. **Custom Browser Navigation**: Navigate to any URL and perform actions
3. **Form Automation**: Fill out forms with AI-guided field detection
4. **Screenshot Capture**: Take screenshots of any page or workflow step
5. **Database Verification**: Validate data persistence and return confirmation

### **Example Commands**
- `"Visit localhost:3000, find preferences, toggle MHMD preferences, save data to db and send validation back to user with screenshot"`
- `"Navigate to the preferences page and take a screenshot"`
- `"Fill out the form with name John and email john@example.com then save"`
- `"Toggle MHMD preference to OPT_IN and capture the result"`

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   # Create .env file in backend directory
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   echo "FASTAPI_HOST=0.0.0.0" >> .env
   echo "FASTAPI_PORT=8000" >> .env
   echo "FASTAPI_RELOAD=true" >> .env
   echo "ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000" >> .env
   ```
   
   **⚠️ Important**: You must provide your OpenAI API key for AI automation to work.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment configuration:
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```
   
   **Note**: Frontend runs on port 3000 by default.

## 🚀 Running the Application

### Option 1: Run Both Servers Manually

**Terminal 1 - Backend (Port 8000):**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend (Port 3000):**
```bash
cd frontend
npm run dev
```

### ✅ Verify Setup
- **Backend**: Visit `http://localhost:8000/docs` for FastAPI documentation
- **Frontend**: Visit `http://localhost:3000` for the main application
- **AI Automation**: Visit `http://localhost:3000/ai-automation` for custom NLP commands

### Option 2: Use the Provided Scripts

Create and run the following scripts from the project root:

**start-backend.sh:**
```bash
#!/bin/bash
cd backend
source venv/bin/activate
python main.py
```

**start-frontend.sh:**
```bash
#!/bin/bash
cd frontend
npm run dev
```

Make them executable:
```bash
chmod +x start-backend.sh start-frontend.sh
```

## 🌐 Accessing the Application

- **Frontend**: http://localhost:3000
- **AI Automation Page**: http://localhost:3000/ai-automation
- **Preferences Page**: http://localhost:3000/preferences
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)

## 📡 API Endpoints

### Health Check
- `GET /` - Basic health check
- `GET /health` - Detailed health check with automation service status

### MCP Server Orchestration
- `POST /mcp/call` - Execute AI automation workflows via MCP
- `GET /mcp/tools` - List available AI automation tools

### User Data Management
- `GET /api/user` - Get user data
- `POST /api/user` - Create/update user data
- `DELETE /api/user` - Delete user data

## 🎯 Usage Examples

### Using the AI Automation Interface

1. **Open the AI Automation Page**: http://localhost:3000/ai-automation
2. **Enter your OpenAI API key** (if not configured in backend .env)
3. **Try example commands**:
   - `"Visit localhost:3000, find preferences, toggle MHMD preferences, save data to db and send validation back to user with screenshot"`
   - `"Navigate to the preferences page and take a screenshot"`
   - `"Fill out the form with name John and email john@example.com then save"`
4. **View results** including:
   - Detailed workflow steps
   - Screenshot file paths
   - Verification data file paths
   - Success/error status

### Using the Preferences Page

1. **Visit**: http://localhost:3000/preferences
2. **Manage user data**: Name, email, MHMD preferences
3. **Save preferences** to JSON database
4. **Test MHMD workflows** through AI automation

### Using the API Directly

**Execute AI Browser Automation:**
```bash
curl -X POST "http://localhost:8000/mcp/call" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "ai_browser_automation",
    "params": {
      "command": "Navigate to the preferences page and take a screenshot",
      "base_url": "http://localhost:3000"
    }
  }'
```

curl -X POST "http://localhost:8000/mcp/call" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "mhmd_toggle_workflow",
    "params": {
      "workflow_input": {
        "user_name": "John Doe",
        "user_email": "john@example.com",
        "target_preference": "OPT_IN"
      },
      "base_url": "http://localhost:3000"
    }
  }'

**List Available AI Tools:**
```bash
curl "http://localhost:8000/mcp/tools"
```

## 🛠️ Development

### Adding New AI Automation Workflows

1. **Backend**: Edit `backend/ai_automation_service.py`
2. **Add new methods** to the `BrowserAutomationService` class
3. **Update MCP server**: Add new tools to `backend/mcp_server.py`
4. **Restart the backend** server to apply changes

### Customizing the Frontend

1. **AI Interface**: Edit `frontend/src/components/AIAutomation.tsx`
2. **Pages**: Modify page components in `frontend/src/app/`
3. **API Service**: Update `frontend/src/lib/api.ts` for new endpoints
4. **Hot Reload**: Frontend automatically reloads during development

### File Storage Configuration

- **Screenshots**: Saved to `backend/automation_results/screenshots/`
- **Verification Files**: Saved to `backend/automation_results/verifications/`
- **Timestamps**: All files include timestamp for organization

## 🔧 Troubleshooting

### Backend Issues
- **Virtual Environment**: Ensure Python virtual environment is activated
- **Dependencies**: Check that all dependencies are installed: `pip install -r requirements.txt`
- **Port Conflicts**: Verify port 8000 is not in use by another application
- **OpenAI API Key**: Ensure valid OpenAI API key is configured in `.env`
- **Playwright**: Run `playwright install` if browser automation fails

### Frontend Issues
- **Node.js**: Ensure Node.js and npm are installed
- **Dependencies**: Check that dependencies are installed: `npm install`
- **Backend Connection**: Verify the backend is running and accessible at port 8000
- **Browser Console**: Check browser console for JavaScript errors
- **Port**: Ensure frontend runs on port 3000 (not 3001)

### AI Automation Issues
- **OpenAI API**: Verify API key is valid and has sufficient credits
- **Browser Automation**: Check Playwright browser installation
- **File Permissions**: Ensure write permissions for `automation_results/` directory
- **Network**: Verify localhost connections work properly

### MCP Server Issues
- **Initialization**: Check FastAPI logs for MCP server startup messages
- **Tool Registration**: Verify AI automation tools are properly registered
- **Response Format**: Check MCP response serialization in logs

## 🚀 Next Steps & Roadmap

### Immediate Enhancements
- **Authentication**: Add user authentication and authorization layers
- **Database**: Implement proper database integration (PostgreSQL/MongoDB)
- **Error Handling**: Enhanced error recovery and user feedback
- **Performance**: Optimize AI automation workflows for speed

### Advanced Features
- **Multi-Browser Support**: Support for different browser engines
- **Workflow Templates**: Pre-built automation workflow templates
- **Scheduling**: Automated workflow scheduling and execution
- **Analytics**: Detailed automation analytics and reporting

### Production Deployment
- **Containerization**: Docker containers for easy deployment
- **Cloud Deployment**: AWS/GCP/Azure deployment configurations
- **Monitoring**: Application monitoring and health checks
- **Scaling**: Horizontal scaling for high-volume automation

### Integration Possibilities
- **Webhook Support**: External system integration via webhooks
- **API Extensions**: Additional REST API endpoints for automation
- **Third-party Tools**: Integration with popular automation platforms
- **Real-time Updates**: WebSocket support for live automation status

## 🔧 Technologies Used

### Frontend Stack
- **NextJS 15**: Latest React framework with App Router
- **React 18**: Modern React with TypeScript support
- **TypeScript**: Type-safe JavaScript development
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **ESLint**: Code linting and formatting

### Backend Stack
- **FastAPI**: High-performance Python web framework
- **Python 3.8+**: Modern Python with async/await support
- **Uvicorn**: ASGI server for FastAPI applications
- **Pydantic**: Data validation and serialization
- **CORS**: Cross-origin resource sharing support

### AI & Automation
- **OpenAI GPT-4.1**: Advanced language model for command interpretation
- **Langchain**: AI application framework for LLM integration
- **Playwright**: Browser automation library for web interactions
- **Natural Language Processing**: Custom NLP command processing

### Data & Storage
- **JSON**: Lightweight data persistence for user preferences
- **File System**: PNG screenshots and JSON verification files
- **Timestamped Storage**: Organized file storage with timestamps

### Architecture & Communication
- **MCP (Model Context Protocol)**: Unified server orchestration layer
- **REST API**: HTTP-based communication between frontend and backend
- **Async Processing**: Non-blocking automation workflow execution

## 🏗️ System Architecture

This sophisticated full-stack application demonstrates unified MCP server orchestration for AI-powered browser automation:

```
┌─────────────────┐    HTTP/REST    ┌──────────────────┐
│   NextJS 15     │ ◄──────────────► │   FastAPI        │
│   Frontend      │                  │   Backend        │
│   Port 3000     │                  │   Port 8000      │
└─────────────────┘                  └──────────────────┘
         │                                     │
         │                                     ▼
         │                           ┌──────────────────┐
         │                           │   MCP Server     │
         │                           │   Orchestration  │
         │                           └──────────────────┘
         │                                     │
         │                                     ▼
         │                           ┌──────────────────┐
         │                           │ AI Automation    │
         │                           │ Service          │
         │                           │ - OpenAI GPT-4.1 │
         │                           │ - Playwright     │
         │                           │ - Langchain      │
         │                           └──────────────────┘
         │                                     │
         │                                     ▼
         │                           ┌──────────────────┐
         └──────────────────────────►│ Browser          │
                                     │ Automation       │
                                     │ (Headless)       │
                                     └──────────────────┘
                                               │
                                               ▼
                                     ┌──────────────────┐
                                     │ File Storage     │
                                     │ - Screenshots    │
                                     │ - Verifications  │
                                     └──────────────────┘
```

### Key Architectural Principles
- **Unified Orchestration**: Single MCP server handles all AI automation
- **Separation of Concerns**: Frontend focuses on UI, backend handles automation
- **Persistent Storage**: All automation results saved as files
- **Scalable Design**: Modular architecture supports easy extension
## 📋 Project Summary

**NextJS-MCP-Playwright-AI-Automation** is a cutting-edge system that combines modern web development with AI-powered browser automation. The unified MCP server architecture provides a streamlined interface for executing complex automation workflows through natural language commands, with persistent file storage for screenshots and verification data.

**Perfect for**: AI automation research, browser testing, workflow automation, and demonstrating advanced full-stack integration with AI capabilities.

---

*Built with ❤️ using NextJS, FastAPI, OpenAI GPT-4.1, and Playwright*
- **`ai_automation_service.py`**: Advanced browser automation service using OpenAI GPT-4.1, Langchain agents, and Playwright for headless browser control
- **`data_service.py`**: JSON-based data persistence layer for user preferences
- **`models.py`**: Pydantic data models for type safety and validation
- **`mcp_server.py`**: Simulated MCP (Model Context Protocol) tools
- **`user_data.json`**: User preference storage

### Frontend (`/frontend/src/`)

- **App Pages**: Home, MCP Demo, and Preferences with responsive design
- **Components**: Modular React components for layout, navigation, MCP interaction, and AI automation
- **API Layer**: Comprehensive service layer for backend communication
- **Styling**: Modern UI with Tailwind CSS

## 🚀 Key Capabilities

### AI-Powered Browser Automation
- Natural language command processing
- Automated web interactions using Playwright
- Screenshot capture and validation
- Specific MHMD preference workflow automation

### MCP Tools Integration
- Echo tool for message reflection
- Calculator for arithmetic operations
- System information retrieval

### User Data Management
- CRUD operations for user preferences
- MHMD (My Health My Data) preference toggling
- JSON-based persistence

### Modern Web Interface
- Responsive design with mobile support
- Real-time status indicators
- Interactive demo interfaces

## 🔄 Data Flow

1. **Frontend** → API calls via `api.ts` service layer
2. **Backend** → FastAPI endpoints process requests
3. **AI Automation** → Langchain agents execute browser workflows
4. **Data Persistence** → JSON file storage via `JSONDataService`
5. **Response** → Results with screenshots and validation back to frontend

## 🎯 Special Features

- **Lifecycle Management**: Proper Playwright browser initialization/cleanup
- **Error Handling**: Comprehensive error management across all layers
- **Type Safety**: Full TypeScript integration with Pydantic models
- **Workflow Automation**: Specific MHMD toggle workflow with database verification

The codebase is well-structured, follows modern development practices, and successfully integrates cutting-edge AI technologies with traditional web development patterns. It's ready for extension and can handle complex browser automation tasks through natural language commands.