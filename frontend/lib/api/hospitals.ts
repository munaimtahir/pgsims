import apiClient from './client';
import type { UserbaseHospital } from './userbase';

export const getHospitals = () => apiClient.get('/api/hospitals/');
export const createHospital = (data: Partial<UserbaseHospital>) => apiClient.post('/api/hospitals/', data);
export const updateHospital = (id: number, data: Partial<UserbaseHospital>) => apiClient.patch(`/api/hospitals/${id}/`, data);
export const deleteHospital = (id: number) => apiClient.delete(`/api/hospitals/${id}/`);
