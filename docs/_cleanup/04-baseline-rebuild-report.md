# Phase D — Trusted Baseline Rebuild Report

Date (UTC): 2026-04-21

## Rebuild Actions
1. Recreated runtime from clean state (`docker compose down -v` then `up -d`).
2. Re-applied migrations.
3. Seeded canonical organization reference data only (`seed_org_data`).
4. Recreated minimal verification users by role:
   - `admin`
   - `pilot_pg`
   - `pilot_resident`
   - `pilot_supervisor`
   - `pilot_utrmc_admin`
   - `pilot_utrmc_user`
5. Rebuilt backend/frontend containers (`docker compose build --no-cache backend frontend`) and restarted.

## Rebuild Verification
- Backend health endpoint: HTTP 200 (`/healthz/`)
- Frontend root endpoint: HTTP 200 (`/`)
- Compose services healthy: backend, frontend, db, redis, worker, beat.

## Observed Rebuild Caveat
- A transient connection-reset occurred immediately after container recreation while health probing; subsequent probes succeeded after service warm-up.

## Baseline Outcome
- Trusted clean baseline established with minimal identities and canonical reference entities.
- No retained dependency on previous dirty runtime state.
