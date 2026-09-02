# PGR SIMS Android
## Locked Product Policy, MVP Scope & Production Roadmap

**Status:** LOCKED BASELINE  
**Purpose:** Authoritative product and architecture context for development of the PGR SIMS Android application.

---

# 1. PRODUCT POLICY

PGR SIMS Android is not a separate postgraduate management system and is not intended to remain a limited onboarding utility.

It is the Android client of the same PGR SIMS platform currently accessed through the web application.

The strategic end-state is:

```text
                         PGR SIMS
                    CANONICAL BACKEND
                          Django
                            │
                  Canonical Services/API
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Web Application             Android Application
              │                           │
              └──── SAME SYSTEM / DATA ──┘
```

The Android MVP deliberately focuses primarily on resident onboarding because the immediate business objective is to increase onboarding compliance and reduce resident friction.

Over successive releases, Android will progressively gain the major postgraduate management capabilities available through the web application.

The long-term goal is functional parity where appropriate so that authorized users can choose web or Android while interacting with the same account, data, permissions, workflows and backend.

---

# 2. CORE ARCHITECTURE POLICY

## Backend is canonical

The backend remains authoritative for:

- users
- authentication
- roles
- permissions
- resident profiles
- training records
- onboarding status
- onboarding validation
- programmes
- departments
- supervisor assignments
- `ResidentSupervisorAssignment`
- documents
- workshop status
- logbooks
- assessments
- research workflows
- approval states
- administrative rules
- audit-relevant operations

Android is a client.

Web is a client.

Neither frontend should independently redefine canonical business rules.

---

# 3. API-FIRST FRONTEND POLICY

Every functional Android UI capability must map to an explicit backend API/service capability.

```text
Android UI
    ↓
API
    ↓
Canonical backend service
    ↓
Canonical database
```

Android must NOT:

- manipulate backend persistence directly
- recreate supervision rules
- recreate onboarding validation
- independently calculate authoritative training status
- maintain a separate resident profile database
- maintain a separate supervisor assignment model
- invent parallel approval states

Where existing web APIs are canonical and suitable, Android should reuse them.

Mobile-specific endpoints should be added only where aggregation, mobile performance or a genuine client requirement justifies them.

---

# 4. IMMEDIATE BUSINESS OBJECTIVE

The first Android production release exists primarily to improve resident onboarding compliance.

Current intended flow:

```text
Administration creates resident account
        ↓
Resident receives institutional login credentials
        ↓
Resident installs PGR SIMS Android
        ↓
Resident logs in
        ↓
First-login onboarding is required
        ↓
Resident completes personal/training profile
        ↓
Resident declares/selects supervisor
        ↓
Resident uploads documents OR defers eligible documents
        ↓
Resident reviews information
        ↓
Resident submits profile
        ↓
Pending administrative review
        ↓
Approved
OR
Correction required → edit → resubmit
```

There is NO resident self-registration in MVP.

Accounts continue to originate from the canonical institutional onboarding workflow.

---

# 5. RESIDENT ONBOARDING — LOCKED MVP

First login should route residents with incomplete onboarding directly into the onboarding workflow rather than an empty dashboard.

Core stages:

1. Personal information
2. Training information
3. Programme/department details
4. Supervisor information
5. Documents
6. Review and submit

Existing backend data should be pre-populated wherever available.

Progress should be retained between sessions.

Backend determines authoritative completion/submission status.

---

# 6. SUPERVISOR WORKFLOW

Canonical supervision remains based on:

`ResidentSupervisorAssignment`

If the supervisor already exists:

- resident selects/searches for the supervisor through the approved workflow

If the supervisor does not exist:

- resident provides the required identifying details
- a pending resolution workflow is created
- the app must not create an uncontrolled duplicate supervisor identity
- administration subsequently resolves the supervisor relationship

Android must use the existing supervision service architecture.

---

# 7. DOCUMENT POLICY

Eligible onboarding documents may be deferred during initial onboarding.

Missing eligible documents must not unnecessarily prevent initial profile submission.

However, deferred does NOT mean completed.

Outstanding documents remain persistently visible after onboarding.

The app should remind the resident at subsequent login until requirements are fulfilled.

Mobile document capture should support:

- camera
- gallery/photo picker
- files
- PDF
- preview
- upload
- replacement/re-upload
- review status
- rejection/correction status

