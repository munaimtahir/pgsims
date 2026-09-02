# Role Permission Model

## System Roles

PGSIMS defines five primary roles plus the superuser. Roles are stored in the `User.role` field.

| Role Code | Display Name | Description |
|-----------|-------------|-------------|
| `admin` | System Administrator | Full system access including technical operations |
| `utrmc_admin` | UTRMC Administrator | Administrative oversight and approvals |
| `utrmc_user` | UTRMC Staff | Read-only administrative visibility |
| `supervisor` | Supervisor | Clinical supervisor with assigned resident oversight |
| `pg` | Postgraduate Trainee | The resident/trainee under training |
| `resident` | Resident | Alias for pg in some contexts |

---

## Permission Helper Classes

Backend permission classes that implement the role model:

| Class / Helper | Logic | Used On |
|----------------|-------|---------|
| `IsTechAdmin` | `role == "admin" AND is_staff` | Hospital/Department write operations |
| `IsManager` | `role in ["admin", "utrmc_admin"]` | Org graph management |
| `IsAdminUser` (DRF) | `is_staff == True` | Audit logs |
| `_is_admin_or_utrmc_admin()` | `role in ["admin", "utrmc_admin"]` | Training program write |
| `IsAuthenticated` | Valid JWT token | Most read operations |

---

## Endpoint Permission Matrix

### Authentication Endpoints (`/api/auth/`)

| Endpoint | Method | admin | utrmc_admin | utrmc_user | supervisor | pg |
|----------|--------|-------|-------------|------------|------------|----|
| `/api/auth/login/` | POST | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/auth/register/` | POST | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/auth/logout/` | POST | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/auth/profile/` | GET | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/auth/profile/update/` | PATCH | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/auth/me/` | GET | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/auth/refresh/` | POST | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/auth/change-password/` | POST | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/auth/password-reset/` | POST | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/auth/password-reset/confirm/` | POST | ✓ | ✓ | ✓ | ✓ | ✓ |

### Organisation Graph (`/api/hospitals/`, `/api/departments/`, etc.)

| Endpoint | Method | admin | utrmc_admin | utrmc_user | supervisor | pg |
|----------|--------|-------|-------------|------------|------------|----|
| `/api/hospitals/` | GET | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/hospitals/` | POST | ✓ | ✗ | ✗ | ✗ | ✗ |
| `/api/hospitals/{id}/` | PATCH | ✓ | ✗ | ✗ | ✗ | ✗ |
| `/api/hospitals/{id}/` | DELETE | ✓ | ✗ | ✗ | ✗ | ✗ |
| `/api/hospitals/{id}/departments/` | GET | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/departments/` | GET | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/departments/` | POST | ✓ | ✗ | ✗ | ✗ | ✗ |
| `/api/departments/{id}/` | PATCH | ✓ | ✗ | ✗ | ✗ | ✗ |
| `/api/departments/{id}/roster/` | GET | ✓ | ✓ | ✓ | ✓ | ✗ |
| `/api/hospital-departments/` | GET | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/hospital-departments/` | POST/DELETE | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/supervision-links/` | GET/POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/hod-assignments/` | GET/POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/department-memberships/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/hospital-assignments/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |

### User Management (`/api/users/`)

| Endpoint | Method | admin | utrmc_admin | utrmc_user | supervisor | pg |
|----------|--------|-------|-------------|------------|------------|----|
| `/api/users/` | GET | ✓ | ✓ | ✓ | ✓ | ✗ |
| `/api/users/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/users/{id}/` | PATCH | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/users/assigned-pgs/` | GET | ✗ | ✗ | ✗ | ✓ | ✗ |
| `/api/residents/` | GET | ✓ | ✓ | ✓ | ✓ | ✗ |
| `/api/staff/` | GET | ✓ | ✓ | ✓ | ✗ | ✗ |

### Training Programs (`/api/programs/`)

| Endpoint | Method | admin | utrmc_admin | utrmc_user | supervisor | pg |
|----------|--------|-------|-------------|------------|------------|----|
| `/api/programs/` | GET | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/programs/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/programs/{id}/` | PUT/PATCH | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/programs/{id}/policy/` | GET | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/programs/{id}/policy/` | PUT | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/programs/{id}/milestones/` | GET | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/programs/{id}/milestones/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |

### Rotations (`/api/rotations/`)

| Endpoint | Method | admin | utrmc_admin | utrmc_user | supervisor | pg |
|----------|--------|-------|-------------|------------|------------|----|
| `/api/rotations/` | GET | ✓ | ✓ | ✓ | ✓(assigned) | ✓(own) |
| `/api/rotations/` | POST | ✓ | ✓ | ✗ | ✗ | ✓ |
| `/api/rotations/{id}/submit/` | POST | ✗ | ✗ | ✗ | ✗ | ✓ |
| `/api/rotations/{id}/hod-approve/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/rotations/{id}/utrmc-approve/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/rotations/{id}/activate/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/rotations/{id}/complete/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/rotations/{id}/returned/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/rotations/{id}/reject/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/my/rotations/` | GET | ✗ | ✗ | ✗ | ✗ | ✓ |
| `/api/utrmc/approvals/rotations/` | GET | ✓ | ✓ | ✓ | ✗ | ✗ |
| `/api/supervisor/rotations/pending/` | GET | ✗ | ✗ | ✗ | ✓ | ✗ |

