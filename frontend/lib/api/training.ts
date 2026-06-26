/**
 * Phase 6 — Academic Core API client
 * Covers: Programs, Milestones, Research, Thesis, Workshops, Eligibility
 */
import apiClient from './client';

// ------------------------------------------------------------------ Types

export interface TrainingProgram {
  id: number;
  code: string;
  name: string;
  degree_type: string;
  degree_type_display: string;
  department: number | null;
  duration_months: number;
  is_active: boolean;
  notes: string;
}

export interface ProgramPolicy {
  allow_program_change: boolean;
  program_change_requires_restart: boolean;
  min_active_months_before_imm: number | null;
  imm_allowed_from_month: number | null;
  final_allowed_from_month: number | null;
  exception_rules_text: string;
}

export interface ProgramMilestone {
  id: number;
  program: number;
  code: string;
  name: string;
  recommended_month: number | null;
  is_active: boolean;
  research_requirement: MilestoneResearchReq | null;
  workshop_requirements: MilestoneWorkshopReq[];
  logbook_requirements: MilestoneLogbookReq[];
}

export interface MilestoneResearchReq {
  requires_synopsis_approved: boolean;
  requires_synopsis_submitted_to_university: boolean;
  requires_thesis_submitted: boolean;
}

export interface MilestoneWorkshopReq {
  id: number;
  workshop: number;
  workshop_name: string;
  required_count: number;
}

export interface MilestoneLogbookReq {
  id: number;
  procedure_key: string;
  category: string;
  min_entries: number;
}