Document status remains backend-authoritative.

---

# 8. ONBOARDING STATE MODEL

Recommended canonical lifecycle:

```text
ACCOUNT CREATED
    ↓
NOT STARTED
    ↓
IN PROGRESS
    ↓
SUBMITTED
    ↓
PENDING REVIEW
    ↓
 ┌─────────────────────┐
 │                     │
APPROVED        CORRECTION REQUIRED
                       ↓
                   RESIDENT EDITS
                       ↓
                   RESUBMITTED
```

Document completion/verification is related to onboarding but must remain separately representable.

---

# 9. MVP ROLE SCOPE

## Resident — PRIMARY

MVP capabilities:

- authentication
- first-login onboarding
- personal information
- training information
- supervisor declaration
- missing-supervisor workflow
- document upload
- eligible document deferral
- review/submit onboarding
- correction/resubmission
- profile/onboarding status
- persistent outstanding-document reminders
- own profile
- basic active training information
- basic supervisor information
- document status
- workshop status where already available
- logbook summary/status where already available

The MVP should NOT initially allow new patient/logbook entries.

## Supervisor — LIMITED MVP

- authentication
- own information
- assigned residents
- basic resident training status
- resident onboarding status
- profile completion/submission status
- document-completion summary where appropriate

Advanced supervisor actions are deferred.

## Staff/Admin — LIMITED MVP

Android may provide basic onboarding monitoring/status visibility.

Complex administration remains web-first during MVP.

---

# 10. POST-ONBOARDING RESIDENT EXPERIENCE

Suggested MVP navigation:

- Home
- Training
- Documents
- Profile

Home should prioritize actionable information.

Examples:

- onboarding status
- profile approval
- outstanding documents
- training status
- supervisor
- workshop summary
- logbook summary
- recent relevant updates

Design principle:

**Action → Context → Detail**

Avoid reproducing dense desktop administration tables on mobile.

---

# 11. MVP NON-GOALS

Explicitly outside initial MVP:

- resident self-registration
- complete AdminOps
- bulk user import
- programme configuration
- complex admin configuration
- full mobile approval engine
- advanced analytics
- complete audit explorer
- new mobile patient/logbook entry
- workplace-based assessments
- detailed supervisor assessments
- complex research workflow
- attendance
- leave
- rotation management
- Google Bridge
- complex offline transactional synchronization

These exclusions are scope controls, not permanent exclusions.

---

# 12. LONG-TERM RELEASE POLICY

## Version 1 — Onboarding MVP

Focus:

- secure authentication
- onboarding
- supervision declaration
- documents/compliance
- submission/correction lifecycle
- basic resident information
- basic supervisor/staff status views

## Version 1.x — Stabilization

Focus:

- onboarding UX
- reliability
- upload robustness
- compliance analytics
- notification quality
- authentication/session improvements
- production issues discovered through real use

## Version 2 — Resident Companion

Progressively add:

- richer training dashboard
- workshops
- research milestones
- full document wallet
- training history
- announcements
- notification centre
- richer profile workflows
- logbook browsing

## Version 3 — Active Training Workflows

Likely additions:

- create logbook entries
- patient/case entries
- procedures
- competencies
- evidence submission
- supervisor review
- assessment requests
- research progress
- rotation workflows
- other high-frequency resident operations

## Version 3/4 and beyond — Functional Parity

Target:

Resident:
- complete relevant web functionality

Supervisor:
- complete relevant web functionality

Staff:
- major operational workflows

Admin:
- mobile-suitable administrative functions

Some extremely complex bulk/configuration screens may remain web-optimized, but Android and web must operate against the same canonical workflow and backend.

---

# 13. ANDROID TECHNICAL DIRECTION

Preferred platform:

- native Android
- Kotlin
- Jetpack Compose
- Material 3
- Coroutines / Flow
- Navigation Compose
- Hilt
- Retrofit / OkHttp
- Kotlin Serialization
- Room
- DataStore
- WorkManager
- Android Keystore-backed secure session handling

Exact dependency and version decisions must be confirmed during implementation against current supported stable versions.

---

# 14. PROPOSED ANDROID MODULE BOUNDARIES

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

Later feature modules can include:

- logbook
- workshops
- research
- assessments
- rotations
- attendance
- leave
- admin