### Leaves (`/api/leaves/`)

| Endpoint | Method | admin | utrmc_admin | utrmc_user | supervisor | pg |
|----------|--------|-------|-------------|------------|------------|----|
| `/api/leaves/` | GET/POST | ✓ | ✓ | ✓ | ✓(assigned) | ✓(own) |
| `/api/leaves/{id}/submit/` | POST | ✗ | ✗ | ✗ | ✗ | ✓ |
| `/api/leaves/{id}/approve/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/leaves/{id}/reject/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/my/leaves/` | GET | ✗ | ✗ | ✗ | ✗ | ✓ |
| `/api/utrmc/approvals/leaves/` | GET | ✓ | ✓ | ✓ | ✗ | ✗ |

### Research, Thesis, Workshops, Eligibility (Resident-only)

| Endpoint | Method | admin | utrmc_admin | utrmc_user | supervisor | pg |
|----------|--------|-------|-------------|------------|------------|----|
| `/api/my/research/` | GET/POST/PATCH | ✗ | ✗ | ✗ | ✗ | ✓ |
| `/api/my/research/action/{action}/` | POST | ✗ | ✗ | ✗ | ✗ | ✓ |
| `/api/supervisor/research-approvals/` | GET | ✗ | ✗ | ✗ | ✓ | ✗ |
| `/api/my/thesis/` | GET/POST | ✗ | ✗ | ✗ | ✗ | ✓ |
| `/api/my/thesis/submit/` | POST | ✗ | ✗ | ✗ | ✗ | ✓ |
| `/api/my/workshops/` | GET/POST | ✗ | ✗ | ✗ | ✗ | ✓ |
| `/api/my/eligibility/` | GET | ✗ | ✗ | ✗ | ✗ | ✓ |
| `/api/utrmc/eligibility/` | GET | ✓ | ✓ | ✓ | ✗ | ✗ |

### Notifications (`/api/notifications/`)

| Endpoint | Method | admin | utrmc_admin | utrmc_user | supervisor | pg |
|----------|--------|-------|-------------|------------|------------|----|
| `/api/notifications/` | GET | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/notifications/unread-count/` | GET | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/notifications/mark-read/` | POST | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/api/notifications/preferences/` | GET/PATCH | ✓ | ✓ | ✓ | ✓ | ✓ |

### Audit (`/api/audit/`)

| Endpoint | Method | admin | utrmc_admin | utrmc_user | supervisor | pg |
|----------|--------|-------|-------------|------------|------------|----|
| `/api/audit/activity/` | GET | ✓ | ✗ | ✗ | ✗ | ✗ |
| `/api/audit/reports/` | GET/POST | ✓ | ✗ | ✗ | ✗ | ✗ |

### Bulk Operations (`/api/bulk/`)

| Endpoint | Method | admin | utrmc_admin | utrmc_user | supervisor | pg |
|----------|--------|-------|-------------|------------|------------|----|
| `/api/bulk/import/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/bulk/assignment/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/bulk/review/` | POST | ✓ | ✓ | ✗ | ✗ | ✗ |
| `/api/bulk/exports/{resource}/` | GET | ✓ | ✓ | ✓ | ✗ | ✗ |

---

## UI Visibility Rules

| UI Area | admin | utrmc_admin | utrmc_user | supervisor | pg |
|---------|-------|-------------|------------|------------|----|
| Dashboard (role-specific) | /dashboard | /dashboard/utrmc | /dashboard/utrmc | /dashboard/supervisor | /dashboard/pg |
| Hospital/Dept management | ✓ | ✗ | ✗ | ✗ | ✗ |
| User management | ✓ | ✓ | ✗ | ✗ | ✗ |
| Training programs config | ✓ | ✓ | ✗ | ✗ | ✗ |
| Rotation approvals inbox | ✓ | ✓ | view-only | ✗ | ✗ |
| Supervision assignment | ✓ | ✓ | ✗ | ✗ | ✗ |
| My rotations/leaves | ✗ | ✗ | ✗ | ✗ | ✓ |
| Assigned residents view | ✗ | ✗ | ✗ | ✓ | ✗ |
| Research/Thesis/Workshop | ✗ | ✗ | ✗ | ✗ | ✓ |
| Eligibility matrix | ✓ | ✓ | ✓ | ✗ | view-own |
| Audit logs | ✓ | ✗ | ✗ | ✗ | ✗ |
| Bulk import/export | ✓ | ✓ | view-only | ✗ | ✗ |
