> Current verification (2026-09-15): parity is merged to `main`; final signed release metadata is
> version 1.1.9/code9 because the owner confirmed code9 has not been uploaded to Play. Android 41
> unit tests, 7 synthetic emulator tests,
> process-death recovery and isolated Django 929 tests pass; PostgreSQL concurrency passes separately.
> Production remains verified 1.1.9. The historical baseline/version/failure sections below are
> retained as roadmap history; they do not supersede the current reconciliation report or
> `SPRINT_STATE.md`. Signed 1.1.9/code9 APK/AAB and isolated backend gates pass. The earlier
> 1.1.10/code10 emulator evidence remains valid because the retarget changed only release metadata;
> the final code9 debug build is also installed on `pgsims` and its default instrumentation run
> passes (29 tests). Authenticated four-role shell and recovery results are recorded in the current
> acceptance reports.

# Android feature-parity review and development roadmap

Review date: **2026-09-15** (Asia/Karachi). Last evidence reconciliation: **2026-09-15**.

## Baseline and evidence limits

- Checkout: `/media/munaim/shared1/Documents/github/pgsims`; branch: `main`.
- HEAD, local `main`, local `remediation/pgsims-final-production-readiness`, and their recorded origin refs: `13f1bb752c5b0e1dff9d747b3a7c738c0bab6c1d`. `git diff main remediation/pgsims-final-production-readiness` is empty. The plan's newer-remediation premise has been superseded in this checkout. No fetch was performed; remote server branch state is not independently confirmed.
- Recent shared history includes `3b4a6f0` (offline recovery/notifications), `46eccbd` (release handoff), and `13f1bb7` (production verification documentation). An existing agent worktree at `f4e1938` is outside this comparison and was not modified.
- Working tree was clean at review start. Subsequent release verification added Android instrumentation, evidence files, documentation changes, and a worktree candidate version bump. Those changes are now reflected as evidence where the canonical test report supports them; they remain uncommitted and are not treated as merged or released. No application feature was implemented as part of this documentation update.
- Source reachability was traced from Next pages/shared components and Compose navigation to clients and mounted backend URLs. Later authenticated emulator and isolated-backend results are incorporated from the canonical evidence files linked below. Artifact signature, current remote branch state, live proxy routing and shared-database identity were not independently reverified by this documentation update.
- Historical matrices under `docs/discovery/20260909_pgrsims_unified_platform_baseline/` and `docs/PORTAL_WEB_PARITY_MATRIX.md` are supporting history, not acceptance evidence. Current source controls this inventory.
- [Update 0 verdict](docs/implementation/20260626_update_0_universal_identity_dynamic_onboarding/FINAL_VERDICT.md) records GO. Later clean-room workflows already exist; this roadmap inventories them without implementing a new brick or reviving retired modules.

## Architecture and production requirement

Retain Kotlin/Jetpack Compose, `:app-companion`, and package/application ID `pk.vexel.pgrcompanion` (debug suffix `.debug`). The tested emulator application was version 1.1.7/code 7. [Build configuration](android/app-companion/build.gradle.kts) currently contains an uncommitted 1.1.8/code 8 candidate plus release-acceptance instrumentation dependencies; that candidate must be rebuilt and installed before its behavior is accepted. SDK 26 minimum/36 target, Retrofit/OkHttp, and `FCM_ENABLED=false` remain unchanged. The web client is Next.js; Django APIs and canonical services own identity, authorization, state transitions, audit and persistence.

Android must use the **same production Django services and PostgreSQL database as web**. Do not create a mobile database authority or parallel identity/workflow service. Local encrypted queues are temporary delivery state only. [Android configuration](android/app-companion/build.gradle.kts) points at `https://android.pgsims.alshifalab.pk/`; [web proxy source](deploy/Caddyfile.pgsims) sends API traffic for `pgsims.alshifalab.pk` / `pg.fmu.edu.pk` to port 8014 and frontend traffic to 8082. The checked-in proxy does not itself establish the current Android hostname mapping. [Earlier deployment discovery](docs/implementation/20260908_pgr_companion_production_resident_expansion/DISCOVERY.md) reports the Android host behind the port-8014 image-backed service. Together these support the intended shared service; they do not prove today's DNS/proxy/image/database equality. Stage 0 must record both host routes, running image revision and database service identity without exposing credentials; Stage 6 must verify the same record across clients.

Only roles ADMIN, RESIDENT, SUPERVISOR and SUPPORT_STAFF are permitted. Historical strings in existing URL paths are transport compatibility, not extra identities. Backend permission checks remain authoritative: web navigation (`frontend/lib/navRegistry.ts`) is not a grant. In particular SUPPORT_STAFF has only dashboard/profile web navigation; some backend reads are broader, while academic workflow/report endpoints explicitly deny staff. Do not infer administrative rights or user creation rights from a successful login.

Two training record families remain: `academics.ResidentTrainingRecord` and `training.ResidentTrainingRecord`. Academic logbook/evaluations use `/api/academics/`; leave/rotations use training APIs. Never interchange profile IDs, user IDs, training-record IDs or review-queue IDs. Use `users/services.py`, profile requirement registry and existing academics/training services rather than recreating rules in Android.

## Matrix conventions and evidence index

`B` means source is present in **both local main and remediation at the baseline**; `—` means no Android action. Neither means released or runtime verified. Matrix QA marker **Q** means the row still needs its complete acceptance test unless a narrower result appears in the current verification section. Stage is the development/closure stage, not proof of readiness.

- `[x] ~~Built action~~`: reachable UI plus matching API wiring exists for that narrowly named action.
- `[ ] Pending action`: absent, incomplete, or incompatible. A callable repository method alone is not built UI.
- Each pending row's last column states its dependency and observable acceptance criterion. Q applies independently to built and pending actions.

Android source aliases (all under `android/app-companion/src/main/java/pk/vexel/pgrcompanion/`):

- **I**: [InstitutionalScreen.kt](android/app-companion/src/main/java/pk/vexel/pgrcompanion/InstitutionalScreen.kt).
- **R**: [InstitutionalRepository.kt](android/app-companion/src/main/java/pk/vexel/pgrcompanion/InstitutionalRepository.kt).
- **L**: [ResidentWorkflowScreens.kt](android/app-companion/src/main/java/pk/vexel/pgrcompanion/ResidentWorkflowScreens.kt).
- **E**: [ResidentAcademicScreens.kt](android/app-companion/src/main/java/pk/vexel/pgrcompanion/ResidentAcademicScreens.kt).
- **S**: [SupervisorScreens.kt](android/app-companion/src/main/java/pk/vexel/pgrcompanion/SupervisorScreens.kt).
- **W**: [SupervisorWorkflowScreens.kt](android/app-companion/src/main/java/pk/vexel/pgrcompanion/SupervisorWorkflowScreens.kt).
- **O**: [Onboarding.kt](android/app-companion/src/main/java/pk/vexel/pgrcompanion/Onboarding.kt).
- **P**: [ProgressReporting.kt](android/app-companion/src/main/java/pk/vexel/pgrcompanion/ProgressReporting.kt).
- **N**: [NotificationCenter.kt](android/app-companion/src/main/java/pk/vexel/pgrcompanion/NotificationCenter.kt).
- **D**: [OfflineDraftStore.kt](android/app-companion/src/main/java/pk/vexel/pgrcompanion/OfflineDraftStore.kt).
- **U**: [OfflineUploadStore.kt](android/app-companion/src/main/java/pk/vexel/pgrcompanion/OfflineUploadStore.kt).
- **J**: [OfflineDraftSyncWorker.kt](android/app-companion/src/main/java/pk/vexel/pgrcompanion/OfflineDraftSyncWorker.kt).

`I.InstitutionalWorkspace` is the reachable root; `ConnectedPane` opens L/E/P/N and profile/documents; `SupervisorPane` opens S/W/N. R is the Retrofit interface plus repository callbacks. Backend route anchors: [auth](backend/sims/users/api_urls.py), [identity](backend/sims/users/userbase_urls.py), [academics](backend/sims/academics/workflow_urls.py), [training](backend/sims/training/urls.py), [supervision](backend/sims/supervision/urls.py), [bulk](backend/sims/bulk/urls.py), [backup](backend/sims/backup_center/urls.py). Their mounted prefixes are established in [project URLs](backend/sims_project/urls.py). Web paths below resolve to `frontend/app/<path>/page.tsx` unless a component is explicitly named. API paths start at `/api/`; `{id}` denotes the actual resource identifier.

