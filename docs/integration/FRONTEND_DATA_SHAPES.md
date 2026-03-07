# Frontend Data Shapes

**Generated:** 2026-03-07  
**Source:** `frontend/lib/api/*.ts` TypeScript interface definitions

This document catalogs every TypeScript type used in frontend API interactions.

---

## Authentication Types (`auth.ts`)

```typescript
interface LoginCredentials {
  email: string;
  password: string;
}

interface LoginResponse {
  access: string;
  refresh: string;
  user: User;
}

interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  role: string;
}

interface RegisterResponse {
  id: number;
  email: string;
  // ...user fields
}

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  is_staff: boolean;
  // profile fields
}
```

---

## Userbase Types (`userbase.ts`)

```typescript
interface UserbaseHospital {
  id: number;
  name: string;
  code: string;
  city?: string;
  is_active: boolean;
}

interface UserbaseDepartment {
  id: number;
  name: string;
  code: string;
  is_active: boolean;
}

interface UserbaseHospitalDepartment {
  id: number;
  hospital: number;
  hospital_name: string;
  department: number;
  department_name: string;
  is_active: boolean;
}

interface UserbaseUser {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  is_active: boolean;
  home_hospital?: number;
  home_department?: number;
}

interface DepartmentRosterResponse {
  members: UserbaseUser[];
  hod?: UserbaseUser;
}
```

---

## Training Types (`training.ts`)

### Programs

```typescript
interface TrainingProgram {
  id: number;
  code: string;
  name: string;
  degree_type: string;         // "FCPS" | "MD" | "MS" | "Diploma" | "Other"
  degree_type_display: string;
  department: number | null;
  duration_months: number;
  is_active: boolean;
  notes: string;
}

interface ProgramPolicy {
  allow_program_change: boolean;
  program_change_requires_restart: boolean;
  min_active_months_before_imm: number | null;
  imm_allowed_from_month: number | null;
  final_allowed_from_month: number | null;
  exception_rules_text: string;
}

interface ProgramMilestone {
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

interface MilestoneResearchReq {
  requires_synopsis_approved: boolean;
  requires_synopsis_submitted_to_university: boolean;
  requires_thesis_submitted: boolean;
}

interface MilestoneWorkshopReq {
  id: number;
  workshop: number;
  workshop_name: string;
  required_count: number;
}

interface MilestoneLogbookReq {
  id: number;
  procedure_key: string;
  category: string;
  min_entries: number;
}
```

### Research

```typescript
interface ResidentResearchProject {
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
```

### Thesis

```typescript
interface ResidentThesis {
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
```

### Workshops

```typescript
interface Workshop {
  id: number;
  name: string;
  code: string;
  description: string;
  is_active: boolean;
}

interface WorkshopCompletion {
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
```

### Eligibility

```typescript
interface MilestoneEligibility {
  id: number;
  milestone: number;
  milestone_code: string;
  milestone_name: string;
  status: string;           // "eligible" | "not_eligible" | "pending"
  status_display: string;
  reasons: string[];
  computed_at: string;
}
```

### Summaries

```typescript
interface ResidentSummary {
  resident: UserbaseUser;
  training_record: {
    id: number;
    program: TrainingProgram;
    current_level: string;    // "y1" | "y2" | "y3" | "y4" | "y5"
    enrollment_date: string;
    is_active: boolean;
  };
  rotation_stats: {
    total: number;
    active: number;
    completed: number;
    pending: number;
  };
  leave_stats: {
    total: number;
    approved: number;
    pending: number;
  };
  research_status: string | null;
  thesis_status: string | null;
  workshop_completions: number;
  eligibility_status: string;
}

interface SupervisorSummary {
  supervisor: UserbaseUser;
  assigned_residents: number;
  pending_rotations: number;
  pending_research_approvals: number;
}

interface ResidentProgressSnapshot {
  resident: UserbaseUser;
  training_record: object;
  milestones: MilestoneEligibility[];
  rotations: object[];
  research: ResidentResearchProject | null;
  thesis: ResidentThesis | null;
  workshop_completions: WorkshopCompletion[];
}

interface SystemSettings {
  WORKSHOP_MANAGEMENT_ENABLED: boolean;
  [key: string]: unknown;
}
```

---

## Notification Types (`notifications.ts`)

```typescript
interface Notification {
  id: number;
  verb: string;
  title: string;
  body: string;
  is_read: boolean;           // computed from read_at
  created_at: string;
  metadata: Record<string, unknown>;
}

interface NotificationPreferences {
  email_enabled: boolean;
  in_app_enabled: boolean;
  // per-verb overrides
}
```

---

## Audit Types (`audit.ts`)

```typescript
interface ActivityLog {
  id: number;
  actor: UserbaseUser;
  verb: string;
  target_type: string;
  target_id: number;
  timestamp: string;
  ip_address: string;
  metadata: Record<string, unknown>;
}

interface AuditReport {
  id: number;
  title: string;
  generated_by: UserbaseUser;
  generated_at: string;
  report_type: string;
  parameters: Record<string, unknown>;
  result_summary: Record<string, unknown>;
}
```

---

## Bulk Types (`bulk.ts`)

```typescript
interface BulkImportResult {
  success_count: number;
  error_count: number;
  errors: Array<{
    row: number;
    field: string;
    message: string;
  }>;
}

interface BulkAssignmentResult {
  assigned: number;
  skipped: number;
  errors: string[];
}
```

---

## Status Value Constants

These string values are used as status codes across the system. They must match exactly between backend and frontend.

### Rotation Status
| Constant | String Value | Display |
|----------|-------------|---------|
| `STATUS_DRAFT` | `"draft"` | Draft |
| `STATUS_SUBMITTED` | `"submitted"` | Submitted |
| `STATUS_APPROVED` | `"approved"` | Approved |
| `STATUS_ACTIVE` | `"active"` | Active |
| `STATUS_COMPLETED` | `"completed"` | Completed |
| `STATUS_RETURNED` | `"returned"` | Returned |
| `STATUS_REJECTED` | `"rejected"` | Rejected |
| `STATUS_CANCELLED` | `"cancelled"` | Cancelled |

### Training Level (current_level)
| Value | Display |
|-------|---------|
| `"y1"` | Year 1 |
| `"y2"` | Year 2 |
| `"y3"` | Year 3 |
| `"y4"` | Year 4 |
| `"y5"` | Year 5 |

### Degree Type
| Value | Display |
|-------|---------|
| `"FCPS"` | FCPS |
| `"MD"` | MD |
| `"MS"` | MS |
| `"Diploma"` | Diploma |
| `"Other"` | Other |
