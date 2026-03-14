# Stabilization Run Log

## Contract and workflow verification commands

```bash
cd backend && SECRET_KEY='audit-secret' DJANGO_SETTINGS_MODULE=sims_project.settings_test \
  pytest sims/training/test_phase6.py::ResearchProjectAPITests::test_supervisor_return_transitions_project_to_draft \
         sims/training/test_phase6.py::EligibilityAPITests::test_my_eligibility_items_use_reasons_field \
         sims/training/test_phase6.py::EligibilityAPITests::test_utrmc_eligibility_items_use_reasons_field -q
```

Result: **3 passed**.

## Backend default startup hygiene

```bash
cd backend && SECRET_KEY='audit-secret' DEBUG='True' python3 manage.py check
```

Result: **passed** (`System check identified no issues`).

Observed behavior after fix:
- If `backend/logs/sims_error.log` is not writable, settings now disable file logging at startup with an explicit message:
  - `[settings] File logging disabled for '/.../logs/sims_error.log': [Errno 13] Permission denied ...`
- Startup continues with console logging instead of crashing.

```bash
cd backend && SECRET_KEY='audit-secret' DEBUG='True' python3 manage.py runserver 127.0.0.1:18015
curl -i http://127.0.0.1:18015/healthz/
```

Result: server started; `/healthz/` returned **HTTP 200**.

## Backend canonical gate

```bash
cd backend && SECRET_KEY='audit-secret' DJANGO_SETTINGS_MODULE=sims_project.settings_test pytest sims -q
```

Result: **188 passed**.

## Frontend unit/build/start gates

```bash
cd frontend && npm test -- --watch=false
```

Result: **2 test suites passed (4 tests)**.

```bash
cd frontend && npm run build
```

Result: **build succeeded**.

```bash
cd frontend && npm run start
curl -I http://127.0.0.1:3000/
```

Result: standalone start script served **HTTP 200** (no `next start` standalone warning).

## Frontend E2E smoke execution

```bash
cd frontend && npm run test:e2e:smoke
```

Result:
- Permission blocker resolved (no `EACCES`).
- Playwright artifacts successfully written to `output/playwright/results` and `output/playwright/report`.
- Suite executed: **7 passed, 10 failed** (functional/auth/environment failures, not filesystem permission failures).
