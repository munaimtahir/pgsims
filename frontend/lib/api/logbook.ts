/**
 * Logbook API client
 * Handles logbook entries and verification
 */

import apiClient from './client';

export interface LogbookEntry {
  id: number;
  case_title: string;
  date: string;
  location_of_activity?: string;
  patient_history_summary?: string;
  management_action?: string;
  topic_subtopic?: string;
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
  status: 'draft' | 'pending' | 'approved' | 'rejected' | 'returned' | 'archived';
  verified_by?: number;
  verified_at?: string;
  supervisor_comments?: string;
  updated_at?: string;
  created_at?: string;
  submitted_to_supervisor_at?: string;
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

export interface PGLogbookEntryPayload {
  case_title: string;
  date: string;
  location_of_activity: string;
  patient_history_summary: string;
  management_action: string;
  topic_subtopic: string;
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

  /**
   * Get PG logbook entries (for PGs)
   */
  getMyEntries: async () => {
    const response = await apiClient.get<{ count?: number; results?: LogbookEntry[] } | LogbookEntry[]>(
      '/api/logbook/my/'
    );
    return response.data;
  },

  /**
   * Create PG logbook entry (draft)
   */
  createMyEntry: async (payload: PGLogbookEntryPayload) => {
    const response = await apiClient.post<LogbookEntry>('/api/logbook/my/', payload);
    return response.data;
  },

  /**
   * Update PG logbook entry (draft-only)
   */
  updateMyEntry: async (id: number, payload: Partial<PGLogbookEntryPayload>) => {
    const response = await apiClient.patch<LogbookEntry>(`/api/logbook/my/${id}/`, payload);
    return response.data;
  },

  /**
   * Submit PG logbook entry (draft -> pending)
   */
  submitMyEntry: async (id: number) => {
    const response = await apiClient.post<LogbookEntry>(`/api/logbook/my/${id}/submit/`);
    return response.data;
  },
};

export default logbookApi;