## Role-by-role action matrix


### Identity and shared access

| Capability / implementation status | Role | Web source | Backend endpoint | Android evidence | Branch | QA | Stage | Dependency and acceptance |
|---|---|---|---|---|---|---|---|---|
| [x] ~~Sign in; restore session; sign out~~ | All | login; components/auth/ProtectedRoute | `auth/login/; auth/me/; auth/refresh/; auth/logout/` | I.SignInPane/InstitutionalWorkspace → R.login/snapshot/logout | B | Q | 0 | Q: invalid credentials, revoked/expired tokens and process restart; restoration is token restoration, not cached workflow data |
| [x] ~~Change password (forced and voluntary)~~ | All | change-password; dashboard/change-password | `auth/change-password/` | IdentityScreens.ChangePasswordScreen → R.changePassword → authoritative me refresh | F | Q | 1 | MockWebServer and route-precedence coverage pass; authenticated runtime remains in the QA matrix |
| [x] ~~Request and confirm password reset~~ | All | forgot-password; reset-password/[uid]/[token] | `auth/password-reset/; auth/password-reset/confirm/` | IdentityScreens request/confirm screens plus HTTPS Android app link | F | Q | 1 | Anonymous endpoint contract and cold deep-link rendering pass; live mail delivery/used-link runtime remains deferred |
| [x] ~~Enforce backend next route and render all required profile fields~~ | All | complete-profile; components/auth/ProtectedRoute | `auth/me/; auth/complete-profile/; identity/options/` | InstitutionalWorkspace uses authoritativeRoute; DynamicProfileCompletionScreen renders backend fields/options | F | Q | 1 | Password → required profile → role workspace precedence and text/email/phone/number/date/select rendering have unit/API coverage |
| [x] ~~View/save resident text profile fields~~ | RESIDENT | complete-profile; profile | `auth/onboarding/ GET/PATCH` | I.OnboardingSection → R.update; O.RESIDENT_EDITABLE | B | Q | 1 | Q: full_name, phone, email, registration_no, cnic, notes persist; this excludes reference/date/declaration completion |
| [ ] Complete resident references, dates and declaration | RESIDENT | complete-profile | `identity/options/; auth/onboarding/; resident-onboarding/state/` | Declaration acceptance is native and registry-required reference/date fields render dynamically; administrative onboarding references/dates remain read-only | F | Q | 1 | Finish only backend-permitted administrative edits; declaration and required-field refresh are wired |
| [x] ~~Native own-profile and dashboard navigation~~ | ADMIN, SUPPORT_STAFF, SUPERVISOR | profile; dashboard; dashboard/utrmc; dashboard/supervisor | `auth/me/; auth/complete-profile/` | AdminScreens, SupervisorPane and SupportStaffPane → OwnProfileEditor | F | Q | 1 | All four roles reach their own allowlisted profile; staff has no user-management surface |
| [x] ~~Complete Inbox UI, read/unread and preferences for RESIDENT and SUPERVISOR~~ | RESIDENT, SUPERVISOR | shared notification UI/client frontend/lib/api/notifications.ts | `notifications/; notifications/unread-count/; mark-read/; mark-unread/; preferences/ (under notifications/)` | Shared NotificationCenter destination; single parent scroll removes the nested-scroll crash | F | Q | 0 | Build/instrumentation pass; authenticated recipient-isolation runtime remains in the QA matrix; FCM remains disabled |
| [x] ~~Inbox for ADMIN/staff and exact-record notification navigation~~ | All | shared notification UI | `notifications/; canonical target detail API` | All role shells expose NotificationCenter; kind + resource ID fetches the authorized detail and stale/forbidden targets show a recoverable error | F | Q | 1 | Exact leave/logbook/evaluation/rotation targets are wired and contract-tested; unsupported target kinds fail safely |

### Resident workflows

| Capability / implementation status | Role | Web source | Backend endpoint | Android evidence | Branch | QA | Stage | Dependency and acceptance |
|---|---|---|---|---|---|---|---|---|
| [x] ~~Read current training, supervisor, rotation history/details~~ | RESIDENT | dashboard/resident; academics/rotation-assignments/[id] | `resident-training/; supervision/assignments/; my/rotations/; residents/me/summary/` | I → L.TrainingDashboard/RotationDetail → R.snapshot | B | Q | 2 | Q: empty/multiple training records and current assignment; snapshot is first-page limited |
| [x] ~~List logbook and view details/feedback~~ | RESIDENT | academics/logbook; academics/logbook/[id] | `academics/logbook-entries/` | I → L.LogbookScreen/LogbookDetailDialog → R.logbook | B | Q | 2 | Q: own records only; full details/pagination still pending |
| [x] ~~Create basic logbook draft~~ | RESIDENT | academics/logbook/new | `academics/logbook-entries/ POST` | L.LogbookEntryDialog → I → R.createLogbook | B | Q | 2 | Q: category, date, title, reflection; not full payload parity |
| [x] ~~Edit title/reflection and submit draft or returned logbook~~ | RESIDENT | academics/logbook/[id] | `academics/logbook-entries/{id}/ PATCH; {id}/submit/` | L.LogbookDetailDialog → I → R.updateLogbook/submitLogbook | B | Q | 2 | Q: allowed transitions and preservation of other fields |
| [x] ~~Full logbook form and nested procedure~~ | RESIDENT | academics/logbook/new | `academics/options/; academics/logbook-entries/` | ResidentAcademicScreens full form → AcademicLogbookPayload with supervisor, period, case and procedure record | F | Q | 2 | Reachable create payload is contract-tested; authenticated round-trip and full-field edit preservation remain runtime QA |
| [x] ~~Cancel logbook~~ | RESIDENT | academics/logbook/[id] | `academics/logbook-entries/{id}/cancel/` | Logbook detail Cancel → R.cancelLogbook | F | Q | 2 | Backend transition/permission remains authoritative |
| [x] ~~List and view evaluations; create template/comments draft; submit draft~~ | RESIDENT | academics/evaluations; academics/evaluations/new; academics/evaluations/[id] | `academics/evaluation-templates/; academics/evaluation-submissions/; {id}/submit/` | I → E.EvaluationsScreen/CreateDialog/DetailDialog → R | B | Q | 2 | Q: basic draft only; templates needing responses may not support complete workflow |
| [x] ~~Dynamic evaluation responses and supervisor/period selection~~ | RESIDENT | academics/evaluations/new | `academics/options/; academics/evaluation-submissions/` | Evaluation create renders template text/numeric fields and supervisor/period selectors into response payloads | F | Q | 2 | Reachable payload wiring is covered; live template variants remain runtime QA |
| [ ] Edit/resubmit returned evaluation | RESIDENT | academics/evaluations/[id] (web revision completeness also needs QA) | `academics/evaluation-submissions/{id}/ PATCH; {id}/submit/` | R.updateEvaluation exists but no E editor; Submit only DRAFT | B | Q | 2 | Revision contract; returned responses editable without loss and resubmitted to same record |
| [x] ~~Cancel evaluation~~ | RESIDENT | academics/evaluations/[id] | `academics/evaluation-submissions/{id}/cancel/` | Evaluation detail Cancel → R.cancelEvaluation | F | Q | 2 | Backend state machine remains authoritative |
| [x] ~~List/detail leave; create draft; submit~~ | RESIDENT | academics/leave-requests; new; [id] | `my/leaves/; leaves/ POST; leaves/{id}/submit/` | I → E.LeaveRequestsScreen/LeaveRequestDialog/LeaveDetailDialog → R | B | Q | 2 | Q: training ID/type/date/reason, overlap errors; no reachable edit UI |
| [ ] Edit leave where backend permits | RESIDENT | academics/leave-requests/[id] (no current web editor) | `leaves/{id}/ PATCH` | R.updateLeave has no UI caller | B | Q | 2 | Backend-only editing extension; verify editable states before adding editor, preserve same record |
| [x] ~~Document list/status/remarks; upload/replace; retry/discard queued upload~~ | RESIDENT | dashboard/resident/documents | `resident-documents/; resident-documents/{id}/upload/` | I requirements/picker → U/J → R.upload | B | Q | 2 | Q: encrypted queue and multipart source exist; verify upload/replace after reconnect and refresh |
| [x] ~~Defer document~~ | RESIDENT | dashboard/resident/documents | `resident-documents/{id}/defer/` | Requirements action → R.deferDocument and refresh | F | Q | 2 | Backend permission contract remains authoritative; authenticated persistence remains runtime QA |
| [x] ~~Show mobile progress summary~~ | RESIDENT | academics/my-progress; dashboard/resident | `residents/me/summary/ plus snapshot lists` | I → P.ResidentProgressReport → R.snapshot | B | Q | 2 | Q: limited snapshot counts, not canonical monitoring/report totals |
| [ ] Canonical academic progress and report detail | RESIDENT | academics/my-progress; academics/reports/logbook; academics/reports/evaluations | `academics/my-progress/; academics/monitoring/my-progress/; academics/reports/{logbook,evaluations}/` | P now renders canonical my-progress and monitoring responses; logbook/evaluation report detail and multi-page QA remain pending | F | Q | 2 | Finish canonical report payloads/filters and prove totals across more than one page |

