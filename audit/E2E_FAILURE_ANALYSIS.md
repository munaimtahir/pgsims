# E2E Failure Analysis (Auth/Environment)

## Scope

Investigated smoke failures reported after filesystem permission fixes:

- login stayed on `/login`
- helper fallback attempted `http://localhost:8000/api/auth/login/` and failed `ECONNREFUSED`

## Evidence reviewed

- `frontend/playwright.config.ts` (pre-fix defaults)
- `frontend/e2e/helpers/auth.ts` (pre-fix API candidate logic)
- `frontend/e2e/smoke/auth_flow.spec.ts`
- `frontend/e2e/smoke/dashboards.spec.ts`
- `frontend/app/login/page.tsx`
- `frontend/lib/api/auth.ts` and `frontend/lib/api/client.ts`
- `frontend/app/api/[...path]/route.ts`
- `backend/sims/users/management/commands/seed_e2e.py`
- `audit/STABILIZATION_TEST_RESULTS.md` and `audit/STABILIZATION_RUN_LOG.md`

## Precise failure chain

1. **Smoke URL default was non-local**
   - Playwright base URL default was `https://pgsims.alshifalab.pk` (`playwright.config.ts`).
   - Smoke command (`npm run test:e2e:smoke`) passed no env overrides.

2. **API login helper used ambiguous fallback order**
   - `loginAs()` tried `E2E_API_URL`, then `E2E_BASE_URL`, then hardcoded `http://localhost:8000`.
   - With unset env, it eventually hit localhost:8000 and failed with `ECONNREFUSED` (as captured in stabilization logs).

3. **Frontend and backend local runtime assumptions were mixed**
   - Local stack was actually on `frontend:8082` and `backend:8014` (Docker mapping).
   - Hardcoded fallback to 8000 was accidental legacy dev assumption, not canonical for this repo’s active Docker runtime.

4. **Auth users were deterministic but not explicitly required in smoke command**
   - `seed_e2e` exists and is idempotent (`update_or_create`), but smoke command did not enforce/declare seed precondition.
   - This made smoke run dependent on ambient DB state.

## Answers to required diagnostic questions

1. **What URL was frontend using for API calls during smoke?**
   - Browser form login uses frontend-origin `/api/auth/login/` (via axios base config in browser).
   - Helper login used its own candidate list and could fall through to `localhost:8000`.

2. **Was backend expected to be started separately or orchestrated by tests?**
   - Separately. Playwright config explicitly did not start app services.

3. **Did required users/data exist deterministically?**
   - Mechanism existed (`seed_e2e`), but smoke command did not encode this prerequisite.

4. **Were CSRF/session/JWT assumptions mismatched?**
   - No primary CSRF mismatch found. Auth uses JWT login endpoint and token/cookie/localStorage sync.
   - Failures were environment routing/URL preconditions, not JWT schema mismatch.

5. **Why did tests remain on `/login`?**
   - Failed authentication (wrong/unreachable API target) prevented token set + role redirect.

6. **Why did fallback hit localhost:8000 and was it canonical?**
   - Because of hardcoded fallback in `loginAs()`.
   - It was **not canonical** for active local Docker baseline (`8014` backend).

## Root cause summary

Primary root cause was **auth/environment ambiguity**:

- non-local default smoke target
- legacy localhost:8000 fallback in helper
- missing explicit seed/runtime preconditions in the canonical smoke run path

Not a permissions problem (that was already fixed in prior milestone).
