import apiClient from './client';

export type BulkUserbaseEntity =
  | 'hospitals'
  | 'departments'
  | 'matrix'
  | 'faculty-supervisors'
  | 'residents'
  | 'supervision-links'
  | 'hod-assignments';

export type BulkImportAction = 'dry-run' | 'apply';
export type BulkExportFormat = 'csv' | 'xlsx';

export interface BulkRowResult {
  row: number | string;
  error?: string;
  [key: string]: unknown;
}

export interface BulkOperationResult {
  operation?: string;
  status?: string;
  success_count: number;
  failure_count: number;
  details?: {
    successes?: BulkRowResult[];
    failures?: BulkRowResult[];
  };
  dry_run?: boolean;
  created_at?: string;
  completed_at?: string;
}

export const bulkApi = {
  importEntity: async (
    entity: BulkUserbaseEntity,
    file: File,
    action: BulkImportAction
  ) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post<BulkOperationResult>(
      `/api/bulk/import/${entity}/${action}/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },

  downloadTemplate: async (resource: BulkUserbaseEntity) => {
    const response = await apiClient.get(`/api/bulk/templates/${resource}/`, {
      responseType: 'blob',
    });
    return response.data as Blob;
  },

  exportDataset: async (
    resource: BulkUserbaseEntity,
    format: BulkExportFormat = 'xlsx'
  ) => {
    const response = await apiClient.get(`/api/bulk/exports/${resource}/`, {
      params: { file_format: format },
      responseType: 'blob',
    });
    return response.data as Blob;
  },
};

export default bulkApi;
