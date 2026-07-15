import apiClient from './client';

export interface UserbaseHospital {
  id: number;
  name: string;
  code?: string | null;
  active: boolean;
  created_at: string;
}

export interface UserbaseDepartment {
  id: number;
  name: string;
  code: string;
  description?: string;
  active: boolean;
  created_at: string;
}

export interface UserbaseHospitalDepartment {
  id: number;
  hospital: UserbaseHospital;
  department: UserbaseDepartment;
  hospital_id?: number;
  department_id?: number;
  active: boolean;
  created_at: string;
}

export interface UserbaseUser {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name?: string;
  role: string;
  is_active: boolean;
  specialty?: string;
  year?: string;
  phone_number?: string;
  departments?: Array<{
    id: number;
    name: string;
    code: string;
    member_type: string;
    is_primary: boolean;
  }>;
}

export interface DataQualitySummary {
  total_users: number;
  users_with_placeholder_email: number;
  users_with_missing_dates: number;
  complete_profiles: number;
  incomplete_profiles: number;
}

export interface DataQualityUserRow {
  id: number;
  name: string;
  email: string;
  year?: string | null;
  supervisor?: string;
  issues: string[];
  is_complete_profile: boolean;
  has_placeholder_email: boolean;
  has_missing_dates: boolean;
}

export interface DataCorrectionAuditRow {
  id: number;
  actor: string;
  entity_type: string;
  entity_id: string;
  field_name: string;
  old_value: string;
  new_value: string;
  metadata: Record<string, unknown>;
  timestamp: string;
}

export type UserbaseUserUpsert = Partial<
  Pick<UserbaseUser, 'username' | 'email' | 'first_name' | 'last_name' | 'role' | 'is_active' | 'specialty'>
> & {
  password?: string;
  full_name?: string;
  phone?: string;
  phone_number?: string;
  profile?: {
    hospital?: number;
    department_ref?: number;
    program_ref?: number;
    academic_session_ref?: string;
    designation_ref?: string;
  };
};

export interface DepartmentRosterResponse {
  department: { id: number; name: string; code: string; active: boolean };
  hod: { id: number; username: string; full_name?: string } | null;
  faculty: Array<{ id: number; username: string; full_name?: string; role: string }>;
  supervisors: Array<{ id: number; username: string; full_name?: string; role: string }>;
  residents: Array<{ id: number; username: string; full_name?: string; role: string }>;
}