### Supervisor workflows

| Capability / implementation status | Role | Web source | Backend endpoint | Android evidence | Branch | QA | Stage | Dependency and acceptance |
|---|---|---|---|---|---|---|---|---|
| [x] ~~Dashboard, assigned residents, resident progress detail~~ | SUPERVISOR | dashboard/supervisor (old progress subroute redirects) | `supervisors/me/summary/; academics/monitoring/supervisor-dashboard/; supervisors/residents/{id}/progress/` | I → S.SupervisorPane/resident progress → R | B | Q | 3 | Q: assigned-only scope and ID semantics; academic web summary equivalence remains incomplete |
| [x] ~~Read logbook queue/details~~ | SUPERVISOR | academics/logbook | `academics/logbook-entries/` | S → W.SupervisorWorkflowQueueScreen → R | B | Q | 3 | Q: queue filtering and pagination; only workflow resource IDs may be used |
| [x] ~~Logbook approval and return/reject actions supported by mobile~~ | SUPERVISOR | academics/logbook/[id]/review | `academics/logbook-entries/; verify/; return_revision/; reject/` | W runAction/ReasonConfirmDialog → R; approval sends empty comments | B | Q | 3 | Q: basic actions only; leave has no return button; evaluation scoring and approval feedback pending |
| [x] ~~Read leave queue/details~~ | SUPERVISOR | academics/leave-requests | `utrmc/approvals/leaves/` | S → W.SupervisorWorkflowQueueScreen → R | B | Q | 3 | Q: queue filtering and pagination; only workflow resource IDs may be used |
| [x] ~~Leave approval and return/reject actions supported by mobile~~ | SUPERVISOR | academics/leave-requests/[id] | `utrmc/approvals/leaves/; leaves/{id}/approve/; reject/` | W runAction/ReasonConfirmDialog → R; approval sends empty comments | B | Q | 3 | Q: basic actions only; leave has no return button; evaluation scoring and approval feedback pending |
| [x] ~~Read evaluation queue/details~~ | SUPERVISOR | academics/evaluations | `academics/evaluation-submissions/` | S → W.SupervisorWorkflowQueueScreen → R | B | Q | 3 | Q: queue filtering and pagination; only workflow resource IDs may be used |
| [x] ~~Evaluation approval and return/reject actions supported by mobile~~ | SUPERVISOR | academics/evaluations/[id]/review | `academics/evaluation-submissions/; approve/; return_revision/; reject/` | W runAction/ReasonConfirmDialog → R; approval sends empty comments | B | Q | 3 | Q: basic actions only; leave has no return button; evaluation scoring and approval feedback pending |
| [x] ~~Read rotation queue~~ | SUPERVISOR | academics/rotation-assignments | `supervisor/rotations/pending/` | S → W → R.supervisorRotationQueue | B | Q | 3 | Q: active assignments and review status filtering |
| [x] ~~Match current rotation application review~~ | SUPERVISOR | academics/rotation-assignments/[id] | `rotations/{id}/review-application/` | W/R approve/defer/reject through the canonical review-application action | F | Q | 3 | Canonical payload is covered by MockWebServer; authenticated effects remain runtime QA |
| [x] ~~Complete review details, approval feedback and evaluation scoring/start review~~ | SUPERVISOR | academics/logbook/[id]/review; academics/evaluations/[id]/review | `logbook-entries verify/; evaluation-submissions start_review/, approve/ under academics/` | Detail dialogs show all responses/procedure data; evaluation review captures score/max/comments and starts review | F | Q | 3 | Reachable lifecycle is wired; transition and assigned-resident runtime QA remains pending |
| [ ] Academic review queue/status and workload | SUPERVISOR | academics/review-queue; academics/supervisor-workload | `academics/review-queue/; academics/supervisor-workload/` | W workflow queues are not generic review-queue parity | B | Q | 3 | Academic queue/workload contract; status updates and assigned-resident counts match web |

### Administration

| Capability / implementation status | Role | Web source | Backend endpoint | Android evidence | Branch | QA | Stage | Dependency and acceptance |
|---|---|---|---|---|---|---|---|---|
| [ ] Dashboard counts and academic/supervision overview | ADMIN | dashboard/utrmc; academics; supervision | `users/?page_size=1; academics/overview/; supervision/data-quality/; supervision/assignments/` | I restricted pane | B | Q | 4 | Backend counts/overview; render complete totals and authorized navigation |
| [x] ~~Universal user creation for four roles~~ | ADMIN | users/new | `users/ POST; identity/options/` | AdminScreens create form exposes only ADMIN/RESIDENT/SUPERVISOR/SUPPORT_STAFF → R.createUser | F | Q | 4 | Four-role payload and backend identity transaction are tested; authenticated device creation remains runtime QA |
| [ ] Universal and four role directories/search/filter/details | ADMIN | users; residents; supervisors; support-staff; admins; role [id] pages | `users/; residents/{id}/; supervisors/{id}/; support-staff/{id}/; users/{id}/` | Universal users directory has server search/role filter, count/next paging and details; dedicated role directories remain pending | F | Q | 4 | Finish role-specific directories and authenticated multi-page QA without duplicating creation logic |
| [ ] Profile management, archive/completion/reset surfaces | ADMIN | role detail pages currently mostly read-only; users/new | `users/{id}/; role profile APIs; service actions subject to contract` | Absent; broader intended management is not all active web UI | — | Q | 4 | Stage 0 distinguish API-supported writes from missing contracts; no invented archive/reset endpoint; implement only agreed canonical actions and audits |
| [ ] Document requirement list/create/update/activate/deactivate | ADMIN | residents/document-requirements | `resident-document-requirements/; {id}/` | Absent | — | Q | 4 | Requirement serializer; same applicability/order/required fields and affected-resident behavior |
| [ ] Resolve pending supervisor name; create/link supervisor | ADMIN | admin/pending-supervisor-links | `pending-supervisor-links/; {id}/resolve/; {id}/create-supervisor/` | Absent | — | Q | 4 | Shared identity service; correct resident link, no duplicate identity |
| [ ] Supervision list/detail/create/end/change primary | ADMIN | supervision/assignments; new; [id]; supervision | `supervision/assignments/; {id}/end/; supervision/change-primary/; supervision/options/` | Resident assignment read only | B | Q | 4 | Supervision services; dates and reasons validated, old primary ended and new assignment visible |
| [ ] Training records: list/create/detail/close | ADMIN | academics/training-records | `academics/training-records/; {id}/close/; academics/options/` | Absent | — | Q | 4 | Academic model/serializer/options; submitted form fields, relationships and resulting list/detail match web |
| [ ] Periods: list/create | ADMIN | academics/periods | `academics/periods/; academics/options/` | Absent | — | Q | 4 | Academic model/serializer/options; submitted form fields, relationships and resulting list/detail match web |
| [ ] Rotation templates: list/create | ADMIN | academics/rotation-templates | `academics/rotation-templates/; academics/options/` | Absent | — | Q | 4 | Academic model/serializer/options; submitted form fields, relationships and resulting list/detail match web |
| [ ] Evaluation templates: list/create | ADMIN | academics/evaluation-templates | `academics/evaluation-templates/; academics/options/` | Absent | — | Q | 4 | Academic model/serializer/options; submitted form fields, relationships and resulting list/detail match web |
| [ ] Logbook categories: list/create | ADMIN | academics/logbook-categories | `academics/logbook-categories/; academics/options/` | Absent | — | Q | 4 | Academic model/serializer/options; submitted form fields, relationships and resulting list/detail match web |
| [ ] Generic review queue: list/create/update status | ADMIN | academics/review-queue | `academics/review-queue/; {id}/; academics/options/` | Absent | — | Q | 4 | Academic model/serializer/options; submitted form fields, relationships and resulting list/detail match web |
| [ ] Rotation create, training-record setup, submit, approve, activate, complete | ADMIN | academics/rotation-assignments/new; [id] | `resident-training/; rotations/; {id}/submit/; {id}/review-application/; {id}/utrmc-approve/; {id}/activate/; {id}/complete/` | Absent | — | Q | 4 | Training service and hospital-department options; each permitted transition and reason persists and refreshes both clients |
| [ ] Leave list/create/detail/submit/approve/reject and academic review actions | ADMIN | academics/leave-requests; academics/logbook; academics/evaluations | `leaves/ and actions; academics/logbook-entries/ and evaluation-submissions/ actions` | Resident/supervisor UI not reachable as ADMIN | B | Q | 4 | Per-action permissions; administrative actions match web and audit, no staff elevation |

