import apiClient from './client';

type ListResponse<T> = { count?: number; results?: T[] } | T[];

function unwrapList<T>(data: ListResponse<T>): T[] {
  return Array.isArray(data) ? data : data.results || [];
}

export interface RotationAssignment {
  id: number;
  resident_training: number;
  resident_name: string;
  program_name: string;
  hospital_department: number;
  hospital_name: string;
  department_name: string;
  template: number | null;
  template_name: string | null;
  start_date: string;
  end_date: string;
  status:
    | 'DRAFT'
    | 'SUBMITTED'
    | 'APPROVED'
    | 'ACTIVE'
    | 'COMPLETED'
    | 'RETURNED'
    | 'REJECTED'
    | 'CANCELLED';
  notes: string;
  return_reason: string;
  reject_reason: string;
  requested_by: number | null;
  approved_by_hod: number | null;
  approved_by_utrmc: number | null;
  submitted_at: string | null;
  approved_at: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface TrainingResidentTrainingRecord {
  id: number;
  resident_user: number;
  resident_name: string;
  program: number;
  program_name: string;
  program_code: string;
  start_date: string;
  expected_end_date: string | null;
  current_level: string;
  active: boolean;
}

export interface HospitalDepartmentOption {
  id: number;
  hospital: { id: number; name: string; code?: string };
  department: { id: number; name: string; code?: string };
  active: boolean;
}

export interface TrainingProgramOption {
  id: number;
  name: string;
  code?: string;
}

export interface RotationListParams {
  status?: string;
  resident?: number;
  department?: number;
  hospital?: number;
}

export const rotationsApi = {
  list: async (params?: RotationListParams) =>
    unwrapList(
      (await apiClient.get<ListResponse<RotationAssignment>>('/api/rotations/', { params })).data
    ),
  get: async (id: number) =>
    (await apiClient.get<RotationAssignment>(`/api/rotations/${id}/`)).data,
  create: async (payload: Record<string, unknown>) =>
    (await apiClient.post<RotationAssignment>('/api/rotations/', payload)).data,
  update: async (id: number, payload: Record<string, unknown>) =>
    (await apiClient.patch<RotationAssignment>(`/api/rotations/${id}/`, payload)).data,
  submit: async (id: number) =>
    (await apiClient.post<RotationAssignment>(`/api/rotations/${id}/submit/`)).data,
  hodApprove: async (id: number) =>
    (await apiClient.post<RotationAssignment>(`/api/rotations/${id}/hod-approve/`)).data,
  utrmcApprove: async (id: number) =>
    (await apiClient.post<RotationAssignment>(`/api/rotations/${id}/utrmc-approve/`)).data,
  activate: async (id: number) =>
    (await apiClient.post<RotationAssignment>(`/api/rotations/${id}/activate/`)).data,
  complete: async (id: number) =>
    (await apiClient.post<RotationAssignment>(`/api/rotations/${id}/complete/`)).data,
  reviewApplication: async (
    id: number,
    payload: { action: 'approve' | 'redirect' | 'defer' | 'reject'; reason?: string; hospital_department?: number }
  ) =>
    (await apiClient.post<RotationAssignment>(`/api/rotations/${id}/review-application/`, payload))
      .data,
  myRotations: async () =>
    unwrapList(
      (await apiClient.get<ListResponse<RotationAssignment>>('/api/my/rotations/')).data
    ),
  pendingForSupervisor: async () =>
    unwrapList(
      (
        await apiClient.get<ListResponse<RotationAssignment>>(
          '/api/supervisor/rotations/pending/'
        )
      ).data
    ),
  approvalInbox: async () =>
    unwrapList(
      (
        await apiClient.get<ListResponse<RotationAssignment>>(
          '/api/utrmc/approvals/rotations/'
        )
      ).data
    ),
  listResidentTrainingRecords: async () =>
    unwrapList(
      (
        await apiClient.get<ListResponse<TrainingResidentTrainingRecord>>(
          '/api/resident-training/'
        )
      ).data
    ),
  createResidentTrainingRecord: async (payload: Record<string, unknown>) =>
    (await apiClient.post<TrainingResidentTrainingRecord>('/api/resident-training/', payload))
      .data,
  listHospitalDepartments: async () =>
    unwrapList(
      (
        await apiClient.get<ListResponse<HospitalDepartmentOption>>('/api/hospital-departments/')
      ).data
    ),
  listTrainingPrograms: async () =>
    unwrapList(
      (await apiClient.get<ListResponse<TrainingProgramOption>>('/api/programs/')).data
    ),
};

export default rotationsApi;