---

# 15. CONNECTIVITY POLICY

Android should initially be:

**online-first with resilient read caching**

Canonical writes require confirmed backend synchronization.

Do not build complex offline conflict resolution in MVP.

Appropriate cached content may include:

- profile
- training identity
- supervisor information
- dashboard summaries
- document status
- notifications

The cache is never authoritative over backend state.

---

# 16. AUTHENTICATION POLICY

Android must use the same canonical PGR SIMS identity.

No mobile-specific identity database.

Security expectations include:

- HTTPS
- secure token/session storage
- no plaintext password persistence
- server-side permission checks
- token expiry/refresh strategy
- logout/session invalidation
- no secrets in logs

Administratively supplied initial credentials remain the onboarding entry mechanism.

Production technical review should determine the safest first-login password/change strategy without altering the locked account-creation workflow.

---

# 17. API COMPATIBILITY POLICY

Android will introduce long-lived installed client versions.

Therefore API evolution must account for older app versions.

Backend API changes should be backward-compatible wherever practical.

API contracts should be explicit and testable.

Android UI visibility is NOT authorization.

Backend must independently enforce permissions for every operation.

---

# 18. MOBILE BOOTSTRAP

A mobile bootstrap/aggregation capability should be assessed during Phase M0.

Potential concept:

`GET /api/mobile/bootstrap`

Possible returned domains:

- authenticated user
- role
- permissions
- onboarding state
- profile
- training summary
- supervision summary
- document summary
- workshop summary
- logbook summary
- unread notifications

Do not create this endpoint until existing APIs and data contracts are audited.

---

# 19. PRODUCTION DEVELOPMENT PHASES

## M0 — Backend & API Mobile Readiness Discovery
Audit existing architecture and establish API inventory, feature-to-endpoint map, missing APIs, legacy APIs, authentication readiness, permission model, onboarding contract, supervision contract, document contract, and mobile bootstrap requirements.

## M1 — Canonical Mobile API Contract
Normalize and extend backend API surfaces only where required.

## M2 — Android Platform Foundation
Establish production Android architecture, build system, modules, navigation, dependency injection, API client, serialization, error handling, design system, caching and tests.

## M3 — Authentication & Bootstrap
Implement login, session management, token lifecycle, bootstrap, role resolution, onboarding routing and failure/offline handling.

## M4 — Resident Onboarding
Implement complete first-login workflow.

## M5 — Documents & Compliance
Implement document capture/upload/status and persistent outstanding-document reminders.

## M6 — Resident Post-Onboarding Experience
Implement Home, Training, Documents, Profile, and available workshop/logbook summaries.

## M7 — Minimal Supervisor/Staff Views
Implement restricted role-specific visibility.

## M8 — Notifications & Compliance Layer
Implement in-app notifications, deep links, onboarding/document reminders and appropriate push capability.

## M9 — Hardening & Production Release
Include regression tests, Android tests, device compatibility, security validation, release AAB, CI integration and production acceptance.

---

# 20. PRIMARY VERSION 1 ACCEPTANCE TEST

A newly created resident who has never used PGR SIMS must be able to:

1. receive institutional credentials
2. install Android application
3. authenticate
4. complete mandatory personal information
5. complete training information
6. declare/select supervisor
7. skip eligible documents
8. submit onboarding
9. see pending-review state
10. receive correction state if applicable
11. edit/resubmit
12. see approved state
13. later upload missing documents
14. see canonical training/profile information

without requiring the web frontend.

Every Android change must appear in the same canonical PGR SIMS record visible through the web application.

Every relevant backend/web change must be reflected in Android following refresh/synchronization.

---

# 21. DEVELOPMENT GOVERNANCE

For every Android feature verify:

```text
UI
→ API
→ canonical backend service
→ model/data source
→ permission enforcement
→ tests
```

No orphan mobile UI.

No Android-only authoritative workflow.

No duplicate business logic.

No hidden backend feature without intended frontend exposure where functionality is user-facing.

---

# 22. NEXT ACTIVE PHASE

The next active phase after repository scaffolding is:

**M0 — Android Mobile Architecture & API Readiness Discovery**

M0 must produce a clear GO / CONDITIONAL GO / NO-GO verdict before substantial feature implementation begins.
