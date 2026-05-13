# API Inventory for Android Mobile Integration

This document lists the existing backend API endpoints classified by their readiness and relevance for a native Android mobile application.

## 1. Authentication & Session Management
Auth uses JWT (JSON Web Token) Bearer authentication.

| Endpoint | Method | Role | Status | Notes |
|----------|--------|------|--------|-------|
| `/api/auth/login/` | POST | Anonymous | Ready | Returns `access`, `refresh` tokens and user summary. |
| `/api/auth/refresh/` | POST | Authenticated | Ready | Refreshes access token using refresh token. |
| `/api/auth/logout/` | POST | Authenticated | Ready | Client-side token removal; server-side blacklist optional. |
| `/api/auth/me/` | GET | Authenticated | Ready | Returns rich current user profile + memberships. |
| `/api/auth/profile/` | GET | Authenticated | Ready | Canonical basic user profile. |
| `/api/auth/profile/update/` | PATCH | Authenticated | Ready | Update basic profile fields. |
| `/api/auth/change-password/` | POST | Authenticated | Ready | Change password for logged-in user. |
| `/api/auth/password-reset/` | POST | Anonymous | Ready | Triggers reset email. |

## 2. Resident Workflows (Active Surface)
Focus on logbook management and rotation status.

| Endpoint | Method | Role | Status | Notes |
|----------|--------|------|--------|-------|
| `/api/residents/me/summary/` | GET | PG | Ready | Dashboard bootstrap (rotation, logbook, eligibility). |
| `/api/logbook/` | GET/POST | PG | Ready | List/Create logbook entries. |
| `/api/logbook/{id}/` | GET/PATCH | PG | Ready | Detail/Update (Draft/Returned only). |
| `/api/logbook/{id}/submit/` | POST | PG | Ready | Submit for supervisor review. |
| `/api/logbook/my-threshold/` | GET | PG | Ready | Progress against program requirements. |
| `/api/my/leaves/` | GET | PG | Ready | List own leave requests. |
| `/api/leaves/` | POST | PG | Ready | Create new leave request. |
| `/api/my/rotations/` | GET | PG | Ready | List assigned rotations. |
| `/api/my/workshops/` | GET/POST | PG | Ready | List/Upload workshop certificates (Multipart). |

## 3. Supervisor Workflows (Active Surface)
Focus on review and oversight.

| Endpoint | Method | Role | Status | Notes |
|----------|--------|------|--------|-------|
| `/api/supervisors/me/summary/` | GET | Supervisor | Ready | Dashboard bootstrap (pending counts, residents). |
| `/api/logbook/review-queue/` | GET | Supervisor | Ready | List of entries awaiting review. |
| `/api/logbook/{id}/review/` | POST | Supervisor | Ready | Approve or Return with feedback. |
| `/api/supervisors/residents/{id}/progress/` | GET | Supervisor | Ready | Snapshop of a specific resident's progress. |
| `/api/leaves/` | GET | Supervisor | Ready | List leaves for supervised residents. |
| `/api/leaves/{id}/approve/` | POST | Supervisor | Ready | Approve leave. |
| `/api/leaves/{id}/reject/` | POST | Supervisor | Ready | Reject leave with reason. |

## 4. Master Data & Utilities

| Endpoint | Method | Role | Status | Notes |
|----------|--------|------|--------|-------|
| `/api/hospitals/` | GET | Authenticated | Ready | List hospitals. |
| `/api/departments/` | GET | Authenticated | Ready | List departments. |
| `/api/notifications/` | GET | Authenticated | Ready | List user notifications. |
| `/api/notifications/unread-count/` | GET | Authenticated | Ready | Quick badge count. |
| `/api/system/settings/` | GET | Authenticated | Ready | System-wide flags (e.g. Workshop enabled). |

## 5. Mobile MVP Classification

### Ready for Android MVP
- All Auth endpoints.
- Logbook CRUD and Submit.
- Supervisor Review Queue and Action.
- Resident/Supervisor Dashboards.
- Leave requests and approvals.

### Exists but needs cleanup
- **Error Responses**: Mobile app needs consistent JSON error structures (currently standard DRF, mostly fine).
- **Pagination**: Most GET lists use `PageNumberPagination`. Ensure consistent response keys (`count`, `next`, `previous`, `results`).

### Missing but required
- **Mobile Bootstrap**: A unified `/api/mobile/bootstrap/` to reduce round-trips (Profile + Summary + Unread Notifications).
- **FCM/Push Integration**: No endpoint for registering Firebase Cloud Messaging tokens found.
- **Logbook Attachments**: `LogbookEntry` model currently lacks a `file_field` or `image_field` for clinical evidence/certificates.

### Not needed for MVP
- Bulk Import/Export.
- System-wide audit reports (Admin only).
- Analytics (Web primary).

### Unsafe/unclear for mobile use
- `/api/auth/register/`: Role-gated and typically disabled in production. Admin usually seeds users.
