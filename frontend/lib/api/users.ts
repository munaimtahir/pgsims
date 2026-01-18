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

export const usersApi = {
  async getAssignedPGs(): Promise<AssignedPG[]> {
    const response = await apiClient.get<AssignedPG[]>('/api/users/assigned-pgs/');
    return response.data;
  },
};
