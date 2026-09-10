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
- Frontend `npm ci`, lint, typecheck, Jest (39 suites / 243 tests), and Next 14.2.35 production build passed.
- Applied non-forced frontend dependency remediation; remaining Next/PostCSS production advisories are documented.
- Disposable PostgreSQL 15 tmpfs container migrated from zero and was removed; compose config parsed with unset-secret warnings.
- Preserved `AUDIT/PGSIMS/FINAL/` unchanged and created the remediation evidence package.
- Pushed through commit `827c380b609c4a11cbcfdded2518fa3ad88a8dff`; PR #16 opened against `main` and left unmerged.

## Pending work

1. Run canonical-stack Playwright smoke/workflow/RBAC suites before release certification.
2. Resolve or formally accept the remaining Next/PostCSS production advisories through a tested compatible upgrade.

## Known conditions

- Ruff reports 2,663 existing findings; broad legacy cleanup is deferred and documented.
- `npm audit --omit=dev` reports 1 high and 1 critical advisory requiring a breaking Next 16 upgrade; no `--force` upgrade was applied.
- Final certification is CONDITIONAL GO until VPS and E2E gates are complete.
