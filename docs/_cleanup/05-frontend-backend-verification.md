# Phase E — Frontend/Backend Verification

Date (UTC): 2026-04-21

## 1) Contract/API Alignment

### Working perfectly
- Auth endpoints used by frontend are reachable and functional:
  - `POST /api/auth/login/` (all verification roles)
  - `GET /api/auth/profile/`
- Frontend build/lint/type gates passed.
- Backend full regression suite passed (`209 passed`).

### Working but needs debugging
- Contract vs runtime behavior drift detected:
  - `GET /api/dashboard/resident/` exists but returns `404` for baseline resident without training record (`No ResidentTrainingRecord matches...`) instead of resilient empty-state payload.
  - `POST /api/leaves/` rejects baseline resident payload with `resident_training` required.

### Not done / misleading / hidden
- Contract currently advertises resident rotation create path, but runtime rejects resident create:
  - `POST /api/rotations/` as `pilot_pg` returned `403` (`Only admin or utrmc_admin can create rotation assignments`).

## 2) RBAC / Permission Validation

### Working perfectly
- `utrmc_user` mutation restrictions enforced:
  - `POST /api/hospitals/` → `403`.
  - `GET /api/utrmc/approvals/rotations/` → `403` while `utrmc_admin` allowed (`200`).

### Working but needs debugging
- `GET /api/users/` for supervisor returned `200` with self-only result set.
  - Behavior may be acceptable as self-scoped read, but current RBAC contract text states list/create/update forbidden for supervisor/faculty. Contract wording and behavior need reconciliation.

## 3) Core Workflow Verification

### Auth/login
- **Working perfectly** (all verification accounts authenticated).

### User setup/onboarding
- **Working but needs debugging** (baseline user requires additional training-record setup for full resident dashboard/workflows).

### Dashboard loading
- **Working but needs debugging**:
  - Supervisor and UTRMC dashboards load.
  - Resident operational dashboard fails on clean baseline due missing training-record dependency.

### Leave flow
- **Working but needs debugging**:
  - Read/list routes available.
  - Create flow blocked by required `resident_training` field in baseline.

### Rotations/postings
- **Not done / misleading / hidden**:
  - Feature-layer rotation E2E failed.
  - Resident rotation create path contract does not match runtime authorization.

### Additional active surfaces (feature-layer E2E)
- Run: `./scripts/e2e_seed.sh && npm run test:e2e:feature-layer:local`
- Result: **9 passed, 5 failed**
  - Failed: dashboards (role-aware counters), permission-boundary logbook submit path, rotations phase-1 workflow, synopsis workflow, thesis workflow.

## 4) UI Truth Verification

### Working but needs debugging
- Multiple E2E failures indicate UI/action availability not consistently aligned with backend readiness/state on clean baseline (missing actionable controls/cards in scenarios expected by tests).

### Not done / misleading / hidden
- Synopsis/thesis submission cards not visible in expected resident surfaces under seeded feature-layer flow; these surfaces should not be represented as fully operational until corrected.

## 5) Build/Test Verification

### Working perfectly
- Backend: `SECRET_KEY=test-secret pytest sims -q` → **209 passed**.
- Frontend: `npm test -- --watch=false`, `npm run lint`, `npx tsc --noEmit`, `npm run build` → **all passed**.

### Working but needs debugging
- Feature-layer Playwright suite has deterministic failures in active workflow coverage (see above).
