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
