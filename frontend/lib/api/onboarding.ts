import apiClient from './client';

export interface OnboardingUploadResponse {
  batch_id: number;
  file_name: string;
  headers: string[];
  sample_rows: Array<Record<string, string>>;
  total_rows: number;
  suggested_mapping: Record<string, string>;
}

export interface OnboardingPreviewRow {
  row_number: number;
  resident_name: string;
  father_name: string;
  department: string;
  program_name: string;
  training_year: string;
  supervisor_name: string;
  mobile_number: string;
  email: string;
  cnic: string;
  registration_number: string;
  joining_date: string;
  status: 'Ready' | 'Error' | 'Possible Duplicate';
  remarks: string;
  _payload?: Record<string, string>;
}

export interface OnboardingBatchRow {
  id: number;
  file_name: string;
  uploaded_by: string;
  uploaded_at: string;
  total_rows: number;
  ready_rows: number;
  error_rows: number;
  duplicate_rows: number;
  imported_rows: number;
  logins_generated: number;
  status: string;
}

export interface OnboardingBatchDetail extends OnboardingBatchRow {
  mapping: Record<string, string>;
  headers: string[];
  sample_rows: Array<Record<string, string>>;
  preview_rows: OnboardingPreviewRow[];
  error_rows_data: Array<Record<string, unknown>>;
  imported_resident_ids: number[];
}

export interface LoginSheetRow {
  resident_id: number;
  resident_name: string;
  department: string;
  program: string;
  training_year: string;
  mobile_number: string;
  email: string;
  cnic: string;
  registration_number: string;
  username: string;
  temporary_password: string;
  login_url: string;
  login_generated: boolean;
  login_issued: boolean;
  login_issued_at: string | null;
  login_issued_by: string;
  profile_completed: boolean;
  force_password_change: boolean;
  last_login: string | null;
  row_status: string;
}

export interface IncompleteProfileRow {
  resident_id: number;
  resident_name: string;
  first_name: string;
  last_name: string;
  username: string;
  department_id: number | null;
  department: string;
  program: string;
  training_year: string;
  joining_date: string | null;
  mobile_number: string;
  email: string;
  cnic: string;
  profile_completed: boolean;
  force_password_change: boolean;
  last_login: string | null;
  login_issued: boolean;
  login_generated: boolean;
}

export const onboardingApi = {
  uploadPreview: async (file: File): Promise<OnboardingUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post<OnboardingUploadResponse>('/api/onboarding/residents/upload-preview/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  mapColumns: async (batchId: number, mapping: Record<string, string>): Promise<{
    batch_id: number;
    total_rows: number;
    ready_rows: number;
    error_rows: number;
    duplicate_rows: number;
    preview_rows: OnboardingPreviewRow[];
    mapping: Record<string, string>;
  }> => {
    const response = await apiClient.post('/api/onboarding/residents/map-columns/', {
      batch_id: batchId,
      mapping,
    });
    return response.data;
  },

  importResidents: async (batchId: number): Promise<{ batch_id: number; imported_rows: number; imported_resident_ids: number[] }> => {
    const response = await apiClient.post('/api/onboarding/residents/import/', { batch_id: batchId });
    return response.data;
  },

  generateLogins: async (batchId?: number): Promise<{ generated: number }> => {
    const response = await apiClient.post('/api/onboarding/residents/generate-logins/', batchId ? { batch_id: batchId } : {});
    return response.data;
  },

  getLoginSheet: async (batchId?: number): Promise<LoginSheetRow[]> => {
    const response = await apiClient.get<LoginSheetRow[]>('/api/onboarding/residents/login-sheet/', {
      params: batchId ? { batch_id: batchId } : undefined,
    });
    return response.data;
  },

  exportLoginSheetExcel: async (batchId?: number): Promise<Blob> => {
    const response = await apiClient.get('/api/onboarding/residents/login-sheet/export-excel/', {
      params: batchId ? { batch_id: batchId } : undefined,
      responseType: 'blob',
    });
    return response.data;
  },

  exportLoginSheetPdf: async (batchId?: number): Promise<Blob> => {
    const response = await apiClient.get('/api/onboarding/residents/login-sheet/export-pdf/', {
      params: batchId ? { batch_id: batchId } : undefined,
      responseType: 'blob',
    });
    return response.data;
  },

  markIssued: async (payload: { resident_ids?: number[]; mark_all?: boolean }): Promise<{ updated: number }> => {
    const response = await apiClient.post('/api/onboarding/residents/mark-issued/', payload);
    return response.data;
  },

  listBatches: async (): Promise<OnboardingBatchRow[]> => {
    const response = await apiClient.get<OnboardingBatchRow[]>('/api/onboarding/residents/batches/');
    return response.data;
  },

  getBatch: async (batchId: number): Promise<OnboardingBatchDetail> => {
    const response = await apiClient.get<OnboardingBatchDetail>(`/api/onboarding/residents/batches/${batchId}/`);
    return response.data;
  },

  listBatchResidents: async (batchId: number): Promise<LoginSheetRow[]> => {
    const response = await apiClient.get<LoginSheetRow[]>(`/api/onboarding/residents/batches/${batchId}/residents/`);
    return response.data;
  },

  generateBatchLogins: async (batchId: number): Promise<{ generated: number }> => {
    const response = await apiClient.post(`/api/onboarding/residents/batches/${batchId}/generate-logins/`);
    return response.data;
  },

  exportBatchLoginSheet: async (batchId: number): Promise<Blob> => {
    const response = await apiClient.get(`/api/onboarding/residents/batches/${batchId}/login-sheet/export/`, {
      responseType: 'blob',
    });
    return response.data;
  },

  downloadBatchErrorReport: async (batchId: number): Promise<Blob> => {
    const response = await apiClient.get(`/api/onboarding/residents/batches/${batchId}/error-report/`, {
      responseType: 'blob',
    });
    return response.data;
  },

  listIncompleteProfiles: async (): Promise<IncompleteProfileRow[]> => {
    const response = await apiClient.get<IncompleteProfileRow[]>('/api/onboarding/residents/incomplete-profiles/');
    return response.data;
  },

  exportIncompleteProfiles: async (): Promise<Blob> => {
    const response = await apiClient.get('/api/onboarding/residents/incomplete-profiles/export/', {
      responseType: 'blob',
    });
    return response.data;
  },

  resetPassword: async (residentId: number): Promise<{ detail: string }> => {
    const response = await apiClient.post(`/api/onboarding/residents/${residentId}/reset-password/`);
    return response.data;
  },

  updateResident: async (
    residentId: number,
    payload: Partial<{
      first_name: string;
      last_name: string;
      email: string;
      mobile_number: string;
      cnic: string;
      program: string;
      training_year: string;
      joining_date: string | null;
      department_id: number | null;
      profile_completed: boolean;
    }>
  ): Promise<{ detail: string }> => {
    const response = await apiClient.patch(`/api/onboarding/residents/${residentId}/`, payload);
    return response.data;
  },

  markProfileComplete: async (residentId: number): Promise<{ detail: string }> => {
    const response = await apiClient.post(`/api/onboarding/residents/${residentId}/mark-profile-complete/`);
    return response.data;
  },
};

export default onboardingApi;
