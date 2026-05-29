# PGSIMS Frontend - Complete Documentation Index

This directory contains comprehensive documentation of the Next.js frontend application for the Postgraduate Student Information Management System (PGSIMS).

## 📋 Documentation Files

### 1. **FRONTEND_SUMMARY.txt** (START HERE)
   - Executive overview of the entire frontend
   - Technology stack and architecture
   - Key statistics and feature breakdown
   - Best for: Getting oriented with the overall structure

### 2. **FRONTEND_API_MAP.md** (DETAILED REFERENCE)
   - Complete API endpoint mapping (84+ endpoints)
   - Grouped by domain (Auth, Training, Users, Notifications, etc.)
   - Page-to-API dependencies
   - Service layer structure
   - Type definitions
   - Best for: Understanding specific API calls and their usage

### 3. **FRONTEND_QUICK_REFERENCE.txt** (LOOKUP GUIDE)
   - Organized reference tables
   - Endpoint summaries by domain
   - Pages by role
   - Type definitions
   - Code examples
   - Best for: Quick lookups and copy-paste references

## 🗂️ Directory Structure at a Glance

```
frontend/
├── app/                    # Next.js pages and routes
│   ├── api/               # API proxy
│   ├── dashboard/         # Role-based dashboards
│   └── [auth pages]
├── lib/
│   ├── api/               # API service modules (11 files)
│   ├── auth/              # Auth utilities
│   └── [utilities]
├── components/            # Reusable React components
├── store/                 # Zustand state management
└── types/                 # TypeScript definitions
```

## 🔑 Key Numbers

| Metric | Count |
|--------|-------|
| API Endpoints | 84+ |
| Service Modules | 11 |
| Pages with API calls | 27 |
| User Roles | 7 |
| TypeScript Source Files | 50+ |
| Lines in lib/api/ | 2,000+ |

## 🚀 Quick Start

### Authentication
- **File**: `lib/api/auth.ts`
- **Main function**: `authApi.login(credentials)` → POST `/api/auth/login/`
- **State**: Stored in localStorage + Zustand + cookies
- **Auto-refresh**: Triggers on 401 response

