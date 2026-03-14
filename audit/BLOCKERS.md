# Real Blockers (Priority Order)

## 1) Contract drift in training workflows (High)

- Broken FE↔BE actions/payloads in active screens:
  - `supervisor-return` action missing in backend state machine.
  - eligibility payload/field mismatch (`eligibilities` + `reasons_json` vs FE expecting array + `reasons`).
- Impact: key resident/supervisor workflows appear present but fail or silently degrade.

## 2) Test baseline is not trustworthy (High)

- `pytest sims` fails at collection due `_legacy` imports.
- `npm test` has no runnable unit tests.
- Playwright smoke blocked by filesystem ownership (`EACCES`).
- Impact: no single reliable quality gate.

## 3) Startup/ops hygiene issues (High)

- Backend default settings fail because `backend/logs/sims_error.log` is not writable by current user.
- Frontend start script conflicts with standalone output expectations.
- Impact: local reproducibility and deployment confidence are reduced.

## 4) Contract documentation drift (Medium-High)

- `docs/contracts/TRUTH_TESTS.md` points to removed/non-existent test modules.
- `docs/contracts/ROUTES.md` route freeze list does not match implemented UTRMC linking routes.
- Impact: governance docs cannot be used as execution truth.

## 5) Static quality debt in active codebase (Medium)

- Frontend lint fails across dashboard/API files.
- Backend flake8 has 355 issues including undefined names.
- Impact: higher defect risk and slower debugging.

---

## Dependency-aware unblock path

1. Fix FE↔BE contract mismatches in active training flows.
2. Restore one green automated gate set (backend full suite strategy + frontend runnable tests).
3. Fix runnability/permission hygiene.
4. Align contract docs to real executable truth.
5. Address lint/static debt after baseline stability is restored.
