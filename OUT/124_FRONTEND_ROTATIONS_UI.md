# OUT/124 — Frontend Rotations UI

Generated: 2026-03-01

## Summary
14 new pages were created for the Training Programs / Rotations Engine module.
All pages use same-origin `/api/` calls (Caddy proxy — no hardcoded domain).

---

## Navigation (navRegistry.ts additions)

### UTRMC Admin section — "Training Admin"
| Label | Route | API |
|-------|-------|-----|
| Training Programs | `/dashboard/utrmc/programs` | GET/POST `/api/programs/` |
| Rotation Templates | `/dashboard/utrmc/program-templates` | GET/POST `/api/program-templates/` |
| Resident Training | `/dashboard/utrmc/resident-training` | GET/POST `/api/resident-training/` |
| Rotations | `/dashboard/utrmc/rotations` | GET/POST `/api/rotations/` |
| Approvals (Rotations) | `/dashboard/utrmc/approvals/rotations` | GET `/api/utrmc/approvals/rotations/` |
| Approvals (Leaves) | `/dashboard/utrmc/approvals/leaves` | GET `/api/utrmc/approvals/leaves/` |
| Leaves | `/dashboard/utrmc/leaves` | GET `/api/leaves/` |
| Postings | `/dashboard/utrmc/postings` | GET `/api/postings/` |

### Supervisor section
| Label | Route | API |
|-------|-------|-----|
| Approvals Inbox | `/dashboard/supervisor/approvals` | GET `/api/utrmc/approvals/leaves/` |
| Rotations | `/dashboard/supervisor/rotations` | GET `/api/rotations/` |

### Resident section
| Label | Route | API |
|-------|-------|-----|
| My Training Schedule | `/dashboard/my-training` | GET `/api/my/rotations/` |
| My Leaves | `/dashboard/my-leaves` | GET `/api/my/leaves/` |
| My Postings | `/dashboard/my-postings` | GET `/api/postings/` |

---

## Page Inventory

### A) Programs CRUD (`/dashboard/utrmc/programs/page.tsx`)
- Lists all training programs with name/code/duration/status columns
- Create form: name, code, duration_months, active toggle
- RBAC: utrmc_admin, admin only

### B) Rotation Templates CRUD (`/dashboard/utrmc/program-templates/page.tsx`)
- Lists templates with program/department/duration/required columns
- Create form with department dropdown (loaded from `/api/departments/`)
- RBAC: utrmc_admin, admin only

### C) Resident Training Records (`/dashboard/utrmc/resident-training/page.tsx`)
- Lists all resident enrollments with resident name/program/start date
- Create form: select resident + program + start date
- RBAC: utrmc_admin, admin; residents see own record only

### D) Rotations Global List + Actions (`/dashboard/utrmc/rotations/page.tsx`)
- Most complex page: filterable table with status filters
- Inline action buttons: Submit / HOD Approve / UTRMC Approve / Return / Reject / Complete
- Create form: resident training record + hospital department + dates
- Overlap validation displayed as error toast
- Status pills with color coding
- RBAC: utrmc_admin/admin full; supervisor sees dept scope; resident read-only

### E) Approvals Inbox — Rotations (`/dashboard/utrmc/approvals/rotations/page.tsx`)
- Shows SUBMITTED + APPROVED rotations pending final approval
- One-click Approve/Return/Reject with confirmation modal
- RBAC: utrmc_admin/admin

### F) Approvals Inbox — Leaves (`/dashboard/utrmc/approvals/leaves/page.tsx`)
- Lists SUBMITTED leaves awaiting action
- Approve/Reject buttons
- RBAC: utrmc_admin, admin, supervisor

### G) Leaves Management (`/dashboard/utrmc/leaves/page.tsx`)
- Table with leave type, dates, status, reason
- Submit/Approve/Reject inline actions
- RBAC: utrmc_admin/admin see all; resident sees own

### H) Postings Management (`/dashboard/utrmc/postings/page.tsx`)
- Deputation/off-service postings table
- Approve/Reject/Complete actions
- RBAC: utrmc_admin/admin see all; resident sees own

### I) Supervisor Approvals (`/dashboard/supervisor/approvals/page.tsx`)
- Approval inbox for leave requests within supervisor's scope
- RBAC: supervisor, faculty

### J) Supervisor Rotations (`/dashboard/supervisor/rotations/page.tsx`)
- Shows rotations in supervisor's department scope
- HOD-approve action
- RBAC: supervisor, faculty

### K) Resident My Training (`/dashboard/my-training/page.tsx`)
- Timeline/list of own rotation schedule
- Status badges: DRAFT / SUBMITTED / APPROVED / ACTIVE / COMPLETED
- Read-only for resident
- RBAC: pg/resident only

### L) Resident My Leaves (`/dashboard/my-leaves/page.tsx`)
- List of own leave requests
- Create new leave + submit action
- RBAC: pg/resident only

### M) Resident My Postings (`/dashboard/my-postings/page.tsx`)
- List of own postings/deputation
- Create + submit
- RBAC: pg/resident only

---

## Data Admin Import Pages (Phase 4)

| Page | Route | API |
|------|-------|-----|
| Import Training Programs | `/dashboard/utrmc/data-admin/training-programs` | POST `/api/bulk/import/training-programs/{action}/` |
| Import Rotation Templates | `/dashboard/utrmc/data-admin/rotation-templates` | POST `/api/bulk/import/rotation-templates/{action}/` |
| Import Resident Training Records | `/dashboard/utrmc/data-admin/resident-training-records` | POST `/api/bulk/import/resident-training-records/{action}/` |

---

## CSV Templates Available
- `/templates/training_programs.csv`
- `/templates/rotation_templates.csv`
- `/templates/resident_training_records.csv`

---

## UX Patterns Used
- Status pills with color mapping (DRAFT=gray, SUBMITTED=blue, APPROVED=green, ACTIVE=teal, COMPLETED=purple, RETURNED=yellow, REJECTED=red)
- Confirm modals before approve/reject/return actions
- Inline validation error display
- Pagination support via `?page=N`
- Role-based tab/button visibility
