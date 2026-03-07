import apiClient from './client';
export const getDepartments = () => apiClient.get('/api/departments/');
export const createDepartment = (data: any) => apiClient.post('/api/departments/', data);
export const updateDepartment = (id: number, data: any) => apiClient.patch(`/api/departments/${id}/`, data);
export const deleteDepartment = (id: number) => apiClient.delete(`/api/departments/${id}/`);
export const getHospitalDepartments = () => apiClient.get('/api/hospital-departments/');
export const createHospitalDepartment = (data: any) => apiClient.post('/api/hospital-departments/', data);
export const deleteHospitalDepartment = (id: number) => apiClient.delete(`/api/hospital-departments/${id}/`);
// Canonical URL is /api/supervision-links/ (fixed from /api/supervisor-resident-links/)
export const getSupervisorResidentLinks = () => apiClient.get('/api/supervision-links/');
export const createSupervisorResidentLink = (data: any) => apiClient.post('/api/supervision-links/', data);
export const deleteSupervisorResidentLink = (id: number) => apiClient.delete(`/api/supervision-links/${id}/`);
export const getHodAssignments = () => apiClient.get('/api/hod-assignments/');
export const createHodAssignment = (data: any) => apiClient.post('/api/hod-assignments/', data);
