import apiClient from './client';

export interface DashboardOverview {
  total_users?: number;
  total_pgs?: number;
  total_supervisors?: number;
  active_rotations?: number;
  pending_reviews?: number;
  recent_activity?: unknown[];
  total_residents?: number;
  pending_certificates?: number;
  last_30d_logs?: number;
  last_30d_cases?: number;
  unverified_logs?: number;
}

export interface AnalyticsCard {
  key: string;
  title: string;
  value: number;
}

export interface AnalyticsTable {
  columns: string[];
  rows: Array<Record<string, unknown>>;
}

export interface AnalyticsTabPayload {
  title: string;
  date_range: {
    start_date: string;
    end_date: string;
  };
  cards: AnalyticsCard[];
  table: AnalyticsTable;
  series: Array<Record<string, unknown>>;
}

export interface AnalyticsLivePayload {
  date_range: {
    start_date: string;
    end_date: string;
  };
  events: Array<Record<string, unknown>>;
}

export interface AnalyticsFiltersPayload {
  roles: string[];
  departments: Array<{ id: number; name: string }>;
  hospitals: Array<{ id: number; name: string }>;
}

export interface AnalyticsQueryParams {
  start_date?: string;
  end_date?: string;
  department_id?: number | '';
  hospital_id?: number | '';
  role?: string;
}

export interface AnalyticsUIEventPayload {
  event_type: 'page.view' | 'feature.used' | 'ui.page.view' | 'ui.feature.used';
  metadata?: Record<string, unknown>;
  department_id?: number;
  hospital_id?: number;
  entity_type?: string;
  entity_id?: string;
  event_key?: string;
  occurred_at?: string;
}

const cleanParams = (params?: AnalyticsQueryParams) => {
  if (!params) return undefined;
  const cleaned: Record<string, string | number> = {};
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      cleaned[key] = value as string | number;
    }
  });
  return cleaned;
};

export const analyticsApi = {
  // Legacy endpoints used by admin dashboard cards
  getDashboardOverview: async () => {
    const response = await apiClient.get<DashboardOverview>('/api/analytics/dashboard/overview/');
    return response.data;
  },

  getFilters: async () => {
    const response = await apiClient.get<AnalyticsFiltersPayload>('/api/analytics/v1/filters/');
    return response.data;
  },

  getTab: async (tab: string, params?: AnalyticsQueryParams) => {
    const response = await apiClient.get<AnalyticsTabPayload>(`/api/analytics/v1/tabs/${tab}/`, {
      params: cleanParams(params),
    });
    return response.data;
  },

  getLive: async (params?: AnalyticsQueryParams & { limit?: number }) => {
    const response = await apiClient.get<AnalyticsLivePayload>('/api/analytics/v1/live/', {
      params: cleanParams(params),
    });
    return response.data;
  },

  exportTabCsv: async (tab: string, params?: AnalyticsQueryParams) => {
    const response = await apiClient.get(`/api/analytics/v1/tabs/${tab}/export/`, {
      params: cleanParams(params),
      responseType: 'blob',
    });
    return response.data as Blob;
  },

  ingestUIEvent: async (payload: AnalyticsUIEventPayload) => {
    const response = await apiClient.post<{ accepted: boolean; event_id: string | null }>(
      '/api/analytics/events/',
      payload
    );
    return response.data;
  },
};

export default analyticsApi;
