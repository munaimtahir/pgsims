import apiClient from './client';

export interface CaseCategory {
  id: number;
  name: string;
  description?: string;
  color_code?: string;
}

export interface ClinicalCasePayload {
  case_title: string;
  date_encountered: string;
  patient_age: number;
  patient_gender: 'M' | 'F' | 'O' | 'U';
  chief_complaint: string;
  history_of_present_illness: string;
  physical_examination: string;
  management_plan: string;
  clinical_reasoning: string;
  learning_points: string;
  category?: number;
  primary_diagnosis?: number;
}

export interface ClinicalCase {
  id: number;
  case_title: string;
  status: string;
  date_encountered: string;
  patient_age: number;
  patient_gender: string;
  chief_complaint: string;
  clinical_reasoning: string;
  learning_points: string;
  supervisor_feedback?: string;
  pg_name?: string;
  supervisor_name?: string;
}

export interface CaseStatistics {
  total_cases: number;
  pending_cases: number;
  approved_cases: number;
  needs_revision_cases: number;
  rejected_cases: number;
  draft_cases: number;
}

export const casesApi = {
  getCategories: async () => {
    const response = await apiClient.get<CaseCategory[]>('/api/cases/categories/');
    return response.data;
  },
  getMyCases: async () => {
    const response = await apiClient.get<ClinicalCase[]>('/api/cases/my/');
    return response.data;
  },
  createMyCase: async (payload: ClinicalCasePayload) => {
    const response = await apiClient.post<ClinicalCase>('/api/cases/my/', payload);
    return response.data;
  },
  updateMyCase: async (id: number, payload: Partial<ClinicalCasePayload>) => {
    const response = await apiClient.patch<ClinicalCase>(`/api/cases/my/${id}/`, payload);
    return response.data;
  },
  submitMyCase: async (id: number) => {
    const response = await apiClient.post<ClinicalCase>(`/api/cases/my/${id}/submit/`);
    return response.data;
  },
  getPendingCases: async () => {
    const response = await apiClient.get<ClinicalCase[]>('/api/cases/pending/');
    return response.data;
  },
  reviewCase: async (
    id: number,
    payload: { status: 'approved' | 'needs_revision' | 'rejected'; overall_feedback: string }
  ) => {
    const response = await apiClient.post<{ case: ClinicalCase; review_status: string }>(
      `/api/cases/${id}/review/`,
      payload
    );
    return response.data;
  },
  getStatistics: async () => {
    const response = await apiClient.get<CaseStatistics>('/api/cases/statistics/');
    return response.data;
  },
};