### Operations

| Capability / implementation status | Role | Web source | Backend endpoint | Android evidence | Branch | QA | Stage | Dependency and acceptance |
|---|---|---|---|---|---|---|---|---|
| [ ] Master setup workspace and standard/flexible import | ADMIN | masters → components/utrmc/BulkSetupWorkspace | `bulk/templates/{entity}/; bulk/import/{entity}/{dry-run,apply}/; flexible API (appendix)` | Absent | — | Q | 5 | Bulk validation and entity contracts; hospitals, departments, matrix, supervisors, residents, supervision links, rotations, programs, sessions preview and apply with row errors |
| [ ] Master dataset/template export and supervision CSV import | ADMIN | masters; supervision/import | `bulk/exports/{entity}/; bulk/templates/{entity}/; supervision/import/` | Absent | — | Q | 5 | Multipart/blob contracts; CSV/XLSX export correct, dry-run does not mutate, explicit apply matches preview |
| [ ] Data quality, monitoring and workflow overview | ADMIN | academics/data-quality; workflow-data-quality; workflow-overview; monitoring; supervision/data-quality | `academics/data-quality/; workflow-data-quality/; admin-workflow-overview/; monitoring/{admin-dashboard,departments,programs,sessions}/; supervision/data-quality/` | Absent | — | Q | 5 | Canonical summary endpoints; filters/counts and drilldowns match web; seed-workflows button disposition below |
| [ ] resident-progress report/filter and CSV export / detail | ADMIN, SUPERVISOR | academics/reports/resident-progress | `academics/reports/resident-progress/; export.csv; {id}/` | No canonical report API or authenticated export UI | B | Q | 5 | Report RBAC/filter contract; same filtered records/counts/CSV as web, correct download authorization |
| [ ] supervisor-workload report/filter and CSV export / detail | ADMIN | academics/reports/supervisor-workload | `academics/reports/supervisor-workload/; export.csv; {id}/` | No canonical report API or authenticated export UI | B | Q | 5 | Report RBAC/filter contract; same filtered records/counts/CSV as web, correct download authorization |
| [ ] logbook report/filter and CSV export | ADMIN, SUPERVISOR, RESIDENT | academics/reports/logbook | `academics/reports/logbook/; export.csv` | No canonical report API or authenticated export UI | B | Q | 5 | Report RBAC/filter contract; same filtered records/counts/CSV as web, correct download authorization |
| [ ] evaluations report/filter and CSV export | ADMIN, SUPERVISOR, RESIDENT | academics/reports/evaluations | `academics/reports/evaluations/; export.csv` | No canonical report API or authenticated export UI | B | Q | 5 | Report RBAC/filter contract; same filtered records/counts/CSV as web, correct download authorization |
| [ ] data-quality report/filter and CSV export | ADMIN | academics/reports/data-quality | `academics/reports/data-quality/; export.csv` | No canonical report API or authenticated export UI | B | Q | 5 | Report RBAC/filter contract; same filtered records/counts/CSV as web, correct download authorization |
| [ ] List backups, restore jobs and audit | ADMIN | dashboard/utrmc/backup; components/backup | `backup_center/backups/; restores/; audit-logs/` | Absent | — | Q | 5 | Existing backup contracts; preserve staged validation/password/typed confirmation and audit; verify destructive behavior only in disposable environment |
| [ ] Create routine/disaster backup | ADMIN | dashboard/utrmc/backup; components/backup | `backup_center/backups/create-routine/; backups/create-disaster/` | Absent | — | Q | 5 | Existing backup contracts; preserve staged validation/password/typed confirmation and audit; verify destructive behavior only in disposable environment |
| [ ] Download, validate and delete backup | ADMIN | dashboard/utrmc/backup; components/backup | `backup_center/backups/{id}/{download,validate,delete}/` | Absent | — | Q | 5 | Existing backup contracts; preserve staged validation/password/typed confirmation and audit; verify destructive behavior only in disposable environment |
| [ ] Upload restore, validate, dry-run, confirm | ADMIN | dashboard/utrmc/backup; components/backup | `backup_center/restores/upload/; restores/{id}/{validate,dry-run,confirm}/` | Absent | — | Q | 5 | Existing backup contracts; preserve staged validation/password/typed confirmation and audit; verify destructive behavior only in disposable environment |
| [x] Complete pagination/filter/search/error recovery for lists | All permitted roles | directory, academic list/report and bulk components | `Each list endpoint with server query parameters/next/count` | Repository follows DRF `next` links for current resident, supervisor, admin setup and notification lists; UI filter/error acceptance remains runtime pending | B | Q | 5 | Unit coverage added; authenticated >page-size data and stable ordering still require emulator verification |

### Release foundations

| Capability / implementation status | Role | Web source | Backend endpoint | Android evidence | Branch | QA | Stage | Dependency and acceptance |
|---|---|---|---|---|---|---|---|---|
| [x] ~~Queue offline leave/logbook create drafts and recover document uploads~~ | RESIDENT | Mobile resilience extension | `leaves/; academics/logbook-entries/; resident-documents/{id}/upload/` | I/E → D/U; CompanionApplication → J → R | B | Q | 6 | Q: create-only draft queues; updates/reviews not declared offline-capable |
| [ ] Finish account isolation, conflict/retry and lifecycle behavior | All | Cross-client acceptance | `auth/session and affected workflow contracts` | Draft/upload metadata is synchronous, owner-bound and stateful; orphan files are removed; leave/logbook request IDs persist and server retries deduplicate; upload retry/discard is visible | F | Q | 6 | Durable/orphan instrumentation and leave API retry coverage pass; live duplicate-worker device acceptance and foreground draft-state reconciliation remain pending |

### Additional active actions and conditional surfaces

| Capability / implementation status | Role | Web source | Backend endpoint | Android evidence | Branch | QA | Stage | Dependency and acceptance |
|---|---|---|---|---|---|---|---|---|
| [ ] Flexible file header detection and column mapping | ADMIN | `frontend/components/utrmc/FlexibleMappingImport.tsx` | `/api/bulk/flexible/schemas/`, `detect-headers/`, `validate-mapping/` | Absent | — | Q | 5 | Match file columns to canonical entity schema; show per-field errors before dry-run. |
| [ ] Save/load/delete mapping presets | ADMIN | same component | `/api/bulk/flexible/presets/`, `{id}/` | Absent | — | Q | 5 | Preserve entity-specific mappings and backend ownership permissions. |
| [ ] Flexible dry-run and apply | ADMIN | same component | `/api/bulk/flexible/dry-run/`, `apply/` | Absent | — | Q | 5 | Same uploaded file/mapping/options in preview and apply; show row outcomes, avoid duplicate apply. |
| [ ] Academic workflow seed button disposition | ADMIN | `frontend/app/academics/workflow-overview/page.tsx` | `/api/academics/seed-workflows/` POST | Absent | — | Q | 0 | Existing reachable web action, not silently omitted. Decide production eligibility with backend owner; retain only if authorized as a production workflow, otherwise explicitly exclude demo seeding from release. Never run it during this review. |
| [ ] Existing cloud-backup panel disposition | ADMIN, backend backup permission | `frontend/components/backup/GoogleDrivePanel.tsx`, `BackupList.tsx` | `/api/backup_center/google-drive/{status,list,connect,disconnect,health-check,create-folder}/`; backup `{id}/google-drive/{upload,verify,download}/` | Absent | — | Q | 0 | Web source exists, controls depend on configured/enabled/connected state. Production enabled state unverified. Explicitly excluded from Android implementation under no-new-integrations scope; record exclusion in acceptance, do not revive/connect an integration. |

