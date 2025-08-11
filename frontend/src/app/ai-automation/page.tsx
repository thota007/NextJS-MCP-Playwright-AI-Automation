'use client';

import Layout from '@/components/Layout';
import AIAutomation from '@/components/AIAutomation';

export default function AIAutomationPage() {
  return (
    <Layout>
      <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            🤖 AI Automation
          </h1>
          <p className="text-lg text-gray-600 mt-2">
            Execute custom natural language commands for browser automation workflows
          </p>
        </div>

        {/* AI Automation Interface */}
        <div className="bg-white shadow rounded-lg p-6">
          <div className="border-b border-gray-200 pb-4 mb-6">
            <h2 className="text-lg font-medium text-gray-900">
              Custom NLP Commands
            </h2>
            <p className="text-sm text-gray-600 mt-1">
              Enter natural language commands to automate browser workflows. The system will process your commands using AI and execute them through the unified MCP server.
            </p>
          </div>
          
          <AIAutomation />
          
          {/* Usage Examples */}
          <div className="mt-8 p-4 bg-blue-50 rounded-lg">
            <h3 className="text-sm font-medium text-blue-900 mb-3">
              💡 Example Commands
            </h3>
            <div className="text-sm text-blue-800 space-y-2">
              <div className="flex items-start">
                <span className="font-medium mr-2">•</span>
                <span>"Visit localhost:3000, find preferences, toggle MHMD preferences, save data to db and send validation back to user with screenshot"</span>
              </div>
              <div className="flex items-start">
                <span className="font-medium mr-2">•</span>
                <span>"Navigate to the preferences page and take a screenshot"</span>
              </div>
              <div className="flex items-start">
                <span className="font-medium mr-2">•</span>
                <span>"Fill out the form with name John and email john@example.com then save"</span>
              </div>
              <div className="flex items-start">
                <span className="font-medium mr-2">•</span>
                <span>"Toggle MHMD preference to OPT_IN and capture the result"</span>
              </div>
            </div>
          </div>

          {/* Features Info */}
          <div className="mt-6 p-4 bg-green-50 rounded-lg">
            <h3 className="text-sm font-medium text-green-900 mb-3">
              ✨ Automation Features
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-green-800">
              <div className="flex items-center">
                <span className="font-medium mr-2">📸</span>
                <span>Screenshots saved as PNG files</span>
              </div>
              <div className="flex items-center">
                <span className="font-medium mr-2">💾</span>
                <span>Verification data saved as JSON files</span>
              </div>
              <div className="flex items-center">
                <span className="font-medium mr-2">🎯</span>
                <span>Natural language command processing</span>
              </div>
              <div className="flex items-center">
                <span className="font-medium mr-2">🔄</span>
                <span>MHMD preference workflow automation</span>
              </div>
              <div className="flex items-center">
                <span className="font-medium mr-2">🗄️</span>
                <span>Database verification and validation</span>
              </div>
              <div className="flex items-center">
                <span className="font-medium mr-2">📋</span>
                <span>Detailed workflow step reporting</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
