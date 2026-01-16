/**
 * Attendance API client
 * Handles attendance records and summaries
 */

import apiClient from './client';

export interface AttendanceSummary {
  total_sessions: number;
  attended: number;
  absent: number;
  late: number;
  excused: number;
  attendance_percentage: number;
  eligibility_status: 'eligible' | 'ineligible';
  period: string;
  start_date: string;
  end_date: string;
}

export interface BulkUploadResult {
  message: string;
  success_count: number;
  error_count?: number;
  errors?: string[];
}

export const attendanceApi = {
  /**
   * Get attendance summary for a user
   */
  getSummary: async (params: {
    user?: number;
    period: 'monthly' | 'quarterly' | 'semester' | 'yearly' | 'custom';
    start_date: string;
    end_date: string;
  }) => {
    const response = await apiClient.get<AttendanceSummary>('/api/attendance/summary/', { params });
    return response.data;
  },

  /**
   * Bulk upload attendance records (CSV)
   */
  bulkUpload: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await apiClient.post<BulkUploadResult>('/api/attendance/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export default attendanceApi;
