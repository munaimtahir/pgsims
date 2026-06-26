# 2026-06-19 Resident Onboarding Audit

Scope:
- Resident onboarding wizard
- Login sheet export and issue tracking
- Imported batch review
- Incomplete profile review
- Forced first-login profile completion

Evidence:
- Backend onboarding endpoints: `backend/sims/users/resident_onboarding_urls.py`
- Backend self-service endpoints: `backend/sims/users/resident_selfservice_urls.py`
- Onboarding models: `backend/sims/users/models.py`
- Frontend onboarding pages: `frontend/app/dashboard/onboarding/residents/page.tsx`
- Resident completion page: `frontend/app/resident/complete-profile/page.tsx`
- API contract updates: `docs/contracts/API_CONTRACT.md`
- Route contract updates: `docs/contracts/ROUTES.md`
- Data model contract updates: `docs/contracts/DATA_MODEL.md`

Validation:
- Backend syntax checked with `python3 -m py_compile` on touched Python files
- Resident onboarding migration created in `backend/sims/users/migrations/0009_historicaluser_cnic_and_more.py`

## 2026-06-20 Limitation Closure

Resolved:
- Email is optional during import and validated only when supplied.
- Mapping rejects spreadsheet columns not present in the uploaded header set.
- Imported batches cannot be imported a second time.
- Generate Missing Logins counts only newly generated credentials while retaining the correct batch total.
- Mark-issued updates only generated logins and computes issued status for every affected batch.
- PDF login sheets now contain the same six credential fields as Excel exports with a printable landscape layout.
- Legacy residents retain existing dashboard access; those explicitly forced to change password can reach and submit first-login profile completion even without a pre-existing `ResidentProfile`.
- Admin profile completion no longer bypasses the mandatory password change.
- Incomplete Profiles API/UI exposes names, department, program, training year, joining date, mobile, email, and CNIC for viewing/editing.
- Previous frontend lint errors were corrected and the production build now passes.

Evidence:
- `SECRET_KEY=test-secret python3 manage.py test sims.users.test_resident_onboarding -v 2 --noinput`: 6/6 passed.
- Focused onboarding plus legacy resident regression gate: 12/12 passed.
- `SECRET_KEY=test-secret python3 manage.py test sims._devtools.tests.test_drift_guards -v 2 --noinput`: 2/2 passed.
- `SECRET_KEY=test-secret python3 manage.py makemigrations --check --dry-run --skip-checks`: no changes detected.
- Migration `users.0009` applied, reversed to `users.0008`, and reapplied on isolated SQLite database.
- Focused onboarding/auth frontend Jest gate: 9 suites, 22 tests passed.
- Full frontend Jest gate: 45 suites, 124 tests passed.
- `npm run lint`: no warnings or errors.
- `npm run typecheck`: passed.
- `npm run build`: passed and generated all onboarding/profile routes.
- Schema generation against the isolated migrated database reports no resident-onboarding serializer or operation-ID warnings; remaining schema errors are in pre-existing Backup Center, Bulk, and AdminOps bridge views.

Repository-wide gate status:
- `SECRET_KEY=test-secret pytest sims -q`: 424 passed, 1 failed, 1 error.
- Remaining failures are outside resident onboarding:
  - `sims/backup_center/tests.py::TestGoogleDriveConnector::test_connect_requires_super_admin` has no `normal_admin_user` fixture.
  - `sims/backup_center/tests.py::TestGoogleDriveConnector::test_oauth_callback_stores_encrypted_tokens` supplies an invalid signed OAuth state.

Next steps:
- Treat resident onboarding limitation closure as complete.
- Resolve the two Backup Center test defects in a separate blocker-scoped session before claiming the canonical backend gate is fully green.
- Run browser E2E against a rebuilt deployed runtime when the production-gate E2E blocker is assigned.
- Apply migration `users.0009` through the normal deployment process before running deploy checks against the shared local/runtime database.
