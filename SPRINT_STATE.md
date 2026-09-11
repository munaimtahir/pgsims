# SPRINT_STATE.md — Next sprint scope

## Scope

Post-remediation follow-up. The final production-readiness remediation is closed as GO for its
defined scope on branch `remediation/pgsims-final-production-readiness`; PR #16 remains open and
unmerged. Do not mutate production data or deployment state.

## Completed baseline

- Confirmed laptop `origin/main` baseline `a08bb16eb321f6154774d1c9edf6be28bffc4a2f` and created the remediation branch.
- Updated Django constraint to `>=5.2,<5.3`; Django 5.2.17 full suite passed (921 tests), checks and migration drift passed.
- Fixed disaster archive destination creation; backup orchestration passed (22 tests), including missing nested path coverage.
- Ran `repair_identity_profiles`: 37 scanned, 0 invalid users, 0 duplicate profiles; Update 0 gate passed.
- Frontend `npm ci`, lint, typecheck, Jest (39 suites / 240 tests), and Next 16.3.4 / React 19.2.0 production build passed locally and on VPS Node 20.20.2.
- Applied non-forced frontend dependency remediation; production audit is zero, with one indirect dev/build-only `glob` advisory documented.
- Updated React 19 tests, Next 16 async route params, ESLint 9 flat config, and generated-report ignores.
- Disposable PostgreSQL 15 tmpfs container migrated from zero and was removed; compose config parsed with unset-secret warnings.
- Preserved `AUDIT/PGSIMS/FINAL/` unchanged and created the remediation evidence package.
- Remediation commit: `228dc0c`; PR #16 remains open against `main` and unmerged.
- Disposable canonical stack smoke gate passed 25/25; stack and project-scoped volumes were removed.
- Canonical workflow gate passed 4/4; VPS production was checked read-only (healthz, frontend HTTP 200, migrations applied) with no mutation or restart.
- RBAC/negative passed 31/31; broader workflows passed 23 with 1 explicit conditional skip; Android `:app-companion` unit tests, lint, and debug assembly passed.

## Pending work

1. When deployment ownership provides secure Android signing properties, run the documented
   `:app-companion:assembleRelease`/`:app-companion:bundleRelease` verification without creating or
   exposing signing material.
2. Review the existing Ruff backlog and Django schema-generation warnings as a separately scoped
   maintenance sprint.

## Known conditions

- Ruff reports 2,663 existing findings; broad legacy cleanup is deferred and documented.
- VPS host Node is 18.19.1; Next 16 verification used disposable Node 20.20.2 tooling, matching the frontend image requirement.
- Playwright smoke executed 25 tests: 25 passed; workflow-gate 4/4 passed; RBAC/negative 31/31 passed; broader workflows 23 passed with 1 explicit conditional skip.
- Final certification: GO for the remediation scope; Android release signing remains NOT VERIFIED.
