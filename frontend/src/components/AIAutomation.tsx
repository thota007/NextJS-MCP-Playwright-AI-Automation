'use client';

import { useState } from 'react';
import { apiService, AICommandResponse } from '@/lib/api';

export default function AIAutomation() {
  const [command, setCommand] = useState('');
  const [loading, setLoading] = useState(false);
  const [mhmdLoading, setMhmdLoading] = useState(false);
  const [swaggerLoading, setSwaggerLoading] = useState(false);
  const [result, setResult] = useState<AICommandResponse | null>(null);

  const handleExecuteCommand = async () => {
    if (!command.trim()) {
      alert('Please enter a command');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      // Use MCP server for AI browser automation
      const response = await apiService.callMCPMethod({
        method: 'ai_browser_automation',
        params: { 
          command: command,
          base_url: 'http://localhost:3000'
        }
      });
      
      // Convert MCP response to AICommandResponse format
      const aiResponse: AICommandResponse = {
        success: response.success,
        message: response.success 
          ? (Array.isArray(response.data) ? response.data[0]?.text || 'Command executed' : 'Command executed')
          : (response.error || 'Command failed'),
        error: response.error
      };
      
      setResult(aiResponse);
    } catch (error) {
      setResult({
        success: false,
        message: `Failed to execute command: ${error}`,
        error: String(error)
      });
    } finally {
      setLoading(false);
    }
  };

  const handleMHMDToggle = async () => {
    setMhmdLoading(true);
    setResult(null);

    try {
      // Use MCP server for MHMD workflow
      const response = await apiService.callMCPMethod({
        method: 'mhmd_toggle_workflow',
        params: {}
      });
      
      // Convert MCP response to AICommandResponse format - preserve full details
      const aiResponse: AICommandResponse = {
        success: response.success,
        message: response.success 
          ? (Array.isArray(response.data) && response.data[0]?.text ? response.data[0].text : 'MHMD workflow executed')
          : (response.error || 'MHMD workflow failed'),
        error: response.error
      };
      
      setResult(aiResponse);
    } catch (error) {
      setResult({
        success: false,
        message: `Failed to execute MHMD toggle: ${error}`,
        error: String(error)
      });
    } finally {
      setMhmdLoading(false);
    }
  };

  const handleSwaggerAPITest = async () => {
    setSwaggerLoading(true);
    setResult(null);

    try {
      // Use MCP server for Swagger API test workflow
      const response = await apiService.callMCPMethod({
        method: 'swagger_api_test_workflow',
        params: { 
          base_url: 'http://localhost:8000'
        }
      });
      
      // Convert MCP response to AICommandResponse format - preserve full details
      const aiResponse: AICommandResponse = {
        success: response.success,
        message: response.success 
          ? (Array.isArray(response.data) && response.data[0]?.text ? response.data[0].text : 'Swagger API test executed')
          : (response.error || 'Swagger API test failed'),
        error: response.error
      };
      
      setResult(aiResponse);
    } catch (error) {
      setResult({
        success: false,
        message: `Failed to execute Swagger API test: ${error}`,
        error: String(error)
      });
    } finally {
      setSwaggerLoading(false);
    }
  };

  const predefinedCommands = [
    "Visit localhost:3000, find preferences, toggle MHMD preferences, save data to db and send validation back to user, letting them know data is updated in DB and also send a screenshot of the preferences toggled",
    "Navigate to preferences page and toggle MHMD setting",
    "Change MHMD preference and save to database"
  ];

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          🤖 AI-Powered Browser Automation
        </h2>
        <p className="text-gray-600 mb-6">
          Use natural language commands to automate browser interactions with OpenAI GPT-4.1, Langchain, and Playwright.
        </p>



        {/* Quick Action Buttons */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Quick Actions</h3>
          <div className="space-y-4">
            <div>
              <button
                onClick={handleMHMDToggle}
                disabled={mhmdLoading || swaggerLoading || loading}
                className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed mr-4"
              >
                {mhmdLoading ? '🔄 Executing...' : '🎯 Execute MHMD Toggle Workflow'}
              </button>
              <p className="text-sm text-gray-500 mt-2">
                Automatically visit preferences, toggle MHMD setting, save to database, and capture screenshot
              </p>
            </div>
            <div>
              <button
                onClick={handleSwaggerAPITest}
                disabled={mhmdLoading || swaggerLoading || loading}
                className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {swaggerLoading ? '🔄 Executing...' : '🔧 Execute Swagger API Test Workflow'}
              </button>
              <p className="text-sm text-gray-500 mt-2">
                Create test user with random MHMD preference and verify through Swagger UI docs
              </p>
            </div>
          </div>
        </div>

        {/* Custom Command Input */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Custom Commands</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Natural Language Command
              </label>
              <textarea
                value={command}
                onChange={(e) => setCommand(e.target.value)}
                placeholder="Enter your automation command in natural language..."
                rows={3}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-black"
                disabled={loading}
              />
            </div>

            {/* Predefined Commands */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Or select a predefined command:
              </label>
              <div className="space-y-2">
                {predefinedCommands.map((cmd, index) => (
                  <button
                    key={index}
                    onClick={() => setCommand(cmd)}
                    className="block w-full text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-md text-sm text-gray-700 transition-colors"
                    disabled={loading}
                  >
                    {cmd}
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={handleExecuteCommand}
              disabled={loading || !command.trim()}
              className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? '🔄 Processing...' : '🚀 Execute Command'}
            </button>
          </div>
        </div>
      </div>

      {/* Results */}
      {result && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            {result.success ? '✅ Execution Results' : '❌ Execution Failed'}
          </h3>
          
          <div className={`p-4 rounded-md mb-4 ${
            result.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
          }`}>
            <p className={result.success ? 'text-green-800' : 'text-red-800'}>
              {result.message}
            </p>
          </div>

          {/* Workflow Steps */}
          {result.workflow_steps && result.workflow_steps.length > 0 && (
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-2">Workflow Steps:</h4>
              <div className="bg-gray-50 p-4 rounded-md">
                <ul className="space-y-1">
                  {result.workflow_steps.map((step, index) => (
                    <li key={index} className="text-sm text-gray-700">
                      {step}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* Final Preference */}
          {result.final_preference && (
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-2">Final MHMD Preference:</h4>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                result.final_preference === 'OPT_IN' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {result.final_preference}
              </span>
            </div>
          )}

          {/* Database Verification */}
          {result.database_verification && (
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-2">Database Verification:</h4>
              <div className="bg-gray-50 p-4 rounded-md">
                <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                  {JSON.stringify(result.database_verification, null, 2)}
                </pre>
              </div>
            </div>
          )}

          {/* Screenshots */}
          {result.screenshot && (
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-2">Screenshot:</h4>
              <div className="border border-gray-200 rounded-md overflow-hidden">
                <img
                  src={`data:image/png;base64,${result.screenshot}`}
                  alt="Automation Screenshot"
                  className="w-full h-auto"
                />
              </div>
            </div>
          )}

          {/* Multiple Screenshots for Combined Workflows */}
          {result.screenshots && Array.isArray(result.screenshots) && result.screenshots.length > 0 && (
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-2">Screenshots:</h4>
              <div className="space-y-4">
                {result.screenshots.map((screenshot, index) => (
                  <div key={index} className="border border-gray-200 rounded-md overflow-hidden">
                    <div className="bg-gray-50 px-3 py-2 border-b border-gray-200">
                      <h5 className="text-sm font-medium text-gray-700">
                        {screenshot.description || `Screenshot ${index + 1}`}
                      </h5>
                    </div>
                    <img
                      src={`data:image/png;base64,${screenshot.screenshot}`}
                      alt={screenshot.description || `Screenshot ${index + 1}`}
                      className="w-full h-auto"
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Error Details */}
          {result.error && (
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-2">Error Details:</h4>
              <div className="bg-red-50 p-4 rounded-md">
                <pre className="text-sm text-red-700 whitespace-pre-wrap">
                  {result.error}
                </pre>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
