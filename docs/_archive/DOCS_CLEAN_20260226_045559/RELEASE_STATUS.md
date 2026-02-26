# SIMS Release Status (Canonical)

**Status Date:** 2026-01-31  
**Scope:** This is the single source of truth for feature status and release readiness.  
**Supersedes:** `FEATURES_STATUS.md`, `STAGE2_READINESS_REVIEW.md`, `PRODUCTION_READINESS_ASSESSMENT.md`, `SYSTEM_STATUS.md`, and `PROJECT_SUMMARY.md` where they conflict.

---

## Overall Readiness

**Current Stage:** Pilot-ready / not production-ready.  

**Why:** Core workflows are functional and smoke/E2E checks pass, but there are unresolved production blockers and documentation conflicts that require verification and remediation before a production release.

---

## Verified in This Environment (2026-01-31)

### Backend Smoke Tests
`scripts/smoke_test_endpoints.sh` against local server  
**Result:** PASS (9/9 endpoints)

### Frontend E2E (Playwright)
`npm --prefix frontend run test:e2e`  
**Result:** PASS (7/7 tests)

---

## Production Blockers (Must Resolve Before Production)

1. **Committed secrets** in `.env` (rotate keys, move to secure storage).  
2. **Unresolved merge conflict marker** in `TESTS.md`.  
3. **Password reset flow** is a stub on the frontend (API integration incomplete).  
4. **Feature verification incomplete** for analytics/notifications/reporting/search/audit/bulk (code exists but needs runtime verification and tests).

---

## Feature Status (Verified Code-Level Presence)

### Core Modules
- **Authentication, User Management, Cases, Logbook, Certificates, Rotations:** Functional for pilot use.

### Disputed Modules — Code-Level Verification (2026-01-31)

| Module | Status | Evidence (code wired) | Runtime caveats |
| --- | --- | --- | --- |
| Analytics | Implemented | `sims_project/settings.py` (INSTALLED_APPS), `sims_project/urls.py` (`api/analytics/`) | Requires data volume to validate trends/performance |
| Notifications | Implemented | `sims_project/settings.py`, `sims_project/urls.py` (`api/notifications/`), `sims/notifications/signals.py` | Email delivery depends on SMTP settings |
| Reporting (PDF/XLSX) | Implemented | `sims_project/settings.py`, `sims_project/urls.py` (`api/reports/`), `sims/reports/services.py` | Email + scheduled reports depend on SMTP/Celery |
| Global Search | Implemented | `sims_project/settings.py`, `sims_project/urls.py` (`api/search/`), `sims/search/services.py` | Full-text search uses PostgreSQL; SQLite uses fallback |
| Audit Trail | Implemented | `sims_project/settings.py`, `sims_project/urls.py` (`api/audit/`), `sims/audit/views.py` | Admin-only access; verify export/reporting in runtime |
| Bulk Operations | Implemented | `sims_project/settings.py`, `sims_project/urls.py` (`api/bulk/`), `sims/bulk/services.py` | Import workflows need sample data for validation |

**Action:** run module-level tests/flows in a staging environment and update status to “Runtime-verified” once validated.

### Disputed Modules — Runtime Verification (2026-01-31)

| Module | Runtime check | Result | Notes |
| --- | --- | --- | --- |
| Global Search | `GET /api/search/?q=test` | ✅ 200 | Returns JSON payload |
| Analytics | `GET /api/analytics/dashboard/overview/` | ✅ 200 | Returns JSON payload |
| Notifications | `GET /api/notifications/unread-count/` and list | ✅ 200 | Both endpoints respond |
| Reporting | `GET /api/reports/templates/`, `POST /api/reports/generate/` | ✅ 200 | Generated `logbook-summary` PDF |
| Audit Trail | `GET /api/audit/activity/` | ✅ 200 | Admin-only endpoint responds |
| Bulk Operations | `POST /api/bulk/review/` with empty `entry_ids` | ⚠️ 400 | Endpoint reachable; validation error expected |

---

## Required Next Actions

1. **Security hygiene:** remove committed secrets and rotate credentials.  
2. **Documentation alignment:** update this file after verifying disputed modules.  
3. **Test baseline:** run full backend test suite (`pytest`) and record results.  
4. **Deployment hardening:** ensure production settings (Postgres, secure cookies, HSTS, host headers).

---

## Test Baseline (2026-01-31)

- **Pytest (full suite)**: Incomplete — timed out after 120s with an early failure in `sims/logbook/test_api.py`.  
- **Focused failure:** `sims/logbook/test_api.py::PGLogbookEntryAPITests::test_non_pg_user_cannot_access_pg_endpoints`  
  - **Error:** `AttributeError: 'PGLogbookEntryAPITests' object has no attribute 'admin'`

**Action:** fix the failing test fixture/setup and re-run full pytest to completion.

---

## Change Control

All future status updates must be made here first. Other documents should only summarize or reference this file.
