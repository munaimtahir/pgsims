import apiClient from './client';

export interface SupervisionPerson {
  id: number;
  name: string;
  username: string;
  email?: string;
  phone?: string;
  designation?: string;
  department?: string;
  training_site?: string;
}

export interface SupervisionAssignment {
  id: number;
  assignment_type: 'PRIMARY' | 'CO_SUPERVISOR';
  status: 'ACTIVE' | 'ENDED' | 'SUSPENDED';
  start_date: string | null;
  end_date: string | null;
  notes?: string;
  reason_for_change?: string;
  supervisor: SupervisionPerson;
  resident: SupervisionPerson;
}

export interface SupervisionAssignmentPayload {
  resident_id: number;
  supervisor_id: number;
  assignment_type?: 'PRIMARY' | 'CO_SUPERVISOR';
  start_date: string;
  notes?: string;
}

export interface SupervisionEndPayload {
  end_date: string;
  reason_for_change?: string;
}

export interface SupervisionChangePrimaryPayload {
  resident_id: number;
  new_supervisor_id: number;
  start_date: string;
  reason_for_change?: string;
}

export interface SupervisionOptionPerson {
  id: number;
  name: string;
  username: string;
  training_site?: string;
  department?: string;
  designation?: string;
  has_active_primary?: boolean;
  active_primary_count?: number;
  active_total_count?: number;
}

export interface SupervisionOptions {
  residents: SupervisionOptionPerson[];
  supervisors: SupervisionOptionPerson[];
}

export type SupervisionDataQuality = Record<string, Array<Record<string, unknown>>>;

export interface SupervisionImportResult {
  success: boolean;
  dry_run: boolean;
  successes: Array<Record<string, unknown>>;
  failures: Array<Record<string, unknown>>;
  warnings?: Array<Record<string, unknown>>;
}

export const supervisionApi = {
  listAssignments: async (params?: Record<string, unknown>) => {
    const response = await apiClient.get<{ count?: number; results?: SupervisionAssignment[] } | SupervisionAssignment[]>(
      '/api/supervision/assignments/',
      { params }
    );
    return Array.isArray(response.data) ? response.data : response.data.results || [];
  },
  getAssignment: async (id: number) => {
    const response = await apiClient.get<SupervisionAssignment>(`/api/supervision/assignments/${id}/`);
    return response.data;
  },
  createAssignment: async (payload: SupervisionAssignmentPayload) => {
    const response = await apiClient.post<SupervisionAssignment>('/api/supervision/assignments/', payload);
    return response.data;
  },
  endAssignment: async (id: number, payload: SupervisionEndPayload) => {
    const response = await apiClient.post<SupervisionAssignment>(`/api/supervision/assignments/${id}/end/`, payload);
    return response.data;
  },
  changePrimary: async (payload: SupervisionChangePrimaryPayload) => {
    const response = await apiClient.post<SupervisionAssignment>('/api/supervision/change-primary/', payload);
    return response.data;
  },
  getSupervisionOptions: async (params?: Record<string, unknown>) => {
    const response = await apiClient.get<SupervisionOptions>('/api/supervision/options/', { params });
    return response.data;
  },
  getSupervisionDataQuality: async () => {
    const response = await apiClient.get<SupervisionDataQuality>('/api/supervision/data-quality/');
    return response.data;
  },
  importSupervisionCsv: async (file: File, dryRun = true) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('dry_run', dryRun ? 'true' : 'false');
    const response = await apiClient.post<SupervisionImportResult>('/api/supervision/import/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
};

export default supervisionApi;
