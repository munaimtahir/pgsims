# OUT/120_ROTATIONS_SPEC_LOCK.md — Option 5 Training & Rotations Spec Lock

## Canonical Data Model

| Model | App | Status |
|---|---|---|
| TrainingProgram | sims.training | NEW |
| ProgramRotationTemplate | sims.training | NEW |
| ResidentTrainingRecord | sims.training | NEW |
| RotationAssignment | sims.training | NEW (replaces legacy Rotation) |
| LeaveRequest | sims.training | NEW |
| DeputationPosting | sims.training | NEW |
| Hospital | sims.rotations | REUSE (canonical) |
| HospitalDepartment | sims.rotations | REUSE (canonical) |
| Rotation | sims.rotations | LEGACY (kept for backward compat, to be removed in Phase 6) |

## RotationAssignment State Machine

```
DRAFT → SUBMITTED → APPROVED → ACTIVE → COMPLETED
                 ↘ RETURNED (send-back)
                 ↘ REJECTED
DRAFT → CANCELLED
```

## Approval Chain

1. Resident (or UTRMC admin) creates DRAFT → submits → SUBMITTED
2. HOD / Supervisor (dept-scoped) performs hod-approve → APPROVED
3. UTRMC admin can also directly approve from SUBMITTED or APPROVED
4. UTRMC admin activates → ACTIVE → marks complete → COMPLETED

## API Endpoints Implemented

- GET/POST/PATCH/DELETE `/api/programs/`
- GET/POST/PATCH/DELETE `/api/program-templates/`
- GET/POST/PATCH/DELETE `/api/resident-training/`
- GET/POST/PATCH/DELETE `/api/rotations/` + state actions: submit, hod-approve, utrmc-approve, activate, complete, returned, reject
- GET/POST/PATCH/DELETE `/api/leaves/` + actions: submit, approve, reject
- GET/POST/PATCH/DELETE `/api/postings/` + actions: approve, reject, complete
- GET `/api/utrmc/approvals/rotations/`
- GET `/api/utrmc/approvals/leaves/`
- GET `/api/my/rotations/`
- GET `/api/my/leaves/`
- GET `/api/supervisor/rotations/pending/`

## UI Screens Implemented

| Route | Role | Description |
|---|---|---|
| /dashboard/utrmc/programs | utrmc_admin | CRUD programs |
| /dashboard/utrmc/program-templates | utrmc_admin | CRUD rotation templates |
| /dashboard/utrmc/resident-training | utrmc_admin | Enroll residents in programs |
| /dashboard/utrmc/rotations | utrmc_admin | Manage all rotation assignments + state actions |
| /dashboard/utrmc/approvals/rotations | utrmc_admin, supervisor | Pending rotation approvals |
| /dashboard/utrmc/approvals/leaves | utrmc_admin, supervisor | Pending leave approvals |
| /dashboard/utrmc/leaves | utrmc_admin | All leave requests |
| /dashboard/utrmc/postings | utrmc_admin | All deputation/postings |
| /dashboard/supervisor/approvals | supervisor, faculty | Department-scoped pending approvals |
| /dashboard/supervisor/rotations | supervisor, faculty | Department-scoped rotations |
| /dashboard/my-training | pg, resident | Own rotation schedule |
| /dashboard/my-leaves | pg, resident | Own leave requests + submit |
| /dashboard/my-postings | pg, resident | Own postings + submit |
