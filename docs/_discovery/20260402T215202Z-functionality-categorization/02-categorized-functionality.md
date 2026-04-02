# Categorized Functionality

## Not Done

### 1. Logbook workflow

- Name: Digital logbook
- Surface/module: legacy resident/supervisor workflow
- Why it is classified as not done:
  - no active frontend route in `frontend/app/dashboard`
  - no active backend URL include in `backend/sims_project/urls.py`
  - only `_legacy/logbook` code remains on disk
- Evidence:
  - `find backend/sims -maxdepth 2 -type d`
  - `rg -n "_legacy" backend/sims_project backend/sims -g'*.py'`
  - no active Next route under `frontend/app/dashboard/**/logbook*`
- What would be needed to complete it:
  - explicit product decision to reactivate it
  - contract update in `docs/contracts/`
  - active backend include
  - real Next.js routes/pages
  - verified resident -> supervisor end-to-end flow

### 2. Cases workflow

- Name: Clinical cases
- Surface/module: legacy resident/supervisor workflow
- Why it is classified as not done:
  - no active frontend route
  - no active backend include
  - only `_legacy/cases` remains on disk
- Evidence:
  - `find backend/sims -maxdepth 2 -type d`
  - no `cases` include in `backend/sims_project/urls.py`
- What would be needed to complete it:
  - explicit reactivation plan
  - active contracts
  - real frontend surfaces and verified end-to-end workflow

### 3. Legacy analytics dashboards

- Name: Analytics and historical reporting dashboards
- Surface/module: `_legacy/analytics`
- Why it is classified as not done:
  - not part of the promoted dashboard navigation
  - not part of the active runtime boundary
  - README still suggests broader analytics readiness than current truth supports
- Evidence:
  - `frontend/lib/navRegistry.ts`
  - `backend/sims_project/urls.py`
  - `_legacy/analytics` directory on disk only
- What would be needed to complete it:
  - clarify whether analytics is to be rebuilt on active APIs or retired
  - new active routes and contracts
  - verified role-specific runtime behavior

### 4. Certificate management

- Name: Certificates
- Surface/module: legacy certificates plus workshop attachment overlap
- Why it is classified as not done:
  - README claims active certificate management
  - active frontend has no certificate routes
  - runtime points to `_legacy/certificates`, not active surface
- Evidence:
  - `README.md`
  - `backend/sims/_legacy/certificates/*`
  - no active Next route for certificates
- What would be needed to complete it:
  - separate active certificate workflow from workshop attachment storage
  - add active UI/API/runtime path
  - verify permissions and review lifecycle

### 5. Global search and search history

- Name: Global search
- Surface/module: `_legacy/search`
- Why it is classified as not done:
  - README claims global search and history
  - active runtime exposes no search route or active dashboard search experience
  - implementation on disk is legacy only
- Evidence:
  - `README.md`
  - `backend/sims/_legacy/search/*`
  - no active route in `frontend/app/dashboard`
- What would be needed to complete it:
  - restore as an active feature with contracts and UI
  - role-aware search permissions
  - runtime verification beyond code presence

### 6. Legacy reporting / results / attendance ecosystem

- Name: Reports, results, attendance legacy modules
- Surface/module: `_legacy/reports`, `_legacy/results`, `_legacy/attendance`
- Why it is classified as not done:
  - modules exist only as legacy code
  - active runtime does not expose them
  - top-level docs still imply a wider reporting/export surface than runtime supports
- Evidence:
  - `find backend/sims -maxdepth 2 -type d`
  - `README.md`
  - `backend/sims_project/urls.py`
- What would be needed to complete it:
  - explicit scope decision
  - active UI/API contracts
  - current runtime verification

## Done But Needs Debugging

### 1. Authentication and protected-route baseline

- Name: Login + role-protected dashboard entry
- Surface/module: auth pages, `ProtectedRoute`, dashboard entry
- What exists already:
  - login is used repeatedly in browser tests
  - protected routes redirect users into role dashboards
  - forgot-password is live and successful
- What is failing or unreliable:
  - rapid repeated auth calls during the workflow gate produced a transient `429` on `/api/auth/login/`
  - auth is usable, but throttling behavior under automation needs explicit hardening/understanding
- Severity: Medium
- Evidence:
  - workflow gate output: `6 passed`
  - backend runtime logs during that run showed a `429` before the suite still completed
  - `frontend/components/auth/ProtectedRoute.tsx`
