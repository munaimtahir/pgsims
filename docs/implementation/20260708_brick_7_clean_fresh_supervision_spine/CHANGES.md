# CHANGES — PGMS Brick 7 Clean Fresh Pilot Supervision Spine

This document records the exact file and architectural changes made in the backend for **Brick 7**.

---

## 1. Registered Django App

- **`backend/sims_project/settings.py`**:
  - Registered the new `"sims.supervision"` app in `INSTALLED_APPS`.
- **`backend/sims_project/urls.py`**:
  - Registered path `path("api/supervision/", include("sims.supervision.urls")),`.

---

## 2. Models Created

- **`ResidentSupervisorAssignment`** (in `backend/sims/supervision/models.py`):
  - Primary key `id`.
  - `resident` (ForeignKey to `ResidentProfile`).
  - `supervisor` (ForeignKey to `SupervisorProfile`).
  - `assignment_type` (Choices: `PRIMARY`, `CO_SUPERVISOR`).
  - `start_date` (DateField).
  - `end_date` (DateField, null/blank).
  - `status` (Choices: `ACTIVE`, `ENDED`, `SUSPENDED`).
  - `is_active` (BooleanField, convenience query helper).
  - `notes` (TextField).
  - `reason_for_change` (TextField).
  - `created_by`, `updated_by` (ForeignKeys to User).
  - `history` (simple-history audit tracker).
  - Conditional unique database constraint: `unique_active_primary_supervisor` (only one active primary supervisor per resident).
  - Conditional unique database constraint: `unique_active_resident_supervisor_type` (prevent duplicate active supervisor/resident links of the same type).

---

## 3. Business Service Layer

- **`backend/sims/supervision/services.py`**:
  - `validate_supervision_match`: Enforces department matching and hospital matching rules.
  - `create_supervisor_assignment`: Creates a new active mapping and logs it in the system audit trail.
  - `change_primary_supervisor`: Atomically ends the old primary supervisor and creates a new one in a single transaction.
  - `end_supervisor_assignment`: Ends the mapping, records the end date, deactivates the convenience flag, and preserves history.
  - `get_resident_supervision_summary`: Generates structured active and historical summaries for residents.
  - `get_supervisor_resident_summary`: Generates structured active and historical summaries for supervisors.
  - `get_supervision_data_quality`: Computes 15 audit/anomaly categories (mismatches, missing records, load analysis, archived profiles).

---

## 4. API Controllers & Serializers

- **`backend/sims/supervision/serializers.py`**:
  - `ResidentSupervisorAssignmentSerializer`: Handles read/write actions using ID payloads (`resident_id` / `supervisor_id`) and read representation objects.
  - `ResidentSummarySerializer` and `SupervisorSummarySerializer` for lightweight nested models.
- **`backend/sims/supervision/views.py`**:
  - `ResidentSupervisorAssignmentViewSet`: Enforces role-based query filters and endpoints.
  - `/api/supervision/change-primary/`: Rotating/replacing primary supervisor.
  - `/api/supervision/options/`: Form choice helpers list.
  - `/api/supervision/data-quality/`: Admin data-quality analytics dashboard query.
  - `/api/supervision/import/`: Bulk CSV importer with dry-run support.
- **`backend/sims/supervision/permissions.py`**:
  - `IsSupervisionAdminOrReadOnly`: Enforces admin-only writes, allowing read actions for authenticated roles.

---

## 5. Management Commands

- **`seed_pilot_supervision`** (in `backend/sims/supervision/management/commands/seed_pilot_supervision.py`):
  - Idempotent script to seed master data, 3 residents, 2 supervisors, and establish active pilot supervision relationships.

---

## 6. Brick 7.1 Closure

- Added the `/supervision/*` frontend route family:
  - `/supervision`
  - `/supervision/assignments`
  - `/supervision/assignments/new`
  - `/supervision/assignments/[id]`
  - `/supervision/import`
  - `/supervision/data-quality`
- Redirected legacy dashboard supervision pages to the new `/supervision` surfaces.
- Added resident dashboard "My Supervisor" and supervisor dashboard "My Residents" integration using the canonical assignment summary APIs.
- Removed active frontend API helper usage of `SupervisorResidentLink` and routed supervision helpers through `frontend/lib/api/supervision.ts`.
- Updated backend training and bulk compatibility code to use `ResidentSupervisorAssignment` and the `/api/supervision/*` endpoints.
