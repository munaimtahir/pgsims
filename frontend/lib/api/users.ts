import apiClient from './client';

export interface AssignedPG {
  id: number;
  username?: string;
  full_name?: string;
  email?: string;
  specialty?: string;
  year?: string;
  is_active?: boolean;
}

export interface SupervisorUser {
  id: number;
  username: string;
  full_name?: string;
  email?: string;
}

export const usersApi = {
  async getAssignedPGs(): Promise<AssignedPG[]> {
    const response = await apiClient.get<AssignedPG[]>('/api/users/assigned-pgs/');
    return response.data;
  },

  async getSupervisors(): Promise<SupervisorUser[]> {
    const response = await apiClient.get<SupervisorUser[] | { results: SupervisorUser[] }>('/api/users/?role=supervisor');
    const data = response.data;
    return Array.isArray(data) ? data : (data.results ?? []);
  },
};
