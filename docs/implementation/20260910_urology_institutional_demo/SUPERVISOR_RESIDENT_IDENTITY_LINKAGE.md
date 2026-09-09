# Supervisor/Resident Demo Identity Linkage — Report

## Baseline

```text
Laptop branch:  main
Laptop SHA (before): ebaf8c4
VPS branch:     main
VPS SHA (before): b2aec1a (one Android commit ahead of laptop; fast-forwarded, no divergence)
Database:       PostgreSQL sims_db (pgsims_db_prod container)
Backup taken:   /tmp/pgsims_pre_supervisor_link_20260910.dump (pg_dump -Fc, before any writes)
```

## Root cause

The canonical identity chain is `User` (auth/role) → `SupervisorProfile`/`ResidentProfile`
(one-to-one) → `ResidentSupervisorAssignment` (FK to both profiles). No duplicate
Department/Hospital/legacy models exist; this is a single, consistent chain.

The Urology institutional bootstrap created real profiles (with hospital, department,
`ResidentTrainingRecord`, and `ResidentSupervisorAssignment` rows) under dedicated usernames
(`supmtahirbashirmalik`, `pgrdrjawadsaifullah`, ...), while the canonical demo-login accounts
`supervisor` and `resident` each had their own separate, empty profile. Logging in as
`supervisor`/`resident` therefore resolved to an empty identity with zero residents/supervisor,
while all the real Urology data sat under logins nobody used interactively.

All 28 resident-supervisor assignments were already correct and matched the approved
distribution exactly (Irfan Munir 14, Tahir Bashir Malik 7, Akmal 5, Sheraz Javed 2, Akram 0) —
this was purely an identity-linkage problem, not a data problem.

## Canonical Supervisor Mapping

| User | Canonical supervisor | Role | Residents | Status |
| ---- | --------------------- | ---- | --------: | ------ |
| `supervisor` (id 63) | Prof. Dr. M. Tahir Bashir Malik | SUPERVISOR | 7 | PASS |
| `supmuhammadirfanmunir` | Dr. Muhammad Irfan Munir | SUPERVISOR | 14 | unchanged, already correct |
| `supmuhammadakmal` | Prof. Dr. Muhammad Akmal | SUPERVISOR | 5 | unchanged, already correct |
| `supsherazjaved` | Dr. Sheraz Javed | SUPERVISOR | 2 | unchanged, already correct |
| `supmuhammadakram` | Prof. Dr. Muhammad Akram | SUPERVISOR | 0 (allied/co-supervisor) | unchanged, already correct |
| `supmtahirbashirmalik` | (retired placeholder) | SUPERVISOR | 0 | deactivated, data preserved |

```text
supervisor
→ Prof. Dr. M. Tahir Bashir Malik   ✅ PASS
```

## Demo Resident Mapping (addendum)

| Username | Role | Linked canonical identity | Relationship status |
| -------- | ---- | -------------------------- | -------------------- |
| `resident` (id 62) | RESIDENT | Dr. Jawad Saifullah (MS Urology, y5, Urology Dept, Allied Hospital-I Faisalabad) | PASS |

Selection rationale: of Tahir's 7 residents, Dr. Jawad Saifullah was the only one with populated
workflow demo data (1 `SUBMITTED` logbook entry + 1 `SUBMITTED` evaluation, both already routed to
Tahir's review queue by the earlier Urology workflow seeder) — satisfying the addendum's
"prefer a resident with existing detailed source data" rule without any new seeding.

## Resident Assignment Audit

```text
Residents:                    28 (unchanged)
Active primary assignments:   28 (unchanged)
Irfan Munir:                  14
Tahir Bashir Malik:           7
Muhammad Akmal:               5
Sheraz Javed:                 2
Orphans:                      0
Duplicates:                   0
```

## The fix

New idempotent management command `reconcile_urology_supervisor_profiles`
(`backend/sims/users/management/commands/reconcile_urology_supervisor_profiles.py`):

- Re-points the real `SupervisorProfile`/`ResidentProfile` (and, for residents, the real
  `ResidentTrainingRecord`, which is keyed by `resident_user` directly rather than by profile)
  onto the canonical login account, swapping via a scratch user slot to avoid the OneToOne
  unique-constraint collision of a naive two-step update.
- Copies the real identity's name/email onto the login account.
- Deactivates the now-redundant real-identity login (`is_active=False`) — data preserved, never
  deleted, and it had never been used to log in (`must_change_password=True`, untouched).
- Idempotent: keys off `real_user.is_active` — a second run reports "already correct" and makes
  no writes. Verified with a real re-run against production.

No duplicate users, profiles, or assignments were created at any point.

## Second bug found and fixed during verification

Loading the admin's Supervisor Detail page (`/supervisors/63`) for the now-linked `supervisor`
account 500'd. Root cause: `SupervisorAcademicSummaryView` / `ResidentAcademicSummaryView`
(`backend/sims/academics/views.py`) looked the profile up by **its own pk**, but every caller —
the frontend's `/residents/{id}` and `/supervisors/{id}` detail pages, and the sibling
`ResidentProfileViewSet`/`SupervisorProfileViewSet` (`lookup_field="user_id"`) — passes the
resident/supervisor's **User id**. A profile's own pk only coincidentally equals its user id, so
this 500'd for any resident/supervisor whose profile pk differed from their user id (i.e. almost
always in real data; it went unnoticed because the existing tests' fixtures happened to line the
two up). Fixed to look up by `user_id`, matching the rest of the app's convention, and to return
404 instead of an uncaught `DoesNotExist` for a bad id. Added regression tests asserting
`profile.pk != profile.user_id` in the fixture and that only the user-id URL succeeds.

