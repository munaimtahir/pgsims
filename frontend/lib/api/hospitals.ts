import apiClient from './client';
export const getHospitals = () => apiClient.get('/api/hospitals/');
export const createHospital = (data: any) => apiClient.post('/api/hospitals/', data);
export const updateHospital = (id: number, data: any) => apiClient.patch(`/api/hospitals/${id}/`, data);
export const deleteHospital = (id: number) => apiClient.delete(`/api/hospitals/${id}/`);
