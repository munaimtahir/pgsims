/**
 * Base API client configuration using axios
 * Uses NEXT_PUBLIC_API_URL for browser and SERVER_API_URL for server-side execution
 */

import axios from 'axios';
import { clearAuthCookies, syncAuthCookies } from '@/lib/auth/cookies';

/**
 * Resolve API base URL:
 * - Browser/client: default to same-origin paths (effective /api usage)
 * - Server-only contexts: default to internal Docker DNS
 */
function getApiUrl(): string {
  const isServer = typeof window === 'undefined';

  if (isServer) {
    return process.env.SERVER_API_URL || 'http://backend:8014';
  }

  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  if (!apiUrl || apiUrl === '/api') {
    if (process.env.NODE_ENV === 'development' && !apiUrl) {
      console.warn('NEXT_PUBLIC_API_URL not set, defaulting to same-origin API paths');
    }
    // Endpoints already include /api/... so keep base empty to avoid /api/api/* duplication.
    return '';
  }

  // If an absolute URL points to the same origin, keep requests relative.
  try {
    const resolved = new URL(apiUrl, window.location.origin);
    if (resolved.origin === window.location.origin) {
      return '';
    }
  } catch {
    // Keep raw value for non-URL strings.
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
            syncAuthCookies({
              accessToken: access,
              role: (() => {
                try {
                  const user = JSON.parse(localStorage.getItem('user') || 'null');
                  return user?.role ?? null;
                } catch {
                  return null;
                }
              })(),
            });

            originalRequest.headers.Authorization = `Bearer ${access}`;
            return apiClient(originalRequest);
          }
        } catch (refreshError) {
          // Refresh token failed, clear auth and redirect to login
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');
          clearAuthCookies();
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
