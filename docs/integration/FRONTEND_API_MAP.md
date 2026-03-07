# PGSIMS FRONTEND - COMPLETE API CALL MAP

## 1. API CONFIGURATION

**Base URL Resolution** (`lib/api/client.ts`):
- **Server-side**: `process.env.SERVER_API_URL || 'http://backend:8014'`
- **Client-side**: `process.env.NEXT_PUBLIC_API_URL` (same-origin by default)
- **Framework**: Axios with interceptors
- **Auth**: Bearer token in Authorization header (from localStorage)
- **Token Refresh**: Auto-refresh on 401 via POST `/api/auth/refresh/`

**API Proxy** (`app/api/[...path]/route.ts`):
- Proxies all requests to backend via `INTERNAL_API_URL`
- Supports: GET, POST, PUT, PATCH, DELETE, OPTIONS

---

## 2. API ENDPOINTS BY DOMAIN

### AUTH ENDPOINTS (`lib/api/auth.ts`)
| Endpoint | Method | Function | Used In |
|----------|--------|----------|---------|
| /api/auth/login/ | POST | login(credentials) | login page |
| /api/auth/register/ | POST | register(data) | (disabled) |
| /api/auth/logout/ | POST | logout() | auth store |
| /api/auth/profile/ | GET | getCurrentUser() | - |
| /api/auth/profile/update/ | PATCH | updateProfile(data) | - |
| /api/auth/password-reset/ | POST | passwordReset(email) | forgot-password page |
| /api/auth/password-reset/confirm/ | POST | passwordResetConfirm(data) | - |
| /api/auth/change-password/ | POST | changePassword(data) | - |
| /api/auth/refresh/ | POST | refreshToken(token) | auto-refresh on 401 |

### TRAINING ENDPOINTS (`lib/api/training.ts`)
| Endpoint | Method | Function | Used In |
|----------|--------|----------|---------|
| /api/programs/ | GET | listPrograms() | utrmc/programs page |
| /api/programs/{id}/ | GET/PUT | getProgram() / updateProgram() | utrmc/programs page |
| /api/programs/{id}/policy/ | GET/PUT | getProgramPolicy() / updateProgramPolicy() | utrmc/programs page |
| /api/programs/{id}/milestones/ | GET/POST | listMilestones() / createMilestone() | utrmc/programs page |
| /api/my/research/ | GET/POST/PATCH | getMyResearch() / createResearch() / patchResearch() | resident/research page |
| /api/my/research/action/{action}/ | POST | researchAction(action) | research page |
| /api/supervisor/research-approvals/ | GET | getSupervisorResearchApprovals() | supervisor/research-approvals page |
| /api/my/thesis/ | GET/POST | getMyThesis() / createThesis() | resident/thesis page |
| /api/my/thesis/submit/ | POST | submitThesis() | resident/thesis page |
| /api/workshops/ | GET | listWorkshops() | resident/workshops page |
| /api/my/workshops/ | GET/POST/DELETE | listMyWorkshopCompletions() / createWorkshopCompletion() / deleteWorkshopCompletion() | resident/workshops page |
| /api/my/eligibility/ | GET | getMyEligibility() | resident dashboard |
| /api/utrmc/eligibility/ | GET | getUTRMCEligibility(params) | utrmc/eligibility-monitoring page |
| /api/residents/me/summary/ | GET | getResidentSummary() | resident pages |
| /api/supervisors/me/summary/ | GET | getSupervisorSummary() | supervisor/page |
| /api/supervisors/residents/{id}/progress/ | GET | getResidentProgress(id) | supervisor/residents/[id]/progress page |
| /api/system/settings/ | GET | getSystemSettings() | - |

### USER MANAGEMENT ENDPOINTS (`lib/api/userbase.ts`)
| Endpoint | Method | Function | Used In |
|----------|--------|----------|---------|
| /api/hospitals/ | GET/POST/PATCH | hotels.list() / create() / update() | utrmc/page, utrmc/hospitals page |
| /api/hospitals/{id}/departments/ | GET | hotels.listDepartments(id) | - |
| /api/departments/ | GET/POST/PATCH | departments.list() / create() / update() | utrmc/page, utrmc/departments page |
| /api/departments/{id}/roster/ | GET | departments.roster(id) | roster pages |
| /api/hospital-departments/ | GET/POST/PATCH | matrix.list() / create() / update() | utrmc/matrix page |
| /api/users/ | GET/POST/PATCH | users.list(params) / create() / update() | resident/research page, utrmc/users page, utrmc/page |
| /api/users/{id}/ | GET | users.get(id) | - |
| /api/users/assigned-pgs/ | GET | getAssignedPGs() | - |
| /api/department-memberships/ | POST/PATCH/DELETE | memberships.create() / update() / remove() | - |
| /api/hospital-assignments/ | POST/PATCH/DELETE | hospitalAssignments.create() / update() / remove() | - |
| /api/supervision-links/ | GET/POST/PATCH | supervisionLinks.list() / create() / update() | utrmc/supervision page |
| /api/hod-assignments/ | GET/POST/PATCH | hodAssignments.list() / create() / update() | utrmc/hod page |

