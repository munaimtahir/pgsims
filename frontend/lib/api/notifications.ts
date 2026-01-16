/**
 * Notifications API client
 * Handles user notifications
 */

import apiClient from './client';

export interface Notification {
  id: number;
  title: string;
  body: string;
  notification_type: string;
  is_read: boolean;
  created_at: string;
  recipient: number;
}

export interface NotificationPreferences {
  email_enabled: boolean;
  sms_enabled: boolean;
  push_enabled: boolean;
  notification_types: Record<string, boolean>;
}

export const notificationsApi = {
  /**
   * Get all notifications
   */
  list: async (params?: { is_read?: boolean; notification_type?: string; ordering?: string }) => {
    const response = await apiClient.get<{ results: Notification[]; count: number }>('/api/notifications/', { params });
    return response.data;
  },

  /**
   * Get unread notifications
   */
  getUnread: async () => {
    const response = await apiClient.get<{ results: Notification[]; count: number }>('/api/notifications/unread/');
    return response.data;
  },

  /**
   * Get unread count
   */
  getUnreadCount: async () => {
    const response = await apiClient.get<{ count: number }>('/api/notifications/unread-count/');
    return response.data;
  },

  /**
   * Mark notification as read
   */
  markRead: async (id: number) => {
    const response = await apiClient.post<{ message: string }>(`/api/notifications/mark-read/`, { id });
    return response.data;
  },

  /**
   * Get notification preferences
   */
  getPreferences: async () => {
    const response = await apiClient.get<NotificationPreferences>('/api/notifications/preferences/');
    return response.data;
  },

  /**
   * Update notification preferences
   */
  updatePreferences: async (preferences: Partial<NotificationPreferences>) => {
    const response = await apiClient.put<NotificationPreferences>('/api/notifications/preferences/', preferences);
    return response.data;
  },
};

export default notificationsApi;