export interface UserbaseStaffProfile {
  id: number;
  user: UserbaseUser;
  user_id?: number;
  designation: string;
  phone: string;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export const userbaseApi = {
  hospitals: {
    list: async () => {
      const response = await apiClient.get<{ count?: number; results?: UserbaseHospital[] } | UserbaseHospital[]>(
        '/api/hospitals/'
      );
      return Array.isArray(response.data) ? response.data : response.data.results || [];
    },
    create: async (payload: Partial<UserbaseHospital>) => {
      const response = await apiClient.post<UserbaseHospital>('/api/hospitals/', payload);
      return response.data;
    },
    update: async (id: number, payload: Partial<UserbaseHospital>) => {
      const response = await apiClient.patch<UserbaseHospital>(`/api/hospitals/${id}/`, payload);
      return response.data;
    },
    listDepartments: async (id: number) => {
      const response = await apiClient.get(`/api/hospitals/${id}/departments/`);
      return response.data;
    },
    delete: async (id: number) => {
      await apiClient.delete(`/api/hospitals/${id}/`);
    },
  },
  departments: {
    list: async () => {
      const response = await apiClient.get<{ count?: number; results?: UserbaseDepartment[] } | UserbaseDepartment[]>(
        '/api/departments/'
      );
      return Array.isArray(response.data) ? response.data : response.data.results || [];
    },
    create: async (payload: Partial<UserbaseDepartment>) => {
      const response = await apiClient.post<UserbaseDepartment>('/api/departments/', payload);
      return response.data;
    },
    update: async (id: number, payload: Partial<UserbaseDepartment>) => {
      const response = await apiClient.patch<UserbaseDepartment>(`/api/departments/${id}/`, payload);
      return response.data;
    },
    delete: async (id: number) => {
      await apiClient.delete(`/api/departments/${id}/`);
    },
    roster: async (id: number) => {
      const response = await apiClient.get<DepartmentRosterResponse>(`/api/departments/${id}/roster/`);
      return response.data;
    },
  },
  matrix: {
    list: async () => {
      const response = await apiClient.get<
        { count?: number; results?: UserbaseHospitalDepartment[] } | UserbaseHospitalDepartment[]
      >('/api/hospital-departments/');
      return Array.isArray(response.data) ? response.data : response.data.results || [];
    },
    create: async (payload: { hospital_id: number; department_id: number; active?: boolean }) => {
      const response = await apiClient.post<UserbaseHospitalDepartment>('/api/hospital-departments/', payload);
      return response.data;
    },
    update: async (id: number, payload: Partial<{ active: boolean }>) => {
      const response = await apiClient.patch<UserbaseHospitalDepartment>(`/api/hospital-departments/${id}/`, payload);
      return response.data;
    },
  },
  users: {
    list: async (params?: { role?: string; department?: number; active?: boolean; search?: string }) => {
      const response = await apiClient.get<{ count?: number; results?: UserbaseUser[] } | UserbaseUser[]>(
        '/api/users/',
        { params }
      );
      return Array.isArray(response.data) ? response.data : response.data.results || [];
    },
    create: async (payload: UserbaseUserUpsert) => {
      const response = await apiClient.post<UserbaseUser>('/api/users/', payload);
      return response.data;
    },
    get: async (id: number) => {
      const response = await apiClient.get<UserbaseUser>(`/api/users/${id}/`);
      return response.data;
    },
    update: async (id: number, payload: UserbaseUserUpsert) => {
      const response = await apiClient.patch<UserbaseUser>(`/api/users/${id}/`, payload);
      return response.data;
    },
  },
  residents: {
    get: async (userId: number) => {
      const response = await apiClient.get(`/api/residents/${userId}/`);
      return response.data;
    },
    update: async (
      userId: number,
      payload: Partial<{ training_start: string; training_end: string; training_level: string }>
    ) => {
      const response = await apiClient.patch(`/api/residents/${userId}/`, payload);
      return response.data;
    },
  },
  staff: {
    list: async () => {
      const response = await apiClient.get<{ count?: number; results?: UserbaseStaffProfile[] } | UserbaseStaffProfile[]>(
        '/api/staff/'
      );
      return Array.isArray(response.data) ? response.data : response.data.results || [];
    },
    update: async (
      userId: number,
      payload: Partial<{ designation: string; phone: string; active?: boolean }>
    ) => {
      const response = await apiClient.patch(`/api/staff/${userId}/`, payload);
      return response.data;
    },
  },
  supervisors: {
    get: async (userId: number) => {
      const response = await apiClient.get(`/api/supervisors/${userId}/`);
      return response.data;
    },
  },
  dataQuality: {
    summary: async () => {
      const response = await apiClient.get<DataQualitySummary>('/api/admin/data-quality/summary');
      return response.data;
    },
    users: async (filter?: string) => {
      const response = await apiClient.get<DataQualityUserRow[]>('/api/admin/data-quality/users', {
        params: filter ? { filter } : undefined,
      });
      return response.data;
    },
    recompute: async () => {
      const response = await apiClient.post<DataQualitySummary>('/api/admin/data-quality/recompute');
      return response.data;
    },
    audit: async () => {
      const response = await apiClient.get<DataCorrectionAuditRow[]>('/api/admin/data-quality/audit');
      return response.data;
    },
  },
  memberships: {
    create: async (payload: Record<string, unknown>) => {
      const response = await apiClient.post('/api/department-memberships/', payload);
      return response.data;
    },
    update: async (id: number, payload: Record<string, unknown>) => {
      const response = await apiClient.patch(`/api/department-memberships/${id}/`, payload);
      return response.data;
    },
    remove: async (id: number) => {
      await apiClient.delete(`/api/department-memberships/${id}/`);
    },
  },
  hospitalAssignments: {
    create: async (payload: Record<string, unknown>) => {
      const response = await apiClient.post('/api/hospital-assignments/', payload);
      return response.data;
    },
    update: async (id: number, payload: Record<string, unknown>) => {
      const response = await apiClient.patch(`/api/hospital-assignments/${id}/`, payload);
      return response.data;
    },
    remove: async (id: number) => {
      await apiClient.delete(`/api/hospital-assignments/${id}/`);
    },
  },
};

export default userbaseApi;
