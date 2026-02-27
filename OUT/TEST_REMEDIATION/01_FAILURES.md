# Failure Triage (A-G)

## A) Missing dependency/import
- `sims.cases.tests` import error: `ModuleNotFoundError: No module named 'factory'`
- `sims.certificates.tests` import error: `ModuleNotFoundError: No module named 'factory'`
- `sims.logbook.tests` import error: `ModuleNotFoundError: No module named 'factory'`
- `sims.tests.factories` import error: `ModuleNotFoundError: No module named 'factory'`

## B) Migration/db/schema mismatch
- None in failing set.

## C) Timezone/datetime nondeterminism
- Runtime warnings for naive datetimes observed in other tests, but not baseline blockers.

## D) Seed/fixture assumptions
- `test_frontend_create` imported as a test module and executed imperative setup at import time, creating invalid `User` via `User.objects.create(...)` without password.

## E) Permissions/RBAC expectation mismatch
- None in failing set.

## F) External/network calls
- None in failing set.

## G) Flaky ordering / nondeterministic queries
- `sims.search.tests.SearchServiceTests.test_search_users_admin_sees_all`
- `sims.search.tests.SearchServiceTests.test_search_users_supervisor_sees_supervised`
- `sims.search.tests.SearchServiceTests.test_search_users_pg_sees_only_self`

Observed behavior: query term `"pg"` returned zero rows in `_search_users` under PostgreSQL full-text ranking threshold, while test expectation assumes partial-match behavior.