export interface ResidentResearchProject {
  id: number;
  resident_training_record: number;
  title: string;
  topic_area: string;
  supervisor: number | null;
  supervisor_name: string | null;
  resident_name: string;
  status: string;
  status_display: string;
  synopsis_file: string | null;
  synopsis_approved_at: string | null;
  supervisor_feedback: string;
  university_submission_ref: string;
  submitted_to_supervisor_at: string | null;
  submitted_to_university_at: string | null;
  accepted_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface ResidentThesis {
  id: number;
  resident_training_record: number;
  status: string;
  status_display: string;
  thesis_file: string | null;
  submitted_at: string | null;
  final_submission_ref: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface Workshop {
  id: number;
  name: string;
  code: string;
  description: string;
  is_active: boolean;
}

export interface WorkshopCompletion {
  id: number;
  resident_training_record: number;
  workshop: number;
  workshop_name: string;
  completed_at: string;
  certificate_file: string | null;
  source: string;
  source_display: string;
  notes: string;
}

export interface MilestoneEligibility {
  id: number;
  milestone: number;
  milestone_code: string;
  milestone_name: string;
  status: string;
  status_display: string;
  reasons: string[];
  computed_at: string;
}

interface MilestoneEligibilityApiShape extends Omit<MilestoneEligibility, 'reasons'> {
  reasons?: string[];
  reasons_json?: string[];
}

export interface SystemSettings {
  WORKSHOP_MANAGEMENT_ENABLED: boolean;
  [key: string]: unknown;
}

export interface ProgramRotationTemplate {
  id: number;
  program: number;
  program_name: string;
  name: string;
  department: number;
  department_name: string;
  duration_weeks: number;
  required: boolean;
  sequence_order: number;
  allowed_hospitals: number[];
  allowed_hospital_names: string[];
  active: boolean;
  created_at: string;
}

export interface ResidentTrainingRecordListItem {
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
  created_by: number | null;
  created_at: string;
  updated_at: string;
}

export interface ResidentTrainingRecordUpsert {
  resident_user: number;
  program: number;
  start_date: string;
  expected_end_date?: string | null;
  current_level?: string;
  active?: boolean;
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
  status: string;
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

export interface DeputationPosting {
  id: number;
  resident_training: number;
  resident_name: string;
  posting_type: string;
  institution_name: string;
  city: string;
  start_date: string;
  end_date: string;
  status: string;
  notes: string;
  approved_by: number | null;
  approved_at: string | null;
  reject_reason: string;
  created_at: string;
  updated_at: string;
}

export interface LeaveRequest {
  id: number;
  resident_training: number;
  resident_name: string;
  leave_type: string;
  start_date: string;
  end_date: string;
  reason: string;
  status: string;
  approved_at: string | null;
  reject_reason: string;
  created_at: string;
  updated_at: string;
}

export interface LogbookEntry {
  id: number;
  resident_training_record: number;
  resident_name: string;
  rotation_assignment: number | null;
  patient_id_number: string;
  patient_name: string;
  age: number | null;
  gender: string;
  demographics: string;
  disease_area: string;
  diagnosis: string;
  clinical_presentation: string;
  management_plan: string;
  resident_reflection: string;
  patient_seen_at: string;
  status: 'DRAFT' | 'SUBMITTED' | 'RETURNED' | 'APPROVED';
  feedback: string;
  submitted_at: string | null;
  returned_at: string | null;
  approved_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface LogbookThresholdSnapshot {
  id: number;
  threshold_config: number;
  threshold_name: string;
  rotation_assignment: number | null;
  window_start: string | null;
  window_end: string | null;
  approved_entries: number;
  required_entries: number;
  is_met: boolean;
  computed_at: string;
}

export interface SubmissionRequirementTemplate {
  id: number;
  submission_type: 'SYNOPSIS' | 'THESIS';
  code: string;
  title: string;
  description: string;
  is_required: boolean;
  active: boolean;
  sort_order: number;
  program: number | null;
  program_name: string | null;
  department: number | null;
  department_name: string | null;
}

export interface SubmissionDocumentRecord {
  id: number;
  submission: number;
  requirement: number | null;
  requirement_title: string | null;
  file: string;
  original_filename: string;
  uploaded_at: string;
  is_active: boolean;
}

export interface SubmissionCertificateRecord {
  id: number;
  submission: number;
  certificate_number: string;
  status: 'ISSUED' | 'VERIFIED';
  issued_at: string;
  verified_at: string | null;
}

export interface ResidentSubmissionRecord {
  id: number;
  resident_training_record: number;
  resident_name: string;
  submission_type: 'SYNOPSIS' | 'THESIS';
  status: 'DRAFT' | 'SUBMITTED' | 'UNDER_REVIEW' | 'RETURNED' | 'VERIFIED' | 'CERTIFICATE_ISSUED';
  submitted_at: string | null;
  under_review_at: string | null;
  returned_at: string | null;
  verified_at: string | null;
  certificate_issued_at: string | null;
  feedback: string;
  required_documents_count: number;
  uploaded_required_count: number;
  all_required_uploaded: boolean;
  documents: SubmissionDocumentRecord[];
  certificate: SubmissionCertificateRecord | null;
}

export interface RotationCompletionRecord {
  id: number;
  rotation: number;
  status: 'CONFIRMED_BY_DEPARTMENT' | 'PENDING_UTRMC_VERIFICATION' | 'VERIFIED';
  resident_name: string;
  confirmed_at: string | null;
  verification_submitted_at: string | null;
  verified_at: string | null;
  notes: string;
}

export interface ResidentOperationalDashboard {
  training_record_id: number;
  logbook: {
    total: number;
    draft: number;
    submitted: number;
    returned: number;
    approved: number;
    threshold: {
      overall_met: boolean;
      count: number;
      items: Array<{
        threshold_config_id: number;
        rotation_assignment_id: number | null;
        approved_entries: number;
        required_entries: number;
        is_met: boolean;
      }>;
    };
  };
  submissions: {
    synopsis: ResidentSubmissionRecord | null;
    thesis: ResidentSubmissionRecord | null;
  };
  certificates: Array<{
    type: string;
    certificate_number: string;
    issued_at: string;
    status: string;
    rotation_id?: number;
  }>;
  readiness: {
    logbook_threshold_met: boolean;
    synopsis_certificate_issued: boolean;
    thesis_certificate_issued: boolean;
    required_rotations_verified: boolean;
    required_rotation_count: number;
    verified_rotation_count: number;
  };
  pending_actions: string[];
}

export interface SupervisorOperationalDashboard {
  assigned_residents: number;
  pending_logbook_reviews: number;
  returned_logbook_queue: number;
  pending_rotation_applications: number;
  pending_synopsis_reviews: number;
  pending_thesis_reviews: number;
  residents: Array<{
    resident_id: number;
    resident_name: string;
    program: string;
    logbook_approved: number;
    pending_reviews: number;
    threshold_met: boolean;
  }>;
  lagging_residents: Array<{
    resident_id: number;
    resident_name: string;
    program: string;
    logbook_approved: number;
    pending_reviews: number;
    threshold_met: boolean;
  }>;
  is_hod: boolean;
}

export interface HODOperationalDashboard {
  departments: number[];
  department_residents: number;
  pending_logbook_approvals: number;
  rotation_applications: number;
  supervisor_lag: Array<{
    supervisor_id: number | null;
    supervisor_name: string;
    pending_logbook_reviews: number;
  }>;
  milestone_completion: {
    synopsis_certificates: number;
    thesis_certificates: number;
    rotation_verified: number;
  };
}

export interface UTRMCOperationalDashboard {
  cross_department_overview: {
    active_residents: number;
    program_count: number;
    pending_logbook_reviews: number;
  };
  pending_synopsis_reviews: number;
  pending_thesis_reviews: number;
  pending_rotation_completion_verifications: number;
  resident_milestone_readiness: Array<{
    resident_id: number;
    resident_name: string;
    program: string;
    logbook_threshold_met: boolean;
    synopsis_certificate_issued: boolean;
    thesis_certificate_issued: boolean;
    required_rotation_count: number;
    verified_rotation_count: number;
    rotation_requirement_met: boolean;
  }>;
  readiness_summary: {
    fully_ready_count: number;
    total_rows: number;
  };
}

// ------------------------------------------------------------------ helpers

function toArray<T>(data: unknown): T[] {
  if (Array.isArray(data)) return data as T[];
  if (data && typeof data === 'object' && 'results' in data) return ((data as { results?: T[] }).results) || [];
  return [];
}

function normalizeEligibility(item: MilestoneEligibilityApiShape): MilestoneEligibility {
  const reasons = Array.isArray(item.reasons)
    ? item.reasons
    : (Array.isArray(item.reasons_json) ? item.reasons_json : []);

  return {
    ...item,
    reasons,
  };
}

// ------------------------------------------------------------------ API

export const trainingApi = {
  // Programs
  async listPrograms(): Promise<TrainingProgram[]> {
    const r = await apiClient.get('/api/programs/');
    return toArray<TrainingProgram>(r.data);
  },

  async getProgram(id: number): Promise<TrainingProgram> {
    const r = await apiClient.get<TrainingProgram>(`/api/programs/${id}/`);
    return r.data;
  },

  async createProgram(data: Partial<TrainingProgram>): Promise<TrainingProgram> {
    const r = await apiClient.post<TrainingProgram>('/api/programs/', data);
    return r.data;
  },

  async updateProgram(id: number, data: Partial<TrainingProgram>): Promise<TrainingProgram> {
    const r = await apiClient.put<TrainingProgram>(`/api/programs/${id}/`, data);
    return r.data;
  },

  // Program Policy
  async getProgramPolicy(programId: number): Promise<ProgramPolicy> {
    const r = await apiClient.get<ProgramPolicy>(`/api/programs/${programId}/policy/`);
    return r.data;
  },

  async updateProgramPolicy(programId: number, data: Partial<ProgramPolicy>): Promise<ProgramPolicy> {
    const r = await apiClient.put<ProgramPolicy>(`/api/programs/${programId}/policy/`, data);
    return r.data;
  },

  // Milestones
  async listMilestones(programId: number): Promise<ProgramMilestone[]> {
    const r = await apiClient.get(`/api/programs/${programId}/milestones/`);
    return toArray<ProgramMilestone>(r.data);
  },

  async createMilestone(programId: number, data: Partial<ProgramMilestone>): Promise<ProgramMilestone> {
    const r = await apiClient.post<ProgramMilestone>(`/api/programs/${programId}/milestones/`, data);
    return r.data;
  },

  // Research project
  async getMyResearch(): Promise<ResidentResearchProject> {
    const r = await apiClient.get<ResidentResearchProject>('/api/my/research/');
    return r.data;
  },

  async createResearch(data: { title: string; topic_area?: string; supervisor?: number }): Promise<ResidentResearchProject> {
    const r = await apiClient.post<ResidentResearchProject>('/api/my/research/', data);
    return r.data;
  },

  async patchResearch(data: Partial<ResidentResearchProject>): Promise<ResidentResearchProject> {
    const r = await apiClient.patch<ResidentResearchProject>('/api/my/research/', data);
    return r.data;
  },

  async patchResearchFile(file: File): Promise<ResidentResearchProject> {
    const fd = new FormData();
    fd.append('synopsis_file', file);
    const r = await apiClient.patch<ResidentResearchProject>('/api/my/research/', fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return r.data;
  },

  async researchAction(action: string, data?: object): Promise<ResidentResearchProject> {
    const r = await apiClient.post<ResidentResearchProject>(`/api/my/research/action/${action}/`, data || {});
    return r.data;
  },

  // Supervisor research approvals
  async getSupervisorResearchApprovals(): Promise<ResidentResearchProject[]> {
    const r = await apiClient.get('/api/supervisor/research-approvals/');
    return toArray<ResidentResearchProject>(r.data);
  },

  async supervisorApproveResearch(projectId: number, feedback?: string): Promise<ResidentResearchProject> {
    const r = await apiClient.post<ResidentResearchProject>('/api/my/research/action/supervisor-approve/', {
      project_id: projectId,
      feedback,
    });
    return r.data;
  },

  async supervisorReturnResearch(projectId: number, feedback: string): Promise<ResidentResearchProject> {
    const r = await apiClient.post<ResidentResearchProject>('/api/my/research/action/supervisor-return/', {
      project_id: projectId,
      feedback,
    });
    return r.data;
  },

  // Thesis
  async getMyThesis(): Promise<ResidentThesis> {
    const r = await apiClient.get<ResidentThesis>('/api/my/thesis/');
    return r.data;
  },

  async createThesis(data?: object): Promise<ResidentThesis> {
    const r = await apiClient.post<ResidentThesis>('/api/my/thesis/', data || {});
    return r.data;
  },

  async submitThesis(data?: object): Promise<ResidentThesis> {
    const r = await apiClient.post<ResidentThesis>('/api/my/thesis/submit/', data || {});
    return r.data;
  },

  // Workshops
  async listWorkshops(): Promise<Workshop[]> {
    const r = await apiClient.get('/api/workshops/');
    return toArray<Workshop>(r.data);
  },

  async listMyWorkshopCompletions(): Promise<{ count: number; results: WorkshopCompletion[] }> {
    const r = await apiClient.get<{ count: number; results: WorkshopCompletion[] }>('/api/my/workshops/');
    return r.data;
  },

  async createWorkshopCompletion(data: {
    workshop: number;
    completed_at: string;
    notes?: string;
  }): Promise<WorkshopCompletion> {
    const r = await apiClient.post<WorkshopCompletion>('/api/my/workshops/', data);
    return r.data;
  },

  async deleteWorkshopCompletion(id: number): Promise<void> {
    await apiClient.delete(`/api/my/workshops/${id}/`);
  },

  // Eligibility
  async getMyEligibility(): Promise<MilestoneEligibility[]> {
    const r = await apiClient.get('/api/my/eligibility/');
    const payload = r.data as {
      eligibilities?: MilestoneEligibilityApiShape[];
      results?: MilestoneEligibilityApiShape[];
    } | MilestoneEligibilityApiShape[];
    const items = Array.isArray(payload)
      ? payload
      : (payload.eligibilities || payload.results || []);
    return items.map(normalizeEligibility);
  },

  async getUTRMCEligibility(params?: {
    program?: number;
    department?: number;
    status?: string;
  }): Promise<{ count: number; results: MilestoneEligibility[] }> {
    const r = await apiClient.get<{ count: number; results: MilestoneEligibilityApiShape[] }>(
      '/api/utrmc/eligibility/',
      { params }
    );
    return {
      count: r.data.count,
      results: (r.data.results || []).map(normalizeEligibility),
    };
  },


  // Summary endpoints (Phase 6B/6C)
  async getResidentSummary(): Promise<ResidentSummary> {
    const r = await apiClient.get<ResidentSummary>('/api/residents/me/summary/');
    return r.data;
  },

  async getSupervisorSummary(): Promise<SupervisorSummary> {
    const r = await apiClient.get<SupervisorSummary>('/api/supervisors/me/summary/');
    return r.data;
  },

  async getResidentProgress(residentId: number): Promise<ResidentProgressSnapshot> {
    const r = await apiClient.get<ResidentProgressSnapshot>(`/api/supervisors/residents/${residentId}/progress/`);
    return r.data;
  },

  // ------------------------------------------------------------------ Rotation assignments

  async listResidentTrainingRecords(): Promise<ResidentTrainingRecordListItem[]> {
    const r = await apiClient.get('/api/resident-training/');
    return toArray<ResidentTrainingRecordListItem>(r.data);
  },

  async createResidentTrainingRecord(data: ResidentTrainingRecordUpsert): Promise<ResidentTrainingRecordListItem> {
    const r = await apiClient.post<ResidentTrainingRecordListItem>('/api/resident-training/', data);
    return r.data;
  },

  async updateResidentTrainingRecord(
    id: number,
    data: Partial<ResidentTrainingRecordUpsert>
  ): Promise<ResidentTrainingRecordListItem> {
    const r = await apiClient.patch<ResidentTrainingRecordListItem>(`/api/resident-training/${id}/`, data);
    return r.data;
  },

  async deleteResidentTrainingRecord(id: number): Promise<void> {
    await apiClient.delete(`/api/resident-training/${id}/`);
  },

  async listMyRotations(): Promise<{ count: number; results: RotationAssignment[] }> {
    const r = await apiClient.get<{ count: number; results: RotationAssignment[] }>('/api/my/rotations/');
    return r.data;
  },

  async listRotations(params?: {
    status?: string;
    resident_training?: number;
  }): Promise<RotationAssignment[]> {
    const r = await apiClient.get('/api/rotations/', {
      params: {
        status: params?.status,
        resident: params?.resident_training,
      },
    });
    return toArray<RotationAssignment>(r.data);
  },

  async listSupervisorPendingRotations(): Promise<{ count: number; results: RotationAssignment[] }> {
    const r = await apiClient.get<{ count: number; results: RotationAssignment[] }>('/api/supervisor/rotations/pending/');
    return r.data;
  },

  async listRotationApprovals(): Promise<{ count: number; results: RotationAssignment[] }> {
    const r = await apiClient.get<{ count: number; results: RotationAssignment[] }>('/api/utrmc/approvals/rotations/');
    return r.data;
  },

  async createRotation(data: {
    resident_training: number;
    hospital_department: number;
    start_date: string;
    end_date: string;
    notes?: string;
  }): Promise<RotationAssignment> {
    const r = await apiClient.post<RotationAssignment>('/api/rotations/', data);
    return r.data;
  },

  async rotationAction(
    id: number,
    action:
      | 'submit'
      | 'hod-approve'
      | 'utrmc-approve'
      | 'activate'
      | 'complete'
      | 'returned'
      | 'reject'
      | 'review-application'
      | 'confirm-completion'
      | 'verify-completion',
    data?: object
  ): Promise<RotationAssignment> {
    const r = await apiClient.post<RotationAssignment>(`/api/rotations/${id}/${action}/`, data || {});
    return r.data;
  },

  // ------------------------------------------------------------------ Logbook

  async listLogbook(params?: { status?: string }): Promise<{ count: number; results: LogbookEntry[] }> {
    const r = await apiClient.get('/api/logbook/', { params });
    return {
      count: typeof r.data?.count === 'number' ? r.data.count : toArray<LogbookEntry>(r.data).length,
      results: toArray<LogbookEntry>(r.data),
    };
  },

  async createLogbookEntry(data: Partial<LogbookEntry>): Promise<LogbookEntry> {
    const r = await apiClient.post<LogbookEntry>('/api/logbook/', data);
    return r.data;
  },

  async updateLogbookEntry(id: number, data: Partial<LogbookEntry>): Promise<LogbookEntry> {
    const r = await apiClient.patch<LogbookEntry>(`/api/logbook/${id}/`, data);
    return r.data;
  },

  async submitLogbookEntry(id: number): Promise<LogbookEntry> {
    const r = await apiClient.post<LogbookEntry>(`/api/logbook/${id}/submit/`);
    return r.data;
  },

  async reviewLogbookEntry(
    id: number,
    action: 'approved' | 'returned',
    feedback?: string
  ): Promise<LogbookEntry> {
    const r = await apiClient.post<LogbookEntry>(`/api/logbook/${id}/review/`, {
      action,
      feedback,
    });
    return r.data;
  },

  async getLogbookReviewQueue(): Promise<{ count: number; results: LogbookEntry[] }> {
    const r = await apiClient.get<{ count: number; results: LogbookEntry[] }>('/api/logbook/review-queue/');
    return r.data;
  },

  async getMyLogbookThreshold(): Promise<{
    count: number;
    results: LogbookThresholdSnapshot[];
    overall_met: boolean;
  }> {
    const r = await apiClient.get('/api/logbook/my-threshold/');
    return {
      count: r.data.count || 0,
      results: toArray<LogbookThresholdSnapshot>(r.data.results || []),
      overall_met: Boolean(r.data.overall_met),
    };
  },

  // -------------------------------------------------- Submission completeness

  async listSubmissionRequirements(
    submissionType: 'SYNOPSIS' | 'THESIS'
  ): Promise<SubmissionRequirementTemplate[]> {
    const r = await apiClient.get('/api/submissions/requirements/', {
      params: { submission_type: submissionType, active: true },
    });
    return toArray<SubmissionRequirementTemplate>(r.data);
  },

  async getSynopsisSubmission(): Promise<ResidentSubmissionRecord> {
    const r = await apiClient.get<ResidentSubmissionRecord>('/api/submissions/synopsis/');
    return r.data;
  },

  async createSynopsisSubmission(data?: { feedback?: string }): Promise<ResidentSubmissionRecord> {
    const r = await apiClient.post<ResidentSubmissionRecord>('/api/submissions/synopsis/', data || {});
    return r.data;
  },

  async patchSynopsisSubmission(data: { feedback?: string }): Promise<ResidentSubmissionRecord> {
    const r = await apiClient.patch<ResidentSubmissionRecord>('/api/submissions/synopsis/', data);
    return r.data;
  },

  async uploadSynopsisDocument(file: File, requirementId?: number): Promise<SubmissionDocumentRecord> {
    const fd = new FormData();
    fd.append('file', file);
    if (requirementId) fd.append('requirement', String(requirementId));
    const r = await apiClient.post<SubmissionDocumentRecord>(
      '/api/submissions/synopsis/documents/',
      fd,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );
    return r.data;
  },

  async submitSynopsisSubmission(): Promise<ResidentSubmissionRecord> {
    const r = await apiClient.post<ResidentSubmissionRecord>('/api/submissions/synopsis/submit/');
    return r.data;
  },

  async getThesisSubmission(): Promise<ResidentSubmissionRecord> {
    const r = await apiClient.get<ResidentSubmissionRecord>('/api/submissions/thesis/');
    return r.data;
  },

  async createThesisSubmission(data?: { feedback?: string }): Promise<ResidentSubmissionRecord> {
    const r = await apiClient.post<ResidentSubmissionRecord>('/api/submissions/thesis/', data || {});
    return r.data;
  },

  async patchThesisSubmission(data: { feedback?: string }): Promise<ResidentSubmissionRecord> {
    const r = await apiClient.patch<ResidentSubmissionRecord>('/api/submissions/thesis/', data);
    return r.data;
  },

  async uploadThesisDocument(file: File, requirementId?: number): Promise<SubmissionDocumentRecord> {
    const fd = new FormData();
    fd.append('file', file);
    if (requirementId) fd.append('requirement', String(requirementId));
    const r = await apiClient.post<SubmissionDocumentRecord>(
      '/api/submissions/thesis/documents/',
      fd,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );
    return r.data;
  },

  async submitThesisSubmission(): Promise<ResidentSubmissionRecord> {
    const r = await apiClient.post<ResidentSubmissionRecord>('/api/submissions/thesis/submit/');
    return r.data;
  },

  async getSynopsisReviewQueue(): Promise<{ count: number; results: ResidentSubmissionRecord[] }> {
    const r = await apiClient.get('/api/submissions/synopsis/review-queue/');
    return { count: r.data.count || 0, results: toArray<ResidentSubmissionRecord>(r.data) };
  },

  async getThesisReviewQueue(): Promise<{ count: number; results: ResidentSubmissionRecord[] }> {
    const r = await apiClient.get('/api/submissions/thesis/review-queue/');
    return { count: r.data.count || 0, results: toArray<ResidentSubmissionRecord>(r.data) };
  },

  async reviewSynopsisSubmission(
    submissionId: number,
    action: 'start-review' | 'return' | 'verify',
    comments?: string
  ): Promise<ResidentSubmissionRecord> {
    const r = await apiClient.post<ResidentSubmissionRecord>(
      `/api/submissions/synopsis/${submissionId}/review/`,
      { action, comments }
    );
    return r.data;
  },

  async reviewThesisSubmission(
    submissionId: number,
    action: 'start-review' | 'return' | 'verify',
    comments?: string
  ): Promise<ResidentSubmissionRecord> {
    const r = await apiClient.post<ResidentSubmissionRecord>(
      `/api/submissions/thesis/${submissionId}/review/`,
      { action, comments }
    );
    return r.data;
  },

  async listSubmissionCertificates(params?: {
    submission_type?: 'SYNOPSIS' | 'THESIS';
  }): Promise<{ count: number; results: SubmissionCertificateRecord[] }> {
    const r = await apiClient.get('/api/submissions/certificates/', { params });
    return { count: r.data.count || 0, results: toArray<SubmissionCertificateRecord>(r.data) };
  },

  // ------------------------------------------------ Rotation completion queue

  async listRotationCompletions(params?: {
    status?: 'CONFIRMED_BY_DEPARTMENT' | 'PENDING_UTRMC_VERIFICATION' | 'VERIFIED';
  }): Promise<{ count: number; results: RotationCompletionRecord[] }> {
    const r = await apiClient.get('/api/rotations/completions/', { params });
    return {
      count: r.data.count || 0,
      results: toArray<RotationCompletionRecord>(r.data),
    };
  },

  async verifyRotationCompletion(completionId: number): Promise<RotationCompletionRecord> {
    const r = await apiClient.post<RotationCompletionRecord>(
      `/api/rotations/completions/${completionId}/verify/`
    );
    return r.data;
  },

  // ------------------------------------------------------ Operational metrics

  async getResidentOperationalDashboard(): Promise<ResidentOperationalDashboard> {
    const r = await apiClient.get<ResidentOperationalDashboard>('/api/dashboard/resident/');
    return r.data;
  },

  async getSupervisorOperationalDashboard(): Promise<SupervisorOperationalDashboard> {
    const r = await apiClient.get<SupervisorOperationalDashboard>('/api/dashboard/supervisor/');
    return r.data;
  },

  async getHODOperationalDashboard(): Promise<HODOperationalDashboard> {
    const r = await apiClient.get<HODOperationalDashboard>('/api/dashboard/hod/');
    return r.data;
  },

  async getUTRMCOperationalDashboard(params?: { search?: string }): Promise<UTRMCOperationalDashboard> {
    const r = await apiClient.get<UTRMCOperationalDashboard>('/api/dashboard/utrmc/', { params });
    return r.data;
  },

  // ------------------------------------------------------------------ Leave requests

  async listMyLeaves(): Promise<{ count: number; results: LeaveRequest[] }> {
    const r = await apiClient.get<{ count: number; results: LeaveRequest[] }>('/api/my/leaves/');
    return r.data;
  },

  async createLeave(data: {
    resident_training: number;
    leave_type: string;
    start_date: string;
    end_date: string;
    reason?: string;
  }): Promise<LeaveRequest> {
    const r = await apiClient.post<LeaveRequest>('/api/leaves/', data);
    return r.data;
  },

  async submitLeave(id: number): Promise<LeaveRequest> {
    const r = await apiClient.post<LeaveRequest>(`/api/leaves/${id}/submit/`);
    return r.data;
  },

  async getSupervisorPendingLeaves(): Promise<LeaveRequest[]> {
    const r = await apiClient.get('/api/utrmc/approvals/leaves/');
    return toArray<LeaveRequest>(r.data);
  },

  async approveLeave(id: number): Promise<LeaveRequest> {
    const r = await apiClient.post<LeaveRequest>(`/api/leaves/${id}/approve/`);
    return r.data;
  },

  async rejectLeave(id: number, reason: string): Promise<LeaveRequest> {
    const r = await apiClient.post<LeaveRequest>(`/api/leaves/${id}/reject/`, { reason });
    return r.data;
  },

  // System settings
  async getSystemSettings(): Promise<SystemSettings> {
    const r = await apiClient.get<SystemSettings>('/api/system/settings/');
    return r.data;
  },

  // ------------------------------------------------------------------ Program Rotation Templates

  async listProgramTemplates(programId: number): Promise<ProgramRotationTemplate[]> {
    const r = await apiClient.get(`/api/program-templates/?program=${programId}`);
    return toArray<ProgramRotationTemplate>(r.data);
  },

  async createProgramTemplate(data: Partial<ProgramRotationTemplate>): Promise<ProgramRotationTemplate> {
    const r = await apiClient.post<ProgramRotationTemplate>('/api/program-templates/', data);
    return r.data;
  },

  async updateProgramTemplate(id: number, data: Partial<ProgramRotationTemplate>): Promise<ProgramRotationTemplate> {
    const r = await apiClient.patch<ProgramRotationTemplate>(`/api/program-templates/${id}/`, data);
    return r.data;
  },

  async deleteProgramTemplate(id: number): Promise<void> {
    await apiClient.delete(`/api/program-templates/${id}/`);
  },

  // ------------------------------------------------------------------ Deputation Postings

  async listPostings(params?: { status?: string }): Promise<DeputationPosting[]> {
    const qs = params?.status ? `?status=${params.status}` : '';
    const r = await apiClient.get(`/api/postings/${qs}`);
    return toArray<DeputationPosting>(r.data);
  },

  async createPosting(data: Partial<DeputationPosting>): Promise<DeputationPosting> {
    const r = await apiClient.post<DeputationPosting>('/api/postings/', data);
    return r.data;
  },

  async postingAction(id: number, action: 'approve' | 'reject' | 'complete', data?: object): Promise<DeputationPosting> {
    const r = await apiClient.post<DeputationPosting>(`/api/postings/${id}/${action}/`, data || {});
    return r.data;
  },

  async deletePosting(id: number): Promise<void> {
    await apiClient.delete(`/api/postings/${id}/`);
  },
};

// ------------------------------------------------------------------ Summary types

export interface ResidentSummary {
  training_record: {
    id: number;
    program_code: string;
    program_name: string;
    degree_type: string;
    start_date: string;
    current_month_index: number;
  };
  rotation: {
    current: { id: number; department: string; hospital: string; start_date: string; end_date: string; status: string } | null;
    next: { id: number; department: string; hospital: string; start_date: string; end_date: string; status: string } | null;
  };
  schedule: Array<{ id: number; department: string; hospital: string; start_date: string; end_date: string; status: string }>;
  leaves: { active_count: number; pending_count: number; list: Array<{ id: number; leave_type: string; start_date: string; end_date: string; status: string }> };
  postings: { active_count: number; pending_count: number };
  research: { status: string | null; supervisor_name: string | null; synopsis_uploaded: boolean; university_submitted: boolean };
  thesis: { status: string; submitted_at: string | null };
  workshops: { total_completed: number; required_for_imm: number; required_for_final: number; completed_list: Array<{ id: number; workshop_name: string; completed_at: string }> };
  eligibility: {
    IMM: { status: string | null; reasons: string[] };
    FINAL: { status: string | null; reasons: string[] };
  };
}

export interface SupervisorSummary {
  pending: { rotation_approvals: number; leave_approvals: number; research_approvals: number };
  residents: Array<{
    id: number;
    rtr_id: number;
    name: string;
    program: string;
    current_rotation: string | null;
    imm_status: string | null;
    final_status: string | null;
    research_status: string | null;
  }>;
}

export interface ResidentProgressSnapshot {
  resident: { id: number; name: string; username: string };
  resident_name: string;
  training_record: { program_code: string; program_name: string; degree_type: string; start_date: string; current_month_index: number };
  program_name: string;
  current_month_index: number;
  current_rotation: { department: string; hospital: string; start_date: string; end_date: string; status: string } | null;
  research: { status: string | null; title: string | null; synopsis_file?: string | null } | null;
  thesis: { status: string; submitted_at?: string | null } | null;
  workshops: { total_completed: number; required_for_imm?: number; required_for_final?: number; completed_list?: string[] };
  eligibility: { IMM: { status: string | null; reasons: string[] } | null; FINAL: { status: string | null; reasons: string[] } | null };
}
