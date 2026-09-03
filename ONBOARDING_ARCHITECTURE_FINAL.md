# PGR SIMS Resident Onboarding Architecture Final

## Canonical architecture

- Authentication and account state: `sims.users.models.User`.
- Resident-owned profile: `sims.users.models.ResidentProfile`.
- Institution-controlled training: `sims.training.models.ResidentTrainingRecord`.
- Resolved supervision: `sims.supervision.models.ResidentSupervisorAssignment`.
- Unresolved supervisor names: `sims.supervision.models.PendingSupervisorAssignment`; this never creates a fake account.
- Generic resident documents and configurable requirements: `ResidentDocument` and `ResidentDocumentRequirement` in `sims.users.models`.
- Synopsis/thesis remains on `ResidentSubmission`, `SubmissionDocument`, `SubmissionRequirementTemplate`, `SubmissionReview`, and `SubmissionCertificate`.

## Onboarding behavior

`POST /api/users/` remains the universal creation endpoint. Resident bootstrap accepts institution-controlled program, department, training site, session, start date, and either an existing supervisor profile or a pending supervisor name. The service creates identity, profile, training record, assignment/pending record, and audit events transactionally. Generated resident usernames use `pgrNNN`; the temporary password is `pgfmu123` and password change is forced.

Profile completion remains distinct from document collection. Each configured requirement gets a resident fulfillment row. `DEFERRED` means the resident acknowledged the requirement and will upload later; it is not waived. Upload changes the item to `PENDING_REVIEW`. Admin review supports `VERIFIED` and `REUPLOAD_REQUIRED`. `/api/auth/me/` and `/api/resident-onboarding/state/` return specific pending uploads, allowing dashboard access while reminders persist.

The declaration is persisted on `ResidentProfile` and completion is recorded with `ONBOARDING_COMPLETED`. Training fields are read-only to residents. Document list/upload/review endpoints enforce owner/admin scope and a 10MB upload limit.

## Supervisor resolution

The admin pending-link API is `/api/pending-supervisor-links/`. `POST <id>/resolve/` links an existing `SupervisorProfile`; `POST <id>/create-supervisor/` invokes the canonical supervisor identity service and automatically creates the real assignment. New code does not use `User.supervisor` as authoritative. The legacy field remains only for compatibility and requires a later reconciled deletion.

## Frontend routes and APIs

- `/users/new` is the universal creation screen and shows credentials with copy/print actions.
- `/dashboard/resident/documents` is the resident document center.
- `/admin/pending-supervisor-links` is the admin queue.
- `/change-password`, `/complete-profile`, `ProtectedRoute`, and `/api/auth/me/` remain the single first-login guard flow.
- APIs: `/api/resident-documents/`, `/api/resident-document-requirements/`, `/api/pending-supervisor-links/`, `/api/resident-onboarding/state/`.

## Migration and technical debt

Forward migrations `users.0014` and `supervision.0002` add the new architecture. Historical migrations were not edited. Flexible bulk resident import now creates canonical assignments or pending links while retaining the deprecated direct FK for compatibility.

## Final stabilization status (2026-08-21)

The admin requirements UI is `/residents/document-requirements`; it supports list, create, edit,
enable/disable, required/optional, stage, display order, program scope, department scope, and
server-error reporting. The pending-supervisor UI is `/admin/pending-supervisor-links` and supports
linking an existing supervisor or creating and auto-linking one.

Active onboarding/supervision code no longer directly queries or writes `User.supervisor`. The field
is retained as `KEEP-DEPRECATED` compatibility data because legacy seed/test/import surfaces and
historical models still reference it. `User.email` remains the login address; profile email fields
are contact snapshots. `ResidentProfile` owns resident contact/registration data and
`ResidentTrainingRecord` owns institution-controlled training data. `User.home_hospital`,
`User.home_department`, `User.registration_number`, and `User.phone_number` remain compatibility
fields, not canonical onboarding owners.

The integrity audit reports zero residents in the current development database, hence zero
supervision conflicts, pending-with-assignment records, or duplicate active requirements. Forward
migrations are applied and no migration plan remains.

Targeted onboarding tests pass (4 tests), and the complete backend suite passes 830 tests with zero
failures and zero errors. Django checks, migration checks, migration plan validation, the integrity
audit, Python compilation, the legacy-supervision guard, and consolidation gate pass. Frontend
TypeScript, 37 Jest suites/107 tests, lint, and the production build (79 pages) pass. The new
`users.0014` migration uses additive database operations for profile declaration fields so clean
SQLite test databases do not rebuild the large historical/profile tables.

The final cleanup retains `User.supervisor` as deprecated compatibility data; no active onboarding
or supervision business logic reads or writes it. `User.home_hospital`, `User.home_department`,
`User.registration_number`, and `User.phone_number` are likewise retained compatibility fields.
The repository has no `compose.yml`, so the requested Docker compose validation is not applicable.

