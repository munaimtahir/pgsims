# Database and Auth Audit

## Schema and migrations

- Migration inventory spans active and legacy modules (`backend/sims/**/migrations`).
- `showmigrations --plan` indicates listed migrations are applied.
- Canonical governance model preserved:
  - `academics.Department`
  - `rotations.Hospital`
  - `rotations.HospitalDepartment`

## Model inventory (key active)

- Users: `User` + `ResidentProfile`, `StaffProfile`, memberships/assignments/links.
- Training: programs, templates, training records, rotations, leaves, postings, research, thesis, workshops, eligibility.
- Notifications: `Notification`, `NotificationPreference`.
- Audit/Bulk: activity/report and bulk operation models.

## Data integrity signals

- Drift tests enforce no duplicate Department model drift and no legacy notification create keys.
- Soft-deactivate semantics used in several assignment entities.
- State-machine transitions for rotations/leaves/postings use explicit status gates.

## Auth strategy

- JWT (access + refresh) on backend; frontend interceptor refreshes on 401.
- Session auth also enabled in DRF defaults.

## Authorization/RBAC findings

- Backend enforcement exists and is not only UI-based.
- Manager-level restrictions used for org-management mutations.
- Supervisor/resident scoping applied in querysets for multiple workflows.

## Weak spots

- Endpoint duplication (`/api/auth/me/` and `/api/auth/profile/`) can create contract ambiguity.
- Legacy auth/workflow assumptions in docs/tests can bypass active-route reality.
