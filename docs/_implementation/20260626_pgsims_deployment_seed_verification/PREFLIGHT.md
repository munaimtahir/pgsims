# PGSIMS Deployment Seed Verification - Preflight

Date: 2026-06-26

## Session Window

PRIMARY PURPOSE: Verify existing PGSIMS deployment readiness and minimal seed state.
IN-SCOPE: Docker runtime, Caddy/domain routing, data backup/cleanup, login/smoke verification.
OUT-OF-SCOPE: new PGMS app, rebuild, new modules, feature work, broad refactors.
SUCCESS CRITERIA: pg.fmu.edu.pk reachable, services healthy, sample users active and linked, evidence complete.
FALLBACK PLAN: fix only deployment blockers or document BLOCKED/CONDITIONAL GO.
GUARDRAILS ACTIVE: G1-G20 enforced.

## Repository State

- Working directory: `/home/munaim/srv/apps/pgsims`
- Branch: `main`
- Latest commit: `3599a67 Ignore local Gemini artifacts and redact transcripts`
- Recent commits:
  - `3599a67 Ignore local Gemini artifacts and redact transcripts`
  - `7e16dcd Update session log for Drive frontend`
  - `4b83727 Add Google Drive backup frontend`
  - `686bd7f Pass Google Drive env vars to services`
  - `7022dc3 Document Google Drive backup env vars`
- Initial `git status --short`: clean output was not shown before this run; after fixes, expected modified files are deployment-blocker fixes plus evidence docs.

## Files Found

- Compose files:
  - `docker/docker-compose.yml`
  - `docker/docker-compose.prod.yml`
  - `docker/docker-compose.dev.yml`
  - `docker/docker-compose.local.yml`
  - `docker/docker-compose.coolify.yml`
  - `docker/docker-compose.phc.yml`
- Caddy files:
  - `deploy/Caddyfile.pgsims`
  - `ops/caddy_sync_reload.sh`
  - `ops/caddy_sync_reload_askpass.sh`
  - active system config: `/etc/caddy/Caddyfile`
- Env files:
  - `.env` exists; used with `docker compose --env-file .env ...`
  - `backend/.env` exists
  - `backend/.env.example` exists
  - Secrets were not printed; sensitive values were masked in compose/env inspection.

## Compose/Runtime Assumptions

- Plain `docker compose config` from repo root fails because there is no root compose file.
- Effective command used: `docker compose --env-file .env -f docker/docker-compose.yml ...`
- Services defined: `db`, `redis`, `backend`, `worker`, `beat`, `frontend`
- Database service/container: `db` / `pgsims_db`
- Exposed local ports:
  - backend: `127.0.0.1:8014 -> 8014`
  - frontend: `127.0.0.1:8082 -> 3000`
- Domain/routing assumption:
  - `pg.fmu.edu.pk` resolves to `34.10.178.210`
  - Caddy terminates HTTPS and proxies `/api/*` and `/admin/*` to `127.0.0.1:8014`, frontend to `127.0.0.1:8082`

## PGMS Check

- No local `pgms/` folder was found under this repository.
- Separate old `pgms-*` Docker containers were present on unrelated loopback ports (`3026`, `8026`) but are not required by this PGSIMS deployment.

