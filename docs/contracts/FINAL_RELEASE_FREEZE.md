# PGSIMS/UTRMC — FINAL RELEASE FREEZE

**Freeze Date**: 2026-02-26  
**Tag**: `pgsims-utrmc-freeze-20260226`  
**Status**: LOCKED FOR PRODUCTION ROLLOUT

This document defines what is frozen and how to verify the frozen baseline remains intact.

---

## Frozen Scope

The following features, flows, and policies are **LOCKED** and verified as production-ready:

### 1. Authentication & Session Management (LOCKED)
- **Login/Logout Flow**: JWT-based authentication with cookie-only session
- **Cookie Contract**:
  - `access_token` (httpOnly, secure)
  - `role` (user role for client-side guards)
  - `exp` (expiration timestamp)
- **Refresh Token**: Stored in `localStorage` only (not in cookies)
- **Invalid/Expired Handling**: Middleware treats invalid/expired tokens as logged-out, clears cookies, redirects to `/login`
- **No changes allowed** to cookie names, storage strategy, or middleware auth flow

### 2. Middleware RBAC (LOCKED)
- **Roles**: `pg`, `supervisor`, `admin`, `utrmc_user`, `utrmc_admin`
- **Authorization Rules**: Defined in `docs/contracts/RBAC_MATRIX.md`
- **Supervisor Scope**: Option A (supervisees-only) - supervisors can only access records for assigned PGs
- **No changes allowed** to role names, scope rules, or permission matrix

### 3. PG Logbook Flow (LOCKED)
- **Status Workflow**: `draft` → `pending` (UI: "Submitted") → `returned`/`rejected`/`approved`
- **Edit Permissions**: PG can edit only when status in `draft`, `returned`
- **Supervisor Review**: `PATCH /api/logbook/<id>/verify/` with `action` + `feedback`
- **API Contract**: Payload shapes in `docs/contracts/API_CONTRACT.md`
- **No changes allowed** to status names, edit rules, or API payload structure

### 4. Supervisor Review Flow (LOCKED)
- **Pending Queue**: Supervisor sees only assigned supervisees' pending entries
- **Verify Actions**: `approved`, `returned`, `rejected`
- **Feedback Field**: `supervisor_feedback` (aliased as `feedback` in API responses)
- **No changes allowed** to queue filtering, verify actions, or feedback schema

### 5. UTRMC Roles (LOCKED)
- **utrmc_user**: Read-only oversight dashboards, logs, reports, statistics
- **utrmc_admin**: UTRMC super-admin with configuration and override approval powers
- **No changes allowed** to UTRMC role capabilities or dashboard access

### 6. Rotations Canonical Display (LOCKED)
- **Canonical Models**: 
  - ONE `academics.Department` model (university-wide)
  - ONE `rotations.Hospital` model
  - `HospitalDepartment` matrix for hospital-department relationships
- **Rotation Fields**: `pg`, `department`, `hospital`, `start_date`, `end_date`, `status`
- **Inter-Hospital Policy**: Requires override + approval if destination department exists in home hospital
- **No changes allowed** to canonical model structure or policy rules

### 7. Option A Reference Data Authority (LOCKED)
- **Department CRUD**: `admin` role only
- **Hospital CRUD**: `admin` role only
- **HospitalDepartment CRUD**: `utrmc_admin` primary; `admin` recovery allowed
- **No changes allowed** to reference data authority rules

### 8. Bulk Review (LOCKED)
- **Endpoint**: `POST /api/logbook/bulk-review/`
- **Payload**: Array of `{id, action, feedback}`
- **Authorization**: Supervisor can bulk-verify only assigned supervisees' entries
- **No changes allowed** to bulk review endpoint or authorization logic

### 9. Notification Preferences (LOCKED)
- **Endpoint**: `PATCH /api/notifications/preferences/`
- **Schema**: `recipient`, `verb`, `body`, `metadata` (canonical keys)
- **Service**: `NotificationService` at `sims/notifications/services.py`
- **No legacy keys allowed**: `user`, `message`, `type`, `related_object_id`

### 10. UI Routes and Terminology (LOCKED)
- **Routes**: Defined in `docs/contracts/ROUTES.md`
- **Terminology**: Defined in `docs/contracts/TERMINOLOGY.md`
- **No changes allowed** to route structure, navigation labels, or user-facing terms

---

## Verification Commands

Run these commands **serially** (not in parallel) to verify the frozen baseline:

### Backend Verification

```bash
cd /home/munaim/srv/apps/pgsims/backend

# Django system check
../.venv/bin/python manage.py check

# Full test suite
../.venv/bin/python manage.py test
```

**Expected**: All checks PASS, all tests PASS.

### Frontend Verification

```bash
cd /home/munaim/srv/apps/pgsims/frontend

# Build (must be serial, not parallel with Playwright)
npm run build

# Playwright E2E tests (must be serial, after build completes)
npx playwright test
```

**Expected**: Build succeeds, all Playwright tests PASS.

### Integration Truth-Map Verification

```bash
cd /home/munaim/srv/apps/pgsims

# Regenerate truth-map (using existing resolver/static analysis scripts)
# Example command structure (adjust to actual scripts):
# python scripts/generate_truth_map.py

# Check verdict in docs/contracts/INTEGRATION_TRUTH_MAP.md
grep "Verdict:" docs/contracts/INTEGRATION_TRUTH_MAP.md
```

