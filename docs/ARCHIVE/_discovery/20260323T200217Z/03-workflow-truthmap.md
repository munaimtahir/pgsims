# Workflow Truthmap

## Workflow: Login and role redirect

- Intended journey: user logs in, gets role dashboard.
- Frontend screens: `/login`.
- API calls: `POST /api/auth/login/`, token refresh endpoint as needed.
- Backend handlers: `CustomTokenObtainPairView`, JWT auth.
- DB touchpoints: `users.User` read/authenticate.
- Runtime result: backend-auth path verified by passing backend tests, browser path not executed in this run.
- Status: **Partial**.

## Workflow: UTRMC user management

- Intended journey: list users, create/edit user.
- Frontend screens: `/dashboard/utrmc/users`.
- API calls: `/api/users/`, `/api/users/{id}/`.
- Backend handlers: `UserViewSet` with manager checks.
- DB touchpoints: `users.User` + related profile/membership relationships.
- Runtime result: backend role rules tested; no manual browser CRUD performed.
- Status: **Partial**.

## Workflow: Resident research + supervisor review

- Intended journey: resident drafts/submits, supervisor approves/returns.
- Frontend screens: `/dashboard/resident/research`, `/dashboard/supervisor/research-approvals`.
- API calls: `/api/my/research/`, `/api/my/research/action/{action}/`, `/api/supervisor/research-approvals/`.
- Backend handlers: `ResidentResearchProjectView`, `ResearchProjectActionView`, `SupervisorResearchApprovalsView`.
- DB touchpoints: `ResidentResearchProject`.
- Runtime result: backend tests include phase6 coverage and pass; browser workflow unverified in this run.
- Status: **Partial**.

## Workflow: Rotation approval

- Intended journey: create/submit → hod/utrmc approve → activate/complete.
- Frontend screens: distributed across resident/supervisor/utrmc pages.
- API calls: `/api/rotations/*` action endpoints.
- Backend handlers: `RotationAssignmentViewSet` actions.
- DB touchpoints: `RotationAssignment` and related records.
- Runtime result: backend state logic and role gating test-backed; no browser flow run.
- Status: **Partial**.

## Workflow: Logbook submit-return-resubmit-approve

- Intended journey: PG logbook submit and supervisor verification.
- Frontend screens expected: `/dashboard/pg/logbook`, `/dashboard/supervisor/logbooks`.
- API calls expected: `/api/logbook/*`.
- Backend handlers present only in legacy module (`_legacy/logbook/api_urls.py`).
- Active URL wiring: root `sims_project/urls.py` does **not** include legacy logbook API urls.
- Runtime result: contract references this workflow, but active frontend/backend routing evidence is inconsistent.
- Status: **Broken**.

---

## Frontend ↔ Backend contract mismatches

- `API_CONTRACT.md` still defines logbook API contract; active frontend pages are missing and active URL include is absent.
- E2E/regression docs explicitly note missing/incomplete features while contract language reads as active.

## Missing links

- Missing App Router pages for contract-referenced logbook flows.
- Legacy backend logbook API not mounted in active root urls.

## Fake integrations / placeholders

- Regression suite docs mark some tests as pending feature completion and excluded from default run.

## Dead endpoints

- Not proven dead globally, but legacy endpoints are effectively unreachable from active root URL wiring in default stack.

## Orphan UI

- Not many strict orphan pages found; bigger issue is inverse (backend legacy functionality with no active pages).
