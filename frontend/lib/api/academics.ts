import apiClient from './client';

type ListResponse<T> = { count?: number; results?: T[] } | T[];

function unwrapList<T>(data: ListResponse<T>): T[] {
  return Array.isArray(data) ? data : data.results || [];
}

export interface AcademicOptionRow {
  id: number;
  name: string;
  code?: string | null;
  username?: string;
}

export interface AcademicTrainingRecord {
  id: number;
  resident: number;
  resident_name: string;
  resident_username: string;
  program: number | null;
  program_name: string | null;
  academic_session: number | null;
  academic_session_name: string | null;
  training_site: number | null;
  training_site_name: string | null;
  department: number | null;
  department_name: string | null;
  start_date: string | null;
  expected_end_date: string | null;
  actual_end_date: string | null;
  training_year: number | null;
  status: string;
  is_active: boolean;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface AcademicPeriod {
  id: number;
  name: string;
  code: string;
  academic_session: number | null;
  academic_session_name: string | null;
  start_date: string;
  end_date: string;
  period_type: string;
  is_active: boolean;
  sort_order: number;
  description: string;
}

export interface RotationTemplate {
  id: number;
  name: string;
  code: string;
  program: number | null;
  program_name: string | null;
  department: number | null;
  department_name: string | null;
  training_year: number | null;
  duration_weeks: number | null;
  is_required: boolean;
  is_active: boolean;
  description: string;
}

export interface EvaluationFormTemplate {
  id: number;
  name: string;
  code: string;
  program: number | null;
  program_name: string | null;
  department: number | null;
  department_name: string | null;
  form_type: string;
  schema: Record<string, unknown>;
  is_active: boolean;
  description: string;
}

export interface LogbookCategory {
  id: number;
  name: string;
  code: string;
  program: number | null;
  program_name: string | null;
  department: number | null;
  department_name: string | null;
  category_type: string;
  minimum_required: number | null;
  is_active: boolean;
  description: string;
}

export interface ReviewQueueItem {
  id: number;
  resident: number;
  resident_name: string;
  supervisor: number;
  supervisor_name: string;
  training_record: number | null;
  queue_type: string;
  status: string;
  due_date: string | null;
  notes: string;
}

export interface AcademicOverview {
  cards: Record<string, number>;
}

export interface AcademicSummary {
  resident?: {
    id: number;
    name: string;
    username: string;
    department: string | null;
    program: string | null;
    academic_session: string | null;
  };
  training_record?: {
    id: number;
    status: string;
    is_active: boolean;
    training_year: number | null;
    start_date: string | null;
    expected_end_date: string | null;
    actual_end_date: string | null;
    program: { id: number | null; name: string | null; code: string | null };
    academic_session: { id: number | null; name: string | null; code: string | null };
    training_site: { id: number | null; name: string | null };
    department: { id: number | null; name: string | null; code: string | null };
    notes: string;
  } | null;
  supervision?: {
    primary_supervisor: {
      id: number;
      assignment_type: string;
      status: string;
      start_date: string | null;
      end_date: string | null;
      supervisor: {
        id: number;
        name: string;
        username: string;
        department: string | null;
        designation: string | null;
        email: string | null;
        phone: string | null;
      };
    } | null;
    co_supervisors: Array<{
      id: number;
      assignment_type: string;
      status: string;
      start_date: string | null;
      end_date: string | null;
      supervisor: {
        id: number;
        name: string;
        username: string;
        department: string | null;
        designation: string | null;
        email: string | null;
        phone: string | null;
      };
    }>;
  };
  review_queue?: {
    pending_count: number;
    items: ReviewQueueItem[];
  };
  readiness?: {
    has_active_training_record: boolean;
    has_primary_supervisor: boolean;
    missing_items: string[];
  };
  supervisor?: {
    id: number;
    name: string;
    username: string;
  };
  assigned_residents?: Array<{
    resident_id: number;
    name: string;
    username: string;
    program: string | null;
    training_record_id: number | null;
    training_year: number | null;
    status: string;
  }>;
  summary?: {
    assigned_residents: number;
    active_training_records: number;
    residents_missing_training_records: number;
    pending_review_queue_items: number;
  };
  residents_missing_training_records?: Array<{
    resident_id: number;
    name: string;
    username: string;
    program: string | null;
    training_record_id: number | null;
    training_year: number | null;
    status: string;
  }>;
}

export interface AcademicDataQualitySection {
  key: string;
  label: string;
  count: number;
  items: Array<Record<string, unknown>>;
}

export interface AcademicDataQuality {
  summary: Record<string, number>;
  sections: AcademicDataQualitySection[];
}

export interface AcademicOptions {
  residents: AcademicOptionRow[];
  supervisors: AcademicOptionRow[];
  programs: AcademicOptionRow[];
  academic_sessions: AcademicOptionRow[];
  training_sites: AcademicOptionRow[];
  departments: AcademicOptionRow[];
  periods: AcademicOptionRow[];
}

export interface EvaluationResponse {
  id: number;
  field_key: string;
  field_label: string;
  field_type: string;
  value_text: string;
  value_number: number | null;
  value_json: Record<string, unknown>;
  sort_order: number;
}

export interface EvaluationSubmission {
  id: number;
  resident: number;
  resident_name: string;
  resident_username: string;
  training_record: number | null;
  template: number;
  template_name: string;
  supervisor: number | null;
  supervisor_name: string | null;
  academic_period: number | null;
  status: string;
  submitted_at: string | null;
  reviewed_at: string | null;
  approved_at: string | null;
  score: number | null;
  max_score: number | null;
  resident_comments: string;
  supervisor_comments: string;
  extra_data: Record<string, unknown>;
  responses: EvaluationResponse[];
}

export interface ProcedureRecord {
  id?: number;
  procedure_name: string;
  procedure_code: string;
  role_performed: string;
  complexity: string;
  outcome: string;
  complications: string;
}

export interface LogbookEntry {
  id: number;
  resident: number;
  resident_name: string;
  resident_username: string;
  training_record: number | null;
  category: number;
  category_name: string;
  supervisor: number | null;
  supervisor_name: string | null;
  academic_period: number | null;
  entry_date: string;
  title: string;
  description: string;
  case_identifier: string;
  patient_age: string;
  patient_gender: string;
  status: string;
  submitted_at: string | null;
  verified_at: string | null;
  resident_reflection: string;
  supervisor_comments: string;
  extra_data: Record<string, unknown>;
  procedure_record?: ProcedureRecord | null;
}

export const academicsApi = {
  listTrainingRecords: async (params?: Record<string, string | number | boolean>) => {
    const response = await apiClient.get<ListResponse<AcademicTrainingRecord>>('/api/academics/training-records/', { params });
    return unwrapList(response.data);
  },
  getTrainingRecord: async (id: number) => (await apiClient.get<AcademicTrainingRecord>(`/api/academics/training-records/${id}/`)).data,
  createTrainingRecord: async (payload: Record<string, unknown>) => (await apiClient.post<AcademicTrainingRecord>('/api/academics/training-records/', payload)).data,
  updateTrainingRecord: async (id: number, payload: Record<string, unknown>) => (await apiClient.patch<AcademicTrainingRecord>(`/api/academics/training-records/${id}/`, payload)).data,
  closeTrainingRecord: async (id: number, payload: Record<string, unknown>) => (await apiClient.post<AcademicTrainingRecord>(`/api/academics/training-records/${id}/close/`, payload)).data,
  listPeriods: async () => unwrapList((await apiClient.get<ListResponse<AcademicPeriod>>('/api/academics/periods/')).data),
  createPeriod: async (payload: Record<string, unknown>) => (await apiClient.post<AcademicPeriod>('/api/academics/periods/', payload)).data,
  updatePeriod: async (id: number, payload: Record<string, unknown>) => (await apiClient.patch<AcademicPeriod>(`/api/academics/periods/${id}/`, payload)).data,
  listRotationTemplates: async () => unwrapList((await apiClient.get<ListResponse<RotationTemplate>>('/api/academics/rotation-templates/')).data),
  createRotationTemplate: async (payload: Record<string, unknown>) => (await apiClient.post<RotationTemplate>('/api/academics/rotation-templates/', payload)).data,
  updateRotationTemplate: async (id: number, payload: Record<string, unknown>) => (await apiClient.patch<RotationTemplate>(`/api/academics/rotation-templates/${id}/`, payload)).data,
  listEvaluationTemplates: async () => unwrapList((await apiClient.get<ListResponse<EvaluationFormTemplate>>('/api/academics/evaluation-templates/')).data),
  createEvaluationTemplate: async (payload: Record<string, unknown>) => (await apiClient.post<EvaluationFormTemplate>('/api/academics/evaluation-templates/', payload)).data,
  updateEvaluationTemplate: async (id: number, payload: Record<string, unknown>) => (await apiClient.patch<EvaluationFormTemplate>(`/api/academics/evaluation-templates/${id}/`, payload)).data,
  listLogbookCategories: async () => unwrapList((await apiClient.get<ListResponse<LogbookCategory>>('/api/academics/logbook-categories/')).data),
  createLogbookCategory: async (payload: Record<string, unknown>) => (await apiClient.post<LogbookCategory>('/api/academics/logbook-categories/', payload)).data,
  updateLogbookCategory: async (id: number, payload: Record<string, unknown>) => (await apiClient.patch<LogbookCategory>(`/api/academics/logbook-categories/${id}/`, payload)).data,
  listReviewQueue: async () => unwrapList((await apiClient.get<ListResponse<ReviewQueueItem>>('/api/academics/review-queue/')).data),
  createReviewQueueItem: async (payload: Record<string, unknown>) => (await apiClient.post<ReviewQueueItem>('/api/academics/review-queue/', payload)).data,
  updateReviewQueueItem: async (id: number, payload: Record<string, unknown>) => (await apiClient.patch<ReviewQueueItem>(`/api/academics/review-queue/${id}/`, payload)).data,
  getOverview: async () => (await apiClient.get<AcademicOverview>('/api/academics/overview/')).data,
  getDataQuality: async () => (await apiClient.get<AcademicDataQuality>('/api/academics/data-quality/')).data,
  getOptions: async () => (await apiClient.get<AcademicOptions>('/api/academics/options/')).data,
  getResidentSummary: async (residentId: number) => (await apiClient.get<AcademicSummary>(`/api/academics/residents/${residentId}/summary/`)).data,
  getMyResidentSummary: async () => (await apiClient.get<AcademicSummary>('/api/academics/residents/me/summary/')).data,
  getSupervisorSummary: async (supervisorId: number) => (await apiClient.get<AcademicSummary>(`/api/academics/supervisors/${supervisorId}/summary/`)).data,
  getMySupervisorSummary: async () => (await apiClient.get<AcademicSummary>('/api/academics/supervisors/me/summary/')).data,
  seedPilotAcademics: async () => (await apiClient.post<Record<string, number>>('/api/academics/seed/')).data,

  listEvaluationSubmissions: async (params?: Record<string, string | number | boolean>) => unwrapList((await apiClient.get<ListResponse<EvaluationSubmission>>('/api/academics/evaluation-submissions/', { params })).data),
  getEvaluationSubmission: async (id: number) => (await apiClient.get<EvaluationSubmission>(`/api/academics/evaluation-submissions/${id}/`)).data,
  createEvaluationSubmission: async (payload: Record<string, unknown>) => (await apiClient.post<EvaluationSubmission>('/api/academics/evaluation-submissions/', payload)).data,
  updateEvaluationSubmission: async (id: number, payload: Record<string, unknown>) => (await apiClient.patch<EvaluationSubmission>(`/api/academics/evaluation-submissions/${id}/`, payload)).data,
  submitEvaluation: async (id: number) => (await apiClient.post<EvaluationSubmission>(`/api/academics/evaluation-submissions/${id}/submit/`)).data,
  startEvaluationReview: async (id: number) => (await apiClient.post<EvaluationSubmission>(`/api/academics/evaluation-submissions/${id}/start_review/`)).data,
  approveEvaluation: async (id: number, payload: Record<string, unknown>) => (await apiClient.post<EvaluationSubmission>(`/api/academics/evaluation-submissions/${id}/approve/`, payload)).data,
  returnEvaluation: async (id: number, payload: Record<string, unknown>) => (await apiClient.post<EvaluationSubmission>(`/api/academics/evaluation-submissions/${id}/return_revision/`, payload)).data,
  rejectEvaluation: async (id: number, payload: Record<string, unknown>) => (await apiClient.post<EvaluationSubmission>(`/api/academics/evaluation-submissions/${id}/reject/`, payload)).data,
  cancelEvaluation: async (id: number) => (await apiClient.post<EvaluationSubmission>(`/api/academics/evaluation-submissions/${id}/cancel/`)).data,

  listLogbookEntries: async (params?: Record<string, string | number | boolean>) => unwrapList((await apiClient.get<ListResponse<LogbookEntry>>('/api/academics/logbook-entries/', { params })).data),
  getLogbookEntry: async (id: number) => (await apiClient.get<LogbookEntry>(`/api/academics/logbook-entries/${id}/`)).data,
  createLogbookEntry: async (payload: Record<string, unknown>) => (await apiClient.post<LogbookEntry>('/api/academics/logbook-entries/', payload)).data,
  updateLogbookEntry: async (id: number, payload: Record<string, unknown>) => (await apiClient.patch<LogbookEntry>(`/api/academics/logbook-entries/${id}/`, payload)).data,
  submitLogbookEntry: async (id: number) => (await apiClient.post<LogbookEntry>(`/api/academics/logbook-entries/${id}/submit/`)).data,
  verifyLogbookEntry: async (id: number, payload: Record<string, unknown>) => (await apiClient.post<LogbookEntry>(`/api/academics/logbook-entries/${id}/verify/`, payload)).data,
  returnLogbookEntry: async (id: number, payload: Record<string, unknown>) => (await apiClient.post<LogbookEntry>(`/api/academics/logbook-entries/${id}/return_revision/`, payload)).data,
  rejectLogbookEntry: async (id: number, payload: Record<string, unknown>) => (await apiClient.post<LogbookEntry>(`/api/academics/logbook-entries/${id}/reject/`, payload)).data,
  cancelLogbookEntry: async (id: number) => (await apiClient.post<LogbookEntry>(`/api/academics/logbook-entries/${id}/cancel/`)).data,

  getMyAcademicProgress: async () => (await apiClient.get<Record<string, unknown>>('/api/academics/my-progress/')).data,
  getResidentAcademicProgress: async (id: number) => (await apiClient.get<Record<string, unknown>>(`/api/academics/residents/${id}/progress/`)).data,
  getSupervisorAcademicWorkload: async () => (await apiClient.get<Record<string, unknown>>('/api/academics/supervisor-workload/')).data,
  getAdminAcademicWorkflowOverview: async () => (await apiClient.get<Record<string, unknown>>('/api/academics/admin-workflow-overview/')).data,
  getAcademicWorkflowDataQuality: async () => (await apiClient.get<Record<string, unknown>>('/api/academics/workflow-data-quality/')).data,
  seedWorkflows: async () => (await apiClient.post<Record<string, number>>('/api/academics/seed-workflows/')).data,

  // Brick 11 dashboards
  getAdminDashboardMonitoring: async () => (await apiClient.get<Record<string, unknown>>('/api/academics/monitoring/admin-dashboard/')).data,
  getSupervisorDashboardMonitoring: async () => (await apiClient.get<Record<string, unknown>>('/api/academics/monitoring/supervisor-dashboard/')).data,
  getMyProgressMonitoring: async () => (await apiClient.get<Record<string, unknown>>('/api/academics/monitoring/my-progress/')).data,
  getDepartmentMonitoringSummary: async () => unwrapList((await apiClient.get<ListResponse<Record<string, unknown>>>('/api/academics/monitoring/departments/')).data),
  getProgramMonitoringSummary: async () => unwrapList((await apiClient.get<ListResponse<Record<string, unknown>>>('/api/academics/monitoring/programs/')).data),
  getSessionMonitoringSummary: async () => unwrapList((await apiClient.get<ListResponse<Record<string, unknown>>>('/api/academics/monitoring/sessions/')).data),

  // Brick 11 reports
  getResidentProgressReportList: async () => unwrapList((await apiClient.get<ListResponse<Record<string, unknown>>>('/api/academics/reports/resident-progress/')).data),
  getResidentProgressReportDetail: async (id: number) => (await apiClient.get<Record<string, unknown>>(`/api/academics/reports/resident-progress/${id}/`)).data,
  getSupervisorWorkloadReportList: async () => unwrapList((await apiClient.get<ListResponse<Record<string, unknown>>>('/api/academics/reports/supervisor-workload/')).data),
  getSupervisorWorkloadReportDetail: async (id: number) => (await apiClient.get<Record<string, unknown>>(`/api/academics/reports/supervisor-workload/${id}/`)).data,
  getEvaluationReport: async (params?: Record<string, string | number | boolean>) => unwrapList((await apiClient.get<ListResponse<Record<string, unknown>>>('/api/academics/reports/evaluations/', { params })).data),
  getLogbookReport: async (params?: Record<string, string | number | boolean>) => unwrapList((await apiClient.get<ListResponse<Record<string, unknown>>>('/api/academics/reports/logbook/', { params })).data),
  getDataQualityReport: async () => (await apiClient.get<Record<string, unknown>>('/api/academics/reports/data-quality/')).data,
};
