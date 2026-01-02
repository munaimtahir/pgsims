/**
 * Base API client configuration using axios
 * Auto-detects localhost vs VPS deployment
 */

import axios from 'axios';

/**
 * Get API URL based on environment
 * Priority:
 * 1. NEXT_PUBLIC_API_URL environment variable
 * 2. Auto-detect from window.location (localhost vs VPS)
 * 3. Default to localhost:8000
 */
function getApiUrl(): string {
  // Use explicit environment variable if set
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }

  // Auto-detect from browser location (client-side only)
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
    const port = window.location.port;

    // VPS deployment (139.162.9.224, 172.237.95.120 or port 81)
    if (hostname === '139.162.9.224' || hostname === '172.237.95.120' || port === '81') {
      // Return API URL based on detected hostname
      if (hostname === '172.237.95.120') {
        return `http://172.237.95.120:81`;
      }
      return `http://139.162.9.224:81`;
    }

    // Localhost deployment
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      // If frontend is on 3000, backend is on 8000
      if (port === '3000' || !port) {
        return 'http://localhost:8000';
      }
      // If frontend is on same port or different, use 8000
      return 'http://localhost:8000';
    }
  }

  // Default fallback (server-side or unknown)
  return 'http://localhost:8000';
}

const API_URL = getApiUrl();

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      if (typeof window !== 'undefined') {
        try {
          const refreshToken = localStorage.getItem('refresh_token');
          if (refreshToken) {
            const response = await axios.post(`${API_URL}/api/token/refresh/`, {
              refresh: refreshToken,
            });

            const { access } = response.data;
            localStorage.setItem('access_token', access);

            originalRequest.headers.Authorization = `Bearer ${access}`;
            return apiClient(originalRequest);
          }
        } catch (refreshError) {
          // Refresh token failed, clear auth and redirect to login
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