- Likely fix scope:
  - clarify login throttling policy
  - stabilize repeated-login behavior for automation and rapid user switching

### 2. UTRMC master data CRUD

- Name: Hospitals, departments, users, matrix
- Surface/module: `/dashboard/utrmc/hospitals`, `/departments`, `/users`, `/matrix`
- What exists already:
  - active pages and active backend APIs
  - create/edit/toggle UI exists
  - Playwright coverage confirms page load plus basic create/modal flows for hospitals/departments and page load for users
- What is failing or unreliable:
  - verification depth is still narrow
  - route docs still list user detail/new routes that do not exist in the actual Next route tree
  - no current workflow-grade proof for full CRUD correctness, validation, or non-seeded multi-role behavior
- Severity: Medium
- Evidence:
  - `frontend/app/dashboard/utrmc/{hospitals,departments,users,matrix}/page.tsx`
  - `backend/sims/users/userbase_urls.py`
  - `frontend/e2e/workflows/utrmc-management.spec.ts`
  - `docs/contracts/ROUTES.md` still references `/dashboard/utrmc/users/new` and `/dashboard/utrmc/users/[id]`
- Likely fix scope:
  - correct route docs
  - add end-to-end coverage for create/edit/update visibility and validation errors

### 3. UTRMC relationship management

- Name: Supervision links and HOD assignments
- Surface/module: `/dashboard/utrmc/supervision`, `/dashboard/utrmc/hod`
- What exists already:
  - active pages load, list entries, and expose add forms
  - active backend APIs exist
- What is failing or unreliable:
  - only shallow verification exists
  - no strong runtime proof yet for lifecycle depth, edit/deactivate flows, or permission edge cases
- Severity: Medium
- Evidence:
  - `frontend/app/dashboard/utrmc/supervision/page.tsx`
  - `frontend/app/dashboard/utrmc/hod/page.tsx`
  - `backend/sims/users/userbase_urls.py`
- Likely fix scope:
  - add targeted browser/API tests for create/list/update boundaries

### 4. Training programme administration

- Name: Programmes, policies, milestones, templates
- Surface/module: `/dashboard/utrmc/programs`
- What exists already:
  - program list
  - policy editing
  - milestone display
  - template add/delete
  - active training endpoints
- What is failing or unreliable:
  - no current end-to-end proof of full admin lifecycle
  - active surface looks complete, but verification is still mostly structural
- Severity: Medium
- Evidence:
  - `frontend/app/dashboard/utrmc/programs/page.tsx`
  - `backend/sims/training/urls.py`
- Likely fix scope:
  - add CRUD-path verification and contract assertions
  - verify role boundaries and persistence on real seeded data

### 5. Resident thesis workflow

- Name: Thesis record and submission
- Surface/module: `/dashboard/resident/thesis`
- What exists already:
  - active page
  - create thesis record path
  - submit thesis path
  - backend endpoints exist
- What is failing or unreliable:
  - not covered by current workflow gate
  - broader state lifecycle, validation, and post-submit behavior remain only lightly proven
- Severity: Medium
- Evidence:
  - `frontend/app/dashboard/resident/thesis/page.tsx`
  - `backend/sims/training/urls.py`
- Likely fix scope:
  - targeted resident thesis E2E/API verification

### 6. Resident workshops workflow

- Name: Workshop completions
- Surface/module: `/dashboard/resident/workshops`
- What exists already:
  - active page
  - completion creation and deletion UI
  - active backend endpoints
- What is failing or unreliable:
  - no workflow-grade runtime verification
  - relies on list/create/delete behavior without deeper contract assertions
- Severity: Medium
- Evidence:
  - `frontend/app/dashboard/resident/workshops/page.tsx`
  - `backend/sims/training/urls.py`
- Likely fix scope:
  - add end-to-end validation for create/delete and eligibility impact

### 7. Secondary academic read surfaces

- Name: Resident progress, supervisor resident progress, UTRMC eligibility monitor
- Surface/module:
  - `/dashboard/resident/progress`
  - `/dashboard/supervisor/residents/[id]/progress`
  - `/dashboard/utrmc/eligibility-monitoring`
- What exists already:
  - active pages
  - active summary/eligibility endpoints
  - data loads and renders from current APIs
- What is failing or unreliable:
  - page existence is stronger than runtime proof
  - only resident dashboard eligibility reasons are workflow-gated, not these secondary views
