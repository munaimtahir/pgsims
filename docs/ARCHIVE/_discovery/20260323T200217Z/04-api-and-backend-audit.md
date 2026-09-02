# API and Backend Audit

## Backend module inventory

Active apps in settings:

- `sims.users`
- `sims.academics`
- `sims.rotations`
- `sims.audit`
- `sims.bulk`
- `sims.notifications`
- `sims.training`

Legacy apps still present in code tree:

- `_legacy/logbook`, `_legacy/cases`, `_legacy/analytics`, `_legacy/attendance`, `_legacy/reports`, `_legacy/results`, `_legacy/certificates`, `_legacy/search`.

## Endpoint readiness overview

### Verified active surfaces

- Auth: `/api/auth/*`
- Userbase/org graph: `/api/hospitals`, `/api/departments`, `/api/hospital-departments`, memberships/links, `/api/users/*`
- Training: `/api/programs`, `/api/rotations`, `/api/leaves`, `/api/postings`, `/api/my/*`, `/api/supervisor/*`, `/api/utrmc/*`
- Notifications: `/api/notifications/*`
- Audit: `/api/audit/*`
- Bulk: `/api/bulk/*`

### Unverified or partially verified

- Full browser runtime for many training endpoints.
- Bulk import special variants beyond baseline route presence.

### Legacy/not-active-by-default

- Logbook API urls defined in `_legacy/logbook/api_urls.py` but not included in root project urls.

## Validation/auth quality

- Permission classes and in-view checks consistently applied.
- Training view actions enforce state transitions with explicit guard responses.
- Userbase manager/admin write restrictions enforced at view level.

## Backend test evidence

- `pytest sims -q` → `188 passed`.
- Drift guard and canonical migration gate pass separately.

## Background jobs and infra hooks

- Celery configured in settings and compose (`worker`, `beat`).
- Redis configured as broker/cache.
- Health endpoints exist: `/healthz`, `/readiness`, `/liveness`.

## Major backend risks

1. Active+legacy duality may cause accidental dependency on inactive paths.
2. Auth profile endpoint duplication (`/me` vs `/profile`) can drift.
3. Some RBAC logic duplicated across helper functions and in-method checks, increasing maintenance complexity.
