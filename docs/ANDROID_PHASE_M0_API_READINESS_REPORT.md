# PGR SIMS Android — Phase M0 API Readiness Report

**Discovery date:** 2026-09-02  
**Baseline branch:** `main`  
**Baseline commit:** `1a249e0fb3e8ea2e644c9c7d95240477fd01c44f`  
**Baseline tracking state:** `main` matched `origin/main`  
**Authoritative product baseline:** `docs/ANDROID_MOBILE_PRODUCT_POLICY_AND_PRODUCTION_PLAN.md`

## 1. Executive verdict

**CONDITIONAL GO for Phase M1 contract/security work. NO-GO for production Android feature delivery until the P0 items in this report are closed.**

The repository has a viable native-client foundation: Django REST Framework, JWT login and refresh, a backend-owned four-role identity model, dynamic profile-completion state, canonical supervision assignments, resident document records, academic summaries, and an in-app notification API. The Android scaffold also has appropriate implementation-light boundaries.

The current API cannot yet be treated as a safe, stable mobile contract. Four release blockers were confirmed:

1. `PATCH /api/auth/profile/update/` permits an authenticated user to write `role`, `is_active`, and `username`; a resident can therefore promote their own account to `ADMIN`.
2. The role-profile viewsets use the global `IsAuthenticated` default and constrain only `retrieve`; their list/create/update/delete routes can expose or mutate other users' profiles.
3. resident document URLs are served by Caddy directly from `/media/*` with public caching, bypassing object authorization.
4. `GET /api/supervisors/residents/{resident_id}/progress/` checks only that the caller is a supervisor/admin and does not verify the resident is assigned to that supervisor.

The locked onboarding lifecycle is also not implemented. The current backend has draft field saving, computed profile completeness, declaration acceptance, and independent document states, but no canonical onboarding submission/review/correction/resubmission/approval state machine.

M1 should remediate the authorization and file-delivery blockers, establish tested API contracts, and implement the minimum backend-owned onboarding workflow. M0 did not implement endpoints or Android features.

## 2. Repository and safety baseline

### Discovered layout

| Area | Path | Finding |
|---|---|---|
| Backend | `backend/` | Django + Django REST Framework under `backend/sims/`; project settings/routes under `backend/sims_project/` |
| Web frontend | `frontend/` | Next.js App Router, Axios API client, client/server route guards |
| Android | `android/` | implementation-light module directory scaffold; no Gradle or production code |
| Documentation | `docs/` | contracts, truth maps, implementation records, product policy, archived mobile notes |
| CI | `.github/workflows/` | drift gates and Playwright smoke workflow |
| Deployment/config | `deploy/`, `docker/`, `ops/` | Caddy, multiple Docker Compose targets, operational scripts |

At discovery start the working tree was clean. No unrelated artifacts were deleted or cleaned. This report is the only M0 source change.

### Relevant backend domains

- `sims.users`: custom user, four role-specific profiles, identity service, dynamic completion, resident onboarding/documents.
- `sims.supervision`: `ResidentSupervisorAssignment`, pending supervisor resolution, services and scoped APIs.
- `sims.training`: programmes, training records, rotations, research, thesis, workshops, eligibility, summary endpoints.
- `sims.academics`: academic workflow, evaluations, canonical exposed logbook endpoints, summaries/reporting.
- `sims.notifications`: in-app/email records, preferences and read-state APIs.
- `sims.audit`: `ActivityLog` audit trail.
- `sims.bulk`: administrative import/export.
- `sims.backup_center`: administrative backup and optional Google Drive connector; not an Android MVP domain.
- `sims._legacy`: retained legacy code namespace; Android must not consume it.

No current runtime AdminOps identity bridge was found. Historical bridge material appears only in archived/back-up evidence. Backup Center/Google Drive is a distinct technical-admin capability and remains outside mobile MVP.

## 3. Current authentication architecture

### End-to-end trace

| Step | Current implementation | Mobile assessment |
|---|---|---|
| Account creation | Admin calls `POST /api/users/`; `create_user_with_profile()` creates `User`, correct profile and audit records atomically | READY for admin-created-account policy |
| Credential issuance | generated username; default password `pgfmu123` when omitted; `must_change_password=True` | PARTIAL: secure out-of-band delivery is operationally unspecified |
| Login | `POST /api/auth/login/` using SimpleJWT custom serializer | READY WITH MINOR ADAPTATION |
| Access token | JWT Bearer, default 60 minutes | READY |
| Refresh token | `POST /api/auth/refresh/`, default 7 days, rotation enabled | PARTIAL: rotation/revocation lifecycle needs correction |
| Current state | `GET /api/auth/me/` returns role and onboarding routing state | READY WITH CONTRACT HARDENING |
| First password change | `POST /api/auth/change-password/` clears `must_change_password` | PARTIAL: password validators are not called |
| Logout | `POST /api/auth/logout/` parses refresh token but does not revoke/blacklist it | BLOCKED for reliable server-side logout |
| Password reset | email token flow; reset URL is built from backend request host | PARTIAL: browser URL/deep-link behavior is not mobile-defined |
| Public registration | route exists but is disabled by default; if enabled it creates residents | Keep disabled for locked MVP |
| Role resolution | JWT claim plus authoritative database user and `/api/auth/me/` | PARTIAL: writable self-role endpoint is a P0 flaw |
| Throttling | login 5/minute default; global anonymous 100/hour and user 1000/hour | READY WITH POLICY REVIEW |

