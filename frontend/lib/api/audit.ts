/**
 * Audit API client
 * Handles audit logs and activity tracking
 */

import apiClient from './client';

export interface ActivityLog {
  id: number;
  user: number;
  action: string;
  details: Record<string, any>;
  ip_address?: string;
  user_agent?: string;
  created_at: string;
}

export interface AuditReport {
  id: number;
  report_type: string;
  parameters: Record<string, any>;
  generated_at: string;
  file_url?: string;
}

export const auditApi = {
  /**
   * Get activity logs
   */
  getActivityLogs: async (params?: { user?: number; action?: string; start_date?: string; end_date?: string; ordering?: string }) => {
    const response = await apiClient.get<{ results: ActivityLog[]; count: number }>('/api/audit/activity/', { params });
    return response.data;
  },

  /**
   * Get audit reports
   */
  getReports: async (params?: { report_type?: string; ordering?: string }) => {
    const response = await apiClient.get<{ results: AuditReport[]; count: number }>('/api/audit/reports/', { params });
    return response.data;
  },

  /**
   * Create audit report
   */
  createReport: async (data: { report_type: string; parameters: Record<string, any> }) => {
    const response = await apiClient.post<AuditReport>('/api/audit/reports/', data);
    return response.data;
  },
};

export default auditApi;
