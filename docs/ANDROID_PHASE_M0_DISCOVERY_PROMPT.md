# PGR SIMS ANDROID — PHASE M0
## Mobile Architecture & API Readiness Discovery Mega Sprint

You are working from the root of the existing PGR SIMS repository.

The Android scaffold has already been created.

Before doing anything, read:

`docs/ANDROID_MOBILE_PRODUCT_POLICY_AND_PRODUCTION_PLAN.md`

Treat that document as the authoritative locked Android product baseline.

Also inspect all existing project architecture/documentation relevant to:

- resident onboarding
- authentication
- roles/permissions
- resident profiles
- supervision
- `ResidentSupervisorAssignment`
- documents
- workshops
- logbooks
- notifications
- AdminOps
- frontend/backend API conventions

Do not contradict locked product decisions unless you discover a genuine technical impossibility or security-critical issue.

# MISSION

Perform a complete **Phase M0 Android Mobile Architecture & API Readiness Discovery**.

The objective is to establish precisely how a native Android application can become a first-class client of the existing canonical PGR SIMS backend.

This is primarily a DISCOVERY AND ARCHITECTURE phase.

Do NOT build the onboarding UI yet.
Do NOT start broad Android feature implementation.
Do NOT create APIs simply because they seem convenient.
First prove what exists.

# LOCKED ARCHITECTURE

```text
                         PGR SIMS
                    CANONICAL BACKEND
                            │
                    Services/API Layer
                            │
              ┌─────────────┴─────────────┐
              │                           │
         Web Frontend               Android App
```

The backend is authoritative.
Web and Android are clients.
Android must consume canonical APIs/services.
No duplicate mobile database or duplicate business logic is allowed.

# PRIMARY MVP GOAL

Version 1 is resident-first and onboarding-first.

```text
Administrator creates resident
→ resident receives credentials
→ resident installs Android app
→ login
→ first-login onboarding
→ personal profile
→ training profile
→ supervisor declaration
→ optional deferral of eligible documents
→ review
→ submit
→ admin review
→ approved or correction required
→ persistent missing-document compliance reminders
```

After onboarding, MVP provides lightweight resident status information.

Supervisor/staff functionality remains minimal initially.

Long-term Android target is progressive functional parity with the web application.

# STAGE 0 — REPOSITORY & SAFETY BASELINE

1. Inspect git status.
2. Record current branch/commit.
3. Identify uncommitted/untracked files.
4. Preserve unrelated work.
5. Identify backend root, web frontend root, android root, docs root, CI, deployment/configuration directories.

Do not delete or clean unrelated artifacts.

# STAGE 1 — CURRENT SYSTEM ARCHITECTURE MAP

Map the current PGR SIMS system.

Backend:
- framework/layout
- main apps/modules
- API framework
- serializers/schemas
- views/controllers
- services
- permission enforcement
- authentication system
- file/document storage
- notification infrastructure
- relevant background jobs

Web:
- API client abstraction
- authentication flow
- token/session strategy
- onboarding pages
- resident profile pages
- supervisor workflows
- document interfaces
- training/logbook/workshop status UI
- status/approval UI
- route structure

# STAGE 2 — AUTHENTICATION DISCOVERY

Trace end-to-end:

1. account creation
2. credential issuance
3. login endpoints
4. session/token mechanism
5. CSRF dependencies
6. cookie dependencies
7. refresh/session expiry
8. logout
9. role resolution
10. client permissions
11. native Android suitability
12. password-change/first-login support
13. rate limiting
14. browser assumptions

Classify: READY / PARTIAL / BLOCKED.

# STAGE 3 — RESIDENT ONBOARDING TRACE

Trace web UI → API → serializer/schema → endpoint → service/business logic → models.

Determine:
- validation
- status fields
- audit behavior
- approval process
- correction/resubmission
- first-login routing
- profile completeness logic

Determine the ACTUAL state machine from code.

Report documentation/code drift explicitly.

# STAGE 4 — PROFILE DATA MODEL

Classify every onboarding field:

A. resident-editable
B. resident-editable before approval only
C. correction-request controlled
D. administration-controlled
E. derived/system-controlled
F. ambiguous

Record field names, models, serializers, validation, required/optional state, choices and dependencies.

Create a canonical onboarding field matrix.

# STAGE 5 — SUPERVISION DISCOVERY

Verify current use of `ResidentSupervisorAssignment`.

Trace:
- supervisor lookup
- existing supervisor selection
- supervisor-not-found workflow
- pending supervisor details
- assignment creation
- primary supervisor rules
- `change_primary_supervisor`
- approval/resolution
- historical assignments
- permission enforcement

Identify any legacy/duplicate pathway Android must not use.

# STAGE 6 — DOCUMENT WORKFLOW DISCOVERY

Determine:
- document models
- required definitions
- optional/deferrable documents
- upload API
- file types
- file size rules
- storage backend
- authenticated download/view
- replacement
- verification
- rejection/correction
- reviewer workflow
- missing-document calculation
- reminders

Assess support for camera images, gallery images, PDFs and files without changing canonical semantics.

Identify security gaps.

# STAGE 7 — TRAINING STATUS / POST-ONBOARDING DATA

