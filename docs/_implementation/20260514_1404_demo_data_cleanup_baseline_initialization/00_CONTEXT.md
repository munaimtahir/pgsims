# Demo Data Cleanup and Baseline Initialization

## Session Purpose

Remove E2E, workflow-test, pilot-test, placeholder, and fake seeded data from the live PGSIMS database, then initialize only the minimum real master data needed for manual entry.

## Repo

- Path: `/home/munaim/srv/apps/pgsims`
- Branch: `main`
- Commit at start of run: `e566991`

## Guardrails Followed

- Read `docs/ANTI_DRIFT_GUARDRAILS.md`
- Read `docs/PROD_GATE_CLOSURE/00_README.md`
- Read `docs/PROD_GATE_CLOSURE/QUICK_REFERENCE.md`
- Read `docs/PROD_GATE_CLOSURE/INDEX.md`
- Read `docs/PROD_GATE_CLOSURE/01_blocker_analysis.md`
- Read `docs/PROD_GATE_CLOSURE/06_testing_procedures.md`

## Scope

- Add a repeatable cleanup command with dry-run and explicit confirmation.
- Add a repeatable baseline initialization command.
- Add tests for cleanup, idempotent initialization, and smoke verification.
- Document the live cleanup run with before/after evidence.

## Out of Scope

- No major application logic rewrite.
- No route structure changes.
- No auth/RBAC redesign.
- No migration resets.
- No truncation of the database.

## Live Environment

- Backend container: `pgsims_backend`
- Frontend container: `pgsims_frontend`
- Database container: `pgsims_db`
- Backend URL: `http://127.0.0.1:8014`
- Frontend URL: `http://127.0.0.1:8082`