## Backend-only, redirects and intended extensions

These are dispositions, not assertions of absent backend code:

- Resident research/synopsis, thesis, workshops, eligibility, postings and schedule routes under `/dashboard/resident/` redirect to the resident dashboard. Supervisor research approvals and the old resident-progress subroute redirect to the supervisor dashboard. They are not active web forms.
- Training APIs still mount `/api/my/research/`, research actions, `/api/my/thesis/`, thesis submit, workshop completion APIs, eligibility, submission/certificate actions, program policies/milestones, postings, rotation completions and system settings. See `backend/sims/training/urls.py` and `views.py`. List these as backend-only optional extensions, with separate approval/contract acceptance before scope expansion; do not claim they are required web parity.
- Android already reads research/workshop status through R and displays it in L.RequirementsScreen/P.ResidentProgressReport. W also has research approval/return UI wired to R.approveResearch/returnResearch. These are existing Android additions beyond the active web baseline, available B, runtime QA pending, retained subject to Stage 0 permission/contract verification; not proof of complete research workflow parity.
- `/register` has `PUBLIC_REGISTRATION_ENABLED=false`. Do not implement public Android registration. Universal ADMIN creation uses `/api/users/` only.
- `/users/[id]` is required by the architectural guidance but no corresponding Next `page.tsx` exists at this baseline. Role detail pages are mostly informational. Profile editing/archive/admin password-reset actions must be distinguished from active UI; API/contract readiness is a Stage 0 prerequisite, not assumed endpoint availability.
- Resident document page supports upload/replace/defer, but no file-open link. A native file viewer would be a Stage 2 extension subject to an authenticated download contract, not missing active-web parity.
- `/masters` is an import/export setup workspace, not a set of native CRUD tables. Hospitals/departments/programs/matrix/roster APIs still exist; standalone historical dashboard pages redirect to masters. Do not count every method in `frontend/lib/api/masters.ts` or `userbase.ts` as a reachable form.
- Existing backend profile/document review actions without active Next controls (inspect `users/onboarding_api.py`), audit APIs, legacy-style bulk endpoints, program policies and other API-only mutations are not automatically mandatory Android features. Stage 4 may include them only after workflow/permission contracts are agreed.
- `backend/sims/_legacy/` and dummy cases/logbook/certificates routes are excluded. Current academic logbook is `/api/academics/logbook-entries/`; do not substitute the separate training logbook family or revive retired modules. No legacy directory was modified.
- Backup endpoints use an existing backend permission class whose historical name is `IsSuperAdmin`. Inspect its actual predicate in `backend/sims/users/permissions.py`; do not introduce a fifth role or assume every ADMIN account satisfies any additional flags.

### Explicitly deferred roadmap rows for this increment

- Stage 4 academic master-data authoring rows: training records, periods, rotation templates, evaluation templates, logbook categories, generic review queue and administrative rotation lifecycle.
- Stage 5 bulk rows: master setup workspace, standard/flexible import, flexible header mapping and saved mapping presets, dry-run/apply and dataset/template export.
- Stage 5 backup rows: backup list/create/download/validate/delete and restore upload/validate/dry-run/confirm. No destructive backup or restore was executed.
- These rows stay unchecked. No partial mobile-only state, alternate database, or substitute endpoint was introduced.

## Staged development roadmap

Stages are sequential foundations with role work split into independently reviewable actions. This document does not authorize implementation or deployment.

| Stage | Outcome and scope | Entry dependencies | Exit acceptance |
|---|---|---|---|
| 0 — Baseline | Reconcile identical local branches, source/status matrix, actual production contracts, historical test/artifact provenance and deferred conditional surfaces. | Current baseline and preserved release ledger. | Record current remote/VPS/image/proxy evidence; close or explicitly retain each verification gap; classify API-only management, rotation action differences and seed/cloud panel dispositions. |
| 1 — Identity and access | Native password change/reset, strict me-driven routing, dynamic completion, own-profile editing and permitted navigation for all four roles. | Canonical identity/profile registry, schema versions, options, role permissions; Stage 0 contract decisions. | Password-first and required-field completion tested for all roles, including schema increase; no role can bypass onboarding or gain privileges through mobile. |
| 2 — Resident workflows | Full logbook/procedure and evaluation payloads, corrections/cancellation, permitted leave/rotation actions, document deferral and canonical progress. | Stage 1; both training record families correctly resolved; serializers and transition contracts. | Each resident matrix action persists the complete payload; corresponding web view agrees; read-only rotations remain read-only if backend disallows resident creation. |
| 3 — Supervisor workflows | Full review display, scoring/feedback, approval/revision/rejection, rotation application semantics, assigned progress/workload. | Stage 1; Stage 2 creates valid review fixtures; assignment authorization and workflow actions. | End-to-end resident→supervisor→resident correction loops pass; unassigned supervisor denied; each score/reason retained. |
| 4 — Administration | Universal identity, directories, canonical profile management, supervision, document requirements, academic configuration and approvals. | Stage 1; canonical service contracts for each planned write. | Four-role creation atomic; all active web administrative actions work with backend permissions and audit; staff has only explicitly permitted actions. |
| 5 — Operational parity | Active reporting, filtering/pagination, import/export, data quality and existing local backup-center workflows. | Stages 2–4 data and report/bulk/backup contracts. | All pages and exports match server totals/filter scope; dry-run/apply and disposable restore verification pass; no new external integration. |
| 6 — Release readiness | Cross-client consistency, offline recovery/account isolation, accessibility/lifecycle, signed build and production compatibility. | All scoped implementation complete; isolated full suite and authenticated matrix. | Reproducible tested commit/artifact hashes and signing certificate, installation/upgrade evidence, four-role QA, backend compatibility and release verdict. |

## Current verification status

The feature branch adds the checked source actions above; unchecked rows remain pending. Source
completion and runtime acceptance remain separate, and the earlier baseline evidence is not silently
transferred to this new candidate.

Verified evidence:

- Production backend/frontend health, required notification/training migrations, identity repair, and `FCM_ENABLED=False` were recorded after the `46eccbd` rollout.
- All four demo identities returned the expected role through the production API. Raw credentials and tokens were not retained.
- Android unit tests, lint, debug and debug-test assembly passed for version 1.1.8/code 8; that rebuilt APK and test APK installed on emulator `pgsims`.
- Ten noncredentialed instrumentation tests passed. The cold HTTPS password-reset app link opened the native confirmation screen. Eight credential-gated release tests were skipped by design because no approved demo session was supplied to this run.
- ADMIN reached the restricted mobile screen.
- SUPPORT_STAFF reached the restricted screen, signed out, and had empty token/draft/upload stores afterward.
- SUPERVISOR fresh login, dashboard, assigned-resident list, selected workflow queues, process restoration, forced access-token refresh, and logout/relogin passed.
- RESIDENT fresh login, dashboard, and forced access-token refresh passed.
- The final-source isolated Django suite passed: 922 tests, zero failures/errors/skips, exit 0. The three deployment-domain tests also passed in a repository-aware isolated run.
- Offline leave and logbook drafts were retained in encrypted storage across a process restart. Server synchronization and exactly-once creation remain pending.

Observed failures and evidence limits:

- Inbox navigation and the nested-scroll defect are repaired in source and the candidate builds, but authenticated read/unread/preferences/recipient-isolation and exact-target device QA remain pending.
- Immediate queue metadata durability, account ownership and orphan cleanup pass noncredentialed instrumentation; lost-response exactly-once creation and worker/foreground reconciliation still require an authorized session.
- `makemigrations --check --dry-run` reports two pre-existing model/migration-state drifts (a notification index rename and historical leave field alteration). No unrelated migration was generated.

Canonical evidence: [verification ledger](docs/implementation/20260914_android_sprints_2_3_4/VERIFICATION_LEDGER.md), [test results](docs/implementation/20260914_android_sprints_2_3_4/TEST_RESULTS.md), and the sanitized files under `docs/implementation/20260914_android_sprints_2_3_4/evidence/`.

## Pending implementation checklist