### Browser dependencies

The web client stores access and refresh tokens in `localStorage` and mirrors access/role state into JavaScript-readable cookies for Next.js middleware. Android must not reproduce that design. Native Android can call the Bearer-token API without CSRF or cookies and should store refresh credentials using Android Keystore-backed encrypted storage. Session authentication remains useful for browser/Django clients but is not needed by Android. CORS is not a native-app control.

The web refresh interceptor stores only the returned access token even though refresh-token rotation is enabled. The server has blacklisting disabled, and logout does not revoke tokens. M1 must choose and test one coherent rotation/revocation strategy for both clients.

### Authentication readiness

**PARTIAL / security-blocked.** JWT itself is suitable for Android, but self-role mutation, incomplete logout/revocation, password validation, archived-account handling, and mobile reset-link behavior must be resolved before production use.

## 4. Current onboarding architecture

### Actual trace

```text
Admin POST /api/users/
  -> create_user_with_profile(transaction.atomic)
  -> User + ResidentProfile (+ optional TrainingRecord)
  -> optional existing ResidentSupervisorAssignment OR PendingSupervisorAssignment
  -> audit events

Resident POST /api/auth/login/
  -> GET /api/auth/me/
  -> must_change_password ? /change-password
  -> missing registry fields or resident onboarding incomplete ? /complete-profile
  -> otherwise resident dashboard

/complete-profile (resident path)
  -> GET/PATCH /api/auth/onboarding/
  -> per-field or grouped draft save
  -> recalculate_profile_completion()
  -> POST /api/resident-onboarding/state/ {accepted: true}
  -> declaration_accepted=True
  -> onboarding_complete = profile complete AND declaration accepted
```

The web page follows this API and dynamically renders returned identity/enrolment fields. It autosaves fields, exposes a supervisor-status choice, a declaration checkbox, document baseline, research/thesis fields and workshops. Its “Finish onboarding” behavior re-reads `/api/auth/me/`; it does not submit an application for administrative review.

### Validation and audit behavior

- Draft saving is transaction-wrapped across the submitted field set.
- Foreign keys are checked for existence, but active-state and cross-field compatibility checks are inconsistent.
- Phone and email are assigned directly without explicit API-level format validation.
- `current_level` is stored on a model choice field but the onboarding setter does not explicitly validate the submitted choice.
- `locked_program` does not prevent the resident onboarding setter from changing the programme.
- Every draft patch produces `ONBOARDING_DRAFT_SAVED`.
- Declaration acceptance produces `ONBOARDING_COMPLETED`, even though no administrative review or approval occurred.
- Reading onboarding state creates missing `ResidentDocument` fulfillment rows. A GET therefore has database write side effects.

### Documentation/code drift

1. The locked product policy describes submit, pending review, correction, resubmission and approval; code has none of those aggregate states.
2. the Update 0 profile-requirement documentation lists only basic resident identity fields in places, while the code registry also requires hospital, department, programme and academic session.
3. resident onboarding adds specialty, training start date and current level beyond the central profile-completion registry. `/api/auth/me/` consequently exposes two different missing-field concepts.
4. service comments describe resident bootstrap/enrolment fields as institution-controlled, while the resident onboarding endpoint lets residents edit them.
5. `ResidentOnboardingDeclaration` exists, but the active endpoint writes declaration fields directly on `ResidentProfile` instead.
6. “onboarding complete” currently means profile complete plus declaration, not administratively approved.

## 5. Actual onboarding state machine

### Implemented state

```text
must_change_password = true
        |
        v
PASSWORD CHANGE REQUIRED
        |
        v
missing registry fields OR missing resident-only fields OR declaration not accepted
        |
        v
PROFILE/ONBOARDING INCOMPLETE (draft saves allowed)
        |
        +---- independent document states:
        |     NOT_STARTED / DEFERRED / PENDING_REVIEW /
        |     VERIFIED / REJECTED / REUPLOAD_REQUIRED
        |
        v
profile complete + declaration accepted
        |
        v
ONBOARDING COMPLETE -> dashboard
```

There is no model or field representing `SUBMITTED`, `PENDING_REVIEW`, `CORRECTION_REQUIRED`, `RESUBMITTED`, or `APPROVED` for the onboarding application. An administrator cannot review or correct an aggregate onboarding submission. Document review is independent and does not gate the completion boolean.

### Required canonical state for M1

The backend should own an explicit, auditable state machine:

```text
NOT_STARTED -> IN_PROGRESS -> SUBMITTED -> PENDING_REVIEW -> APPROVED
                                      \-> CORRECTION_REQUIRED -> RESUBMITTED -> PENDING_REVIEW
```

Transitions, editable fields, correction scope, reviewer identity/timestamps, and document defer eligibility must be enforced server-side. Android and web should consume the same transition/actions contract.

## 6. Canonical resident onboarding field matrix

Classification describes the current enforceable behavior, not merely UI wording:

- **A:** resident-editable
- **B:** resident-editable before approval only
- **C:** correction-request controlled
- **D:** administration-controlled
- **E:** derived/system-controlled
- **F:** ambiguous or contradictory ownership