Audit existing APIs/data for:
- active programme
- department
- training start/end
- training year/stage
- active status
- primary supervisor
- workshop summary
- document summary
- logbook count/status
- research status if canonical
- recent relevant actions/notifications

Do not implement missing future features during M0.

# STAGE 8 — SUPERVISOR & STAFF MVP READINESS

Supervisor:
- own profile
- assigned residents
- resident onboarding status
- resident training status
- document completion summary

Staff/Admin:
- onboarding overview
- not started
- in progress
- submitted
- pending review
- correction required
- approved
- documents incomplete

Complex admin actions remain out of mobile MVP.

# STAGE 9 — NOTIFICATION DISCOVERY

Determine whether backend currently has:
- notification models
- event generation
- unread state
- API endpoints
- deep-link-equivalent targets
- email notifications
- background jobs
- push infrastructure

Recommend Android integration without duplicating backend event logic.

# STAGE 10 — COMPLETE FEATURE → API MATRIX

Produce:

| Mobile Feature | Web UI Exists | Existing Endpoint | Backend Service | Canonical Model | Permission | Android Readiness | Required Work |

Readiness values:
- READY
- READY WITH MINOR ADAPTATION
- PARTIAL
- MISSING API
- LEGACY / DO NOT USE
- BLOCKED

Cover at minimum:
- login/logout/current user
- role/permissions
- onboarding state
- personal/training profile
- programme/department choices
- supervisor search
- supervisor-not-found
- save-progress
- submit
- correction/resubmit
- approval status
- document requirements/upload/replace/status
- outstanding documents
- resident training summary
- workshop summary
- logbook summary
- resident supervisor summary
- supervisor assigned residents
- supervisor resident status
- admin/staff overview
- notifications

# STAGE 11 — IDENTIFY API GAPS

For every missing requirement determine:

A. reuse existing endpoint
B. extend serializer/schema
C. extend endpoint
D. expose existing service
E. create focused endpoint
F. aggregate/bootstrap
G. defer from MVP

Prefer reuse. Do not automatically create new APIs.

# STAGE 12 — MOBILE BOOTSTRAP ASSESSMENT

Assess a possible:

`GET /api/mobile/bootstrap`

Potential domains:
- user
- role
- permissions
- onboarding
- profile
- training
- supervision
- document summary
- workshop summary
- logbook summary
- unread notifications

Verdict:
- RECOMMENDED
- NOT REQUIRED
- DEFER

Do not implement during M0 unless explicitly justified and still within discovery limits.

# STAGE 13 — ERROR CONTRACT REVIEW

Assess current handling of:
- validation errors
- field errors
- auth errors
- permission errors
- conflict/state errors
- upload errors
- server errors

Recommend normalization only if needed.

# STAGE 14 — ANDROID ARCHITECTURE VALIDATION

Review scaffold and confirm/revise module boundaries.

Do not create implementation code yet.

# STAGE 15 — SECURITY REVIEW FOR MOBILE EXPOSURE

Check:
- HTTPS assumptions
- token handling
- browser-only trust assumptions
- CSRF coupling
- CORS relevance
- direct-object authorization
- file/download permissions
- information exposure
- enumeration risks
- resident/supervisor isolation
- staff/admin isolation
- frontend secrets
- logging of credentials/tokens
- password reset/change
- rate limiting

Report blockers explicitly.

# STAGE 16 — VERSIONING & COMPATIBILITY

Assess API versioning and recommend a practical compatibility strategy for long-lived Android clients.

Do not introduce unnecessary versioning changes during discovery.

# STAGE 17 — TEST COVERAGE

Find backend tests covering:
- authentication
- onboarding
- resident profiles
- supervision
- documents
- permissions

Identify gaps required before Android consumption.

Recommend M1 contract/API tests.

# STAGE 18 — AUTHORITATIVE M0 REPORT

Create:

`docs/ANDROID_PHASE_M0_API_READINESS_REPORT.md`

It must contain:

1. Executive verdict
2. Repository architecture
3. Current authentication architecture
4. Current onboarding architecture
5. Onboarding state machine
6. Resident field matrix
7. Supervision architecture
8. Document architecture
9. Resident post-onboarding data availability
10. Supervisor/staff readiness
11. Notification readiness
12. Complete feature/API matrix
13. API gaps
14. Mobile bootstrap verdict
15. Error contract assessment
16. Security findings
17. Android module architecture verdict
18. API/version compatibility recommendation
19. Required backend work
20. Required Android foundation work
21. Test requirements
22. Risks
23. Exact M1 implementation backlog
24. GO / CONDITIONAL GO / NO-GO verdict

# IMPLEMENTATION LIMIT FOR M0

You MAY make tiny non-functional documentation corrections if required.

You MUST NOT:
- build onboarding screens
- add broad Android production code
- redesign backend architecture
- migrate models
- create speculative endpoints
- remove legacy code
- perform unrelated refactoring

If a blocker is found, document it and continue discovery as far as possible.

# FINAL RESPONSE FORMAT

## VERDICT
GO / CONDITIONAL GO / NO-GO

## Key architecture finding

## Android-ready areas

## Backend/API gaps

## Security blockers

## Required M1 work

## Files created/modified

## Verification

## Next sprint

Do not begin M1 automatically.
