import apiClient from './client';
import type { UserbaseDepartment, UserbaseHospitalDepartment } from './userbase';

interface SupervisionLinkPayload {
  supervisor: number;
  resident: number;
  start_date?: string;
  active?: boolean;
}

interface HodAssignmentPayload {
  department: number;
  hod: number;
  start_date?: string;
  active?: boolean;
}

export const getDepartments = () => apiClient.get('/api/departments/');
export const createDepartment = (data: Partial<UserbaseDepartment>) => apiClient.post('/api/departments/', data);
export const updateDepartment = (id: number, data: Partial<UserbaseDepartment>) => apiClient.patch(`/api/departments/${id}/`, data);
export const deleteDepartment = (id: number) => apiClient.delete(`/api/departments/${id}/`);
export const getHospitalDepartments = () => apiClient.get('/api/hospital-departments/');
export const createHospitalDepartment = (data: Partial<UserbaseHospitalDepartment>) => apiClient.post('/api/hospital-departments/', data);
export const deleteHospitalDepartment = (id: number) => apiClient.delete(`/api/hospital-departments/${id}/`);
// Canonical URL is /api/supervision-links/ (fixed from /api/supervisor-resident-links/)
export const getSupervisorResidentLinks = () => apiClient.get('/api/supervision-links/');
export const createSupervisorResidentLink = (data: SupervisionLinkPayload) => apiClient.post('/api/supervision-links/', data);
export const deleteSupervisorResidentLink = (id: number) => apiClient.delete(`/api/supervision-links/${id}/`);
export const getHodAssignments = () => apiClient.get('/api/hod-assignments/');
export const createHodAssignment = (data: HodAssignmentPayload) => apiClient.post('/api/hod-assignments/', data);