## Profile-level review gate (added 2026-09-02, Resident Onboarding MVP / Android)

Before this addition, `ResidentProfile.profile_status` (`INCOMPLETE`/`COMPLETE`) was purely a
computed required-field-completeness flag with no administrative review step: a resident's
`onboarding_complete` flag (`is_profile_complete AND declaration_accepted`) became true entirely
from the resident's own actions, with no admin "approve" or "request correction" gate on the
profile as a whole (per-document review via `ResidentDocument.status` already existed and is
unchanged). This is now closed additively:

- New fields on `ResidentProfile`: `review_status` (`NOT_SUBMITTED` / `PENDING_REVIEW` /
  `APPROVED` / `CORRECTION_REQUIRED`, migration `users.0015`), `review_note`, `submitted_at`,
  `reviewed_by`, `reviewed_at`. Tracked by the existing `HistoricalRecords()` on `ResidentProfile`
  — no parallel audit system was introduced.
- `POST /api/resident-onboarding/state/` (the existing declaration-accept "submit" action) now
  requires `user.is_profile_complete` (400 if not) and rejects re-submission once
  `review_status == APPROVED` (409). On success it sets `review_status = PENDING_REVIEW` and
  `submitted_at`; an `ActivityLog` verb of `ONBOARDING_RESUBMITTED` (vs. `ONBOARDING_COMPLETED` for
  a first submission) is recorded when resubmitting from `CORRECTION_REQUIRED`.
- New admin-only actions on the existing `ResidentProfileViewSet`
  (`permission: _is_manager`, i.e. superuser or `role=ADMIN` — same check already used for
  create/update/destroy on this viewset):
  - `POST /api/residents/<user_id>/approve-onboarding/` — requires `review_status == PENDING_REVIEW`
    (409 otherwise), sets `APPROVED` + `reviewed_by`/`reviewed_at`.
  - `POST /api/residents/<user_id>/request-onboarding-correction/` — requires a non-empty `reason`
    (400 otherwise) and `review_status` currently `PENDING_REVIEW` or `CORRECTION_REQUIRED` (409
    otherwise); sets `CORRECTION_REQUIRED`, stores `reason` in `review_note`, resets
    `declaration_accepted = False` (so the existing `onboarding_complete`/`allowed_next_route`
    routing logic remains unchanged and correctly sends the resident back through onboarding
    without needing its own edit).
  - Both actions record an `ActivityLog` entry (`ONBOARDING_APPROVED` /
    `ONBOARDING_CORRECTION_REQUESTED`) and are covered by
    `sims/users/test_resident_onboarding.py::ResidentOnboardingReviewGateTests` (resident
    self-approval, cross-resident approval, unassigned-supervisor correction requests, and
    incomplete/duplicate submission are all explicitly denied).
- `get_resident_onboarding_state()` (`sims/users/onboarding_api.py`) now returns `review_status`,
  `review_note`, `submitted_at`, `reviewed_at`; `AuthMeView` surfaces the same as
  `onboarding_review_status`, `onboarding_review_note`, `onboarding_submitted_at`,
  `onboarding_reviewed_at`. `ResidentProfileSerializer` exposes all five new fields read-only.
- Deliberately unchanged: `onboarding_complete` and `allowed_next_route` keep their existing
  meaning (profile-complete + declaration-accepted), so existing web behavior is not gated on
  admin approval — a resident still reaches the dashboard as soon as they complete and declare,
  exactly as before. `review_status` is an additive signal for the Android resident-onboarding MVP
  to show Pending Review / Correction Required / Approved screens distinctly from that existing
  boolean; it does not currently gate web dashboard access. Revisit if web onboarding UX is later
  changed to require admin approval before dashboard access.

Also fixed in this pass: `sims_project/wsgi.py` previously wrapped the production WSGI app with
`WhiteNoise(...).add_files(BASE_DIR / 'media', prefix='/media/')`, which serves files straight from
the WSGI layer with no authentication — bypassing Django's URL routing and therefore
`ResidentDocumentViewSet`'s ownership/role checks entirely. The trigger condition
(`os.environ.get('DJANGO_DEBUG', 'True')`) also referenced the wrong environment variable (the
actual settings flag is `DEBUG`), so the vulnerable branch happened to never fire under the current
deployment's real env (`DEBUG=False`, `DJANGO_DEBUG` unset) — but it is live and exploitable the
moment anyone sets the more conventional `DJANGO_DEBUG` name, and the mismatch made the code's own
intent (skip WhiteNoise costs only in real dev) silently not work either. Fixed by removing the
`add_files` call for `media/` entirely and switching the check to the real `DEBUG` variable, with a
regression test at `sims_project/tests.py::WsgiMediaExposureTests` that loads the WSGI app under a
simulated production environment and asserts a resident-document path is neither registered with
WhiteNoise nor servable.