| Field/API name | Storage | Required now | Type/choices | Current validation/dependency | Class | Finding |
|---|---|---:|---|---|---|---|
| `full_name` | `User.first_name/last_name` | Yes | text | truthy; split once on space | A | no robust name validation |
| `phone` | `User.phone_number` | Yes | telephone text | truthy only | A | duplicate `ResidentProfile.phone` is not used here |
| `email` | `User.email` | Yes | email text | truthy only in this setter | A | duplicate `ResidentProfile.email`; format/uniqueness not explicit |
| `registration_no` | `ResidentProfile.registration_no` | No | text, max 50 | no workflow-specific rule | A | likely needs uniqueness/authority decision |
| `cnic` | `ResidentProfile.cnic` | No | text, max 20 | no format/uniqueness rule | A | sensitive identifier; exposure policy required |
| `hospital` | `ResidentProfile.hospital`; copied to training site | Yes | active hospital option by PK | existence only | F | resident-writable but described elsewhere as institution-controlled |
| `department_ref` | `ResidentProfile.department_ref`; copied to training record | Yes | department PK | existence only | F | no hospital/department compatibility enforcement |
| `program_ref` | `ResidentProfile.program_ref`; TrainingRecord key | Yes | programme PK | existence; creates/gets TrainingRecord | F | resident can alter despite `locked_program` semantics |
| `academic_session_ref` | `ResidentProfile.academic_session_ref`; copied to training record | Yes | code value | code existence | F | ownership must be locked; state value uses FK code |
| `specialty_ref` | `ResidentProfile.specialty_ref` | Yes in resident endpoint, absent central registry | code value | code existence | F | two required-field registries disagree |
| `training_start_date` | `ResidentTrainingRecord.start_date` | Yes in resident endpoint | ISO date | programme required; parser errors not normalized | F | institution-controlled semantics unresolved |
| `expected_end_date` | `ResidentTrainingRecord.expected_end_date` | No | ISO date | programme required | F | likely derived/admin-controlled but resident-writable |
| `current_level` | `ResidentTrainingRecord.current_level` | Yes in resident endpoint | `y1`…`y5` | programme required; explicit choice check absent | F | training year ownership unresolved |
| `notes` | `ResidentTrainingRecord.notes` | No | text | programme required | A | resident draft note is reasonable |
| `supervisor_status` | `ResidentProfile.extra_data` | No | free submitted value | no canonical choice validation | F | not a supervisor declaration; can disagree with assignments |
| primary supervisor | `ResidentSupervisorAssignment` | Not completion-gating | canonical assignment | admin/service controlled | D/E | correct model; resident selection API missing |
| pending supervisor details | `PendingSupervisorAssignment` | No | structured free text | created only during admin account creation | D today | resident cannot submit “not found” details |
| `declaration_accepted` | `ResidentProfile` | Required for completion | boolean | once accepted via endpoint; no revoke path | A/E | duplicate declaration model unused |
| `declaration_accepted_at` | `ResidentProfile` | Derived | timestamp | server-set | E | should be tied to declaration/version snapshot |
| `is_profile_complete` | `User` | Derived | boolean | central registry calculation | E | does not include all resident-only fields itself |
| `profile_status` | `ResidentProfile` | Derived | INCOMPLETE/COMPLETE | central registry | E | not onboarding approval status |
| schema versions | `ResidentProfile` | Derived | positive integers | registry version currently 1 | E | viable but registry split must be removed |
| research/thesis baseline | training domain models | No | domain status/text | resident onboarding setter can write status | F | should not be onboarding authority without explicit policy |
| workshop completion dates | `ResidentWorkshopCompletion` | No | date per workshop | resident can create/update/delete | F | training evidence semantics need contract decision |
| document status/review fields | `ResidentDocument` | requirement-dependent | status enum | partly server-controlled | E/D | defer eligibility and aggregate gating absent |

**M1 ownership decision required:** enrolment facts (site, department, programme, session, specialty, dates, level) should normally be admin-controlled or resident-proposed then approved. They must not remain unrestricted after approval. Classes B and C cannot exist until an application state and correction scope exist.

## 7. Supervision architecture

### Canonical path

`ResidentSupervisorAssignment` is the canonical relationship. It stores resident and supervisor profiles, assignment type (`PRIMARY`/`CO_SUPERVISOR`), status, active flag, dates, change reason, actors and history. Database constraints prevent more than one active primary and duplicate active assignment tuples. Transactional services create, end and change the primary supervisor and emit audit events.

API behavior:

- `/api/supervision/assignments/`: residents see own; supervisors see their assignments; admins see all. Mutation is admin-only.
- `/api/supervision/change-primary/`: admin-only transactional primary change.
- `/api/supervision/options/`: any authenticated user receives resident and supervisor option sets; this is overly broad for mobile lookup.
- `/api/pending-supervisor-links/`: admin-only list and resolution/create-supervisor workflow.
- academic resident and supervisor summaries consume canonical supervision services.

### Missing resident-first workflow

- no scoped supervisor search contract designed for residents;
- no resident action to declare/select an existing supervisor;
- no resident action to submit structured “supervisor not found” details;
- pending links can be created during admin account creation but not by the resident onboarding flow;
- no resident-visible resolution lifecycle beyond summary state;
- no onboarding review link between a declaration and the final assignment.

