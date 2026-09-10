# 09 — Production Baseline (read-only inspection via `ssh test`, 2026-09-09)

All inspection was read-only: `git status/log/rev-parse/fetch`, `docker compose ps/logs/exec` with
non-mutating management commands (`showmigrations --plan`, never `migrate`), `curl` GET only, `env`
piped through a name-only filter (no secret values printed), `df/free/uptime`, and Caddyfile reads.
No deploy, migrate, restart, or data-mutating command was run.

## Repo path & deployed SHA

- Host: `vps-clone`, repo at `/home/munaim/srv/apps/pgsims`.
- Deployed HEAD: `4f8e27624c0c01c6dadd82322220ad06b99cdc51` ("Verify production logbook correction
  and release 1.1.4", 2026-09-08 23:20:01 +0500).
- Local main HEAD (this session): `56861124aa6a9a73122c1e5f56f85fb5e6914cfb` ("Freeze PGR Companion
  1.1.4 release", 2026-09-08 23:39:18 +0500).
- **Drift: prod is 1 commit behind `origin/main`.** `git log 4f8e276..5686112 --stat` shows the
  pending commit touches only `ANDROID_RELEASE_1.1.4.md`, `SPRINT_STATE.md`,
  `scripts/check_pgr_companion_release.sh` — docs/release-notes and a gate script, **no backend
  code, no migrations, no frontend code**. Safe to fast-forward whenever convenient; not urgent.
- Working tree on prod: clean (`nothing to commit`).

## Deployment structure

- Compose file: `docker/docker-compose.prod.yml` with `--env-file .env`.
- Production stack (`pgsims_*`, project likely `pgsims`): `backend` (healthy, up 13h — recently
  recreated, see below), `frontend` (healthy, up 3d), `db` (postgres:15-alpine, healthy, up 3d),
  `redis` (healthy, up 3d), `worker` (celery, up 3d), `beat` (celery beat, up 3d).
- A **separate staging stack** also runs on the same host: `pgsims-staging-{backend,worker,db,redis}-1`,
  backend on `127.0.0.1:18014` (healthy, up 44h), fully isolated (own DB/redis containers, no shared
  DB with prod). Not part of production traffic; noted for completeness only.
- Ports bound only to `127.0.0.1` (8014 backend, 8082 frontend, 18014 staging backend) — not
  directly internet-exposed; all public traffic goes through Caddy.

## Host facts

- Ubuntu 24.04.4 LTS, uptime 3d 11h, load average 0.70/0.81/0.74 (light).
- Disk: `/` at 145G total, **117G used (81%)**, 28G available. Worth monitoring — not critical yet
  but should be tracked given Docker image/log growth; not urgent enough for Build Wave 0.
- Memory: 15Gi total, 5.1Gi used, 10Gi available, 0B swap.

## Reverse proxy (Caddy)

`/etc/caddy/Caddyfile` (note: **shared multi-tenant host** — also serves unrelated products
`lims.alshifalab.pk`, `consult.alshifalab.pk`, etc. Only PGR SIMS blocks are relevant here):

- **Production web + resident-facing domains**: `pgsims.alshifalab.pk`, `pgsims.pmc.edu.pk`,
  `pg.fmu.edu.pk` → `/static/*` and `/media/*` served directly from
  `backend/staticfiles`/`backend/media`; `/api/*` and `/admin/*` → `127.0.0.1:8014` (backend);
  everything else → `127.0.0.1:8082` (frontend). This matches `docker-compose.prod.yml`'s port
  mapping exactly.
- **API-only / Android-facing domains**: `api.pgsims.alshifalab.pk`, `api.pgsims.pmc.edu.pk`, and
  `android.pgsims.alshifalab.pk` all → `127.0.0.1:8014` (same backend). This is the production
  Android API host referenced by CLAUDE.md/`PGR_SIMS_ANDROID_API_INTEGRATION.md` — confirms a
  single canonical backend, no separate Android-only service.
- **P2 finding — dangling Caddy route**: `pgr.fmu.edu.pk` is configured to reverse-proxy to
  `127.0.0.1:8026` (API) and `127.0.0.1:3026` (web), but `ss -ltnp` shows **nothing listens on
  either port** on this host. This route currently 502s. It is not part of the `docker-compose.prod.yml`
  stack described in CLAUDE.md/AGENTS.md and does not match any compose file's port mappings found
  in `docker/`. Likely a stale/planned domain from an earlier or different deployment plan (possibly
  the historical PGR/PGMS naming referenced in AGENTS.md, or a decommissioned parallel stack). Not a
  security risk, but it's config drift that should be cleaned up or documented — recommend
  confirming with the domain owner (fmu.edu.pk) whether it's needed, then either wiring it to the
  correct backend or removing the block.

## Service health

- `GET http://127.0.0.1:8014/api/health/` → **200** (prod backend).
- `GET http://127.0.0.1:8082/` → **200** (prod frontend).
- `GET http://127.0.0.1:18014/api/health/` → **200** (staging backend, informational only).
- DB connectivity confirmed indirectly (health endpoint 200 implies DB reachable) and directly via
  successful `showmigrations` DB query (below).

### P2 finding — gunicorn worker timeout coincident with inspection load

`docker compose logs --since 6h backend` shows a run of `GET /healthz/` requests slowing to
~1000-1030ms each over ~90 seconds, followed by:
```
[CRITICAL] WORKER TIMEOUT (pid:45)
[ERROR] Error handling request (no URI read)
[ERROR] Worker (pid:45) was sent SIGKILL! Perhaps out of memory?
```
This occurred at 07:02 UTC, overlapping with this session's own `docker compose exec` management
commands running inside the same container/host. It is plausibly caused by this inspection's own
load on a synchronous gunicorn worker pool rather than a pre-existing production defect, but it does
indicate the backend's gunicorn config has **thin headroom under concurrent load** (sync workers,
apparently low worker count, single-request-at-a-time blocking behavior visible in the `/healthz/`
latency creep). Recommend reviewing gunicorn worker class/count (`--workers`, `--worker-class`,
timeout) as a Build Wave 1 hardening item — not urgent, but worth a controlled load-test rather than
inferring from this one incidental event.

## Migration state

`python manage.py showmigrations --plan` inside the prod backend container: **106 migrations
applied, 0 pending** (`grep -c '^\[X\]'` = 106, `grep -c '^\[ \]'` = 0). Includes
`training.0009_add_training_year_notes`, `training.0010_add_actual_end_date`,
`users.0014_historicalresidentprofile_declaration_accepted_and_more`,
`users.0015_historicalresidentprofile_review_note_and_more` as the most recent applied migrations —
consistent with an up-to-date, fully-migrated production schema at the deployed SHA.

## Environment sanity (presence only, no values printed)

Confirmed **set** on the running backend container: `SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS`,
`CORS_ALLOWED_ORIGINS`. `DEBUG=False` confirmed (boolean, not a secret — safe to state directly).
No secret values were read or written anywhere in this process.

## Production vs main drift — summary

| | SHA | Notes |
|---|---|---|
| Production | `4f8e276` | 2026-09-08 23:20 |
| origin/main / local main | `5686112` | 2026-09-08 23:39, 1 commit ahead |

Pending commit is docs/scripts-only (Android release freeze notes + a release gate script tweak) —
**no backend/frontend code, no migrations**. No production risk from this drift; safe to
fast-forward on the next routine deploy, no dedicated deploy needed for this alone.

## Confirmation

No mutating command (`migrate`, `restart`, `up -d --build`, data writes, config edits, service
start/stop) was executed against the production or staging stacks during this inspection. All
`docker compose exec` calls used read-only Django management commands or `env` filtered to variable
names only.
