# PGSIMS Backend API Quick Reference Guide

## 📊 API Summary
- **Total Endpoints:** 120+
- **ViewSets:** 24 (generating 5-7 endpoints each)
- **Custom @action Endpoints:** 25+
- **Direct APIView Endpoints:** 40+

## 🔐 Authentication

### Get JWT Token
```bash
POST /api/auth/login/
Content-Type: application/json
{
  "username": "user@example.com",
  "password": "password123"
}
# Returns: access, refresh tokens
```

### Refresh Token
```bash
POST /api/auth/refresh/
{
  "refresh": "your_refresh_token"
}
```

### Current User Profile
```bash
GET /api/auth/me/
Authorization: Bearer <access_token>
```

---

## 📋 Main API Groups

### 1. **Authentication** (`/api/auth/`)
- `POST /api/auth/login/` - JWT login
- `POST /api/auth/refresh/` - Refresh token
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/password-reset/` - Request password reset
- `POST /api/auth/change-password/` - Change password
- `GET /api/auth/me/` - Get current user
- `PUT /api/auth/profile/update/` - Update profile

### 2. **Organizational Graph** (`/api/`)
**ViewSets (Full CRUD):**
- `/api/hospitals/` - Hospital management
  - `GET /api/hospitals/{id}/departments/` - Get hospital's departments
- `/api/departments/` - Department management
  - `GET /api/departments/{id}/roster/` - Get department roster
- `/api/hospital-departments/` - Hospital-Department mappings
- `/api/residents/` - Resident profiles
- `/api/staff/` - Staff profiles
- `/api/department-memberships/` - Membership tracking
- `/api/hospital-assignments/` - Hospital assignments
- `/api/supervision-links/` - Supervision relationships
- `/api/hod-assignments/` - HOD assignments

### 3. **Users Extended** (`/api/users/`)
- `/api/users/` - All users (full CRUD)
- `/api/users/assigned-pgs/` - Get supervisor's assigned PGs

### 4. **Training & Rotations** (`/api/`)
**ViewSets:**
- `/api/programs/` - Training programs (admin write)
- `/api/program-templates/` - Rotation templates (admin write)
- `/api/resident-training/` - Training records
- `/api/rotations/` - Rotation assignments (with state machine)
- `/api/leaves/` - Leave requests
- `/api/postings/` - Deputation postings
- `/api/workshops/` - Workshop info (read-only)
- `/api/programs/{id}/milestones/` - Program milestones

**State Machine Actions (Rotations):**
```
DRAFT → SUBMITTED → APPROVED → ACTIVE → COMPLETED
       ↓                    ↓
      RETURNED            REJECTED
