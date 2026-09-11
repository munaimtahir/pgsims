# SPRINT_STATE.md — Final production readiness remediation

## Scope

Remediate confirmed Session D production blockers from `AUDIT/PGSIMS/FINAL/` on branch
`remediation/pgsims-final-production-readiness`, without changing production state or the audit
package. Backend/frontend verification is to be repeated in the VPS checkout at
`/home/munaim/srv/apps/pgsims`; Android remains on this laptop.

## Completed work

- Confirmed laptop `origin/main` baseline `a08bb16eb321f6154774d1c9edf6be28bffc4a2f` and created the remediation branch.
- Updated Django constraint to `>=5.2,<5.3`; Django 5.2.17 full suite passed (921 tests), checks and migration drift passed.
- Fixed disaster archive destination creation; backup orchestration passed (22 tests), including missing nested path coverage.
- Ran `repair_identity_profiles`: 37 scanned, 0 invalid users, 0 duplicate profiles; Update 0 gate passed.
- Frontend `npm ci`, lint, typecheck, Jest (39 suites / 243 tests), and Next 16.3.4 / React 19.2.0 production build passed locally and on VPS Node 20.20.2.
- Applied non-forced frontend dependency remediation; production audit is zero, with one indirect dev/build-only `glob` advisory documented.
- Updated React 19 tests, Next 16 async route params, ESLint 9 flat config, and generated-report ignores.
- Disposable PostgreSQL 15 tmpfs container migrated from zero and was removed; compose config parsed with unset-secret warnings.
- Preserved `AUDIT/PGSIMS/FINAL/` unchanged and created the remediation evidence package.
- Pushed through commit `3d45f1ce614aec6203fc341896f9e77f961e522a`; PR #16 remains open against `main` and unmerged.

## Pending work

1. Migrate stale Playwright smoke fixtures/contracts to canonical four-role routes/labels, then rerun smoke.
2. Run workflow-gate, RBAC, negative, and database-state E2E suites against the isolated canonical stack.

## Known conditions

- Ruff reports 2,663 existing findings; broad legacy cleanup is deferred and documented.
- VPS host Node is 18.19.1; Next 16 verification used disposable Node 20.20.2 tooling, matching the frontend image requirement.
- Playwright smoke executed 25 tests: 11 passed, 14 stale-contract failures; E2E certification remains conditional.
- Final certification is CONDITIONAL GO until canonical E2E gates are complete.