### Do not use

- deprecated `User.supervisor` and `/api/users/assigned-pgs/` compatibility behavior;
- old `/api/supervision-links/` or imported/legacy link pathways;
- anything under `sims._legacy`.

### Security finding

`/api/supervisors/residents/{resident_id}/progress/` has an object-authorization gap: any supervisor can request any resident ID. `/api/supervision/options/` and `/api/academics/options/` also enumerate all residents and supervisors to any authenticated caller. M1 must scope these endpoints or replace their mobile use with a purpose-specific, non-enumerable search contract.

## 8. Document architecture

### Current model and API

`ResidentDocumentRequirement` defines type, label, stage (`ONBOARDING`, `DURING_TRAINING`, `OPTIONAL`), programme/department scope, required flag and active/order state. `ResidentDocument` records one fulfillment per resident/requirement with file, filename, dates, status, reviewer, remarks and archive metadata.

Residents/admins can list records and upload or replace a file via multipart. Upload is limited to 10 MiB and moves status to `PENDING_REVIEW`. Admins can review to `VERIFIED` or `REUPLOAD_REQUIRED`. Residents can call `defer`.

### Camera/gallery/PDF/file support

Multipart upload is technically compatible with Android camera output, gallery content, PDFs and document-provider files. The Android client should copy a selected content URI to a controlled upload stream, preserve a safe display filename, and never rely on filesystem paths. This technical compatibility does not make the upload safe: the backend currently has no allow-list or content inspection.

### Gaps and blockers

- **P0:** Caddy serves `/media/*` directly and publicly with cache headers. API authorization is bypassed for resident files.
- no authenticated download/preview endpoint, signed short-lived URL, or protected object storage policy;
- no MIME, extension, magic-byte, malware, image-dimension, or PDF validation;
- defer is allowed for any document the resident owns, including required-onboarding requirements; eligibility is not enforced;
- “outstanding” calculation includes only `DEFERRED` and `REUPLOAD_REQUIRED`, omitting `NOT_STARTED` and other incomplete states;
- replacement overwrites the file reference without a dedicated version/audit contract or concurrency control;
- no explicit stale-file cleanup/retention behavior was found;
- GET onboarding state creates fulfillment rows;
- document review is not connected to an aggregate onboarding submission/approval;
- supervisor document-completion summary is absent.

File delivery and upload validation must be fixed before Android exposes document upload or viewing.

## 9. Resident post-onboarding data availability

| Data | Existing source | Readiness |
|---|---|---|
| Active programme/start/current level/status | academic resident summary and training record | READY WITH MINOR ADAPTATION |
| Department/training site/session | `/api/academics/residents/me/summary/` | READY |
| Training end date | academic summary | READY |
| Primary/co-supervisors | academic resident summary / supervision summary | READY |
| Workshop count/details | training resident summary and `/api/my/workshops/` | READY WITH CONTRACT CHOICE |
| Document summary | onboarding/auth state plus document list | PARTIAL; incomplete count semantics |
| Logbook status/count | `/api/academics/logbook-entries/` and progress/reporting | PARTIAL; no lightweight canonical MVP summary |
| Research/thesis status | training resident summary and dedicated routes | READY but outside onboarding core |
| Recent actions | audit APIs are administrative; no resident activity feed contract | MISSING API / defer |
| Notifications | notification list/unread APIs | PARTIAL |

There are two overlapping resident summary families: `/api/residents/me/summary/` under training and `/api/academics/residents/me/summary/`. They expose different shapes. The web resident dashboard uses the academics summary. M1 should designate one stable mobile summary contract or a bootstrap aggregation without duplicating models.

The active logbook API is the academics route family, while training still contains a separate `LogbookEntry` model used by training calculations. Android must not guess between them; M1 needs a documented canonical source and contract-level tests.

## 10. Supervisor and staff readiness

### Supervisor MVP

- own identity/profile: available, but profile viewset authorization must be fixed;
- assigned residents: academics supervisor summary is scoped through `ResidentSupervisorAssignment`;
- resident training status: summary contains programme/year/status; detailed training progress endpoint has an IDOR blocker;
- resident onboarding status: no supervisor-scoped API;
- resident document completion: no supervisor-scoped summary;
- direct review actions remain broader future scope.

Verdict: **PARTIAL**.

### Admin/support-staff MVP

The web “onboarding” route redirects to `/users/new`; there is no dedicated onboarding operations overview with the locked lifecycle buckets. User/profile lists can approximate incomplete profile counts for admins, but not `NOT_STARTED`, `IN_PROGRESS`, `SUBMITTED`, `PENDING_REVIEW`, `CORRECTION_REQUIRED`, `APPROVED`, or documents-incomplete in one canonical view.

`SUPPORT_STAFF` can enter the web UTRMC dashboard, but most backend administrative APIs correctly remain admin-only under current Update 0 policy. No delegated mobile staff permission model exists. Complex staff/admin operations should remain web-only in the MVP.

Verdict: **PARTIAL for admin read-only aggregation; BLOCKED/MISSING for the requested lifecycle overview; DEFER support-staff operations.**

## 11. Notification readiness

The backend has:

