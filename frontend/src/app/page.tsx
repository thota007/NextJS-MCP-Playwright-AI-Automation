import Layout from '@/components/Layout';

export default function Home() {
  return (
    <Layout>
      <div className="max-w-4xl mx-auto px-6">
        <div className="bg-white rounded-lg shadow-md p-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-6">
            Welcome to NextJS + FastAPI + MCP
          </h1>
          <p className="text-lg text-gray-600 mb-8">
            This project demonstrates the integration between a NextJS React frontend 
            and a FastAPI backend with Model Context Protocol (MCP) server capabilities.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-blue-50 p-6 rounded-lg">
              <h2 className="text-xl font-semibold text-blue-900 mb-3">
                🚀 Features
              </h2>
              <ul className="text-blue-800 space-y-2">
                <li>• NextJS 15 with TypeScript</li>
                <li>• FastAPI backend with Python</li>
                <li>• Simulated MCP tools integration</li>
                <li>• Modern responsive UI with Tailwind CSS</li>
                <li>• Real-time API communication</li>
              </ul>
            </div>
            
            <div className="bg-green-50 p-6 rounded-lg">
              <h2 className="text-xl font-semibold text-green-900 mb-3">
                🛠️ Available Tools
              </h2>
              <ul className="text-green-800 space-y-2">
                <li>• <strong>Echo Tool</strong>: Message reflection</li>
                <li>• <strong>Calculator</strong>: Basic arithmetic</li>
                <li>• <strong>System Info</strong>: Platform details</li>
              </ul>
            </div>
          </div>
          
          <div className="bg-gray-50 p-6 rounded-lg">
            <h2 className="text-xl font-semibold text-gray-900 mb-3">
              🎯 Quick Start
            </h2>
            <p className="text-gray-700 mb-4">
              Visit <strong>Preferences</strong> to configure your settings and test the AI automation workflows.
            </p>
            <div className="flex space-x-4">
              <a 
                href="/preferences" 
                className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Settings
              </a>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
