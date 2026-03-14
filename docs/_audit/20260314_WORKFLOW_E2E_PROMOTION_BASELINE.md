# 2026-03-14 — Workflow E2E Promotion Baseline

## Scope

Promote a small deterministic subset of contract-critical workflows into a dedicated browser gate above smoke.

## Promoted flows

- Forgot-password request submit path
- Supervisor approvals list + `resident_name` rendering + supervisor-return
- Resident eligibility reasons display

## Key implementation points

- Added deterministic workflow preconditions to `seed_e2e`.
- Added Playwright project `workflow-gate`.
- Added gate commands:
  - `npm run test:e2e:smoke:local`
  - `npm run test:e2e:workflow:local`
- Updated runbook and truth-test docs to separate smoke vs workflow responsibilities.

## Verification

- Smoke gate: `17 passed`
- Workflow gate: `3 passed`

## Evidence

- `audit/WORKFLOW_E2E_READINESS.md`
- `audit/WORKFLOW_E2E_MODEL.md`
- `audit/WORKFLOW_E2E_RUN_LOG.md`
- `audit/WORKFLOW_E2E_TEST_RESULTS.md`
- `audit/WORKFLOW_E2E_DIFF_NOTES.md`
- `audit/WORKFLOW_E2E_SUMMARY.md`
