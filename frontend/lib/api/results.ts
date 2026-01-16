/**
 * Results API client
 * Handles exams and scores
 */

import apiClient from './client';

export interface Exam {
  id: number;
  title: string;
  module_name?: string;
  exam_type: string;
  date: string;
  max_marks: number;
  passing_marks: number;
  status: string;
  rotation?: number;
  requires_eligibility: boolean;
  created_at: string;
  updated_at: string;
}

export interface Score {
  id: number;
  exam: number;
  student: number;
  marks_obtained: number;
  percentage: number;
  grade: string;
  is_passing: boolean;
  is_eligible: boolean;
  ineligibility_reason?: string;
  entered_by: number;
  created_at: string;
  updated_at: string;
}

export interface ExamStatistics {
  total_students: number;
  passed: number;
  failed: number;
  pass_percentage: number;
  average_marks: number;
  max_marks: number;
  passing_marks: number;
}

export const resultsApi = {
  /**
   * Exams
   */
  exams: {
    list: async (params?: { exam_type?: string; status?: string; rotation?: number; requires_eligibility?: boolean; search?: string; ordering?: string }) => {
      const response = await apiClient.get<{ results: Exam[]; count: number }>('/results/api/exams/', { params });
      return response.data;
    },
    get: async (id: number) => {
      const response = await apiClient.get<Exam>(`/results/api/exams/${id}/`);
      return response.data;
    },
    create: async (data: Partial<Exam>) => {
      const response = await apiClient.post<Exam>('/results/api/exams/', data);
      return response.data;
    },
    update: async (id: number, data: Partial<Exam>) => {
      const response = await apiClient.put<Exam>(`/results/api/exams/${id}/`, data);
      return response.data;
    },
    delete: async (id: number) => {
      await apiClient.delete(`/results/api/exams/${id}/`);
    },
    getScores: async (id: number) => {
      const response = await apiClient.get<Score[]>(`/results/api/exams/${id}/scores/`);
      return response.data;
    },
    getStatistics: async (id: number) => {
      const response = await apiClient.get<ExamStatistics>(`/results/api/exams/${id}/statistics/`);
      return response.data;
    },
  },

  /**
   * Scores
   */
  scores: {
    list: async (params?: { exam?: number; student?: number; is_passing?: boolean; is_eligible?: boolean; grade?: string; search?: string; ordering?: string }) => {
      const response = await apiClient.get<{ results: Score[]; count: number }>('/results/api/scores/', { params });
      return response.data;
    },
    get: async (id: number) => {
      const response = await apiClient.get<Score>(`/results/api/scores/${id}/`);
      return response.data;
    },
    create: async (data: Partial<Score>) => {
      const response = await apiClient.post<Score>('/results/api/scores/', data);
      return response.data;
    },
    update: async (id: number, data: Partial<Score>) => {
      const response = await apiClient.put<Score>(`/results/api/scores/${id}/`, data);
      return response.data;
    },
    delete: async (id: number) => {
      await apiClient.delete(`/results/api/scores/${id}/`);
    },
    getMyScores: async () => {
      const response = await apiClient.get<Score[]>('/results/api/scores/my_scores/');
      return response.data;
    },
  },
};

export default resultsApi;
