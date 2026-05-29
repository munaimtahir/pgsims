# Feature Status Matrix

Classification key: Done / Partial / Broken / Placeholder / Missing / Unverified / Blocked.

| Module | Feature | Intended purpose | Frontend | Backend | Data model | Runtime status | Classification | Evidence |
|---|---|---|---|---|---|---|---|---|
| Auth | JWT login/profile/reset | Authenticate and manage session | Present (`/login`, auth store) | Present (`/api/auth/*`) | User model + roles | API/tests pass; UI not e2e-verified in this run | Partial | `frontend/app/login/page.tsx`, `backend/sims/users/api_urls.py`, backend tests pass |
| Userbase | Hospitals/Departments/Matrix | Org graph management | Present (UTRMC pages) | Present (viewsets/router) | Canonical models present | Backend tests pass | Partial | `userbase_views.py`, `userbase_urls.py`, UTRMC pages |
| Userbase | Users CRUD | User admin and role assignment | Present (`/dashboard/utrmc/users`) | Present (`/api/users/*`) | `users.User` + profiles | Works by backend tests; frontend lint issues | Partial | `frontend/app/dashboard/utrmc/users/page.tsx`, `api_user_urls.py` |
| Supervision | Supervisor links/HOD assignments | Supervision graph | Present | Present | `SupervisorResidentLink`, `HODAssignment` | Backend tests pass | Partial | `userbase_views.py`, UTRMC supervision/hod pages |
| Training | Programs/policy/milestones/templates | Academic governance | Present (`/utrmc/programs`) | Present | `training` models | Backend pass; frontend lint failing | Partial | `training/views.py`, `training.ts`, programs page |
| Training | Research workflow | Resident proposal + supervisor review | Present (resident + supervisor pages) | Present | `ResidentResearchProject` | Backend tests pass; page uses some broad catches | Partial | `training/views.py`, resident/supervisor research pages |
| Training | Thesis workflow | Thesis submit/track | Present page | Present endpoints | `ResidentThesis` | Unverified end-to-end | Unverified | `resident/thesis page`, `training.ts` |
| Training | Workshops workflow | Completion recording and eligibility inputs | Present page | Present endpoints | Workshop/completion models | Unverified end-to-end | Unverified | `resident/workshops page`, `training/views.py` |
| Training | Rotations workflow | Submit/approve/manage postings | Partial UI exposure | Full backend state actions | Rotation models | Backend role workflow tests pass | Partial | `training/views.py` actions, tests pass |
| Training | Leave workflow | Leave request and approval | Partial UI exposure | Present | Leave model | Backend tests pass | Partial | `training/views.py` leave actions |
| Training | Deputation postings | Resident request + admin handling | Present (resident + UTRMC pages) | Present | `DeputationPosting` | Unverified e2e | Unverified | postings pages + `training.ts` |
| Notifications | In-app and preferences | Delivery/read state | No major dedicated page, API client present | Present | Notification models/service | Backend tests pass | Partial | `notifications/services.py`, `notifications/urls.py` |
| Audit | Activity/reports | Traceability/reporting | API client present | Present | Audit models | Backend checks pass | Unverified | `audit/urls.py`, `audit/models.py` |
| Bulk | Imports/exports | Administrative data operations | API client present | Present routes | Bulk models | Unverified; docs mention pending pieces | Unverified | `bulk/urls.py`, docs integration notes |
| Logbook | PG submit/review lifecycle | Core clinical workflow | Missing App Router pages referenced by tests | Legacy backend APIs exist but not active in root urls | Legacy logbook models | Contract/runtime mismatch | Broken | `API_CONTRACT.md`, no frontend page, no include in root `urls.py` |
| Cases | Case submission/review | Another core workflow | Referenced in regression docs only | Legacy module present | Legacy models | Not wired in active runtime path | Placeholder | `frontend/e2e/regression/README.md`, `_legacy/cases` |
| Analytics dashboard | Admin live insights | Observability dashboards | Referenced in tests/docs | Legacy analytics module exists | Legacy analytics models | Not proven in active frontend routes | Blocked | regression docs + no App Router analytics page |