### Most Used Endpoints
1. **GET /api/residents/me/summary/** - Resident dashboard data
2. **GET /api/supervisors/me/summary/** - Supervisor dashboard data
3. **GET /api/users/** - User listings (with role filtering)
4. **GET /api/my/research/** - Research project data
5. **GET /api/programs/** - Training programs list

### Protected Routes
- **Wrapper**: `components/auth/ProtectedRoute.tsx`
- **Store**: `store/authStore.ts` (Zustand)
- **RBAC**: `lib/rbac.ts` with `getDashboardPathForRole()`

## 👥 Roles & Dashboards

| Role | Endpoint | Key Features |
|------|----------|--------------|
| resident / pg | `/dashboard/resident` | Research, thesis, workshops, eligibility |
| supervisor / faculty | `/dashboard/supervisor` | Approve research, track residents |
| utrmc_admin / utrmc_user | `/dashboard/utrmc` | User mgmt, programs, hospitals |
| admin | `/dashboard/utrmc` | Full system access |

## 📡 API Organization

### By Domain
- **Auth** (8 endpoints) - Login, token refresh, password reset
- **Training** (28 endpoints) - Programs, research, thesis, workshops, eligibility
- **Users & Departments** (20 endpoints) - CRUD for users, departments, hospitals
- **Notifications** (5 endpoints) - Notification management
- **Bulk Operations** (8 endpoints) - Import/export
- **Audit** (3 endpoints) - Logging and reports

### By Service Module
- `lib/api/auth.ts` - Authentication
- `lib/api/training.ts` - Academic programs, research, thesis, workshops
- `lib/api/userbase.ts` - User management, departments, hospitals
- `lib/api/notifications.ts` - Notifications
- `lib/api/bulk.ts` - Bulk import/export
- `lib/api/audit.ts` - Audit logs
- `lib/api/users.ts` - User queries
- `lib/api/departments.ts`, `hospitals.ts` - Legacy endpoints

## 🔐 Authentication Details

**Login Flow**:
```
POST /api/auth/login/ → { user, access, refresh }
  ↓
Store in localStorage + Zustand + cookies
  ↓
Add "Bearer {access}" to all requests
  ↓
On 401: POST /api/auth/refresh/ → { access }
  ↓
Retry original request
```

**Token Storage**:
- localStorage: `access_token`, `refresh_token`, `user`, `auth-storage`
- Cookies: `pgsims_access_token`, `pgsims_access_exp`, `pgsims_user_role`

## 📊 Page Breakdown

### Resident Pages (6)
1. Dashboard - Summary with eligibility
2. Research - Project management
3. Thesis - Submission tracking
4. Workshops - Completion recording
5. Schedule - Rotations and leaves
6. Progress - Info display

### Supervisor Pages (3)
1. Dashboard - Pending approvals
2. Research Approvals - Project approval workflow
3. Resident Progress - Progress tracking

### UTRMC Admin Pages (10)
1. Overview - System stats
2. Users - User CRUD
3. Hospitals - Hospital CRUD
4. Departments - Department CRUD
5. Department Roster - Member viewing
6. Programs - Program configuration
7. Matrix - Hospital-department mapping
8. Supervision - Supervision links
9. HOD - HOD assignments
10. Eligibility - Resident eligibility monitoring

## 💾 State Management

**Auth (Zustand with persistence)**:
- `user`: Current logged-in user
- `accessToken`: JWT access token
- `refreshToken`: JWT refresh token
- `isAuthenticated`: Login status
- `hasHydrated`: Hydration flag for SSR

**UI (React hooks)**:
- Loading states
- Form data
- Error/success messages
- Modal/panel visibility

## 📝 Type Definitions

Key types in `types/index.ts` and `lib/api/training.ts`:
- `User` - User profile with roles
- `ResidentSummary` - Dashboard data for residents
- `SupervisorSummary` - Dashboard data for supervisors
- `TrainingProgram` - Academic program
- `ResidentResearchProject` - Research project
- `ResidentThesis` - Thesis submission
- `WorkshopCompletion` - Workshop attendance
- `MilestoneEligibility` - Eligibility status

## 🔧 Configuration

**Environment Variables**:
- `NEXT_PUBLIC_API_URL` - Client-side API base (optional)
- `SERVER_API_URL` - Server-side API base (optional)
- `INTERNAL_API_URL` - API proxy backend (optional)

All default to same-origin or http://backend:8014

## 🎯 Common Patterns

### API Service Pattern
```typescript
// lib/api/[domain].ts
import apiClient from './client';

export const [domain]Api = {
  async functionName(params): Promise<Type> {
    const response = await apiClient.get('/api/endpoint/', { params });
    return response.data;
  },
};
```

### Protected Page Pattern
```typescript
// app/dashboard/[role]/page.tsx
'use client';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

export default function Page() {
  return (
    <ProtectedRoute allowedRoles={['resident']}>
      {/* Page content */}
    </ProtectedRoute>
  );
}
```

### File Upload Pattern
```typescript
const fd = new FormData();
fd.append('file_field', file);
await apiClient.patch('/api/endpoint/', fd, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
```

## 📈 Development Notes

**Frontend URL**: http://localhost:3000 (dev)
**Backend URL**: http://backend:8014
**API Proxy**: /api/[...path] → backend:/api/[...path]

**Tech Stack**:
- Next.js 14+
- React 18+
- TypeScript
- Axios for HTTP
- Zustand for state
- Tailwind CSS for styling

## 🔗 Related Documentation

- Backend API: See backend Django documentation
- Database: See database schema documentation
- Deployment: See deployment/Docker documentation

## 📞 Quick Reference

**Need to**... | **File** | **Function**
---|---|---
Find an API call | `lib/api/` | Search by endpoint name
Add a new page | `app/dashboard/[role]/` | Create page.tsx with ProtectedRoute
Handle auth | `store/authStore.ts` | Use `useAuthStore()` hook
Manage tokens | `lib/auth/cookies.ts` | See token sync logic
See RBAC rules | `lib/rbac.ts` | Check `getDashboardPathForRole()`
Add new endpoint | `lib/api/[domain].ts` | Create new service function

---

**Generated**: March 2024
**Scope**: Complete frontend API mapping and architecture documentation
**Files**: 50+ TypeScript source files across lib/api/, app/, components/, store/
