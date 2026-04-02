# Core Workflow Closure Report

## 1) Active Leave Workflow
- Workflow name:
  Resident leave request and supervisor approval
- Intended journey:
  Resident opens the active schedule page, creates a leave draft, submits it for review, supervisor sees it on the active dashboard, approves it, and the resident sees the approved state reflected back in the UI.
- Screens / components involved:
  - `/dashboard/resident`
  - `/dashboard/resident/schedule`
  - `/dashboard/supervisor`
  - `frontend/lib/api/training.ts`
- Backend endpoints / services involved:
  - `GET /api/residents/me/summary/`
  - `GET /api/my/leaves/`
  - `POST /api/leaves/`
  - `POST /api/leaves/{id}/submit/`
  - `GET /api/leaves/?status=SUBMITTED`
  - `POST /api/leaves/{id}/approve/`
- Models / entities involved:
  - `ResidentTrainingRecord`
  - `LeaveRequest`
  - supervisor-resident assignment
- Pre-fix state:
  - Backend foundation existed.
  - Resident active frontend had no live leave entry/submission path.
  - Supervisor dashboard did not provide actionable leave approval behavior.
  - Resident summary contract did not expose the training record id needed to create a leave.
- Exact gaps:
  - Missing FE API client methods
  - Missing resident form/list/submit UI
  - Missing supervisor approval UI
  - Missing `training_record.id` in summary contract
- Changes made:
  - Added leave API methods and types.
  - Added resident leave draft/list/submit workflow to the active schedule page.
  - Added supervisor pending-leave approval UI on the active supervisor dashboard.
  - Added `training_record.id` to resident summary response and tests.
  - Corrected the resident quick action so "Apply for Leave" points to the real schedule page.
- Verification evidence:
  - Backend tests: `cd backend && SECRET_KEY=test-secret python3 -m pytest sims/training/test_phase6.py -q`
  - Browser workflow gate: `cd frontend && E2E_BASE_URL=http://127.0.0.1:3001 E2E_API_URL=http://127.0.0.1:8000 npx playwright test --project=workflow-gate`
  - Route/page evidence: `frontend/app/dashboard/resident/schedule/page.tsx`, `frontend/app/dashboard/supervisor/page.tsx`
- Post-fix classification:
  - Done
- Remaining limitations:
  - Reject flow is present but not part of the promoted browser gate.

## 2) Supervisor Scoping Alignment
- Workflow name:
  Supervisor resident visibility across summary and approval surfaces
- Intended journey:
  A supervisor assigned to a resident should see the same resident consistently across research approvals, summary counts, leave inbox, and related training views.
- Screens / components involved:
  - `/dashboard/supervisor`
  - `/dashboard/supervisor/research-approvals`
- Backend endpoints / services involved:
  - `GET /api/supervisors/me/summary/`
  - `GET /api/leaves/`
  - resident training and posting viewsets
- Models / entities involved:
  - `User.supervisor`
  - `SupervisorResidentLink`
  - `ResidentTrainingRecord`
- Pre-fix state:
  - Different surfaces used different supervisor scoping rules.
  - Direct supervisor assignment could work for research while leave/summary visibility still broke.
- Exact gaps:
  - Inconsistent resident scoping logic across training views
  - Seed data did not guarantee both assignment representations
- Changes made:
  - Added shared `_get_supervised_resident_ids()` helper and reused it across the affected summary/inbox/query paths.
  - Updated deterministic seed data to create the canonical active supervisor-resident link.
- Verification evidence:
  - Backend test added for direct supervisor assignment scoping
  - Workflow gate leave approval passes after seeding
- Post-fix classification:
  - Done
- Remaining limitations:
  - The domain still has two assignment representations; alignment was restored without widening scope into a broader data-model redesign.

## 3) Dashboard-to-Action Continuation
- Workflow name:
  Resident dashboard quick action to active leave workflow
- Intended journey:
  A resident should be able to continue from dashboard CTA to the actual page where the workflow can be completed.
- Screens / components involved:
  - `/dashboard/resident`
  - `/dashboard/resident/schedule`
- Backend endpoints / services involved:
  - Indirectly the leave endpoints listed above
- Models / entities involved:
  - N/A beyond leave workflow state
- Pre-fix state:
  - The quick action routed to progress instead of the active leave workflow page.
- Exact gaps:
  - Broken continuation from visible CTA to actual task completion surface
- Changes made:
  - Repointed the leave CTA to `/dashboard/resident/schedule`.
- Verification evidence:
  - Source inspection of `frontend/app/dashboard/resident/page.tsx`
  - Leave workflow browser gate succeeds using the active resident surface
- Post-fix classification:
  - Done
- Remaining limitations:
  - None within the current scoped workflow.

## 4) Password Reset Request Path
- Workflow name:
  Forgot-password request submission
- Intended journey:
  A user submits their email from the real forgot-password page and gets a non-enumerating success response.
- Screens / components involved:
  - `/forgot-password`
- Backend endpoints / services involved:
  - `POST /api/auth/password-reset/`
- Models / entities involved:
  - `User`
- Pre-fix state:
  - The UI path failed locally when email delivery raised an exception.
- Exact gaps:
  - Runtime behavior contradicted the expected non-enumerating contract for a request-only flow.
- Changes made:
  - Changed password-reset request behavior to return generic success for send-mail failures and added test coverage.
- Verification evidence:
  - `cd backend && SECRET_KEY=test-secret python3 -m pytest sims/users/tests.py -q`
  - Workflow gate Playwright suite passes the real browser flow
- Post-fix classification:
  - Done
- Remaining limitations:
  - This verifies request submission only, not end-to-end mail delivery in a real outbound mail environment.

## Explicitly deferred workflows

### Logbook
- Intended journey:
  Resident logbook entry lifecycle and supervisor review
- Pre-fix state:
  Historically claimed, not part of the active runtime surface
- Exact gaps:
  - No active dashboard route
  - No active navigation exposure
  - No active backend include in the current runtime boundary
- Changes made:
  - None; claim was downgraded instead of speculative reactivation
- Verification evidence:
  - `backend/sims_project/urls.py`
  - `frontend/lib/navRegistry.ts`
  - `frontend/app/dashboard/*`
- Post-fix classification:
  - Deferred
- Remaining limitations:
  - Requires a separate milestone and a fresh contract decision before activation.

### Cases
- Intended journey:
  Resident cases workflow and review
- Pre-fix state:
  Historically claimed, not part of the active runtime surface
- Exact gaps:
  - Same active-surface absence as logbook
- Changes made:
  - None; claim was downgraded instead of speculative reactivation
- Verification evidence:
  - `backend/sims_project/urls.py`
  - `frontend/lib/navRegistry.ts`
  - `frontend/app/dashboard/*`
- Post-fix classification:
  - Deferred