- `Notification` with recipient, actor, verb, title/body, channel, metadata, read timestamp and schedule timestamp;
- `NotificationPreference` for email/in-app and quiet hours;
- recipient-scoped paginated list, mark-read, preferences and unread-count endpoints;
- a service for in-app/email delivery;
- one rotation-ending helper and unit tests.

It does not have:

- Android push tokens, FCM/APNs delivery or device registration;
- a stable deep-link target schema (metadata is arbitrary);
- onboarding/document reminder event coverage;
- demonstrated scheduled execution wiring for the rotation helper;
- notification deduplication/idempotency contract;
- an unread count inside `/api/auth/me/` or another bootstrap response.

The frontend notification TypeScript types drift from the backend (`notification_type`, recipient, SMS and push fields are declared but not returned/supported). Android should consume a corrected backend contract, not copy those types.

Recommendation: retain backend event generation as canonical. In M1 define event verbs and typed navigation targets for onboarding/document events. Defer FCM transport to the notification implementation phase; Android can begin with authenticated polling after the security gates close.

## 12. Complete mobile feature-to-API matrix

| Mobile Feature | Web UI Exists | Existing Endpoint | Backend Service | Canonical Model | Permission | Android Readiness | Required Work |
|---|---:|---|---:|---|---|---|---|
| Login | Yes | `POST /api/auth/login/` | SimpleJWT serializer | `User` | Public + throttle | READY WITH MINOR ADAPTATION | contract tests; secure Android storage |
| Logout | Yes | `POST /api/auth/logout/` | No revocation | JWT refresh | Authenticated | PARTIAL | implement/test token revocation policy |
| Refresh | implicit | `POST /api/auth/refresh/` | SimpleJWT | JWT | refresh token | PARTIAL | settle rotation; return/store new refresh consistently |
| Current user | Yes | `GET /api/auth/me/` | completion services | User + role profile | self | READY WITH MINOR ADAPTATION | schema serializer/version; eliminate GET writes |
| Role/permissions | Yes | token + `/api/auth/me/` | permission classes | `User.role` | self | BLOCKED | close writable-role/profile authorization flaws |
| Change password | Yes | `POST /api/auth/change-password/` | direct view | User | self | PARTIAL | call Django validators; revoke other sessions as policy dictates |
| Password reset | Yes | reset request/confirm | Django token generator | User | Public | PARTIAL | stable universal/app-link URL and throttling tests |
| Onboarding state | Yes | auth onboarding/state + `/me` | state builder | several models | resident self | PARTIAL | one canonical state schema; no GET mutations |
| Personal profile draft | Yes | `PATCH /api/auth/onboarding/` | field setter | User/ResidentProfile | resident self | PARTIAL | validation and field ownership |
| Training profile draft | Yes | same | field setter | ResidentTrainingRecord | resident self | PARTIAL | ownership, compatibility and locking rules |
| Programme/department choices | Yes | `/api/identity/options/` | query view | master models | authenticated | READY WITH MINOR ADAPTATION | conditional/scoped options and stable IDs |
| Supervisor search | admin web only | `/api/supervision/options/` | query view | SupervisorProfile | any authenticated | PARTIAL | resident-safe scoped search; stop broad enumeration |
| Select existing supervisor | admin creation only | no resident action | creation service can assign | Assignment | admin | MISSING API | expose reviewed proposal/declaration action |
| Supervisor not found | admin creation only | no resident create action | pending model/service fragments | Pending assignment | admin | MISSING API | focused resident submission endpoint/action |
| Save progress | Yes | `PATCH /api/auth/onboarding/` | field setter | multiple | resident self | READY WITH MINOR ADAPTATION | revision/ETag semantics; normalized errors |
| Submit onboarding | No real submit | declaration POST only | none | none | resident | MISSING API | canonical transition/action |
| Admin review | No | none | none | none | none | MISSING API | review queue and transition service |
| Correction/resubmit | No | none | none | none | none | MISSING API | correction scope, comments and resubmit transitions |
| Approval status | No | boolean “complete” only | none | none | self | MISSING API | explicit state/read model |
| Document requirements | Yes admin | `/api/resident-document-requirements/` | queryset | requirement | auth read/admin write | PARTIAL | scope response and defer policy |
| Document upload/replace | Yes | document upload action | view logic | ResidentDocument | owner/admin | BLOCKED | protected delivery + validation/version contract |
| Document review/status | Yes minimal | review/list | view logic | ResidentDocument | admin/owner read | PARTIAL | aggregate linkage; consistent status semantics |
| Outstanding documents | Yes minimal | `/me`, onboarding, list | list calculation | requirement/document | self | PARTIAL | include all incomplete required states; reminders |
| Resident training summary | Yes | academics and training summaries | summary services/view | TrainingRecord et al. | self | READY WITH MINOR ADAPTATION | choose one contract |
| Workshop summary | Yes | training summary / my workshops | view/service fragments | WorkshopCompletion | self | READY WITH MINOR ADAPTATION | choose summary source |
| Logbook summary | Yes broad | academics logbook/progress APIs | academics services | academics LogbookEntry | scoped | PARTIAL | resolve duplicate-model ambiguity; lightweight summary |
| Resident supervisor summary | Yes | academics resident summary | supervision service | Assignment | self/admin/scoped | READY | contract tests |
| Supervisor assigned residents | Yes | academics supervisor summary | supervision/academics services | Assignment/TrainingRecord | supervisor self | READY WITH MINOR ADAPTATION | add onboarding/doc summary |
| Supervisor resident status | broad web | training progress by resident | view aggregation | training models | supervisor/admin | BLOCKED | enforce assignment object permission |
| Admin onboarding overview | No | none | none | none | admin | MISSING API | aggregate after state model exists |
| Support-staff overview | dashboard only | no scoped lifecycle API | none | none | mostly denied | DEFER / PARTIAL | explicit future delegated permission decision |
| Notifications | API helper exists | list/mark/read count/preferences | NotificationService | Notification | self | PARTIAL | events, target contract, push later |
| AdminOps | No current mobile domain | none applicable | none | none | technical admin | LEGACY / DO NOT USE | keep out of MVP |

