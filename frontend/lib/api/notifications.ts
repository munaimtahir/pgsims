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
   * Uses list endpoint with is_read=false filter
   */
  getUnread: async () => {
    const response = await apiClient.get<{ results: Notification[]; count: number }>('/api/notifications/', {
      params: { is_read: false },
    });
    return response.data;
  },

  /**
   * Get unread count
   * Backend returns {"unread": count}, frontend expects {"count": count}
   */
  getUnreadCount: async () => {
    const response = await apiClient.get<{ unread: number }>('/api/notifications/unread-count/');
    return { count: response.data.unread };
  },

  /**
   * Mark notification as read
   * Backend expects { notification_ids: [id] }, not { id }
   */
  markRead: async (id: number) => {
    const response = await apiClient.post<{ marked: number }>(`/api/notifications/mark-read/`, {
      notification_ids: [id],
    });
    return { message: `${response.data.marked} notification(s) marked as read` };
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