### NOTIFICATIONS ENDPOINTS (`lib/api/notifications.ts`)
| Endpoint | Method | Function | Used In |
|----------|--------|----------|---------|
| /api/notifications/ | GET | list(params) / getUnread() | - |
| /api/notifications/unread-count/ | GET | getUnreadCount() | - |
| /api/notifications/mark-read/ | POST | markRead(id) | - |
| /api/notifications/preferences/ | GET/PATCH | getPreferences() / updatePreferences() | - |

### BULK OPERATIONS ENDPOINTS (`lib/api/bulk.ts`)
| Endpoint | Method | Function | Used In |
|----------|--------|----------|---------|
| /api/bulk/import/ | POST | import(file, type) | - |
| /api/bulk/import-trainees/ | POST | importTrainees(file) | - |
| /api/bulk/import-supervisors/ | POST | importSupervisors(file) | - |
| /api/bulk/import-residents/ | POST | importResidents(file) | - |
| /api/bulk/import-departments/ | POST | importDepartments(file) | - |
| /api/bulk/assignment/ | POST | assignment(data) | - |
| /api/bulk/review/ | POST | review(payload) | - |
| /api/bulk/exports/{resource}/ | GET | exportDataset(resource, format) | - |

### AUDIT ENDPOINTS (`lib/api/audit.ts`)
| Endpoint | Method | Function | Used In |
|----------|--------|----------|---------|
| /api/audit/activity/ | GET | getActivityLogs(params) | - |
| /api/audit/reports/ | GET | getReports(params) | - |
| /api/audit/reports/ | POST | createReport(data) | - |

---

## 3. PAGES & FEATURES

### Public Pages
- `/` - Home (redirects to dashboard)
- `/login` - Login with username/password → POST /api/auth/login/
- `/register` - Registration disabled
- `/forgot-password` - Password reset (not implemented)
- `/unauthorized` - Access denied error page

### Resident Pages (Role: pg, resident)
- `/dashboard/resident` - Dashboard with summary, rotations, eligibility status
  - Fetches: GET /api/residents/me/summary/
- `/dashboard/resident/research` - Research project management
  - Creates/updates research, uploads synopsis (multipart), submits to supervisor/university
- `/dashboard/resident/thesis` - Thesis submission tracking
- `/dashboard/resident/workshops` - Record workshop completions
- `/dashboard/resident/schedule` - View rotations and leave requests
- `/dashboard/resident/progress` - Progress snapshot (if supervisor viewing)

### Supervisor Pages (Role: supervisor, faculty, admin)
- `/dashboard/supervisor` - Dashboard with pending approvals and resident list
  - Fetches: GET /api/supervisors/me/summary/
- `/dashboard/supervisor/research-approvals` - Approve/return research projects
- `/dashboard/supervisor/residents/[id]/progress` - View resident progress

### PG/Faculty Pages (Role: pg)
- `/dashboard/pg/departments/[id]/roster` - Department roster view

### UTRMC Admin Pages (Role: utrmc_user, utrmc_admin, admin)
- `/dashboard/utrmc` - Overview with stats (hospitals, departments, users)
- `/dashboard/utrmc/users` - User management (create, edit, list)
- `/dashboard/utrmc/hospitals` - Hospital management
- `/dashboard/utrmc/departments` - Department management
- `/dashboard/utrmc/departments/[id]/roster` - Department roster with HOD, faculty, supervisors, residents
- `/dashboard/utrmc/programs` - Program management with policies and milestones
- `/dashboard/utrmc/matrix` - Hospital-department matrix
- `/dashboard/utrmc/supervision` - Supervision links management
- `/dashboard/utrmc/hod` - HOD assignments
- `/dashboard/utrmc/eligibility-monitoring` - Filter residents by eligibility status

---

## 4. KEY DATA TYPES

**User Roles**: pg, resident, supervisor, faculty, admin, utrmc_user, utrmc_admin

