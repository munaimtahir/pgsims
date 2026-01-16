/**
 * Logbook API client
 * Handles logbook entries and verification
 */

import apiClient from './client';

export interface LogbookEntry {
  id: number;
  case_title: string;
  date: string;
  user?: {
    id: number;
    username: string;
    full_name: string;
  };
  rotation?: {
    id: number;
    department: string;
  };
  submitted_at?: string;
  status: 'pending' | 'approved' | 'rejected';
  verified_by?: number;
  verified_at?: string;
  supervisor_comments?: string;
}

export interface PendingLogbookEntry {
  id: number;
  case_title: string;
  date: string;
  user: {
    id: number;
    username: string;
    full_name: string;
  };
  rotation: {
    id: number;
    department: string;
  };
  submitted_at: string;
  status: string;
}

export const logbookApi = {
  /**
   * Get pending logbook entries (for supervisors/admins)
   */
  getPending: async () => {
    const response = await apiClient.get<{ count: number; results: PendingLogbookEntry[] }>('/api/logbook/pending/');
    return response.data;
  },

  /**
   * Verify a logbook entry (for supervisors/admins)
   */
  verify: async (id: number, feedback?: string) => {
    const response = await apiClient.patch<LogbookEntry>(`/api/logbook/${id}/verify/`, { feedback });
    return response.data;
  },
};

export default logbookApi;
