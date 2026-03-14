# Workflow E2E Diff Notes

## Files changed

- `backend/sims/users/management/commands/seed_e2e.py`
- `frontend/e2e/workflow-gate/stabilized-workflows.spec.ts` (new)
- `frontend/playwright.config.ts`
- `frontend/package.json`
- `docs/testing/playwright-runbook.md`
- `docs/contracts/TRUTH_TESTS.md`

## What changed

1. **Deterministic workflow preconditions in seed**
   - `seed_e2e` now seeds:
     - `E2E-FCPS` training program
     - `IMM` and `FINAL` milestones with deterministic requirement rules
     - active training record for `e2e_pg`
     - submitted research project for supervisor review
     - eligibility recomputation for deterministic reason rendering

2. **Dedicated workflow gate project/spec**
   - Added Playwright project: `workflow-gate`
   - Added workflow spec: `frontend/e2e/workflow-gate/stabilized-workflows.spec.ts`

3. **Explicit workflow gate commands**
   - Added scripts:
     - `npm run test:e2e:workflow`
     - `npm run test:e2e:workflow:local`

4. **Docs split smoke vs workflow responsibilities**
   - Updated runbook and truth-tests docs with command boundaries and deferred scope.
