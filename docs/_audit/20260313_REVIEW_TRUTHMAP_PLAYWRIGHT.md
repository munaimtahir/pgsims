# 2026-03-13 Review Truth Map and Playwright Audit

## Scope

- Backend contract and role workflow verification
- Frontend Playwright verification against local Docker stack
- Screenshot artifact generation for public pages, role dashboards, and major workflows

## Verified Working

- Backend targeted verification:
  - `150` tests passed across:
    - `backend/sims/tests/test_role_workflows.py`
    - `backend/sims/_devtools/tests/test_drift_guards.py`
    - `backend/sims/training/test_phase6.py`
    - `backend/sims/notifications/tests.py`
    - `backend/sims/users/test_userbase_api.py`
- Playwright rerun against corrected local browser-facing config:
  - `114` passed
  - `1` skipped
  - `0` failed
- UI login role tour:
  - `admin`
  - `utrmc_admin`
  - `utrmc_user`
  - `supervisor`
  - `pg`
  - All crossed `/login` successfully and produced post-login screenshots

## Issues Found During Review

- Initial local stack boot failed because Django file logging could not write to `/app/logs/sims_error.log`
- Initial local stack boot also created a Postgres volume with the wrong password when `DB_PASSWORD` was omitted
- Frontend image had previously been built with `NEXT_PUBLIC_API_URL=http://localhost:8014`, which caused browser CORS failures and bypassed the intended Next.js proxy path
- Django `ALLOWED_HOSTS` initially did not include `backend`, which broke proxied `/api/*` requests from the frontend container
- Drift guard test was over-broad and flagged any `user=` in files containing `Notification.objects.create(...)`

## Remediation Applied In This Run

- Tightened `backend/sims/_devtools/tests/test_drift_guards.py` so it inspects only `Notification.objects.create(...)` call blocks
- Rebuilt the local stack with browser-correct frontend settings and backend host allowances
- Reseeded deterministic E2E users with `seed_e2e`

## Artifacts

- Main Playwright outputs:
  - `output/playwright/report`
  - `output/playwright/test-results`
  - `output/playwright/screenshots`
- Corrected rerun outputs:
  - `output/playwright/rerun-report`
  - `output/playwright/rerun-results`
  - `output/playwright/rerun-screenshots`
- Real login role screenshots:
  - `output/playwright/ui-login-role-shots`