## 13. API gap classification

| Gap | Preferred treatment | Reason |
|---|---|---|
| Secure self-profile update | **C — extend endpoint/serializer** | allow-list self-editable fields; do not create a parallel profile API |
| Role-profile viewset authorization | **C — extend endpoints** | object/queryset and mutation permissions belong on existing canonical routes |
| JWT logout/rotation | **C — extend endpoint/configuration** | existing token routes are correct boundary |
| Onboarding application state | **D/E — expose a focused backend service/action** | canonical transitions are missing, not merely serialization |
| Onboarding review/correction | **E — focused endpoints/actions** | distinct state transitions with audit and permissions |
| Mobile onboarding read model | **B/F — extend schema or aggregate** | reuse existing models; consider bootstrap only after contract is stable |
| Resident supervisor existing/not-found declaration | **D/E** | reuse assignment/pending models and service logic with resident-safe actions |
| Protected documents | **C/E** | secure existing document route with authenticated stream/signed delivery |
| Upload validation | **C** | extend current upload action/service |
| Outstanding-document summary | **B/D** | expose corrected calculation; do not duplicate it in Android |
| Supervisor onboarding/document snapshot | **B/F** | extend canonical supervisor summary or aggregate |
| Admin lifecycle overview | **F — aggregate endpoint** | only after canonical onboarding state exists |
| Notification deep-link target | **B** | extend serializer/model metadata convention |
| Push delivery | **G — defer** | polling is adequate for early foundation; event correctness first |
| Resident recent activity | **G — defer** | not required for onboarding-first M1 |
| AdminOps/backup/bridge | **G — defer** | explicitly outside mobile MVP |

## 14. Mobile bootstrap assessment

**Verdict: RECOMMENDED, but DEFER implementation until the M1 domain contracts and security fixes are complete.**

A read-only `GET /api/mobile/bootstrap/` can reduce startup round trips and give the app one coherent snapshot of user, role, permissions, onboarding state, profile/training/supervision summaries, outstanding documents and unread count. It must be an aggregation over existing services/models, not a second business-logic layer or mobile database.

Recommended constraints:

- authenticated and role-shaped;
- explicit schema version and server time;
- additive evolution only within a major contract version;
- no side effects;
- no raw file URLs;
- compact summaries with links/IDs for detail endpoints;
- conditional caching/ETag and a documented staleness policy;
- unavailable domains represented predictably, not omitted arbitrarily.

It is not a substitute for missing onboarding transitions or authorization fixes.

## 15. Error contract assessment

Current responses are inconsistent:

- serializer field maps such as `{field: [messages]}`;
- `{detail: ...}` from DRF and custom views;
- `{error: ...}` from authentication views;
- raw `str(exception)` in some identity endpoints;
- parser/model errors that may surface differently;
- throttle and authentication errors use DRF defaults;
- no consistent machine-readable conflict/state-transition code;
- upload errors are plain detail strings.

M1 should introduce an additive normalization envelope for mobile-relevant endpoints, for example:

```json
{
  "code": "ONBOARDING_INVALID_TRANSITION",
  "message": "The onboarding application cannot be submitted yet.",
  "field_errors": {"training_start_date": ["Enter a valid date."]},
  "meta": {"request_id": "...", "current_state": "IN_PROGRESS"}
}
```

HTTP status remains authoritative: 400 validation, 401 authentication, 403 authorization, 404 non-disclosing absence, 409 state/version conflict, 413 upload size, 415 media type, 429 throttle, and 5xx server failure. Do not leak exception internals. Android `core/network` should map this contract to typed failures while retaining a safe fallback for legacy DRF errors.

## 16. Security findings

### P0 — blocks Android production exposure

1. **Self privilege escalation:** `UserSerializer` exposes writable `role`, `is_active`, and `username`; `/api/auth/profile/update/` applies it to the caller. Use a dedicated self-profile serializer with an explicit allow-list. Add negative tests for every privileged field.
2. **Role-profile API authorization:** Admin/Resident/Supervisor/SupportStaff profile viewsets inherit authenticated-only permission and only guard retrieve. Scope all querysets, block unauthorized list/create/update/destroy, and enforce object-level permissions.
3. **Public resident files:** Caddy directly serves `/media/*`; API-returned file URLs bypass authorization. Move protected documents behind authenticated delivery or short-lived signed object URLs and remove public caching for private content.
4. **Supervisor-to-resident IDOR:** training progress accepts any resident ID for any supervisor. Verify active `ResidentSupervisorAssignment` before lookup/response, using non-disclosing 404/403 policy.

