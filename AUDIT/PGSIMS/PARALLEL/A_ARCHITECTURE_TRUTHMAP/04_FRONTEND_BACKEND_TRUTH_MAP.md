# Frontend to Backend Truth Map

| Frontend Route/Component | API Call | Backend Route | Match Status | Notes |
|---|---|---|---|---|
| N/A | `/api/academics/data-quality/` | `/api/academics/data-quality/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/academics/evaluation-templates/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/academics/logbook-categories/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/academics/options/` | `/api/academics/options/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/academics/overview/` | `/api/academics/overview/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/academics/periods/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/academics/residents/me/summary/` | `/api/academics/residents/me/summary/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/academics/review-queue/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/academics/rotation-templates/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/academics/seed/` | `/api/academics/seed/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/academics/supervisors/me/summary/` | `/api/academics/supervisors/me/summary/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/academics/training-records/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/admin/data-quality/audit` | `/api/admin/data-quality/audit` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/admin/data-quality/recompute` | `/api/admin/data-quality/recompute` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/admin/data-quality/summary` | `/api/admin/data-quality/summary` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/admin/data-quality/users` | `/api/admin/data-quality/users` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/audit/activity/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/audit/reports/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/auth/change-password/` | `/api/auth/change-password/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/auth/complete-profile/` | `/api/auth/complete-profile/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/auth/login/` | `/api/auth/login/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/auth/login/', { username: 'user', password: 'pass` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/auth/logout/` | `/api/auth/logout/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/auth/logout/', { refresh: 'ref-tok` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/auth/me/` | `/api/auth/me/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/auth/password-reset/` | `/api/auth/password-reset/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/auth/password-reset/confirm/` | `/api/auth/password-reset/confirm/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/auth/profile/` | `/api/auth/profile/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/auth/profile/update/` | `/api/auth/profile/update/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/auth/refresh/` | `/api/auth/refresh/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/auth/register/` | `/api/auth/register/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/data-quality/` | `/api/data-quality/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/department-memberships/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/departments/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/hospital-assignments/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/hospital-departments/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/hospitals/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/identity/options/` | `/api/identity/options/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/notifications/` | `/api/notifications/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/notifications/preferences/` | `/api/notifications/preferences/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/notifications/unread-count/` | `/api/notifications/unread-count/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/programs/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/supervision/assignments/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/supervision/change-primary/` | `/api/supervision/change-primary/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/supervision/data-quality/` | `/api/supervision/data-quality/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/supervision/import/` | `/api/supervision/import/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/supervision/options/` | `/api/supervision/options/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/users/` | `/api/users/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/users/', { params: { role: 'RESIDENT` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/users/?role=supervisor` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/users/assigned-pgs/` | `/api/users/assigned-pgs/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/academics/evaluation-templates/{id}/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/academics/logbook-categories/{id}/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/academics/periods/{id}/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/academics/residents/{id}/summary/` | `/api/academics/residents/<int:resident_id>/summary/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/academics/review-queue/{id}/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/academics/rotation-templates/{id}/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/academics/supervisors/{id}/summary/` | `/api/academics/supervisors/<int:supervisor_id>/summary/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/academics/training-records/{id}/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/academics/training-records/{id}/close/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/bulk/exports/{id}/` | `/api/bulk/exports/<str:resource>/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/bulk/templates/{id}/` | `/api/bulk/templates/<str:resource>/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/department-memberships/{id}/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/departments/{id}/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/departments/{id}/roster/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/hospital-assignments/{id}/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/hospital-departments/{id}/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/hospitals/{id}/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/hospitals/{id}/departments/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/notifications/mark-read/` | `/api/notifications/mark-read/` | CONNECTED_UNVERIFIED_RUNTIME | - |
| N/A | `/api/residents/{id}/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/staff/{id}/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/supervision/assignments/{id}/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/supervision/assignments/{id}/end/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/supervisors/{id}/` | Unknown | BROKEN | No exact backend route found |
| N/A | `/api/users/{id}/` | `/api/users/<drf_format_suffix:format>` | CONNECTED_UNVERIFIED_RUNTIME | - |
