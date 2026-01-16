/**
 * Academics API client
 * Handles departments, batches, and student profiles
 */

import apiClient from './client';

export interface Department {
  id: number;
  name: string;
  code: string;
  description?: string;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Batch {
  id: number;
  name: string;
  program: string;
  department: number;
  start_date: string;
  end_date?: string;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export interface StudentProfile {
  id: number;
  user: number;
  roll_number: string;
  batch: number;
  admission_date: string;
  cgpa?: number;
  status: string;
  created_at: string;
  updated_at: string;
}

export const academicsApi = {
  /**
   * Departments
   */
  departments: {
    list: async (params?: { active?: boolean; code?: string; search?: string; ordering?: string }) => {
      const response = await apiClient.get<{ results: Department[]; count: number }>('/academics/api/departments/', { params });
      return response.data;
    },
    get: async (id: number) => {
      const response = await apiClient.get<Department>(`/academics/api/departments/${id}/`);
      return response.data;
    },
    create: async (data: Partial<Department>) => {
      const response = await apiClient.post<Department>('/academics/api/departments/', data);
      return response.data;
    },
    update: async (id: number, data: Partial<Department>) => {
      const response = await apiClient.put<Department>(`/academics/api/departments/${id}/`, data);
      return response.data;
    },
    delete: async (id: number) => {
      await apiClient.delete(`/academics/api/departments/${id}/`);
    },
  },

  /**
   * Batches
   */
  batches: {
    list: async (params?: { program?: string; department?: number; active?: boolean; search?: string; ordering?: string }) => {
      const response = await apiClient.get<{ results: Batch[]; count: number }>('/academics/api/batches/', { params });
      return response.data;
    },
    get: async (id: number) => {
      const response = await apiClient.get<Batch>(`/academics/api/batches/${id}/`);
      return response.data;
    },
    create: async (data: Partial<Batch>) => {
      const response = await apiClient.post<Batch>('/academics/api/batches/', data);
      return response.data;
    },
    update: async (id: number, data: Partial<Batch>) => {
      const response = await apiClient.put<Batch>(`/academics/api/batches/${id}/`, data);
      return response.data;
    },
    delete: async (id: number) => {
      await apiClient.delete(`/academics/api/batches/${id}/`);
    },
    getStudents: async (id: number) => {
      const response = await apiClient.get<StudentProfile[]>(`/academics/api/batches/${id}/students/`);
      return response.data;
    },
  },

  /**
   * Student Profiles
   */
  students: {
    list: async (params?: { status?: string; batch?: number; search?: string; ordering?: string }) => {
      const response = await apiClient.get<{ results: StudentProfile[]; count: number }>('/academics/api/students/', { params });
      return response.data;
    },
    get: async (id: number) => {
      const response = await apiClient.get<StudentProfile>(`/academics/api/students/${id}/`);
      return response.data;
    },
    create: async (data: Partial<StudentProfile>) => {
      const response = await apiClient.post<StudentProfile>('/academics/api/students/', data);
      return response.data;
    },
    update: async (id: number, data: Partial<StudentProfile>) => {
      const response = await apiClient.put<StudentProfile>(`/academics/api/students/${id}/`, data);
      return response.data;
    },
    delete: async (id: number) => {
      await apiClient.delete(`/academics/api/students/${id}/`);
    },
    updateStatus: async (id: number, status: string) => {
      const response = await apiClient.post<StudentProfile>(`/academics/api/students/${id}/update_status/`, { status });
      return response.data;
    },
  },
};

export default academicsApi;