The unchecked matrix entries are the action-level backlog and carry their own stage, dependency and acceptance criterion. This checklist groups handoff work without promoting partial implementations to complete:

- [ ] Stage 0: establish current deployment/remote evidence; resolve current rotation action contract and API-only management scope; document exclusions for disabled/conditional surfaces.
- [ ] Stage 1: password change/reset; backend next-route guard; generic required-field renderer/options; resident reference/date/declaration completion; ADMIN/staff navigation and inbox; supervisor profile editor; exact record targets.
- [ ] Stage 2: full logbook/procedure fields and cancel; evaluation responses/options/revision/cancel; allowed leave editing; document defer; canonical progress. Keep native file viewer separately scoped.
- [ ] Stage 3: complete review content/scoring/approval comments/start-review; canonical rotation application review; generic review queue and workload.
- [ ] Stage 4: universal identity creation, directory/detail management, document requirements, pending links, supervision mutations, academic configuration and administrative workflow actions.
- [ ] Stage 5: standard/flexible imports and presets, dataset/report exports, all report/detail/filter screens, data quality/monitoring, complete pagination and native backup/restore workflow.
- [ ] Stage 6: close account-switch/recovery/conflict/lifecycle gaps discovered by QA; produce and verify release artifacts only in a later authorized release sprint.

## Separate QA checklist

Completed portions are recorded above. The broad acceptance items remain unchecked until every condition in that item passes.

- [ ] Record one source commit, backend image revision, environment and test account role per run. Verify both client hostnames map to the same backend/database without printing credentials; compare a permitted fixture record by stable ID across web/Android.
- [ ] ADMIN: universal four-role creation, directory/configuration/report/approval access and audit; invalid roles denied, rollback leaves no orphan profile; temporary-password/default flags agree with web.
- [ ] SUPPORT_STAFF: own account/dashboard/password/onboarding works; user creation and administrative mutations are denied by backend even with forged requests. Separately enumerate any backend-granted operational reads.
- [ ] RESIDENT: own records only; another resident's IDs denied; full logbook/procedure and evaluation response round-trip, draft/submit/return/edit/resubmit/cancel and immutable final states; correct academic/training IDs.
- [ ] SUPERVISOR: only assigned residents; full review payloads, scoring/max score, approval comments and mandatory return/reject reasons; queue refresh and assignment revoked mid-session.
- [ ] Onboarding for all four roles: must-change-password before missing profile fields; schema bump/new required field on next login; invalid input/options, server errors, partial save, app restart/back navigation and stale cached state; document/declaration review semantics remain distinct from required-field gating.
- [ ] Session: invalid/disabled/archived account, restored session, access expiry, refresh rotation/revocation, simultaneous requests, failed refresh without loop, offline logout and retry; no token/password logs.
- [ ] Payloads: template numeric/text responses, nested procedure values, null versus empty fields, dates/types, supervisor/period references and unsupported transitions. Validate against live disposable backend, not only MockWebServer fixtures.
- [ ] Uploads: supported/unsupported types, limits, empty file, permission denial, replacement confirmation, deferral, remarks; encrypted staging survives process death/reboot, retry/discard works, revoked document permission fails safely, UI refreshes after worker completion.
- [ ] Pagination/filtering: more than one server page, empty and failed pages, changed filters, stable ordering, next URL handling, totals consistent with backend and exports; no truncated supervisor queue or snapshot-derived false totals.
- [ ] Offline drafts: create leave/logbook with stable client_request_id, restart, reconnect, response lost after server commit, duplicate worker execution and backoff; exactly one canonical record created. Updates/reviews are not implicitly queued.
- [ ] Account isolation: logout/login as another user while worker is scheduled/running; expiry mid-upload; queued metadata/file purge, no old account payload sent under new credentials; inspect backup extraction exclusions.
- [ ] Notifications: recipient-only read/unread/preferences; target ID and role-aware deep links; unknown/deleted target; pagination. FCM stays disabled; no push delivery claim.
- [ ] Reports/import/export/backup: backend-scoped totals and CSV/XLSX contents; file chooser/download recovery; preset mapping and dry-run/apply agreement; destructive restore only on isolated data with current password/typed confirmation/audit safeguards.
- [ ] Accessibility/lifecycle: TalkBack, labels/focus, font scale, touch targets, contrast, keyboard/date/number inputs, device rotation/background/low-memory process death, loading/error/retry and double taps.
- [ ] Build/release: the recorded Android unit/lint/debug gate passed, but rebuild/install the current candidate; complete the authenticated emulator `pgsims` matrix and physical-device upload/lifecycle checks; verify signed APK/AAB signature and hashes, correct package/version and Play upload key, and upgrade data behavior. Artifact existence alone is not release proof.
- [ ] Backend/frontend regression: the isolated 922-test Django suite passed with three explicit repository-file skips; focused affected workflow/API tests, applicable identity/brick gates, skipped deployment-domain checks in a repository-aware environment, and frontend typecheck/lint/build/regression remain for the implementation/release candidate.

## Test and artifact provenance

| Evidence | What it establishes | What it does not establish |
|---|---|---|
| `android/app-companion/src/test/java/pk/vexel/pgrcompanion/InstitutionalRepositoryTest.kt` | Mock HTTP tests for login, refresh, role-scoped snapshot, upload and selected workflow payloads; source inspected. | Correct live service authorization/full UI completion. |
| `ResidentPresentationTest.kt` | Labels, onboarding policies/presentation test source. | Dynamic all-role onboarding or authenticated UI parity. |
| `docs/implementation/20260914_android_sprints_2_3_4/TEST_RESULTS.md` | Records the 2026-09-15 unit/lint/debug build, production rollout, isolated 922-test pass, partial authenticated role matrix, and recovery probes with explicit failures. | Complete four-role workflow acceptance or behavior of the uninstalled 1.1.8 candidate. |
| Same report, production and isolated-suite sections | Reports health/check/migrations and 59-user identity repair with no invalid/duplicate profiles, FCM false, and 922 tests passing with three repository-file skips. | Independent recheck of current remote/proxy/database identity or closure of the skipped deployment-domain checks. |
| `REMEDIATION/PGSIMS/FINAL_PRODUCTION_READINESS/TEST_RESULTS.md` and existing `SPRINT_STATE.md` release entries | Historical backend 921-test and web/build/E2E evidence associated with earlier remediation. | Transfer of that result to later changes, or closure of the subsequent 922-test lock. |
| Existing `android/app-companion/build/test-results/testDebugUnitTest/TEST-*.xml` | Local generated unit result artifacts; metadata summarized below. | Reproducible attribution to HEAD without build rerun. |
| Existing `android/app-companion/build/outputs/apk/release/app-companion-release.apk` and `bundle/release/app-companion-release.aab` | Files are present locally; prior ledger reports owner-signed release production. | Signatures, current-source match, distribution or production availability verified here. Old differently named outputs in the same build tree must not be mistaken for the canonical app. |

The old ledger's PR #16 “unmerged” statement conflicts with the identical local branch tips and must not be reused as current merge status. This review establishes local tree equality only; remote PR status was not queried. Earlier “VPS unchanged” entries precede the later rollout report. The isolated full-suite rerun is closed; the authenticated/recovery matrix, current-candidate rebuild and skipped deployment-domain checks remain release conditions.

Generated XML metadata inspected during this review (historical files, not rerun):

| Suite | Tests | Failures | Errors | Recorded timestamp |
|---|---|---|---|---|
| pk.vexel.pgrcompanion.CredentialRedactionTest | 1 | 0 | 0 | 2026-09-14T19:23:00 |
| pk.vexel.pgrcompanion.InstitutionalRepositoryTest | 20 | 0 | 0 | 2026-09-14T19:23:00 |
| pk.vexel.pgrcompanion.InstitutionalTokenStoreTest | 1 | 0 | 0 | 2026-09-14T19:23:06 |
| pk.vexel.pgrcompanion.InstitutionalValidationTest | 5 | 0 | 0 | 2026-09-14T19:23:06 |
| pk.vexel.pgrcompanion.ResidentPresentationTest | 3 | 0 | 0 | 2026-09-14T19:23:06 |

## Complete Next page disposition index

This index covers every current `frontend/app/**/page.tsx` file, including directly addressable pages absent from sidebar navigation. It prevents redirects/disabled screens from inflating feature totals. Active actions map to the role matrices above; shared widgets and API-only extensions are inventoried separately. “Active” means source UI, not runtime certification.