**Expected**: Verdict is `PASS`, 0 unmatched frontend calls.

---

## Evidence Requirements

To verify this frozen baseline, you must provide:

1. **Backend Evidence**:
   - `manage.py check` output showing no issues
   - Test suite summary showing all tests PASS
   - No errors or warnings in test output

2. **Frontend Evidence**:
   - `npm run build` output showing successful build
   - Playwright summary showing all tests passed (e.g., "12 passed")
   - No build errors or test failures

3. **Truth-Map Evidence**:
   - Endpoint counts from backend
   - Frontend call counts
   - Matched/unmatched counts
   - Final verdict: `PASS`
   - Confirmation of 0 unmatched frontend calls

4. **CI Evidence**:
   - GitHub Actions workflow file showing serial gate execution
   - Workflow must enforce: backend tests → frontend build → Playwright → truth-map verification
   - Workflow must FAIL if truth-map verdict is not PASS

---

## Non-Negotiables

These constraints are **ABSOLUTE** and cannot be changed without explicit approval and re-freeze:

### 1. UI Stability
- No route structure changes
- No navigation label changes
- No terminology changes
- No dashboard route structure changes
- Allowed: bug fixes, performance improvements, helper text, small visual cues

### 2. Cookie Contract
- Must use cookies for: `access_token`, `role`, `exp`
- Refresh token stays in `localStorage` only
- Invalid/expired cookies must clear and redirect to `/login`
- No changes to cookie names or storage strategy

### 3. Option A Master-Data Authority
- Department CRUD: `admin` only
- Hospital CRUD: `admin` only
- HospitalDepartment CRUD: `utrmc_admin` primary; `admin` recovery
- No changes to reference data authority

### 4. Canonical Data Model
- ONE `academics.Department` model (no duplicates like "RotationDepartment")
- ONE `rotations.Hospital` model
- `HospitalDepartment` matrix only
- No introduction of duplicate Department/Hospital models

### 5. Serial Verification Only
- Backend tests must run serially
- Frontend build must complete before Playwright runs
- No parallel execution of build + E2E tests
- Reason: Parallel runs can intermittently hit Next.js `/_document` endpoint flake

### 6. Audit Trail
- `docs/_audit/**` is LOCAL-ONLY and must NOT be committed to git
- All state transitions must remain auditable via `django-simple-history`
- No removal of audit trail mechanisms

### 7. Contract-First Integration
- All backend ↔ frontend integration changes require contract updates
- Contracts in `docs/contracts/` are authoritative
- No silent payload changes

---

## Drift Detection

The following patterns are **FORBIDDEN** and will cause drift gate failures:

### Code-Level Drift
1. **Duplicate Department Models**: e.g., `RotationDepartment`, `AcademicDepartment`
2. **Legacy Notification Keys**: `user=`, `message=`, `type=`, `related_object_id=`
3. **Breaking API Payloads**: Without updating `docs/contracts/API_CONTRACT.md`
4. **Direct DB Edits**: Bypassing audit trail for state changes

### Contract-Level Drift
5. **Route Changes**: Without updating `docs/contracts/ROUTES.md`
6. **Terminology Changes**: Without updating `docs/contracts/TERMINOLOGY.md`
7. **RBAC Changes**: Without updating `docs/contracts/RBAC_MATRIX.md`

### Test-Level Drift
8. **Truth-Map Verdict != PASS**: Indicates unmatched frontend calls or integration drift
9. **Gate Test Failures**: Tests in `docs/contracts/TRUTH_TESTS.md` must always pass

---

## CI Drift Gates

A GitHub Actions workflow enforces these gates on every push:

**Workflow**: `.github/workflows/pgsims_drift_gates.yml`

**Serial Execution Order**:
1. Backend tests
2. Frontend build
3. Playwright E2E tests
4. Integration truth-map regeneration
5. Assert truth-map verdict is PASS

**Failure Conditions**:
- Any test failure
- Any build failure
- Truth-map verdict is not PASS
- Presence of forbidden patterns

---

## Release Tag

**Tag**: `pgsims-utrmc-freeze-20260226`  
**Type**: Annotated tag  
**Message**: "RBAC+E2E+TruthMap PASS, Option A locked"

To verify tag:
```bash
git show pgsims-utrmc-freeze-20260226
```

---

## How to Extend (Post-Freeze)

If you need to make changes after this freeze:

1. **Review Frozen Scope**: Determine if your change affects frozen areas
2. **If Frozen Area Affected**:
   - Get explicit approval
   - Update relevant contract docs
   - Re-run all verification commands serially
   - Update truth-map and verify PASS
   - Create new freeze document with new tag
3. **If Non-Frozen Area**:
   - Make changes following `AGENTS.md` governance
   - Run verification commands serially
   - Verify truth-map remains PASS
   - Update contracts if integration changes

---

## Maintenance

This freeze document is **canonical**. A mirror exists at `docs/FINAL_RELEASE_FREEZE.md` for convenience.

**Last Updated**: 2026-02-26  
**Next Review**: After first production deployment feedback
