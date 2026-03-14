# 2026-03-14 — Contract & Gate Stabilization Baseline

## Scope

Executed stabilization-only fixes from audit baseline:
- active contract drift (research action, eligibility payload, supervisor row field)
- forgot-password wiring
- backend/frontend gate restoration
- startup/environment hygiene
- contract/governance doc alignment

## Code changes (high level)

- Backend:
  - `sims/training/views.py` — added `supervisor-return` action support (kept `return-to-draft` alias)
  - `sims/training/serializers.py` — canonicalized eligibility response field to `reasons`
  - `sims/training/test_phase6.py` — added/updated contract tests
  - `pytest.ini` — excluded `sims/_legacy` from canonical gate discovery
  - `sims_project/settings.py` — file logging fallback when log path is not writable

- Frontend:
  - `lib/api/training.ts` — eligibility envelope/field normalization
  - `app/dashboard/supervisor/research-approvals/page.tsx` — switched to `resident_name`
  - `app/forgot-password/page.tsx` — wired to real reset API
  - Added tests:
    - `lib/api/training.test.ts`
    - `app/forgot-password/page.test.tsx`
  - `package.json` + `playwright.config.ts` — standalone start alignment + Playwright output path fix

- Docs:
  - `docs/contracts/TRUTH_TESTS.md`
  - `docs/contracts/ROUTES.md`
  - `docs/contracts/API_CONTRACT.md`
  - `docs/testing/playwright-runbook.md`

## Verification evidence

- Backend default check/start: pass (with explicit file-logging fallback notice).
- Backend canonical gate: `pytest sims -q` → **188 passed**.
- Frontend unit gate: `npm test -- --watch=false` → **pass**.
- Frontend build/start: **pass**.
- Playwright smoke:
  - no more filesystem ownership (`EACCES`) failures
  - now failing on functional auth/environment preconditions (`7 passed, 10 failed`).

Detailed logs:
- `audit/STABILIZATION_RUN_LOG.md`
- `audit/STABILIZATION_TEST_RESULTS.md`
- `audit/STABILIZATION_DIFF_NOTES.md`
- `audit/STABILIZATION_SUMMARY.md`
