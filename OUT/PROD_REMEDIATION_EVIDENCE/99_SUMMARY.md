# PGSIMS Production Remediation Summary

Date: 2026-02-27
Target domain: https://pgsims.alshifalab.pk
Evidence path: `/srv/apps/pgsims/OUT/PROD_REMEDIATION_EVIDENCE/`

## Final Verdict
**PASS**

All production-go-live criteria were met with deterministic seeded users, successful HTTPS routing through Caddy, successful API login, and role/dashboard API data availability.

## What Was Broken (Root Causes)
1. Compose env drift: production commands initially ran without explicitly binding repo `.env`, causing blank `DB_PASSWORD`/`SECRET_KEY` at runtime.
2. Database auth mismatch: Postgres volume retained credentials incompatible with app env, causing backend restart loop (`password authentication failed for user sims_user`).
3. Seed command defect: `seed_e2e` used `Department.update_or_create(code=...)` despite unique `name`, causing duplicate-name integrity failure on existing data.
4. Caddy reload drift: Caddy reload failed due log writer permissions (`/var/log/caddy/pgsims_access.log: permission denied`), preventing route updates from becoming active.

## Exact Fixes Applied
1. Canonical path alignment:
- Created symlink `/srv/apps/pgsims -> /home/munaim/srv/apps/pgsims` (host had no `/srv` tree).

2. Production stack stabilization (only prod compose used):
- Used `docker compose --env-file /srv/apps/pgsims/.env -f docker/docker-compose.prod.yml ...` for all lifecycle/actions.
- Rebuilt and restarted prod services.

3. DB auth repair (non-destructive):
- Updated DB role password in-place to match `.env`:
  - `ALTER USER sims_user WITH PASSWORD '<DB_PASSWORD from .env>'`
- Restarted `web/worker/beat` services.

4. Deterministic seeding fix in code:
- Patched [`/srv/apps/pgsims/backend/sims/users/management/commands/seed_e2e.py`](/srv/apps/pgsims/backend/sims/users/management/commands/seed_e2e.py) to upsert departments by unique `name` and update `code`/`active`.
- Rebuilt backend images and reran seed.

5. Caddy canonical routing + reload reliability:
- Updated canonical Caddy config [`/srv/apps/pgsims/deploy/Caddyfile.pgsims`](/srv/apps/pgsims/deploy/Caddyfile.pgsims) route from `handle /healthz` to `handle /healthz*`.
- Synced to `/etc/caddy/Caddyfile` via `ops/caddy_sync_reload.sh`.
- Fixed Caddy log path permissions (`/var/log/caddy`, `pgsims_access.log` owned by `caddy:caddy`) so reload works.
- Reloaded Caddy successfully and revalidated config.

## Verification Results

### 1) HTTPS frontend serves correctly
- `12_curl_https_root.txt`: `HTTP/2 200`

### 2) Health endpoint reachable via HTTPS and returns 200
- `12_curl_https_healthz_get_headers.txt`: `HTTP/2 200` at `/healthz/`
- Note: `/api/healthz/` returns 404 by current app routing; accepted path is `/healthz/`.

### 3) Login endpoint works with seeded deterministic user
- `13_api_login_response.json`: returns valid `access` + `refresh` JWT and `user` payload for `e2e_admin / Admin123!`.

### 4) Dashboard/data backing APIs return meaningful role data
- `13_admin_dashboard_overview.json`: non-empty metrics (e.g., `total_residents`, `active_rotations`, `last_30d_logs`).
- `13_utrmc_reports_catalog.json`: 20 report entries returned for UTRMC role.
- `13_pg_cases_statistics.json`: valid statistics schema returned for PG role.

### 5) Caddy validates and reloads cleanly
- `10_caddy_validate.txt`: `Valid configuration`
- `10_caddy_sync_reload.txt`: sync + validate + reload routine completed.
- `10_caddy_reload_manual.txt`: successful reload after permission repair.

### 6) Frontend built with correct API base (not localhost)
- `06_frontend_env.txt`: `NEXT_PUBLIC_API_URL=https://pgsims.alshifalab.pk`
- `06_frontend_localhost_grep.txt`: no `localhost:8000` references found in container grep output.

### 7) Backend migrations + seed + superadmin
- `07_migrate.txt`: migrations applied (`No migrations to apply` on final run).
- `08_seed_e2e.txt`: `seed_e2e completed successfully.`
- `09_create_superadmin.txt`: superadmin password reset complete (`admin / admin123`).

### 8) Safety checks
- `14_ss_listening_ports.txt`: backend/frontend bound to loopback (`127.0.0.1:8014`, `127.0.0.1:8082`), no direct public app port exposure.

## Remaining Known Issues (Non-Blocking for this prod smoke gate)
1. `manage.py test` has existing suite issues unrelated to runtime boot (missing `factory` test dependency, plus legacy test failures): see `15_backend_tests.txt`.
2. Local Playwright run fails due repository test runner/config mismatch (`Playwright Test did not expect test() to be called here`): see `16_playwright_test.txt`.
3. Compose warns that `version` key is obsolete in compose file (warning only).

## Changed Files in This Remediation
- [`/srv/apps/pgsims/backend/sims/users/management/commands/seed_e2e.py`](/srv/apps/pgsims/backend/sims/users/management/commands/seed_e2e.py)
- [`/srv/apps/pgsims/deploy/Caddyfile.pgsims`](/srv/apps/pgsims/deploy/Caddyfile.pgsims)
- Evidence artifacts under `/srv/apps/pgsims/OUT/PROD_REMEDIATION_EVIDENCE/`