| Route / web source | Disposition and matrix family |
|---|---|
| [/academics/data-quality](frontend/app/academics/data-quality/page.tsx) | Active monitoring/data quality/overview; Operations stage 5; seed disposition stage 0 |
| [/academics/evaluation-templates](frontend/app/academics/evaluation-templates/page.tsx) | Active academic configuration/overview/review queue; Administration stage 4 (supervisor queue stage 3) |
| [/academics/evaluations/[id]](frontend/app/academics/evaluations/[id]/page.tsx) | Active workflow/form/actions; Resident stage 2, Supervisor stage 3, ADMIN stage 4 as permitted |
| [/academics/evaluations/[id]/review](frontend/app/academics/evaluations/[id]/review/page.tsx) | Active workflow/form/actions; Resident stage 2, Supervisor stage 3, ADMIN stage 4 as permitted |
| [/academics/evaluations/new](frontend/app/academics/evaluations/new/page.tsx) | Active workflow/form/actions; Resident stage 2, Supervisor stage 3, ADMIN stage 4 as permitted |
| [/academics/evaluations](frontend/app/academics/evaluations/page.tsx) | Active workflow/form/actions; Resident stage 2, Supervisor stage 3, ADMIN stage 4 as permitted |
| [/academics/leave-requests/[id]](frontend/app/academics/leave-requests/[id]/page.tsx) | Active workflow/form/actions; Resident stage 2, Supervisor stage 3, ADMIN stage 4 as permitted |
| [/academics/leave-requests/new](frontend/app/academics/leave-requests/new/page.tsx) | Active workflow/form/actions; Resident stage 2, Supervisor stage 3, ADMIN stage 4 as permitted |
| [/academics/leave-requests](frontend/app/academics/leave-requests/page.tsx) | Active workflow/form/actions; Resident stage 2, Supervisor stage 3, ADMIN stage 4 as permitted |
| [/academics/logbook/[id]](frontend/app/academics/logbook/[id]/page.tsx) | Active workflow/form/actions; Resident stage 2, Supervisor stage 3, ADMIN stage 4 as permitted |
| [/academics/logbook/[id]/review](frontend/app/academics/logbook/[id]/review/page.tsx) | Active workflow/form/actions; Resident stage 2, Supervisor stage 3, ADMIN stage 4 as permitted |
| [/academics/logbook/new](frontend/app/academics/logbook/new/page.tsx) | Active workflow/form/actions; Resident stage 2, Supervisor stage 3, ADMIN stage 4 as permitted |
| [/academics/logbook](frontend/app/academics/logbook/page.tsx) | Active workflow/form/actions; Resident stage 2, Supervisor stage 3, ADMIN stage 4 as permitted |
| [/academics/logbook-categories](frontend/app/academics/logbook-categories/page.tsx) | Active academic configuration/overview/review queue; Administration stage 4 (supervisor queue stage 3) |
| [/academics/monitoring](frontend/app/academics/monitoring/page.tsx) | Active monitoring/data quality/overview; Operations stage 5; seed disposition stage 0 |
| [/academics/my-progress](frontend/app/academics/my-progress/page.tsx) | Active own academic progress; Resident stage 2 |
| [/academics](frontend/app/academics/page.tsx) | Active academic configuration/overview/review queue; Administration stage 4 (supervisor queue stage 3) |
| [/academics/periods](frontend/app/academics/periods/page.tsx) | Active academic configuration/overview/review queue; Administration stage 4 (supervisor queue stage 3) |
| [/academics/reports/data-quality](frontend/app/academics/reports/data-quality/page.tsx) | Active report/list/detail/export; Operations stage 5 (resident summary stage 2) |
| [/academics/reports/evaluations](frontend/app/academics/reports/evaluations/page.tsx) | Active report/list/detail/export; Operations stage 5 (resident summary stage 2) |
| [/academics/reports/logbook](frontend/app/academics/reports/logbook/page.tsx) | Active report/list/detail/export; Operations stage 5 (resident summary stage 2) |
| [/academics/reports/resident-progress/[id]](frontend/app/academics/reports/resident-progress/[id]/page.tsx) | Active report/list/detail/export; Operations stage 5 (resident summary stage 2) |
| [/academics/reports/resident-progress](frontend/app/academics/reports/resident-progress/page.tsx) | Active report/list/detail/export; Operations stage 5 (resident summary stage 2) |
| [/academics/reports/supervisor-workload/[id]](frontend/app/academics/reports/supervisor-workload/[id]/page.tsx) | Active report/list/detail/export; Operations stage 5 (resident summary stage 2) |
| [/academics/reports/supervisor-workload](frontend/app/academics/reports/supervisor-workload/page.tsx) | Active report/list/detail/export; Operations stage 5 (resident summary stage 2) |
| [/academics/review-queue](frontend/app/academics/review-queue/page.tsx) | Active academic configuration/overview/review queue; Administration stage 4 (supervisor queue stage 3) |
| [/academics/rotation-assignments/[id]](frontend/app/academics/rotation-assignments/[id]/page.tsx) | Active workflow/form/actions; Resident stage 2, Supervisor stage 3, ADMIN stage 4 as permitted |
| [/academics/rotation-assignments/new](frontend/app/academics/rotation-assignments/new/page.tsx) | Active workflow/form/actions; Resident stage 2, Supervisor stage 3, ADMIN stage 4 as permitted |
| [/academics/rotation-assignments](frontend/app/academics/rotation-assignments/page.tsx) | Active workflow/form/actions; Resident stage 2, Supervisor stage 3, ADMIN stage 4 as permitted |
| [/academics/rotation-templates](frontend/app/academics/rotation-templates/page.tsx) | Active academic configuration/overview/review queue; Administration stage 4 (supervisor queue stage 3) |
| [/academics/supervisor-workload](frontend/app/academics/supervisor-workload/page.tsx) | Active assigned workload; Supervisor stage 3 |
| [/academics/training-records/[id]](frontend/app/academics/training-records/[id]/page.tsx) | Active academic configuration/overview/review queue; Administration stage 4 (supervisor queue stage 3) |
| [/academics/training-records](frontend/app/academics/training-records/page.tsx) | Active academic configuration/overview/review queue; Administration stage 4 (supervisor queue stage 3) |
| [/academics/workflow-data-quality](frontend/app/academics/workflow-data-quality/page.tsx) | Active monitoring/data quality/overview; Operations stage 5; seed disposition stage 0 |
| [/academics/workflow-overview](frontend/app/academics/workflow-overview/page.tsx) | Active monitoring/data quality/overview; Operations stage 5; seed disposition stage 0 |
| [/admin/pending-supervisor-links](frontend/app/admin/pending-supervisor-links/page.tsx) | Active directory/identity/detail/requirements/pending-link UI; Administration stage 4 (details mostly read-only) |
| [/admins/[id]](frontend/app/admins/[id]/page.tsx) | Active directory/identity/detail/requirements/pending-link UI; Administration stage 4 (details mostly read-only) |
| [/admins](frontend/app/admins/page.tsx) | Active directory/identity/detail/requirements/pending-link UI; Administration stage 4 (details mostly read-only) |
| [/change-password](frontend/app/change-password/page.tsx) | Active account/authentication/profile UI; Identity stage 1 |
| [/complete-profile](frontend/app/complete-profile/page.tsx) | Active account/authentication/profile UI; Identity stage 1 |
| [/dashboard/change-password](frontend/app/dashboard/change-password/page.tsx) | Active account/authentication/profile UI; Identity stage 1 |
| [/dashboard](frontend/app/dashboard/page.tsx) | Role redirect hub plus active SUPPORT_STAFF restricted shell; Identity stage 1 |
| [/dashboard/pg/departments/[id]/roster](frontend/app/dashboard/pg/departments/[id]/roster/page.tsx) | Redirect → `/dashboard/resident`; no separate workflow |
| [/dashboard/pg](frontend/app/dashboard/pg/page.tsx) | Redirect → `/dashboard/resident`; no separate workflow |
| [/dashboard/resident/documents](frontend/app/dashboard/resident/documents/page.tsx) | Active resident dashboard/documents; Resident stage 2 |
| [/dashboard/resident](frontend/app/dashboard/resident/page.tsx) | Active resident dashboard/documents; Resident stage 2 |
| [/dashboard/resident/postings](frontend/app/dashboard/resident/postings/page.tsx) | Redirect → `/dashboard/resident`; no separate workflow |
| [/dashboard/resident/progress](frontend/app/dashboard/resident/progress/page.tsx) | Redirect → `/dashboard/resident`; no separate workflow |
| [/dashboard/resident/research](frontend/app/dashboard/resident/research/page.tsx) | Redirect → `/dashboard/resident`; no separate workflow |
| [/dashboard/resident/schedule](frontend/app/dashboard/resident/schedule/page.tsx) | Redirect → `/dashboard/resident`; no separate workflow |
| [/dashboard/resident/thesis](frontend/app/dashboard/resident/thesis/page.tsx) | Redirect → `/dashboard/resident`; no separate workflow |
| [/dashboard/resident/workshops](frontend/app/dashboard/resident/workshops/page.tsx) | Redirect → `/dashboard/resident`; no separate workflow |
| [/dashboard/supervisor](frontend/app/dashboard/supervisor/page.tsx) | Active supervisor dashboard; Supervisor stage 3 |
| [/dashboard/supervisor/research-approvals](frontend/app/dashboard/supervisor/research-approvals/page.tsx) | Redirect → `/dashboard/supervisor`; no separate workflow |
| [/dashboard/supervisor/residents/[id]/progress](frontend/app/dashboard/supervisor/residents/[id]/progress/page.tsx) | Redirect → `/dashboard/supervisor`; no separate workflow |
| [/dashboard/utrmc/academics](frontend/app/dashboard/utrmc/academics/page.tsx) | Redirect → `/academics`; no separate workflow |
| [/dashboard/utrmc/backup](frontend/app/dashboard/utrmc/backup/page.tsx) | Active backup/restore and conditional cloud panel; Operations stage 5, integration excluded |
| [/dashboard/utrmc/data-quality](frontend/app/dashboard/utrmc/data-quality/page.tsx) | Redirect → `/supervision/data-quality`; no separate workflow |
| [/dashboard/utrmc/departments/[id]/roster](frontend/app/dashboard/utrmc/departments/[id]/roster/page.tsx) | Redirect → `/masters`; no separate workflow |
| [/dashboard/utrmc/departments](frontend/app/dashboard/utrmc/departments/page.tsx) | Redirect → `/masters`; no separate workflow |
| [/dashboard/utrmc/eligibility-monitoring](frontend/app/dashboard/utrmc/eligibility-monitoring/page.tsx) | Redirect → `/dashboard/utrmc`; no separate workflow |
| [/dashboard/utrmc/hospitals](frontend/app/dashboard/utrmc/hospitals/page.tsx) | Redirect → `/masters`; no separate workflow |
| [/dashboard/utrmc/matrix](frontend/app/dashboard/utrmc/matrix/page.tsx) | Redirect → `/masters`; no separate workflow |
| [/dashboard/utrmc/onboarding](frontend/app/dashboard/utrmc/onboarding/page.tsx) | Redirect → `/users/new`; no separate workflow |
| [/dashboard/utrmc](frontend/app/dashboard/utrmc/page.tsx) | Active ADMIN dashboard; Administration stage 4 |
| [/dashboard/utrmc/postings](frontend/app/dashboard/utrmc/postings/page.tsx) | Redirect → `/dashboard/utrmc`; no separate workflow |
| [/dashboard/utrmc/programs](frontend/app/dashboard/utrmc/programs/page.tsx) | Redirect → `/masters`; no separate workflow |
| [/dashboard/utrmc/supervision](frontend/app/dashboard/utrmc/supervision/page.tsx) | Redirect → `/supervision`; no separate workflow |
| [/dashboard/utrmc/supervisors](frontend/app/dashboard/utrmc/supervisors/page.tsx) | Redirect → `/supervisors`; no separate workflow |
| [/dashboard/utrmc/users](frontend/app/dashboard/utrmc/users/page.tsx) | Redirect → `/users`; no separate workflow |
| [/forgot-password](frontend/app/forgot-password/page.tsx) | Active account/authentication/profile UI; Identity stage 1 |
| [/login](frontend/app/login/page.tsx) | Active account/authentication/profile UI; Identity stage 1 |
| [/masters](frontend/app/masters/page.tsx) | Active standard/flexible bulk setup/import/export; Operations stage 5 |
| [/](frontend/app/page.tsx) | Public landing/access feedback; navigation shell, no independent domain workflow |
| [/profile](frontend/app/profile/page.tsx) | Active account/authentication/profile UI; Identity stage 1 |
| [/register](frontend/app/register/page.tsx) | Disabled public registration; excluded |
| [/reset-password/[uid]/[token]](frontend/app/reset-password/[uid]/[token]/page.tsx) | Active account/authentication/profile UI; Identity stage 1 |
| [/residents/[id]](frontend/app/residents/[id]/page.tsx) | Active directory/identity/detail/requirements/pending-link UI; Administration stage 4 (details mostly read-only) |
| [/residents/document-requirements](frontend/app/residents/document-requirements/page.tsx) | Active directory/identity/detail/requirements/pending-link UI; Administration stage 4 (details mostly read-only) |
| [/residents](frontend/app/residents/page.tsx) | Active directory/identity/detail/requirements/pending-link UI; Administration stage 4 (details mostly read-only) |
| [/supervision/assignments/[id]](frontend/app/supervision/assignments/[id]/page.tsx) | Active supervision ledger/mutations; Administration stage 4; import/data quality stage 5 |
| [/supervision/assignments/new](frontend/app/supervision/assignments/new/page.tsx) | Active supervision ledger/mutations; Administration stage 4; import/data quality stage 5 |
| [/supervision/assignments](frontend/app/supervision/assignments/page.tsx) | Active supervision ledger/mutations; Administration stage 4; import/data quality stage 5 |
| [/supervision/data-quality](frontend/app/supervision/data-quality/page.tsx) | Active supervision ledger/mutations; Administration stage 4; import/data quality stage 5 |
| [/supervision/import](frontend/app/supervision/import/page.tsx) | Active supervision ledger/mutations; Administration stage 4; import/data quality stage 5 |
| [/supervision](frontend/app/supervision/page.tsx) | Active supervision ledger/mutations; Administration stage 4; import/data quality stage 5 |
| [/supervisors/[id]](frontend/app/supervisors/[id]/page.tsx) | Active directory/identity/detail/requirements/pending-link UI; Administration stage 4 (details mostly read-only) |
| [/supervisors](frontend/app/supervisors/page.tsx) | Active directory/identity/detail/requirements/pending-link UI; Administration stage 4 (details mostly read-only) |
| [/support-staff/[id]](frontend/app/support-staff/[id]/page.tsx) | Active directory/identity/detail/requirements/pending-link UI; Administration stage 4 (details mostly read-only) |
| [/support-staff](frontend/app/support-staff/page.tsx) | Active directory/identity/detail/requirements/pending-link UI; Administration stage 4 (details mostly read-only) |
| [/unauthorized](frontend/app/unauthorized/page.tsx) | Public landing/access feedback; navigation shell, no independent domain workflow |
| [/users/new](frontend/app/users/new/page.tsx) | Active directory/identity/detail/requirements/pending-link UI; Administration stage 4 (details mostly read-only) |
| [/users](frontend/app/users/page.tsx) | Active directory/identity/detail/requirements/pending-link UI; Administration stage 4 (details mostly read-only) |

## Review verification and handoff

Documentation validation in this sprint: compared local branch commit IDs and diff; inventoried all Next page files; traced Compose root/navigation and client methods; inspected backend URL mounts, relevant views/serializers and local historical test metadata; checked all 118 local Markdown links, confirmed all 93 Next page files appear in the disposition index, and ran `git diff --check`. No runtime checks are claimed. The implementation checkboxes reflect source only.

Documentation review verdict: **GO for roadmap handoff**. Complete native parity and release certification remain **not achieved**. The current release verdict is **CONDITIONAL GO** because the Inbox and upload-recovery failures and remaining authenticated matrix are unresolved. Fix those release defects first; the recommended first broader parity stage is **Stage 1 — Identity and access**, after Stage 0 closes contract/deployment evidence decisions.

This reconciliation changes documentation only. It does not claim ownership of the concurrent Android instrumentation/version candidate or evidence files. No files or routes were deleted and no legacy folder was touched or recreated. Baseline commit remains `13f1bb7`; the worktree changes have not been committed/pushed or synchronized to the VPS. Unresolved release work remains in `SPRINT_STATE.md`.
