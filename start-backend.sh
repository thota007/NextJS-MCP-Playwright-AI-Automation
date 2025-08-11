#!/bin/bash
echo "Starting FastAPI MCP Server..."
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