- Severity: Medium
- Evidence:
  - `frontend/app/dashboard/resident/progress/page.tsx`
  - `frontend/app/dashboard/utrmc/eligibility-monitoring/page.tsx`
  - `backend/sims/training/urls.py`
- Likely fix scope:
  - targeted browser checks and cross-surface consistency assertions

### 8. Frontend build/start harness

- Name: Frontend build/runtime delivery path
- Surface/module: build/test/start pipeline
- What exists already:
  - lint, `tsc`, Jest, build, and workflow-gate all pass
- What is failing or unreliable:
  - `next build` skips lint/type enforcement by config
  - `next start` warns that it is incompatible with `output: 'standalone'`
  - Jest reports a haste naming collision with `.next/standalone/package.json`
- Severity: Medium
- Evidence:
  - `frontend/next.config.mjs`
  - `frontend/package.json`
  - command outputs from `npm test -- --watch=false` and `npm run build`
- Likely fix scope:
  - align start script with standalone output
  - remove Jest haste collision
  - decide whether build should remain intentionally lenient or become stricter

## Working Perfectly

### 1. Forgot-password request path

- Name: Forgot password
- Surface/module: `/forgot-password`
- Verified scope:
  - real UI form submits
  - request succeeds through active API path
  - user sees a truthful success message
- Evidence of successful behavior:
  - workflow gate test `forgot-password submits via real UI path and returns success response`
  - current run passed in Playwright
- Any boundary notes:
  - this is password-reset request submission, not full email-delivery proof

### 2. Resident dashboard summary and eligibility reasons

- Name: Resident command dashboard
- Surface/module: `/dashboard/resident`
- Verified scope:
  - summary endpoint renders
  - current training/rotation summary renders
  - canonical eligibility reasons render in the browser
- Evidence of successful behavior:
  - workflow gate test `resident dashboard shows canonical eligibility reasons in browser`
  - page uses active summary endpoint
- Any boundary notes:
  - secondary progress pages are not in this “perfect” verdict

### 3. Leave workflow

- Name: Resident leave draft -> submit -> supervisor approve
- Surface/module:
  - `/dashboard/resident/schedule`
  - `/dashboard/supervisor`
- Verified scope:
  - resident creates draft
  - resident submits
  - supervisor approves
  - resident sees approved state
- Evidence of successful behavior:
  - workflow gate test `resident leave draft can be submitted and approved from supervisor dashboard`
  - backend logs showed create/submit/approve requests completing successfully
- Any boundary notes:
  - rejection/edit edge behavior was not the focus of this pass

### 4. Research supervisor-review workflow

- Name: Resident research submission + supervisor return path
- Surface/module:
  - `/dashboard/resident/research`
  - `/dashboard/supervisor/research-approvals`
- Verified scope:
  - pending supervisor review loads
  - canonical `resident_name` renders
  - supervisor return action succeeds
  - UI updates correctly after return
- Evidence of successful behavior:
  - workflow gate test `supervisor approvals renders resident_name and supports supervisor-return flow`
  - contract drift tests for research return passed
- Any boundary notes:
  - broader university acceptance lifecycle was not re-proven in browser in this pass

### 5. Rotation lifecycle

- Name: Rotation workflow
- Surface/module:
  - `/dashboard/utrmc`
  - `/dashboard/resident/schedule`
  - `/dashboard/supervisor`
- Verified scope:
  - UTRMC creates draft
  - resident submits
  - supervisor approves
  - UTRMC activates and completes
  - resident sees completed state
- Evidence of successful behavior:
  - workflow gate test `rotation workflow closes across UTRMC overview, resident schedule, and supervisor dashboard`
  - canonical migration gate passed
- Any boundary notes:
  - this verdict is for the promoted active lifecycle, not every possible rotation edge case

### 6. Postings lifecycle

- Name: Deputation postings
- Surface/module:
  - `/dashboard/resident/postings`
  - `/dashboard/utrmc/postings`
- Verified scope:
  - resident creates request
  - UTRMC approves
  - UTRMC completes
  - resident sees resulting state
- Evidence of successful behavior:
  - workflow gate test `posting workflow remains truthful from resident submission through UTRMC completion`
  - page/API contract now aligns on uppercase statuses and required payload shape
- Any boundary notes:
  - rejected-follow-up behavior remains less deeply exercised than the happy path