### P1 — required before onboarding/document release

- logout does not revoke refresh tokens; refresh rotation behavior is not coherent across web and server;
- password change/reset do not consistently invoke Django password validators;
- archived-account login/refresh policy is not explicitly enforced independently of `is_active`;
- resident can change institution-controlled enrolment facts and domain statuses without approval/locking;
- supervisor/academic options enumerate people too broadly;
- uploads accept arbitrary content up to 10 MiB without type/content validation or malware strategy;
- defer eligibility is unenforced;
- document URLs and original filenames may expose personal information;
- onboarding GET performs writes, complicating retries, caching and audit expectations;
- frontend logs complete API error bodies to the browser console; sensitive validation responses should be reviewed;
- password reset link host is request-derived and mobile deep-link handling is unspecified.

### Existing strengths

- production settings support HTTPS redirects, secure cookies and HSTS;
- native Bearer auth avoids CSRF coupling;
- global authenticated-by-default DRF posture;
- canonical supervision list querysets and notification list are recipient/scoped;
- transactional identity and supervision services;
- audit and model history foundations;
- no client-side secret is required for JWT login.

## 17. Android module architecture verdict

**Scaffold verdict: PASS; no directory changes required in M0.**

```text
android/
├── app/
├── core/
│   ├── common/
│   ├── model/
│   ├── network/
│   ├── auth/
│   ├── data/
│   ├── database/
│   ├── designsystem/
│   ├── navigation/
│   └── testing/
└── feature/
    ├── authentication/
    ├── onboarding/
    ├── home/
    ├── profile/
    ├── training/
    ├── documents/
    ├── supervision/
    ├── notifications/
    └── supervisor/
```

Boundary guidance for M1:

- `app`: process lifecycle, composition and role/onboarding-aware root routing only.
- `core:model`: transport/domain representations of the versioned backend contract, not duplicated Django business models.
- `core:network`: HTTP, serialization, normalized errors, uploads, token refresh coordination.
- `core:auth`: credential storage/session state/logout; Keystore-backed secrets.
- `core:data`: repositories coordinating canonical remote data and cache.
- `core:database`: non-authoritative cache with user/session partitioning and wipe-on-logout.
- `feature:supervision`: resident-facing supervisor declaration/summary.
- `feature:supervisor`: supervisor-role home and assigned-resident experience.

Do not create reserved feature modules until their phase begins. No Gradle/toolchain/library choices should be locked until M1 selects supported versions from current official sources.

## 18. API version and compatibility recommendation

The API is currently unversioned in its URL despite an OpenAPI document version of `1.0.0`. Long-lived installed clients need a compatibility policy before release.

Recommended practical strategy:

1. stabilize existing web routes and make additive fixes first;
2. define a versioned mobile contract boundary (`/api/v1/mobile/...` or an equivalent negotiated media type) for bootstrap and onboarding orchestration, while reusing stable canonical endpoints where appropriate;
3. publish generated OpenAPI artifacts and snapshot/diff them in CI;
4. treat field additions as optional/additive within v1; never silently rename/remove or change enum meaning;
5. return contract/schema version, minimum supported app version and upgrade guidance from bootstrap/config—not from duplicated business rules;
6. use server-driven onboarding fields and transitions so new required fields do not require an immediate app release;
7. maintain at least one supported older Android contract in backend tests during rollout;
8. use idempotency keys and optimistic versioning for submit/upload/transition actions.

Do not version every existing endpoint merely for appearance. Version the mobile-facing orchestration contract where compatibility risk is real.

## 19. Required backend work

### Release gates

1. close all four P0 authorization/file-delivery findings and add regression tests;
2. define one canonical onboarding application model/state service and audited transitions;
3. reconcile central profile requirements with resident onboarding requirements;
4. decide and enforce ownership/locking for enrolment and training fields;
5. expose resident-safe supervisor search/declaration and not-found submission using canonical models;
6. implement protected document delivery, upload validation, defer eligibility and complete outstanding calculation;
7. normalize mobile-relevant error responses and state conflicts;
8. settle JWT refresh rotation, blacklist/logout and archived-account behavior;
9. designate canonical resident/supervisor/logbook summary sources;
10. emit onboarding/document notifications from backend transition services.

### Useful aggregation after gates

- read-only mobile bootstrap;
- admin onboarding overview;
- supervisor assigned-resident onboarding/document summary.

## 20. Required Android foundation work

After backend contracts are locked, M1 Android foundation should establish only:

- Gradle/version catalog and CI-supported toolchain;
- environment/base-URL configuration with production HTTPS enforcement;
- HTTP client, JSON serialization and normalized-error adapter;
- single-flight token refresh, Keystore-backed refresh storage, memory access token, secure logout/cache wipe;
- contract DTOs and repository interfaces for auth/me/bootstrap/onboarding;
- root routing based exclusively on backend `allowed_next_route`/state semantics;
- online-first cache boundaries and per-user data isolation;
- multipart content-URI upload abstraction, without building onboarding UI;
- unit/contract-test fixtures generated or verified against backend schemas;
- logging redaction and release network-security configuration.

## 21. Test requirements

### Existing useful coverage