**Main Objects**:
- **ResidentSummary**: training_record, rotation, schedule, leaves, postings, research, thesis, workshops, eligibility
- **SupervisorSummary**: pending (rotation/leave/research approvals), residents list
- **ResidentProgressSnapshot**: resident info, training record, rotation, research, thesis, workshops, eligibility
- **TrainingProgram**: code, name, degree_type, duration_months
- **ProgramMilestone**: code, name, research_requirement, workshop_requirements
- **ResidentResearchProject**: title, topic_area, supervisor, status, synopsis_file, university_submission_ref
- **ResidentThesis**: status, thesis_file, submitted_at
- **MilestoneEligibility**: milestone, status (ELIGIBLE|PARTIALLY_READY|NOT_READY), reasons

---

## 5. AUTHENTICATION & STATE

**Auth Storage** (`store/authStore.ts` - Zustand):
- Persists to localStorage: access_token, refresh_token, user
- Also synced to cookies: pgsims_access_token, pgsims_access_exp, pgsims_user_role
- Auto-refresh on 401 via POST /api/auth/refresh/
- Redirect to /login on refresh failure

**Route Protection** (`components/auth/ProtectedRoute.tsx`):
- Wraps pages requiring authentication
- Allows role-based access control via allowedRoles prop
- Redirects unauthenticated users to /login
- Redirects to role-specific dashboard if role not allowed

**Role → Dashboard Mapping** (`lib/rbac.ts`):
- admin/utrmc_admin/utrmc_user → /dashboard/utrmc
- supervisor/faculty → /dashboard/supervisor
- pg/resident → /dashboard/resident
- others → /unauthorized

---

## 6. SPECIAL PATTERNS

### File Upload (Research Synopsis)
```typescript
const fd = new FormData();
fd.append('synopsis_file', file);
const r = await apiClient.patch(`/api/my/research/`, fd, { 
  headers: { 'Content-Type': 'multipart/form-data' } 
});
```

### Bulk Import
```typescript
const formData = new FormData();
formData.append('file', file);
formData.append('import_type', importType);
formData.append('dry_run', 'false');
const response = await apiClient.post('/api/bulk/import/', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
```

### Paginated Response Handling
Some endpoints return `{ count, results: [...] }`, others return arrays directly.
Helper in training.ts:
```typescript
function toArray<T>(data: unknown): T[] {
  if (Array.isArray(data)) return data as T[];
  if (data && typeof data === 'object' && 'results' in data) 
    return ((data as { results?: T[] }).results) || [];
  return [];
}
```

---

## 7. SERVICE LAYER STRUCTURE

```
lib/
├── api/
│   ├── client.ts           # Axios instance with auth interceptors
│   ├── auth.ts             # Authentication service
│   ├── training.ts         # Programs, research, thesis, workshops, eligibility
│   ├── userbase.ts         # Users, departments, hospitals, memberships
│   ├── users.ts            # User queries
│   ├── notifications.ts    # Notifications service
│   ├── bulk.ts             # Bulk import/export
│   ├── audit.ts            # Audit logs
│   ├── departments.ts      # Department operations
│   ├── hospitals.ts        # Hospital operations
│   └── index.ts            # Centralized exports
├── auth/
│   └── cookies.ts          # Cookie management for auth tokens
├── rbac.ts                 # Role-based access control
├── utils.ts                # Utilities
└── navRegistry.ts          # Navigation menu structure

components/
├── auth/
│   └── ProtectedRoute.tsx  # Route protection with RBAC
├── layout/
│   ├── DashboardLayout.tsx # Main dashboard layout
│   └── Sidebar.tsx         # Navigation sidebar
└── ui/
    ├── DataTable.tsx       # Generic table component
    ├── ImportExportPanel.tsx # Bulk operations UI
    └── ...other UI components

store/
└── authStore.ts            # Zustand auth state store

types/
└── index.ts                # TypeScript type definitions
```

---

## 8. DIRECT API CALLS IN PAGES

These pages make direct `apiClient` calls (not through service layer):

1. **resident/research/page.tsx** (line 54, 83):
   - GET /api/users/?role=supervisor
   - PATCH /api/my/research/ (file upload)

All other pages use service functions from lib/api/*.ts

---

## 9. ENVIRONMENT VARIABLES

**Frontend (.env)**:
- `NEXT_PUBLIC_API_URL` - Client-side API base URL (optional, defaults to same-origin)
- `SERVER_API_URL` - Server-side API base URL (optional, defaults to http://backend:8014)
- `INTERNAL_API_URL` - For API proxy route (defaults to http://backend:8014)

---

## SUMMARY

- **Total API endpoints**: 60+
- **Service modules**: 11 (auth, training, userbase, users, notifications, bulk, audit, departments, hospitals + index)
- **Pages with API calls**: 27
- **Authentication**: Token-based (JWT) with auto-refresh
- **State management**: Zustand (auth only)
- **HTTP client**: Axios
- **Deployment model**: Next.js frontend proxying to Django backend

