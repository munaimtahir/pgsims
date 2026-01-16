/**
 * Base API client configuration using axios
 * Uses NEXT_PUBLIC_API_URL environment variable only
 */

import axios from 'axios';

/**
 * Get API URL from environment variable
 * MUST use NEXT_PUBLIC_API_URL only - no auto-detection
 */
function getApiUrl(): string {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  if (!apiUrl) {
    // In development, provide a default but warn
    if (process.env.NODE_ENV === 'development') {
      console.warn('NEXT_PUBLIC_API_URL not set, using default http://localhost:8000');
      return 'http://localhost:8000';
    }
    // In production, throw error
    throw new Error('NEXT_PUBLIC_API_URL environment variable is required');
  }
  return apiUrl;
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
            // Use allowed endpoint: POST /api/auth/refresh/
            const response = await axios.post(`${API_URL}/api/auth/refresh/`, {
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
