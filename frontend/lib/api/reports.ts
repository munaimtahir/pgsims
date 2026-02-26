/**
 * Reports API client
 * Handles report generation and scheduling
 */

import apiClient from './client';

export interface ReportTemplate {
  id: number;
  name: string;
  description: string;
  report_type: string;
  parameters: Record<string, unknown>;
}

export interface ReportCatalogItem {
  key: string;
  title: string;
}

export interface ReportRunResponse {
  key: string;
  rows: Array<Record<string, unknown>>;
  summary: Record<string, unknown>;
}

export interface ScheduledReport {
  id: number;
  template: number;
  schedule_type: string;
  recipients: string[];
  parameters: Record<string, unknown>;
  last_run?: string;
  next_run?: string;
  active: boolean;
}

export interface GeneratedReport {
  id: number;
  template: number;
  generated_at: string;
  file_url?: string;
  parameters: Record<string, unknown>;
}

export const reportsApi = {
  getCatalog: async () => {
    const response = await apiClient.get<{ results: ReportCatalogItem[] }>('/api/reports/catalog/');
    return response.data.results;
  },

  run: async (key: string, filters: Record<string, string | number | undefined> = {}) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([filterKey, value]) => {
      if (value !== undefined && value !== '') params.append(filterKey, String(value));
    });
    const query = params.toString();
    const response = await apiClient.get<ReportRunResponse>(`/api/reports/run/${key}/${query ? `?${query}` : ''}`);
    return response.data;
  },

  export: async (key: string, format: 'xlsx' | 'csv', filters: Record<string, string | number | undefined> = {}) => {
    const params = new URLSearchParams({ file_format: format });
    Object.entries(filters).forEach(([filterKey, value]) => {
      if (value !== undefined && value !== '') params.append(filterKey, String(value));
    });
    const response = await apiClient.get(`/api/reports/export/${key}/?${params.toString()}`, {
      responseType: 'blob',
    });
    return response.data as Blob;
  },

  /**
   * Get available report templates
   */
  getTemplates: async () => {
    const response = await apiClient.get<{ results: ReportTemplate[]; count: number }>('/api/reports/templates/');
    return response.data;
  },

  /**
   * Generate a report
   */
  generate: async (templateId: number, parameters: Record<string, unknown>) => {
    const response = await apiClient.post<GeneratedReport>('/api/reports/generate/', {
      template: templateId,
      parameters,
    });
    return response.data;
  },

  /**
   * Get scheduled reports
   */
  getScheduled: async () => {
    const response = await apiClient.get<{ results: ScheduledReport[]; count: number }>('/api/reports/scheduled/');
    return response.data;
  },

  /**
   * Create a scheduled report
   */
  schedule: async (data: Partial<ScheduledReport>) => {
    const response = await apiClient.post<ScheduledReport>('/api/reports/scheduled/', data);
    return response.data;
  },

  /**
   * Get scheduled report details
   */
  getScheduledDetail: async (id: number) => {
    const response = await apiClient.get<ScheduledReport>(`/api/reports/scheduled/${id}/`);
    return response.data;
  },
};

export default reportsApi;
