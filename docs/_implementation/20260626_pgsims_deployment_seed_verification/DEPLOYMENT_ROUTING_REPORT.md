# Deployment and Routing Report

Date: 2026-06-26

## Docker

- Compose file used: `docker/docker-compose.yml`
- Command used: `docker compose --env-file .env -f docker/docker-compose.yml up -d --build`
- Initial blocker: build failed with `no space left on device`.
- Fix applied:
  - `docker builder prune -af` reclaimed disk space.
  - Added `frontend/.dockerignore` so Docker no longer sends generated/cache directories.
  - Frontend context reduced from about `905MB` to `1.41MB` on the next build.
- Second blocker: `next build` failed on lint errors.
- Fix applied: narrow lint fixes in:
  - `frontend/app/dashboard/change-password/page.tsx`
  - `frontend/app/dashboard/utrmc/supervisors/page.tsx`
  - `frontend/app/register/page.test.tsx`
  - `frontend/app/reset-password/[uid]/[token]/page.tsx`

Final `docker compose ps` evidence:

```text
pgsims_backend    Up (healthy)   127.0.0.1:8014->8014/tcp
pgsims_frontend   Up (healthy)   127.0.0.1:8082->3000/tcp
pgsims_db         Up (healthy)   5432/tcp
pgsims_redis      Up (healthy)   6379/tcp
pgsims_worker     Up
pgsims_beat       Up
```

Backend startup log evidence:

```text
Running migrations:
  No migrations to apply.
156 static files copied to '/app/staticfiles', 3 unmodified, 412 post-processed.
Starting gunicorn 26.0.0
Listening at: http://0.0.0.0:8014
```

Note: PostgreSQL healthcheck logs include `FATAL: database "sims_user" does not exist`, caused by `pg_isready -U sims_user` defaulting to database name `sims_user`. The service is still healthy and the Django app connects to `sims_db`.

## Caddy

- Canonical project Caddyfile: `deploy/Caddyfile.pgsims`
- Active system Caddyfile: `/etc/caddy/Caddyfile`
- `pg.fmu.edu.pk` is present in both configs.
- Canonical config validates:

```text
caddy validate --config deploy/Caddyfile.pgsims
Valid configuration
```

- Active system config validates and Caddy is active:

```text
caddy validate --config /etc/caddy/Caddyfile
Valid configuration
systemctl is-active caddy -> active
```

Active Caddy routing:

- `/api/*` -> `127.0.0.1:8014`
- `/admin/*` -> `127.0.0.1:8014`
- `/static/*` -> `/home/munaim/srv/apps/pgsims/backend/staticfiles`
- `/media/*` -> `/home/munaim/srv/apps/pgsims/backend/media`
- frontend fallback -> `127.0.0.1:8082`

Conditional gap:

- `deploy/Caddyfile.pgsims` contains a `/healthz*` backend handler.
- Active `/etc/caddy/Caddyfile` lacks that handler, so `https://pg.fmu.edu.pk/healthz` returns Next.js `404`.
- Attempted `/etc/caddy/Caddyfile` update was blocked because `sudo` requires an interactive password.

## Domain and HTTPS

- DNS evidence: `pg.fmu.edu.pk -> 34.10.178.210`
- HTTPS works through Caddy.
- Domain checks:

```text
https://pg.fmu.edu.pk/        -> HTTP/2 200
https://pg.fmu.edu.pk/login   -> HTTP/2 200
https://pg.fmu.edu.pk/api/    -> HTTP/2 401 (expected unauthenticated API response)
https://pg.fmu.edu.pk/static/admin/css/base.css -> HTTP/2 200
https://pg.fmu.edu.pk/healthz -> HTTP/2 404 (conditional Caddy health route drift)
```

## Internal Service Checks

```text
http://127.0.0.1:8014/healthz/ -> HEAD 405, Allow: GET
http://127.0.0.1:8014/api/     -> 401 Unauthorized
http://127.0.0.1:8082/         -> 200 OK
http://127.0.0.1:8082/login    -> 200 OK
```

