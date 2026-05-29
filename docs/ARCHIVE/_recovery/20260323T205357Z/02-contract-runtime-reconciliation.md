# Contract / Runtime Reconciliation

## Major mismatches found

1. Logbook and cases appear in historical/discovery narrative but are not active runtime surfaces.
- Runtime evidence:
  - No active include for legacy logbook/cases routes in `backend/sims_project/urls.py`.
  - No logbook/cases nav entries in `frontend/lib/navRegistry.ts`.
  - No corresponding App Router pages under `frontend/app/dashboard/*`.
- Technical blocker evidence:
  - Legacy modules import `sims.logbook` and `sims.analytics`, but current importable packages are `_legacy` namespaces.
  - Import check: `sims.logbook` and `sims.analytics` raise `ModuleNotFoundError`; `_legacy` variants import.

2. Readiness signal mismatch between build and quality.
- `frontend/next.config.mjs` skips lint/type during build; build success alone is insufficient.
- Reconciled by running lint/tests explicitly and restoring lint to clean.

## What was fixed now
- Frontend baseline mismatch resolved: lint failures removed in active surfaces.
- Recovery docs now explicitly classify legacy workflows as deferred/legacy instead of implied active.

## What was downgraded/deferred
- Logbook and cases kept deferred for this pass (not silently reactivated).
- Reason: activation requires controlled backend namespace/app/URL reconciliation beyond minimal safe stabilization.

## Unresolved drift items
- Historical docs still overstate full legacy workflow availability (requires targeted doc cleanup milestone).
- Build pipeline still permits skip of type/lint checks unless CI/job enforces dedicated lint/type steps.

## Evidence references
- `backend/sims_project/settings.py`
- `backend/sims_project/urls.py`
- `backend/sims/_legacy/logbook/api_views.py`
- `backend/sims/_legacy/logbook/api_urls.py`
- `frontend/lib/navRegistry.ts`
- `frontend/next.config.mjs`
