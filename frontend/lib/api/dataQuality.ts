import apiClient from './client';

export interface CanonicalDataQualitySummary {
  summary: Record<string, number>;
  sections: Array<{
    key: string;
    label: string;
    count: number;
    items: Array<Record<string, unknown>>;
  }>;
}

export const dataQualityApi = {
  getIdentityDataQuality: async () => (await apiClient.get<CanonicalDataQualitySummary>('/api/data-quality/')).data,
  getAcademicDataQuality: async () => (await apiClient.get<CanonicalDataQualitySummary>('/api/academics/data-quality/')).data,
  getSupervisionDataQuality: async () => (await apiClient.get<CanonicalDataQualitySummary>('/api/supervision/data-quality/')).data,
};

export default dataQualityApi;
