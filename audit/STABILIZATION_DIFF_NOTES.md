# Stabilization Diff Notes

## Scope mapping (audit finding → change)

1. **Research action drift (`supervisor-return`)**
   - `backend/sims/training/views.py`
   - Added canonical action support: `supervisor-return` → `DRAFT`
   - Preserved `return-to-draft` as backward-compatible alias
   - Supervisor feedback now persisted for return action

2. **Eligibility payload mismatch**
   - `backend/sims/training/serializers.py`
   - Exposed canonical API field `reasons: string[]` (from model `reasons_json`)
   - Removed `reasons_json` from response contract

   - `frontend/lib/api/training.ts`
   - `getMyEligibility()` now parses canonical envelope (`eligibilities`)
   - Added normalization for `reasons` / legacy `reasons_json`
   - `getUTRMCEligibility()` now normalizes result items similarly

3. **Supervisor approvals row mismatch**
   - `frontend/app/dashboard/supervisor/research-approvals/page.tsx`
   - Switched resident row display from non-existent `p.resident` to canonical `p.resident_name`

4. **Forgot-password placeholder flow**
   - `frontend/app/forgot-password/page.tsx`
   - Removed timer placeholder
   - Wired page to real API via `authApi.passwordReset(email)`
   - Added input normalization + success/error handling

5. **Backend global test gate broken by legacy collection**
   - `backend/pytest.ini`
   - Added `--ignore=sims/_legacy` to isolate legacy test tree from canonical gate

6. **Frontend unit gate absent**
   - Added `frontend/lib/api/training.test.ts`
   - Added `frontend/app/forgot-password/page.test.tsx`
   - Restored runnable `npm test -- --watch=false` baseline

7. **Playwright permission blocker**
   - `frontend/playwright.config.ts`
   - Output/report paths moved to `../output/playwright/*` (repo-level writable/ignored path)

   - `frontend/package.json`
   - Updated `test:e2e:report` path to new report location

   - `docs/testing/playwright-runbook.md`
   - Updated artifact locations and report-open command

8. **Backend default startup logging crash**
   - `backend/sims_project/settings.py`
   - Added guarded file logging initialization:
     - attempts to prepare/write log file
     - gracefully disables file handler on `OSError`
     - keeps console logging active

9. **Frontend startup contract inconsistency**
   - `frontend/package.json`
   - Canonical `start` now uses `node .next/standalone/server.js`
   - Added `start:next` for explicit fallback use only

10. **Stale governance/contract docs**
   - `docs/contracts/TRUTH_TESTS.md`
   - `docs/contracts/ROUTES.md`
   - `docs/contracts/API_CONTRACT.md`
   - Updated to executable truths (routes, tests, actions, payloads, response shapes)

## Additional tests updated

- `backend/sims/training/test_phase6.py`
  - Added supervisor return API transition test
  - Added eligibility contract field tests (`reasons` field)
