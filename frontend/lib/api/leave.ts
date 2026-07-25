import apiClient from './client';

type ListResponse<T> = { count?: number; results?: T[]; next?: string | null } | T[];

function unwrapList<T>(data: ListResponse<T>): T[] {
  return Array.isArray(data) ? data : data.results || [];
}

export interface LeaveRequest {
  id: number;
  resident_training: number;
  resident_name: string;
  leave_type: 'annual' | 'sick' | 'casual' | 'study' | 'maternity' | 'other';
  start_date: string;
  end_date: string;
  reason: string;
  status: 'DRAFT' | 'SUBMITTED' | 'APPROVED' | 'REJECTED';
  approved_by: number | null;
  approved_at: string | null;
  reject_reason: string;
  created_at: string;
  updated_at: string;
}

export const LEAVE_TYPE_OPTIONS: Array<{ value: LeaveRequest['leave_type']; label: string }> = [
  { value: 'annual', label: 'Annual Leave' },
  { value: 'sick', label: 'Sick Leave' },
  { value: 'casual', label: 'Casual Leave' },
  { value: 'study', label: 'Study Leave' },
  { value: 'maternity', label: 'Maternity Leave' },
  { value: 'other', label: 'Other' },
];

export const leaveApi = {
  list: async (params?: { status?: string }) =>
    unwrapList(
      (await apiClient.get<ListResponse<LeaveRequest>>('/api/leaves/', { params })).data
    ),
  get: async (id: number) => (await apiClient.get<LeaveRequest>(`/api/leaves/${id}/`)).data,
  create: async (payload: Record<string, unknown>) =>
    (await apiClient.post<LeaveRequest>('/api/leaves/', payload)).data,
  submit: async (id: number) =>
    (await apiClient.post<LeaveRequest>(`/api/leaves/${id}/submit/`)).data,
  approve: async (id: number) =>
    (await apiClient.post<LeaveRequest>(`/api/leaves/${id}/approve/`)).data,
  reject: async (id: number, reason: string) =>
    (await apiClient.post<LeaveRequest>(`/api/leaves/${id}/reject/`, { reason })).data,
  myLeaves: async () =>
    unwrapList((await apiClient.get<ListResponse<LeaveRequest>>('/api/my/leaves/')).data),
  approvalInbox: async () =>
    unwrapList(
      (await apiClient.get<ListResponse<LeaveRequest>>('/api/utrmc/approvals/leaves/')).data
    ),
};

export default leaveApi;
