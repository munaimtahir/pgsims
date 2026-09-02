# Mobile MVP Workflow Map

This document maps user workflows to specific API sequences for the PGSIMS Android application.

## 1. Resident (PG) Workflows

### W1.1 Login & Bootstrap
- **Step 1**: User enters credentials.
- **Action**: `POST /api/auth/login/`
- **Response**: JWT Tokens + User Role.
- **Step 2**: App fetches initial state.
- **Action**: `GET /api/residents/me/summary/`
- **Result**: Display rotation info, next logbook targets, and leave summary.

### W1.2 Logbook Entry Creation
- **Action**: `POST /api/logbook/`
- **Payload**: Patient details, clinical presentation, diagnosis, reflection.
- **Result**: Entry created as `DRAFT`.

### W1.3 Logbook Submission
- **Action**: `POST /api/logbook/{id}/submit/`
- **Result**: Status changes to `SUBMITTED`. Resident can no longer edit.

### W1.4 Leave Request
- **Action**: `POST /api/leaves/`
- **Payload**: Dates, type, reason.
- **Result**: Request created and queued for supervisor approval.

### W1.5 Workshop Certificate Upload
- **Action**: `POST /api/my/workshops/`
- **Payload**: Multipart file upload (PDF/Image) + Workshop ID.
- **Result**: Record created with attachment.

---

## 2. Supervisor Workflows

### W2.1 Login & Bootstrap
- **Step 1**: User enters credentials.
- **Action**: `POST /api/auth/login/`
- **Step 2**: App fetches initial state.
- **Action**: `GET /api/supervisors/me/summary/`
- **Result**: Display counts for pending logbooks and leave requests.

### W2.2 Logbook Review
- **Step 1**: List pending entries.
- **Action**: `GET /api/logbook/review-queue/`
- **Step 2**: Review detail.
- **Action**: `GET /api/logbook/{id}/`
- **Step 3**: Approve or Return.
- **Action**: `POST /api/logbook/{id}/review/`
- **Payload**: `{ "action": "approved" | "returned", "feedback": "..." }`

### W2.3 Leave Approval
- **Step 1**: List pending leaves.
- **Action**: `GET /api/leaves/?status=SUBMITTED`
- **Step 2**: Approve/Reject.
- **Action**: `POST /api/leaves/{id}/approve/` or `POST /api/leaves/{id}/reject/`

---

## 3. Shared Utilities

### W3.1 Profile Management
- **Action**: `GET /api/auth/profile/`
- **Edit**: `PATCH /api/auth/profile/update/`

### W3.2 Notifications
- **Step 1**: Poll unread count.
- **Action**: `GET /api/notifications/unread-count/`
- **Step 2**: View notifications.
- **Action**: `GET /api/notifications/`
- **Step 3**: Mark as read.
- **Action**: `POST /api/notifications/mark-read/`
- **Payload**: `{ "ids": [1, 2, 3] }` or individual mark.

### W3.3 Token Maintenance
- **Action**: `POST /api/auth/refresh/`
- **Trigger**: Interceptor on 401 Unauthorized (if token expired).
