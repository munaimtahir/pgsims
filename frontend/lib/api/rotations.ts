/**
 * Rotations API client
 */

import apiClient from './client';

export interface RotationSummary {
  id: number;
  name: string;
  department: { id: number; name: string; code?: string | null } | null;
  hospital: { id: number; name: string; code?: string | null } | null;
  start_date: string;
  end_date: string;
  status: string;
  supervisor_name?: string | null;
  requires_utrmc_approval?: boolean;
  override_reason?: string | null;
}

export const rotationsApi = {
  /**
   * Get rotations for the authenticated PG
   */
  getMyRotations: async () => {
    const response = await apiClient.get<{ count: number; results: RotationSummary[] }>('/api/rotations/my/');
    return response.data;
  },

  /**
   * Get a rotation detail for the authenticated PG
   */
  getMyRotation: async (id: number) => {
    const response = await apiClient.get<RotationSummary>(`/api/rotations/my/${id}/`);
    return response.data;
  },
};

export default rotationsApi;
