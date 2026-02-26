# FINAL_REPORT

## What changed
- Canonical deploy/Caddy path and ops sync script are in place (`deploy/Caddyfile.pgsims`, `docs/deploy/CADDY_ROUTINE.md`, `ops/caddy_sync_reload.sh`).
- Registration is disabled in UI and feature-flag/role-hardened in backend (`ENABLE_PUBLIC_REGISTRATION`, PG-only on public register).
- Single-hospital deterministic seed is implemented (`python manage.py seed_e2e`).
- Cases module delivered with DRF endpoints + PG/Supervisor/UTRMC pages + tests.
- Bulk import/export expanded with Departments support and export endpoints/UI.
- Reports registry engine delivered with catalog/run/export endpoints and 20-key catalog wiring.
- UTRMC dashboard now renders real KPI data and links into reports/cases.
- Playwright E2E is now real-auth + real-backend (no fake JWT, no route mocks), with deterministic scripts.

## Deployment / Ops commands
- Caddy routine:
  - `bash ops/caddy_sync_reload.sh`
- Docker production stack:
  - `docker compose -f docker/docker-compose.prod.yml up -d --build`
  - `docker compose -f docker/docker-compose.prod.yml exec -T web python manage.py migrate --noinput`
  - `docker compose -f docker/docker-compose.prod.yml exec -T web python manage.py seed_e2e`

## Test commands run
- Backend targeted suite:
  - `pytest -q sims/bulk/tests.py sims/reports/tests.py sims/cases/test_api.py sims/users/test_registration_api.py sims/logbook/test_api.py::PGLogbookEntryAPITests::test_submit_return_feedback_visible_and_resubmit_approve_flow`
- Frontend:
  - `npm run lint`
  - `NEXT_PUBLIC_API_URL=http://localhost:8000 npm run build`
- True integrated E2E:
  - `E2E_BASE_URL=http://localhost:3000 E2E_API_URL=http://localhost:8000 npm run test:e2e -- --workers=1`
  - Result: `6 passed`.

## Evidence paths
- Audit note: `docs/_audit/PHASE_F_TO_I_HARDENING_E2E_2026-02-26.md`
- Playwright artifacts: `frontend/test-results/` and `frontend/playwright-report/`

## TODO CHECKLIST STATUS
- [x] Phase A: deploy cleanup + docs fixed (single path)
- [x] Phase B: Caddyfile canonical + static/media aligned + ops sync script
- [x] Phase C: registration UI disabled + backend hardening + tests
- [x] Phase D: seed_e2e + single hospital + departments matrix
- [ ] Phase E: logbook complete + logbook coverage gate 100%
- [x] Phase F: cases DRF API + frontend + tests + coverage gate wiring
- [x] Phase G: import/export (residents/supervisors/departments) + UI wiring + tests + gates wiring
- [x] Phase H: reports registry + full catalog + exports + UTRMC dashboard + UI pages
- [x] Phase I: real Playwright E2E + scripts + all green (functional suite green)
- [x] FINAL_REPORT.md written + verification commands documented

## Open blocker
- Requested strict per-module/package `--cov-fail-under=100` gates are still failing for legacy-large modules (`sims.logbook`, plus current coverage for cases/bulk/reports API layers). Functional tests and integrated E2E are green, but the strict 100% coverage requirement remains outstanding.
