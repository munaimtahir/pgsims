# PGSIMS Test Truth Results

## 1) Backend full-suite reality

```bash
cd backend && SECRET_KEY='audit-secret' DJANGO_SETTINGS_MODULE=sims_project.settings_test pytest sims -q
```

Result: **failed during collection** (`9 errors`) because `_legacy` tests import removed modules:
- `ModuleNotFoundError: No module named 'sims.logbook'`
- `No module named 'sims.cases'`
- `No module named 'sims.analytics'`
- `No module named 'sims.attendance'`

## 2) Backend active-module suite

```bash
cd backend && SECRET_KEY='audit-secret' DJANGO_SETTINGS_MODULE=sims_project.settings_test \
pytest sims/users sims/training sims/rotations sims/academics sims/notifications sims/audit sims/bulk -q
```

Result: **80 passed**.

## 3) Contract truth-test gates from docs

From `docs/contracts/TRUTH_TESTS.md`:
- `sims.logbook.test_api...` gate
- `sims.analytics.tests.AnalyticsV1ApiTests`

Executed:

```bash
pytest sims/logbook/test_api.py::PGLogbookEntryAPITests::test_submit_return_feedback_visible_and_resubmit_approve_flow -v
pytest sims/analytics/tests.py::AnalyticsV1ApiTests -v
```

Result: both failed with `file or directory not found`.

## 4) Drift and migration gates

```bash
pytest sims/_devtools/tests/test_drift_guards.py -v
pytest sims/rotations/test_canonical_migration_gate.py -v
```

Result: both pass (`2 passed`, `2 passed`).

## 5) Frontend unit tests

```bash
cd frontend && npm test -- --watch=false
```

Result: failed with `No tests found, exiting with code 1`.

Jest config ignores `/e2e/`, and there are no runnable unit test files outside ignored paths.

## 6) Frontend E2E tests

```bash
cd frontend && npm run test:e2e:smoke
```

Result: failed due permissions (`EACCES`) in `pw-test-results` / `playwright-report` directories (owned by root).

## 7) Lint / static quality

```bash
cd frontend && npm run lint -- --quiet
```

Result: failed with many errors (`no-explicit-any`, unused vars, etc.).

```bash
cd backend && flake8 sims --count --statistics
```

Result: failed with **355 violations**, including:
- `F821 undefined name 'LogbookEntry'` in `sims/bulk/services.py`
- many `E402`, `F401`, and whitespace issues, heavily in `_legacy` and devtools surfaces.
