# Runtime Baseline Before Frontend Docker Rebuild

- Timestamp (UTC): `2026-04-25 22:39:18`
- Compose file used: `docker/docker-compose.yml`
- Env file used: `.env`
- Current branch: `main`
- Current commit: `45bc65320e91d57a3c0a4d434f1daefd175c3780`
- Working tree clean: `No`

## Git Status

`git status --short` shows a dirty tree with many untracked files, including existing audit artifacts under `docs/_truthmap/` and numerous backend/frontend test files. This session did not clean or modify those files.

## Compose Baseline

## Requested command note

Running `docker compose ...` from repo root without `-f docker/docker-compose.yml --env-file .env` fails with:

```text
no configuration file provided: not found
```

The repository’s own `Makefile` and scripts consistently use `docker compose -f docker/docker-compose.yml --env-file .env`, so that explicit compose target was used for all runtime evidence below.

## Running Services

`docker compose -f docker/docker-compose.yml --env-file .env ps`

```text
NAME             IMAGE                SERVICE   CREATED        STATUS                  PORTS
pgsims_backend   docker-backend       backend   40 hours ago   Up 40 hours (healthy)   127.0.0.1:8014->8014/tcp
pgsims_beat      docker-beat          beat      40 hours ago   Up 40 hours             8014/tcp
pgsims_db        postgres:15-alpine   db        2 days ago     Up 2 days (healthy)     5432/tcp
pgsims_redis     redis:7-alpine       redis     2 days ago     Up 2 days (healthy)     6379/tcp
pgsims_worker    docker-worker        worker    40 hours ago   Up 40 hours             8014/tcp
```

Critical baseline finding: `frontend` is defined in compose but no `pgsims_frontend` container is currently running.

## Image / Container Identity

### Frontend

- Compose image present: `docker-frontend:latest`
- Image ID before rebuild: `27dcafb0173a`
- Container ID before rebuild: `missing`
- Container state before rebuild: `no such object: pgsims_frontend`

### Backend

- Image ID: `9df4e26d8c147d4f08ca1b60428c5579e2c8de4acf3fc7eca0c76ae23815a931`
- Container ID: `77d760a49b67f6a0e3c1a68e0f7886fe08ad57e80dcfc32e577c4a32501d56e7`
- Container created: `2026-04-24T06:52:03.719242578Z`

## Running URLs

- Backend direct URL: `http://127.0.0.1:8014`
- Backend health URL: `http://127.0.0.1:8014/healthz/`
- Frontend expected direct URL from compose: `http://127.0.0.1:8082`
- Frontend current state: not running, so the expected direct URL is not currently served by the PGSIMS compose stack

## Compose/Image Output Summary

`docker compose ... images` shows:

```text
pgsims_backend -> docker-backend:latest (image id 9df4e26d8c14)
pgsims_beat    -> docker-beat:latest
pgsims_db      -> postgres:15-alpine
pgsims_redis   -> redis:7-alpine
pgsims_worker  -> docker-worker:latest
```

`frontend` is absent from the active compose image/container list despite `docker-frontend:latest` existing locally.

## Log Findings

### Frontend logs

- `docker compose ... logs frontend --tail=100` returned no app logs because no frontend container is active.

### Backend logs

- Backend log tail is dominated by repeated slow `/healthz/` warnings around 1.0-1.1s.
- No frontend-related backend errors were visible in the captured backend tail.

## Obvious Frontend 404 / Build Error Indicators

- No current frontend container means no trustworthy runtime can be inferred from the compose stack.
- Prior truthmap/frontend 404 findings are unreliable until a fresh `frontend` container is rebuilt and started.
- The current compose invocation emits warnings that `DB_PASSWORD` and `SECRET_KEY` are unset in `.env`, which indicates the checked-in `.env` is not the source of the currently running backend container’s environment.

## Stale-Build Risk Indicators Identified Before Rebuild

- `frontend/Dockerfile` uses a multi-stage Next.js standalone build and copies `.next/standalone` plus `.next/static` into the runtime image.
- `docker/docker-compose.yml` defines no frontend bind mount, so host files are not overriding runtime assets through compose.
- Because no frontend container is running, the immediate baseline problem is runtime absence first; rebuild/start verification is required before classifying any app-level route gap.
