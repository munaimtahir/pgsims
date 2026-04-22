# Endpoint Coverage Report

## Tested Directly Or Indirectly
- `/api/auth/login/`, `/api/auth/profile/`, `/api/auth/password-reset/`
- `/api/dashboard/resident/`, `/api/residents/me/summary/`
- `/api/my/leaves/`, `/api/leaves/`, `/api/leaves/{id}/submit/`, approve/reject paths
- `/api/logbook/`, `/api/logbook/{id}/submit/`, `/api/logbook/{id}/review/`, `/api/logbook/review-queue/`, `/api/logbook/my-threshold/`
- `/api/dashboard/supervisor/`, `/api/supervisors/me/summary/`
- `/api/dashboard/utrmc/`, `/api/users/`, `/api/hospitals/`, `/api/departments/`, `/api/hospital-departments/`
- `/api/bulk/import/*/dry-run/`

## Insufficiently Proven
- `/api/departments/{id}/roster/`
- `/api/hospitals/{id}/departments/`
- `/api/hod-assignments/`
- all `/api/admin/data-quality/*` action variants
- every UTRMC admin CTA mutation path
- generated OpenAPI schema endpoint: not wired

Status: FAIL for 100% endpoint coverage.

