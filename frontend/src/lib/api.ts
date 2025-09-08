const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface MCPRequest {
  method: string;
  params?: Record<string, any>;
}

export interface MCPResponse {
  success: boolean;
  data?: any;
  error?: string;
}

export interface HealthResponse {
  status: string;
  message: string;
}

export interface UserData {
  name: string;
  email: string;
  mhmd_preference: 'OPT_IN' | 'OPT_OUT';
}

export interface UserResponse {
  success: boolean;
  data?: UserData;
  message: string;
}

export interface UserUpdateRequest {
  name?: string;
  email?: string;
  mhmd_preference?: 'OPT_IN' | 'OPT_OUT';
}

export interface AICommandRequest {
  command: string;
}

export interface ScreenshotData {
  screenshot: string;
  description?: string;
}

export interface AICommandResponse {
  success: boolean;
  message: string;
  workflow_steps?: string[];
  screenshot?: string;
  screenshots?: ScreenshotData[];
  final_preference?: string;
  database_verification?: any;
  error?: string;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Health check endpoints
  async getHealth(): Promise<HealthResponse> {
    return this.request<HealthResponse>('/health');
  }

  async getRoot(): Promise<HealthResponse> {
    return this.request<HealthResponse>('/');
  }

  // MCP endpoints
  async callMCPMethod(request: MCPRequest): Promise<MCPResponse> {
    return this.request<MCPResponse>('/mcp/call', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async listMCPTools(): Promise<MCPResponse> {
    return this.request<MCPResponse>('/mcp/tools');
  }

  // Example API endpoint
  async getExample(): Promise<any> {
    return this.request('/api/example');
  }

  // AI Automation methods for core functionality
  async executeAIAutomation(command: string, baseUrl?: string): Promise<MCPResponse> {
    return this.callMCPMethod({
      method: 'ai_browser_automation',
      params: { command, base_url: baseUrl || 'http://localhost:3000' }
    });
  }

  async executeMHMDWorkflow(name?: string, email?: string, preference?: string): Promise<MCPResponse> {
    return this.callMCPMethod({
      method: 'mhmd_toggle_workflow',
      params: { name, email, preference }
    });
  }

  // Note: AI Automation now handled exclusively through MCP endpoints
  // Use callMCPMethod() with methods: 'ai_browser_automation', 'mhmd_toggle_workflow', 'take_screenshot'



  // User Data API endpoints
  async getUserData(): Promise<UserResponse> {
    return this.request<UserResponse>('/api/user');
  }

  async createUserData(userData: UserData): Promise<UserResponse> {
    return this.request<UserResponse>('/api/user', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async updateUserData(updateData: UserUpdateRequest): Promise<UserResponse> {
    return this.request<UserResponse>('/api/user', {
      method: 'PATCH',
      body: JSON.stringify(updateData),
    });
  }

  async deleteUserData(): Promise<UserResponse> {
    return this.request<UserResponse>('/api/user', {
      method: 'DELETE',
    });
  }


}

export const apiService = new ApiService();
export default apiService;
