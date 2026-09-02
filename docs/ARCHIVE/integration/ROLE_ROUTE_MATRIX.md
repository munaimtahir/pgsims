# Role → Route Matrix

**Generated:** 2026-03-07  
**Source:** `docs/contracts/ROUTES.md`, frontend route structure, RBAC analysis

---

## Route Accessibility by Role

### Public Routes (No Authentication Required)

| Route | Page | admin | utrmc_admin | utrmc_user | supervisor | pg |
|-------|------|-------|-------------|------------|------------|----|
| `/` | Home / Redirect | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/login` | Login | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/register` | Register | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/forgot-password` | Password reset | ✓ | ✓ | ✓ | ✓ | ✓ |
| `/unauthorized` | Access denied | ✓ | ✓ | ✓ | ✓ | ✓ |

---

### PG / Resident Routes (`/dashboard/pg`, `/dashboard/resident`)

| Route | Page | admin | utrmc_admin | utrmc_user | supervisor | pg |
|-------|------|-------|-------------|------------|------------|----|
| `/dashboard/pg` | PG dashboard | ✗ | ✗ | ✗ | ✗ | ✓ |
| `/dashboard/resident` | Resident dashboard | ✗ | ✗ | ✗ | ✗ | ✓ |
| `/dashboard/resident/schedule` | Rotation schedule | ✗ | ✗ | ✗ | ✗ | ✓ |
| `/dashboard/resident/research` | Research project | ✗ | ✗ | ✗ | ✗ | ✓ |
| `/dashboard/pg/eligibility` | Eligibility check | ✗ | ✗ | ✗ | ✗ | ✓ |

---

### Supervisor Routes (`/dashboard/supervisor`)

| Route | Page | admin | utrmc_admin | utrmc_user | supervisor | pg |
|-------|------|-------|-------------|------------|------------|----|
| `/dashboard/supervisor` | Supervisor dashboard | ✗ | ✗ | ✗ | ✓ | ✗ |
| `/dashboard/supervisor/residents` | Assigned residents | ✗ | ✗ | ✗ | ✓ | ✗ |
| `/dashboard/supervisor/residents/{id}/progress` | Resident progress | ✗ | ✗ | ✗ | ✓ | ✗ |

---

### UTRMC Routes (`/dashboard/utrmc`)

| Route | Page | admin | utrmc_admin | utrmc_user | supervisor | pg |
|-------|------|-------|-------------|------------|------------|----|
| `/dashboard/utrmc` | UTRMC dashboard | ✓ | ✓ | ✓ | ✗ | ✗ |
| `/dashboard/utrmc/hospitals` | Hospital management | ✓ | view-only | view-only | ✗ | ✗ |
| `/dashboard/utrmc/departments` | Department management | ✓ | view-only | view-only | ✗ | ✗ |
| `/dashboard/utrmc/matrix` | Hospital-Dept matrix | ✓ | ✓ | view-only | ✗ | ✗ |
| `/dashboard/utrmc/users` | User management | ✓ | ✓ | view-only | ✗ | ✗ |
| `/dashboard/utrmc/supervision` | Supervision links | ✓ | ✓ | view-only | ✗ | ✗ |
| `/dashboard/utrmc/hod` | HOD assignments | ✓ | ✓ | view-only | ✗ | ✗ |
| `/dashboard/utrmc/programs` | Training programs | ✓ | ✓ | view-only | ✗ | ✗ |
| `/dashboard/utrmc/eligibility` | Eligibility matrix | ✓ | ✓ | ✓ | ✗ | ✗ |
| `/dashboard/utrmc/roster` | Dept roster | ✓ | ✓ | ✓ | ✓ | ✗ |
| `/dashboard/utrmc/bulk` | Bulk import/export | ✓ | ✓ | export-only | ✗ | ✗ |

---

### Admin-Only Routes

| Route | Page | admin | utrmc_admin | utrmc_user | supervisor | pg |
|-------|------|-------|-------------|------------|------------|----|
| `/dashboard/admin/audit` | Audit logs | ✓ | ✗ | ✗ | ✗ | ✗ |

---

## Route Guard Implementation

Frontend route guards are implemented via the authentication middleware / layout components. Routes are protected using role checks from the JWT token payload.

### Role-to-Dashboard Redirect

When a user logs in, they are redirected based on their role:

| Role | Default Redirect |
|------|-----------------|
| `admin` | `/dashboard/utrmc` (with full admin capabilities) |
| `utrmc_admin` | `/dashboard/utrmc` |
| `utrmc_user` | `/dashboard/utrmc` |
| `supervisor` | `/dashboard/supervisor` |
| `pg` / `resident` | `/dashboard/pg` or `/dashboard/resident` |

### Protected Route Rules

1. Unauthenticated users accessing any `/dashboard/*` route are redirected to `/login`
2. Authenticated users accessing a route for a different role are redirected to `/unauthorized`
3. The home page `/` redirects to the appropriate dashboard based on role

---

## Action-Level Permissions per Page

### Hospital Management Page

| Action | Button/UI | admin | utrmc_admin | utrmc_user | supervisor | pg |
|--------|-----------|-------|-------------|------------|------------|----|
| View hospital list | Table | ✓ | ✓ | ✓ | ✗ | ✗ |
| Create hospital | "Add Hospital" button | ✓ | ✗ | ✗ | ✗ | ✗ |
| Edit hospital | Edit button | ✓ | ✗ | ✗ | ✗ | ✗ |
| Delete hospital | Delete button | ✓ | ✗ | ✗ | ✗ | ✗ |

### Department Management Page

| Action | Button/UI | admin | utrmc_admin | utrmc_user | supervisor | pg |
|--------|-----------|-------|-------------|------------|------------|----|
| View dept list | Table | ✓ | ✓ | ✓ | ✗ | ✗ |
| Create dept | "Add Dept" button | ✓ | ✗ | ✗ | ✗ | ✗ |
| Edit dept | Edit button | ✓ | ✗ | ✗ | ✗ | ✗ |
| Delete dept | Delete button | ✓ | ✗ | ✗ | ✗ | ✗ |

### Rotation Workflow Page

| Action | Button/UI | admin | utrmc_admin | utrmc_user | supervisor | pg |
|--------|-----------|-------|-------------|------------|------------|----|
| Submit rotation | Submit button | ✗ | ✗ | ✗ | ✗ | ✓ |
| HOD approve | Approve button | ✓ | ✓ | ✗ | ✗ | ✗ |
| UTRMC approve | UTRMC approve | ✓ | ✓ | ✗ | ✗ | ✗ |
| Return rotation | Return button | ✓ | ✓ | ✗ | ✗ | ✗ |
| Reject rotation | Reject button | ✓ | ✓ | ✗ | ✗ | ✗ |
| Activate rotation | Activate button | ✓ | ✓ | ✗ | ✗ | ✗ |
