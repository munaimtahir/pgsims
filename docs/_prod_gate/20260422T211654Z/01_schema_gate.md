# Schema Gate

## Status
PARTIAL / FAIL for GO threshold.

## What was wired
- `drf_spectacular` added to `INSTALLED_APPS` in `backend/sims_project/settings.py`.
- DRF `DEFAULT_SCHEMA_CLASS` set to `drf_spectacular.openapi.AutoSchema`.
- `/api/schema/` route added in `backend/sims_project/urls.py`.
- Schema endpoint smoke test added at `backend/sims/test_schema_gate.py`.

## Commands
- Endpoint smoke: `SECRET_KEY=test-secret python3 -m pytest sims/test_schema_gate.py -q`
- Strict schema gate: `SECRET_KEY=test-secret python3 manage.py spectacular --file ../OUT/prod_gate_artifacts/20260422T211654Z/schema/openapi.yaml --validate --fail-on-warn`

## Evidence
- Endpoint smoke passed: `1 passed`.
- Strict schema generation failed because `--fail-on-warn` surfaced 49 warnings and 315 schema generation errors.
- Generated schema artifact path when non-strict generation is used: `OUT/prod_gate_artifacts/20260422T211654Z/schema/openapi.yaml`.

## Remaining Gap
The schema gate is now wired and enforceable, but not clean. GO remains blocked until active APIViews and serializer method fields are annotated or converted so `--fail-on-warn` passes.
