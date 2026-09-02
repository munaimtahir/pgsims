# Documentation Gap Report

## Accurate / useful docs

- `docs/contracts/*` provides clear governance intent (API, RBAC, routes, truth tests).
- `docs/testing/playwright-*` and e2e regression notes clearly mark deferred/not-ready coverage.
- `AGENTS.md` governance and drift rules are explicit and actionable.

## Stale or misleading docs

- Root `README.md` claims high readiness and references docs like `docs/FEATURES_STATUS.md` and `docs/SYSTEM_STATUS.md`, but these files are absent at that path (archived under `docs/_archive/...`).
- Integration docs under `docs/integration/*` are extensive but not clearly authoritative compared with `docs/contracts/*`; some mismatch entries are marked fixed historically without current re-verification in this run.

## Missing documentation clarity

- Single canonical “current-state truth” doc for active vs legacy module runtime exposure is missing.
- Explicit note that legacy logbook/cases APIs are not in active root URL wiring is not front-and-center in top-level docs.

## Recommended source-of-truth hierarchy

1. `docs/contracts/*` for active product contract.
2. This discovery pack for current runtime truth snapshot.
3. `docs/integration/*` as supporting analysis, not authority, unless reconciled.
4. Archive docs (`docs/_archive/*`) should remain clearly labeled historical only.
