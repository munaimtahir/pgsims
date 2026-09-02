# Endpoint Coverage Report

## Newly Covered
- `GET /api/departments/{id}/roster/`
- `GET /api/hospitals/{id}/departments/`
- `POST /api/hod-assignments/`
- `POST /api/supervision-links/` denied for UTRMC read-only user
- `PATCH /api/hospital-departments/{id}/`
- `POST /api/users/` denied for UTRMC read-only user
- `POST /api/logbook/{id}/submit/` invalid transition
- `POST /api/logbook/{id}/review/` invalid action/wrong reviewer paths
- `POST /api/leaves/{id}/submit/` invalid transition
- `POST /api/leaves/{id}/approve/` wrong role/wrong supervisor/draft transition paths
- `POST /api/leaves/{id}/reject/` invalid transition after approval
- `GET /api/schema/`

## Still Not Closed
The full active API inventory remains above this subset. The production GO threshold requires 100% active API coverage, which was not achieved.