```

Endpoints:
- `POST /api/rotations/{id}/submit/` - Submit for approval
- `POST /api/rotations/{id}/hod-approve/` - HOD approval
- `POST /api/rotations/{id}/utrmc-approve/` - UTRMC approval
- `POST /api/rotations/{id}/activate/` - Activate rotation
- `POST /api/rotations/{id}/complete/` - Complete rotation
- `POST /api/rotations/{id}/returned/` - Return for changes
- `POST /api/rotations/{id}/reject/` - Reject rotation

**Leave/Posting Actions:**
- `POST /api/leaves/{id}/submit/` - Submit leave
- `POST /api/leaves/{id}/approve/` - Approve leave
- `POST /api/leaves/{id}/reject/` - Reject leave
- `POST /api/postings/{id}/approve/` - Approve posting
- `POST /api/postings/{id}/reject/` - Reject posting
- `POST /api/postings/{id}/complete/` - Complete posting

**Personal Endpoints:**
- `GET /api/my/rotations/` - My rotations
- `GET /api/my/leaves/` - My leaves
- `GET /api/my/research/` - My research project
- `GET /api/my/thesis/` - My thesis
- `GET /api/my/workshops/` - My workshops
- `GET /api/my/eligibility/` - My eligibility status
- `POST /api/my/thesis/submit/` - Submit thesis
- `POST /api/my/research/action/{action}/` - Research actions

**Approval Inboxes:**
- `GET /api/utrmc/approvals/rotations/` - Pending rotation approvals
- `GET /api/utrmc/approvals/leaves/` - Pending leave approvals
- `GET /api/supervisor/rotations/pending/` - Supervisor pending rotations
- `GET /api/supervisor/research-approvals/` - Supervisor research approvals

**Summary Endpoints:**
- `GET /api/residents/me/summary/` - Resident training summary
- `GET /api/supervisors/me/summary/` - Supervisor overview
- `GET /api/supervisors/residents/{id}/progress/` - Resident progress

### 5. **Audit** (`/api/audit/`)
- `GET /api/audit/activity/` - Activity logs (admin only)
- `GET /api/audit/activity/export/` - Export logs (admin only)
- `GET /api/audit/reports/` - Audit reports (admin only)
- `POST /api/audit/reports/` - Create audit report (admin only)
- `GET /api/audit/reports/latest/` - Latest report (admin only)

### 6. **Bulk Operations** (`/api/bulk/`)
- `POST /api/bulk/import/` - Generic bulk import
- `POST /api/bulk/import-trainees/` - Import trainees
- `POST /api/bulk/import-supervisors/` - Import supervisors
- `POST /api/bulk/import-residents/` - Import residents
- `POST /api/bulk/import-departments/` - Import departments
- `POST /api/bulk/import/{entity}/{action}/` - Unified import
- `POST /api/bulk/assignment/` - Bulk assignment
- `POST /api/bulk/review/` - Review bulk operations
- `GET /api/bulk/exports/{resource}/` - Export resources

### 7. **Notifications** (`/api/notifications/`)
- `GET /api/notifications/` - List notifications (paginated)
- `POST /api/notifications/mark-read/` - Mark as read
- `GET /api/notifications/unread-count/` - Unread count
- `GET /api/notifications/preferences/` - Get preferences
- `PUT /api/notifications/preferences/` - Update preferences

### 8. **Academics** (`/academics/api/`)
- `GET /academics/api/departments/` - List departments
- `GET /academics/api/batches/` - List batches
- `GET /academics/api/students/` - List student profiles
- Full CRUD for authenticated users (departments admin-only write)

### 9. **Analytics** (`/api/analytics/`)
- `GET /api/analytics/trends/` - Trend analytics
- `GET /api/analytics/comparative/` - Comparative analytics
- `GET /api/analytics/performance/` - Performance metrics
- `GET /api/analytics/dashboard/overview/` - Dashboard overview
- `GET /api/analytics/dashboard/trends/` - Dashboard trends
- `GET /api/analytics/dashboard/compliance/` - Compliance dashboard
- `GET /api/analytics/v1/filters/` - Available filters
- `GET /api/analytics/v1/tabs/{tab}/` - Tab data
- `GET /api/analytics/v1/tabs/{tab}/export/` - Export tab

### 10. **Legacy - Cases** (`/api/cases/`)
- `GET /api/cases/categories/` - Case categories
- `GET /api/cases/my/` - My cases
- `POST /api/cases/my/` - Create case
- `GET /api/cases/my/{id}/` - Case details
- `POST /api/cases/my/{id}/submit/` - Submit for review
- `POST /api/cases/{id}/review/` - Review case
- `GET /api/cases/pending/` - Pending reviews
- `GET /api/cases/statistics/` - Stats

### 11. **Legacy - Logbook** (`/api/logbook/`)
- `GET /api/logbook/pending/` - Pending entries to verify
- `POST /api/logbook/{id}/verify/` - Verify entry
- `GET /api/logbook/my/` - My entries
- `POST /api/logbook/my/` - Create entry
- `POST /api/logbook/my/{id}/submit/` - Submit entry

### 12. **Legacy - Certificates** (`/api/certificates/`)
- `GET /api/certificates/my/` - My certificates
- `GET /api/certificates/my/{id}/download/` - Download

### 13. **Legacy - Reports** (`/api/reports/`)
- `GET /api/reports/templates/` - Report templates
- `GET /api/reports/catalog/` - Report catalog
- `POST /api/reports/run/{key}/` - Run report
- `GET /api/reports/export/{key}/` - Export
- `POST /api/reports/generate/` - Generate custom
- `GET /api/reports/scheduled/` - Scheduled reports
- `POST /api/reports/scheduled/` - Create scheduled

### 14. **Legacy - Search** (`/api/search/`)
- `GET /api/search/` - Global search
- `GET /api/search/history/` - Search history
- `GET /api/search/suggestions/` - Suggestions

### 15. **Legacy - Attendance** (`/api/attendance/`)
- `POST /api/attendance/upload/` - Bulk upload
- `GET /api/attendance/summary/` - Summary

### 16. **Legacy - Results** (`/api/results/`)
- `GET /api/results/exams/` - Exams CRUD
- `GET /api/results/scores/` - Scores CRUD

---

## 🔑 Common Query Parameters

**Filtering:**
- `?program=1` - Filter by program ID
- `?required=true` - Filter by required flag
- `?active=true` - Filter by active status

**Pagination:**
- `?page=2` - Page number
- `?page_size=50` - Items per page (default: 20)

**Ordering:**
- `?ordering=name` - Order by field
- `?ordering=-created_at` - Descending order

---

## 📡 Common Response Patterns

### Success Response (List)
```json
{
  "count": 42,
  "next": "https://api.example.com/api/resource/?page=2",
  "previous": null,
  "results": [...]
}
```

### Success Response (Detail)
```json
{
  "id": 1,
  "name": "Example",
  "created_at": "2024-01-01T12:00:00Z",
  ...
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

---

## 🔐 Permission Levels

| Role | Access |
|------|--------|
| Admin/UTRMC Admin | Full access to all endpoints, write to programs/templates |
| Supervisor/Faculty | Approve rotations/leaves, view supervisees, read analytics |
| Resident/PG | Submit rotations/leaves, view own records, create entries |
| Authenticated User | Read organizational data, search, view profiles |
| Anonymous | Login/register only |

---

## 🚀 Common Workflows

### Rotation Approval Flow
1. PG submits: `POST /api/rotations/{id}/submit/`
2. HOD approves: `POST /api/rotations/{id}/hod-approve/`
3. UTRMC approves: `POST /api/rotations/{id}/utrmc-approve/`
4. Admin activates: `POST /api/rotations/{id}/activate/`
5. Admin completes: `POST /api/rotations/{id}/complete/`

### Case Submission Flow
1. Create: `POST /api/cases/my/`
2. Submit: `POST /api/cases/my/{id}/submit/`
3. Supervisor reviews: `POST /api/cases/{id}/review/`

### User Import Flow
1. Prepare CSV
2. `POST /api/bulk/import-trainees/` (or residents/supervisors)
3. System validates and imports

---

## 📞 Support Endpoints

- `GET /health/` - Health check
- `GET /healthz/` - K8s health
- `GET /readiness/` - Readiness probe
- `GET /liveness/` - Liveness probe
- `GET /api/system/settings/` - System configuration

