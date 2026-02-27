# Production Runbook

## Canonical Compose Wrapper (target pattern)
Use `ops/prod_dc.sh` as the only production compose entrypoint once guardrails are unblocked.

Example command pattern:
- `ops/prod_dc.sh ps`
- `ops/prod_dc.sh logs -n 200 web`
- `ops/prod_dc.sh up -d --build`

## Current Equivalent (until wrapper is added)
- `docker compose --project-directory /srv/apps/pgsims --env-file /srv/apps/pgsims/.env -f /srv/apps/pgsims/docker/docker-compose.prod.yml ps`

## Restart
- `docker compose --project-directory /srv/apps/pgsims --env-file /srv/apps/pgsims/.env -f /srv/apps/pgsims/docker/docker-compose.prod.yml restart`

## Rebuild
- `docker compose --project-directory /srv/apps/pgsims --env-file /srv/apps/pgsims/.env -f /srv/apps/pgsims/docker/docker-compose.prod.yml up -d --build`

## Migrate (reference only)
- `docker compose --project-directory /srv/apps/pgsims --env-file /srv/apps/pgsims/.env -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T web python manage.py migrate --noinput`

## Seed (reference only)
- `docker compose --project-directory /srv/apps/pgsims --env-file /srv/apps/pgsims/.env -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T web python manage.py loaddata <seed_file.json>`

## Caddy Sync
- `/srv/apps/pgsims/ops/caddy_sync_reload.sh`
- Validate directly:
  - `sudo caddy validate --config /etc/caddy/Caddyfile`
