# Test results

Recorded results for this pass:

- Backend targeted backup orchestration: PASS (22 tests).
- Backend full Django suite: PASS (921 tests).
- Backend system check: PASS (0 issues).
- Backend migration drift: PASS (no changes detected).
- Backend repair command: PASS (37 scanned; 0 invalid; 0 duplicates).
- Disposable PostgreSQL 15 migration from zero: PASS; cleanup complete.
- VPS backend targeted and frontend full gates: PASS under Node 20.20.2.
- Frontend Jest: PASS (39 suites, 240 tests after retiring obsolete public-registration form tests).
- Frontend lint/typecheck/build: PASS on Next 16.3.4 / React 19.2.0.
- Frontend production audit: PASS (0 vulnerabilities); full audit has one indirect dev/build-only
  high `glob` advisory.
- Ruff: informational failure (2,663 existing findings); see `06_P3_DEBT_DISPOSITION.md`.
- Synthetic PostgreSQL duplicate-assignment and duplicate-primary scenarios: PASS; cleanup complete.
- Playwright isolated canonical stack: smoke PASS (25/25); workflow-gate PASS (4/4).
- Playwright RBAC/negative: PASS (31/31).
- Playwright broader workflows: PASS (23 passed, 1 explicit conditional skip); resident training,
  supervisor review, Masters, universal user creation, and supervision surfaces passed.
- Android `:app-companion`: PASS for `testDebugUnitTest`, `lintDebug`, and `assembleDebug`; release
  signing NOT VERIFIED because no owner-controlled signing properties were supplied.
- VPS read-only production verification: backend healthz PASS (DB/cache/Celery), frontend HTTP 200,
  migrations applied; no production mutation or restart performed.
