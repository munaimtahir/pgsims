# Docker Runtime Status

## Restore event

The local pgsims stack was down when verification started. It was restored with:

```bash
docker compose -f docker/docker-compose.yml --env-file .env up -d
```

## Current status

| Service | Status | Notes |
|---|---|---|
| backend | healthy | recreated during restart |
| frontend | healthy | reachable on `127.0.0.1:8082` |
| db | healthy | PostgreSQL container healthy |
| redis | healthy | healthy |
| worker | up | running |
| beat | up | running |

## Evidence

- `docker compose -f docker/docker-compose.yml --env-file .env ps`
- `docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'`

## Staleness note

The stack was recreated in this sprint, so container freshness is current even though the base images are named `docker-backend`, `docker-frontend`, etc.
