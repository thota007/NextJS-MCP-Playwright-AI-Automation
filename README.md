# NextJS + FastAPI + MCP Server Project

This project demonstrates integration between a NextJS React frontend and a FastAPI backend with MCP (Model Context Protocol) server capabilities.

## Project Structure

```
nextjs-fastapi-mcp/
├── frontend/                 # NextJS React application
│   ├── src/
│   │   ├── app/
│   │   │   └── page.tsx     # Main page with MCP demo
│   │   ├── components/
│   │   │   └── MCPDemo.tsx  # MCP integration component
│   │   └── lib/
│   │       └── api.ts       # API service for backend communication
│   └── package.json
├── backend/                  # FastAPI + MCP server
│   ├── main.py              # FastAPI application
│   ├── mcp_server.py        # MCP server implementation
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Backend configuration
└── README.md
```

## Features

- **NextJS Frontend**: Modern React application with TypeScript and Tailwind CSS
- **FastAPI Backend**: High-performance API server with CORS support
- **MCP Integration**: Model Context Protocol server with example tools
- **Real-time Communication**: Frontend communicates with backend via REST API
- **Interactive Demo**: Web interface to test MCP tools

## MCP Tools Available

1. **Echo Tool**: Returns the input message
2. **Calculator**: Performs basic arithmetic operations (add, subtract, multiply, divide)
3. **System Info**: Returns system information (platform, Python version, etc.)

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

4. Configure environment variables (optional):
   ```bash
   # The .env file is already created with default values
   # Modify backend/.env if needed
   ```

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

## Running the Application

### Option 1: Run Both Servers Manually

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

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

## Accessing the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)

## API Endpoints

### Health Check
- `GET /` - Basic health check
- `GET /health` - Detailed health check with MCP status

### MCP Integration
- `POST /mcp/call` - Call an MCP tool
- `GET /mcp/tools` - List available MCP tools

### Example API
- `GET /api/example` - Example endpoint returning sample data

## Usage Examples

### Using the Web Interface

1. Open http://localhost:3000 in your browser
2. Check the backend status indicator
3. Try the quick demo buttons:
   - **Echo Test**: Tests the echo MCP tool
   - **Calculate**: Performs 10 + 5 calculation
   - **System Info**: Gets system information
4. Use the custom tool interface to call MCP tools with custom parameters

### Using the API Directly

**Call Echo Tool:**
```bash
curl -X POST "http://localhost:8000/mcp/call" \
  -H "Content-Type: application/json" \
  -d '{"method": "echo", "params": {"message": "Hello MCP!"}}'
```

**Call Calculator:**
```bash
curl -X POST "http://localhost:8000/mcp/call" \
  -H "Content-Type: application/json" \
  -d '{"method": "calculate", "params": {"operation": "multiply", "a": 7, "b": 6}}'
```

**List Available Tools:**
```bash
curl "http://localhost:8000/mcp/tools"
```

## Development

### Adding New MCP Tools

1. Edit `backend/mcp_server.py`
2. Add your tool to the `list_tools()` function
3. Implement the tool logic in the `call_tool()` function
4. Restart the backend server

### Customizing the Frontend

1. Edit `frontend/src/components/MCPDemo.tsx` for UI changes
2. Modify `frontend/src/lib/api.ts` for API integration changes
3. The frontend will hot-reload automatically during development

## Troubleshooting

### Backend Issues
- Ensure Python virtual environment is activated
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify port 8000 is not in use by another application

### Frontend Issues
- Ensure Node.js and npm are installed
- Check that dependencies are installed: `npm install`
- Verify the backend is running and accessible
- Check browser console for any JavaScript errors

### MCP Issues
- The MCP server runs as a separate process within the FastAPI application
- Check the FastAPI logs for MCP initialization messages
- Ensure the MCP library is properly installed

## Next Steps

- Add authentication and authorization
- Implement more sophisticated MCP tools
- Add database integration
- Deploy to production environment
- Add comprehensive testing

## Technologies Used

- **Frontend**: NextJS 15, React 18, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.8+, Uvicorn
- **MCP**: Model Context Protocol for tool integration
- **Development**: ESLint, Hot reloading, CORS support


## 🏗️ Overall Architecture

This is a sophisticated full-stack application that demonstrates the integration of modern web technologies with AI-powered automation:

- **Frontend**: NextJS 15 + React 18 + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python with AI automation capabilities
- **AI Integration**: OpenAI GPT-4.1 + Langchain + Playwright for browser automation
- **Data Storage**: JSON-based user data persistence
- **Communication**: REST API with CORS support

## 🔧 Core Components

### Backend (`/backend/`)

- **`main.py`**: Central FastAPI application with lifecycle management, CORS configuration, and comprehensive API endpoints
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