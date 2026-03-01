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

export interface SystemSettings {
  WORKSHOP_MANAGEMENT_ENABLED: boolean;
  [key: string]: unknown;
}

// ------------------------------------------------------------------ helpers

function toArray<T>(data: unknown): T[] {
  if (Array.isArray(data)) return data as T[];
  if (data && typeof data === 'object' && 'results' in data) return ((data as { results?: T[] }).results) || [];
  return [];
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
    return toArray<MilestoneEligibility>(r.data);
  },

  async getUTRMCEligibility(params?: {
    program?: number;
    department?: number;
    status?: string;
  }): Promise<{ count: number; results: MilestoneEligibility[] }> {
    const r = await apiClient.get<{ count: number; results: MilestoneEligibility[] }>(
      '/api/utrmc/eligibility/',
      { params }
    );
    return r.data;
  },

  // System settings
  async getSystemSettings(): Promise<SystemSettings> {
    const r = await apiClient.get<SystemSettings>('/api/system/settings/');
    return r.data;
  },
};
