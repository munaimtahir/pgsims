/**
 * Bulk operations API client
 * Handles bulk imports and assignments
 */

import apiClient from './client';

export interface BulkImportResult {
  success: boolean;
  success_count: number;
  failure_count?: number;
  error_count: number;
  errors: string[];
  imported_items: unknown[];
  import_id?: number;
}

export interface BulkAssignmentResult {
  success: boolean;
  assigned_count: number;
  failed_count: number;
  errors: string[];
}

export interface BulkReviewPayload {
  entry_ids: number[];
  status: 'approved' | 'returned' | 'rejected';
}

export const bulkApi = {
  /**
   * Bulk import (generic)
   */
  import: async (file: File, importType: string) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('import_type', importType);
    formData.append('dry_run', 'false');
    formData.append('allow_partial', 'true');
    
    const response = await apiClient.post<BulkImportResult>('/api/bulk/import/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Import trainees
   */
  importTrainees: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('dry_run', 'false');
    formData.append('allow_partial', 'true');
    
    const response = await apiClient.post<BulkImportResult>('/api/bulk/import-trainees/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Import supervisors
   */
  importSupervisors: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('dry_run', 'false');
    formData.append('allow_partial', 'true');
    
    const response = await apiClient.post<BulkImportResult>('/api/bulk/import-supervisors/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Import residents
   */
  importResidents: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('dry_run', 'false');
    formData.append('allow_partial', 'true');
    
    const response = await apiClient.post<BulkImportResult>('/api/bulk/import-residents/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  importDepartments: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('dry_run', 'false');
    formData.append('allow_partial', 'true');

    const response = await apiClient.post<BulkImportResult>('/api/bulk/import-departments/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Bulk assignment
   */
  assignment: async (data: { assignments: Array<{ user_id: number; supervisor_id: number }> }) => {
    const response = await apiClient.post<BulkAssignmentResult>('/api/bulk/assignment/', data);
    return response.data;
  },

  /**
   * Review bulk import
   */
  review: async (payload: BulkReviewPayload) => {
    const response = await apiClient.post<BulkImportResult>('/api/bulk/review/', payload);
    return response.data;
  },

  exportDataset: async (resource: 'residents' | 'supervisors' | 'departments', format: 'xlsx' | 'csv' = 'xlsx') => {
    const response = await apiClient.get(`/api/bulk/exports/${resource}/?file_format=${format}`, {
      responseType: 'blob',
    });
    return response.data as Blob;
  },
};

export default bulkApi;
