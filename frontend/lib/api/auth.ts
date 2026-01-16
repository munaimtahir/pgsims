/**
 * Authentication API client
 */

import apiClient from './client';

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name?: string;
  role: 'pg' | 'supervisor' | 'admin';
  specialty?: string;
  year?: string;
  phone_number?: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password2: string;
  first_name: string;
  last_name: string;
  role: 'pg' | 'supervisor' | 'admin';
  specialty?: string;
  year?: string;
  supervisor?: number;
  phone_number?: string;
}

export interface LoginResponse {
  user: User;
  access: string;
  refresh: string;
}

export interface RegisterResponse {
  user: User;
  tokens: {
    access: string;
    refresh: string;
  };
}

export const authApi = {
  /**
   * Login user
   */
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>('/api/auth/login/', credentials);
    return response.data;
  },

  /**
   * Register new user
   */
  async register(data: RegisterData): Promise<RegisterResponse> {
    const response = await apiClient.post<RegisterResponse>('/api/auth/register/', data);
    return response.data;
  },

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      try {
        await apiClient.post('/api/auth/logout/', { refresh: refreshToken });
      } catch (error) {
        // Ignore logout errors
        console.error('Logout error:', error);
      }
    }
    
    // Clear local storage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },

  /**
   * Get current user profile
   * Uses allowed endpoint: GET /api/auth/profile/
   */
  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<User>('/api/auth/profile/');
    return response.data;
  },

  /**
   * Refresh access token
   * Uses allowed endpoint: POST /api/auth/refresh/
   */
  async refreshToken(refreshToken: string): Promise<{ access: string }> {
    const response = await apiClient.post<{ access: string }>('/api/auth/refresh/', {
      refresh: refreshToken,
    });
    return response.data;
  },

  /**
   * Update user profile
   * Uses allowed endpoint: PUT/PATCH /api/auth/profile/update/
   */
  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await apiClient.patch<User>('/api/auth/profile/update/', data);
    return response.data;
  },

  /**
   * Request password reset
   * Uses allowed endpoint: POST /api/auth/password-reset/
   */
  async passwordReset(email: string): Promise<{ message: string }> {
    const response = await apiClient.post<{ message: string }>('/api/auth/password-reset/', { email });
    return response.data;
  },

  /**
   * Confirm password reset
   * Uses allowed endpoint: POST /api/auth/password-reset/confirm/
   */
  async passwordResetConfirm(data: {
    uid: string;
    token: string;
    new_password: string;
    new_password2: string;
  }): Promise<{ message: string }> {
    const response = await apiClient.post<{ message: string }>('/api/auth/password-reset/confirm/', data);
    return response.data;
  },

  /**
   * Change password
   * Uses allowed endpoint: POST /api/auth/change-password/
   */
  async changePassword(data: {
    old_password: string;
    new_password: string;
    new_password2: string;
  }): Promise<{ message: string }> {
    const response = await apiClient.post<{ message: string }>('/api/auth/change-password/', data);
    return response.data;
  },
};

export default authApi;
