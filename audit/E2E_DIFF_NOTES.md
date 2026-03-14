# E2E Diff Notes

## Files changed for this milestone

- `frontend/playwright.config.ts`
- `frontend/e2e/helpers/auth.ts`
- `frontend/package.json`
- `frontend/e2e/critical/phase6_research_eligibility.spec.ts`
- `frontend/e2e/critical/userbase_foundation.spec.ts`
- `frontend/e2e/negative/validation.spec.ts`
- `frontend/e2e/screenshots/screenshot-tour.spec.ts`
- `frontend/e2e/workflows/resident-training.spec.ts`
- `frontend/e2e/workflows/supervisor-review.spec.ts`
- `docs/testing/playwright-runbook.md`
- `docs/contracts/TRUTH_TESTS.md`

## What changed and why

1. **Playwright canonical local defaults**
   - Default `E2E_BASE_URL` changed to `http://127.0.0.1:8082`.
   - Runbook comments updated to explicit local model.
   - Reason: remove accidental remote target dependency.

2. **Auth helper API target determinism**
   - `loginAs()` now defaults `E2E_API_URL` to `http://127.0.0.1:8014`.
   - Removed legacy fallback to `http://localhost:8000`.
   - Reason: eliminate ambiguous fallback causing `ECONNREFUSED` in local Docker baseline.

3. **Local smoke command standardization**
   - Added `npm run test:e2e:smoke:local`.
   - Reason: one explicit reproducible command for canonical local baseline.

4. **Cross-suite base URL consistency**
   - Updated remaining E2E file-local defaults from hosted URL to canonical local URL.
   - Reason: prevent split-brain URL behavior across suites.

5. **Governance/testing docs alignment**
   - Updated `docs/testing/playwright-runbook.md`.
   - Updated `docs/contracts/TRUTH_TESTS.md` smoke gate instructions.
   - Reason: contract/gate docs now match executable reality.