- identity service, four roles, profile creation/repair and onboarding route behavior;
- resident onboarding draft/declaration and basic document defer/upload/review permission;
- supervision service constraints, changes and scoped lists;
- academics resident/supervisor summary permissions;
- training summaries and domain views;
- notification list scoping, read state, preferences and service behavior;
- frontend auth API, route guards, completion page and dashboards.

### M1 contract/security tests required

- self-profile endpoint rejects role, activity, username and all privileged fields;
- every role-profile viewset action is tested by all four roles and anonymous callers;
- supervisor cannot access unassigned resident progress, including guessed IDs;
- resident documents cannot be fetched without authorization and cannot cross resident boundaries;
- MIME/magic-byte/extension/size cases for camera JPEG/PNG, PDF and invalid/polyglot uploads;
- defer allowed and denied cases by requirement stage/policy;
- full onboarding state transition table, invalid transitions, edit locks, correction scopes, resubmit and idempotency;
- two clients editing/submitting concurrently returns a defined conflict;
- required-field schema increment forces next-login completion without corrupting approval state;
- supervisor existing/not-found/resolution flow and isolation;
- JWT expiration, rotation, reuse, logout revocation, archived/inactive account and password validators;
- normalized 400/401/403/404/409/413/415/429 errors;
- bootstrap role-shaped payload, no side effects, query budget and compatibility snapshot;
- notification event idempotency and typed targets;
- OpenAPI breaking-change detection;
- Android mock-server tests for refresh races, process restart, offline cache, errors and upload retry.

## 22. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Shipping UI before state contract | divergent web/mobile behavior | backend state machine and contract tests first |
| Authorization assumptions inherited from web hiding | cross-user/role data exposure | server-side matrix tests and object scoping |
| Public file delivery | disclosure of identity/training documents | authenticated/signed delivery before upload release |
| Two completion registries | users loop in onboarding or bypass fields | one authoritative registry/read model |
| Overlapping training/academics summaries and logbooks | inconsistent resident status | designate canonical sources in M1 |
| Long-lived unversioned app contract | forced upgrades/breakage | additive v1 mobile contract and CI diffing |
| Mobile retry of non-idempotent actions | duplicate submissions/events | idempotency keys and version checks |
| Offline cache of personal data | device disclosure/cross-account residue | minimal encrypted/partitioned cache; wipe on logout |
| Push before event semantics | duplicated or misleading alerts | backend event contract before FCM |

## 23. Exact Phase M1 implementation backlog

Order is intentional; later items depend on earlier contract/security decisions.

1. **M1-01 — Authorization emergency fixes:** dedicated self-profile serializer; lock role-profile viewsets; supervisor progress assignment check; exhaustive RBAC tests.
2. **M1-02 — Protected resident documents:** remove public private-media path, implement authorized delivery/signed storage, cache policy and cross-user tests.
3. **M1-03 — JWT session contract:** blacklist/rotation/logout decision, rotated-token response handling, archived/inactive behavior, password validation and tests.
4. **M1-04 — Onboarding domain decision record:** authoritative fields, ownership classes, defer rules, reviewer permissions, state/transition diagram and compatibility plan.
5. **M1-05 — Canonical onboarding service/model:** audited transactional transitions, revision/version, timestamps and correction scope; migrate/backfill safely if required.
6. **M1-06 — Unified requirement registry:** one server-driven field schema with types, choices, validation, schema version and all resident requirements.
7. **M1-07 — Resident draft contract:** retain save progress, enforce validation/locking, eliminate GET side effects, return normalized errors.
8. **M1-08 — Supervisor declaration:** scoped lookup, existing selection proposal, structured not-found submission, pending resolution and resident status.
9. **M1-09 — Document policy:** MIME/content checks, eligible defer, complete outstanding calculation, replacement/version/audit behavior and onboarding linkage.
10. **M1-10 — Review APIs:** resident submit/resubmit/status plus admin review/correction/approve and read-only overview.
11. **M1-11 — Summary contract rationalization:** name canonical resident, supervisor, workshop and logbook sources; add missing document/onboarding summaries.
12. **M1-12 — Notification events:** onboarding/document verbs, typed targets, unread aggregation and idempotency; no push transport yet.
13. **M1-13 — Error and OpenAPI contract:** normalized envelope, 409 semantics, generated schema snapshots and breaking-change CI.
14. **M1-14 — Mobile bootstrap:** implement only after M1-05 through M1-13; side-effect-free, role-shaped, versioned and query-tested.
15. **M1-15 — Android foundation:** Gradle/toolchain, networking/auth/storage/contracts/root routing and mock-server tests; no onboarding screens.
16. **M1-16 — Web compatibility update:** adapt web to the same corrected refresh, onboarding transition and error contracts; remove reliance on unsafe behavior.
17. **M1-17 — Security verification gate:** automated API matrix plus deployment check proving private media is not publicly served.

## 24. Final verdict

**CONDITIONAL GO**

Proceed to **Phase M1 — Mobile API Contract, Security Remediation & Android Foundation** only. Do not begin onboarding UI implementation until M1-01 through M1-10 are verified, and do not expose resident document upload/view until M1-02 and M1-09 pass security tests.

The backend remains the canonical source of truth. No duplicate mobile business rules, data models, APIs or database were introduced during M0.
