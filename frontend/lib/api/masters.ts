import apiClient from './client';
import type { UserbaseDepartment, UserbaseHospital, UserbaseHospitalDepartment } from './userbase';

export interface MasterTrainingProgram {
  id: number;
  code: string;
  name: string;
  degree_type?: string;
  duration_months?: number;
  active?: boolean;
}

type ListResponse<T> = { count?: number; results?: T[] } | T[];

function unwrapList<T>(data: ListResponse<T>): T[] {
  return Array.isArray(data) ? data : data.results || [];
}

export const mastersApi = {
  listHospitals: async () => unwrapList((await apiClient.get<ListResponse<UserbaseHospital>>('/api/hospitals/')).data),
  listDepartments: async () => unwrapList((await apiClient.get<ListResponse<UserbaseDepartment>>('/api/departments/')).data),
  listMatrix: async () => unwrapList((await apiClient.get<ListResponse<UserbaseHospitalDepartment>>('/api/hospital-departments/')).data),
  listPrograms: async () => unwrapList((await apiClient.get<ListResponse<MasterTrainingProgram>>('/api/programs/')).data),
};

export default mastersApi;
