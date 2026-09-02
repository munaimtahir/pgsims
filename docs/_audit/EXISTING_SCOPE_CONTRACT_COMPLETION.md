# Existing Scope Contract Completion

**Date:** 2026-03-07  
**Phase:** F — Contract completion for existing scope

---

## Overview

This document records all contract additions made during the Truthmap Remediation Phase to bring the existing implemented features into full contract coverage.

---

## Additions to `docs/contracts/API_CONTRACT.md`

### Phase 7 — Rotation & Leave Workflow

Added full contract definitions for:

| Endpoint Group | Endpoints Added | Notes |
|---------------|----------------|-------|
| Auth Profile | `/api/auth/profile/` declared canonical; `/api/auth/me/` described as richer management payload | Clarifies MISMATCH-004 |
| Auth extras | `POST /api/auth/change-password/`, `POST /api/auth/password-reset/`, `POST /api/auth/password-reset/confirm/` | Were missing |
| Rotation CRUD | `GET/POST /api/rotations/`, `GET/PATCH/DELETE /api/rotations/{id}/` | Were missing |
| Rotation workflow | `POST /api/rotations/{id}/submit/`, `hod-approve/`, `utrmc-approve/`, `activate/`, `complete/`, `returned/`, `reject/` | Were missing |
| My Rotations | `GET /api/my/rotations/` | Was missing |
| Supervisor Rotations | `GET /api/supervisor/rotations/pending/` | Was missing |
| UTRMC Approval Inboxes | `GET /api/utrmc/approvals/rotations/`, `GET /api/utrmc/approvals/leaves/` | Were missing |
| Leave CRUD | `GET/POST /api/leaves/`, `GET/PATCH/DELETE /api/leaves/{id}/` | Were missing |
| Leave workflow | `POST /api/leaves/{id}/submit/`, `approve/`, `reject/` | Were missing |
| My Leaves | `GET /api/my/leaves/` | Was missing |
| Deputation Postings | Full CRUD + approve/reject/complete actions | Were missing |

### Phase 8 — Summary & Reporting

Added:

| Endpoint | Description |
|----------|-------------|
| `GET /api/residents/me/summary/` | Resident dashboard summary |
| `GET /api/supervisors/me/summary/` | Supervisor dashboard summary |
| `GET /api/supervisors/residents/{id}/progress/` | Resident progress snapshot for supervisor |
| `GET /api/audit/reports/` | Audit log reports (admin only) |

---

## Updates to `docs/integration/MISSING_IMPLEMENTATIONS.md`

- Corrected false positives: thesis and workshop pages already exist
- Reclassified 3 backend-only features as low-priority deferred items
- Added section documenting all Phase 7–8 contract additions

---

## Code Changes for MISMATCH-003

### `frontend/lib/api/users.ts`
Added:
```typescript
export interface SupervisorUser { id: number; username: string; full_name?: string; email?: string; }

usersApi.getSupervisors(): Promise<SupervisorUser[]>
// Calls GET /api/users/?role=supervisor
```

### `frontend/lib/api/training.ts`
Added:
```typescript
trainingApi.patchResearchFile(file: File): Promise<ResidentResearchProject>
// Calls PATCH /api/my/research/ with multipart/form-data
```

### `frontend/app/dashboard/resident/research/page.tsx`
- Replaced `import apiClient from '@/lib/api/client'` with `import { usersApi } from '@/lib/api/users'`
- Replaced raw `apiClient.get('/api/users/?role=supervisor')` with `usersApi.getSupervisors()`
- Replaced raw `apiClient.patch('/api/my/research/', fd, ...)` with `trainingApi.patchResearchFile(file)`

---

## Contract Completeness Check

| Module | Contract Section | Backend | API Client | Frontend Page |
|--------|-----------------|---------|-----------|--------------|
| Auth | Phase 1 | ✅ | `auth.ts` | `/login` `/register` |
| Hospitals | Phase 2 | ✅ | `userbase.ts` | `/utrmc/hospitals` |
| Departments | Phase 2 | ✅ | `userbase.ts` | `/utrmc/departments` |
| Users | Phase 3 | ✅ | `userbase.ts` | `/utrmc/users` |
| Supervision | Phase 3 | ✅ | `userbase.ts` | `/utrmc/supervision` |
| Logbook | Phase 4 | ✅ | (existing) | (existing) |
| Analytics | Phase 5 | ✅ | `analytics.ts` | `/utrmc/analytics` |
| Programs | Phase 6 | ✅ | `training.ts` | `/utrmc/programs` |
| Research | Phase 6 | ✅ | `training.ts` | `/resident/research` |
| Thesis | Phase 6 | ✅ | `training.ts` | `/resident/thesis` |
| Workshops | Phase 6 | ✅ | `training.ts` | `/resident/workshops` |
| Eligibility | Phase 6 | ✅ | `training.ts` | `/utrmc/eligibility` |
| Rotations | Phase 7 (NEW) | ✅ | partial `training.ts` | TBD — see note |
| Leaves | Phase 7 (NEW) | ✅ | partial | TBD |
| Summaries | Phase 8 (NEW) | ✅ | `training.ts` | Dashboard widgets |
| Audit Reports | Phase 8 (NEW) | ✅ | `audit.ts` | `/utrmc/audit` |

> **Note on Rotations/Leaves pages:** The training.ts API client has `getMyRotations`, `getRotations`, `createRotation`, `listLeaves`, `createLeaveRequest` methods defined. Whether dedicated frontend pages exist for these was not confirmed during this phase; this should be verified in a future sprint.
