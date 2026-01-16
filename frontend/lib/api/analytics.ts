/**
 * Analytics API client
 * Handles dashboard analytics and metrics
 */

import apiClient from './client';

export interface DashboardOverview {
  total_users: number;
  total_pgs: number;
  total_supervisors: number;
  active_rotations: number;
  pending_reviews: number;
  recent_activity: any[];
}

export interface TrendData {
  period: string;
  value: number;
  label: string;
}

export interface ComplianceMetrics {
  logbook_compliance: number;
  certificate_compliance: number;
  rotation_compliance: number;
  overall_compliance: number;
}

export interface PerformanceMetrics {
  average_scores: number;
  pass_rate: number;
  completion_rate: number;
  top_performers: any[];
}

export const analyticsApi = {
  /**
   * Get dashboard overview
   */
  getDashboardOverview: async () => {
    const response = await apiClient.get<DashboardOverview>('/api/analytics/dashboard/overview/');
    return response.data;
  },

  /**
   * Get trends data
   */
  getTrends: async (params?: { period?: string; metric?: string }) => {
    const response = await apiClient.get<TrendData[]>('/api/analytics/dashboard/trends/', { params });
    return response.data;
  },

  /**
   * Get compliance metrics
   */
  getCompliance: async () => {
    const response = await apiClient.get<ComplianceMetrics>('/api/analytics/dashboard/compliance/');
    return response.data;
  },

  /**
   * Get performance metrics
   */
  getPerformance: async (params?: { period?: string }) => {
    const response = await apiClient.get<PerformanceMetrics>('/api/analytics/performance/', { params });
    return response.data;
  },
};

export default analyticsApi;