This is very likely the underlying cause behind the "Supervisor Resident Link → 404" symptom
reported for the super-admin UI — no stale Django-admin href or broken frontend route was found
anywhere in the codebase; every nav link already pointed at a real, existing app route.

## API Verification (real HTTP calls against the production domain)

```text
POST /api/auth/login/ (supervisor/supervisor123) → 200, JWT issued
GET  /api/auth/me/                                → role SUPERVISOR, profile_id 3, identity M. Tahir Bashir Malik
GET  /api/supervision/assignments/?is_active=true → 200, count 7, all M. Tahir Bashir Malik's residents

POST /api/auth/login/ (resident/resident123)      → 200, JWT issued
GET  /api/auth/me/                                → role RESIDENT, profile_id 36, identity Dr. Jawad Saifullah
GET  /api/supervision/assignments/?is_active=true → 200, count 1, supervisor = M. Tahir Bashir Malik

GET  /api/supervision/assignments/?resident_id=<unassigned> (as supervisor) → 200, count 0 (correctly scoped, no leak)
GET  /api/academics/review-queue/ (as supervisor)  → Dr. Jawad Saifullah's pending LOGBOOK_REVIEW and
                                                      EVALUATION_REVIEW items present, already routed
                                                      to supervisor=3 by the existing assignment
```

No `supervisor_id`/`resident_id` was ever passed by the client to determine "who am I" — both
directions derive entirely from the authenticated session via `request.user`.

## Runtime web verification (super-admin, live production domain)

```text
/supervisors                → M. Tahir Bashir Malik listed with username=supervisor, Active;
                               supmtahirbashirmalik listed as Inactive. No 404, no Django-admin
                               redirect anywhere in this flow.
/supervisors/63              → after the summary-view fix: Assigned residents: 7, Active training
                               records: 7, Pending queue items: 6, including Dr. Jawad Saifullah.
/residents/62                → Dr. Jawad Saifullah, MS Urology, Urology Department,
                               Primary supervisor: M. Tahir Bashir Malik, Pending items: 6.
```

## Tests

```text
Django check:                 no issues (before and after both fixes)
Migration check:               no changes detected
reconcile command tests:       9/9 passed (identity resolution, traversal both directions,
                                no duplicates, retired-not-deleted, dry-run no-op, idempotent rerun)
academics summary regression:  143/143 passed (sims/academics/tests.py +
                                sims/tests/test_academics_coverage_extra.py, including 2 new
                                regression tests pinning the user_id-vs-pk contract)
supervision/users/training:    45/45 passed, no regressions
Idempotent rerun (production): confirmed — second run reports "already correct", zero writes
```

## Known limitations (not in scope of this repair)

- `supervisor`'s profile is `is_profile_complete: false` (missing phone/email/designation_ref)
  and `resident`'s profile is missing `academic_session_ref` — pre-existing onboarding gaps on
  the underlying bootstrap records, unrelated to the identity-linkage bug. Not fixed here since
  the mission scope was the linkage itself, not onboarding completeness.
- Android app verification not performed in this session (no device/emulator access available).
  The backend contract is confirmed identical for both clients since there is no client-specific
  branching anywhere in the reconciled code path — Android should work against the same
  `/api/auth/login/`, `/api/auth/me/`, `/api/supervision/assignments/`, and
  `/api/academics/review-queue/` endpoints already verified above.

## FINAL VERDICT

```text
CONDITIONAL GO — LINKAGE READY WITH DOCUMENTED LIMITATION
```

Web + API chain (`resident` → Dr. Jawad Saifullah → active assignment → Prof. Dr. M. Tahir Bashir
Malik ← `supervisor`) is verified end-to-end against production, including the pre-existing
workflow items routing correctly to the supervisor's review queue. Android-side verification is
the only remaining gap, blocked on device/emulator access rather than any known backend issue.
