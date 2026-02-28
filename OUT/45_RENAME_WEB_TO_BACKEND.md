# Rename Web to Backend

## Scope
- Standardized Docker service naming from `web` to `backend`.
- Primary target compose file: `docker/docker-compose.prod.yml`.
- Also aligned sibling compose files for consistency:
  - `docker/docker-compose.yml`
  - `docker/docker-compose.dev.yml`
  - `docker/docker-compose.local.yml`
  - `docker/docker-compose.coolify.yml`
  - `docker/docker-compose.phc.yml`

## Compose Changes Applied
- Service key renamed: `web:` -> `backend:`
- `depends_on` references updated to `backend` where applicable.
- Internal host references updated (`http://web:...` -> `http://backend:...`).
- No temporary compatibility alias (`web`) was added.

## Caddy Impact
- Caddy upstreams use `127.0.0.1` bindings, not Docker DNS names.
- No upstream hostname rewrite required.
- Evidence:
  - `OUT/Caddyfile.before`
  - `OUT/Caddyfile.after`
  - `OUT/caddy_validate_after.txt`

## Evidence Artifacts
- `OUT/compose_before.yml`
- `OUT/compose_after.yml`
- `OUT/rg_web_before.txt`
- `OUT/rg_web_after.txt`
