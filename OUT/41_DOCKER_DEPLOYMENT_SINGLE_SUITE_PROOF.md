# Docker + Caddy Single-Suite Deployment Proof

## Active Production Compose Source
- Active compose config file(s): `/srv/apps/pgsims/docker/docker-compose.prod.yml`
- Primary compose file used for proof commands: `/srv/apps/pgsims/docker/docker-compose.prod.yml`

## Rendered Compose + Runtime State
- Rendered config: `OUT/compose_rendered.yml`
- Runtime containers: `OUT/docker_ps.txt`

## Static Assets Readiness
- Collectstatic execution output: `OUT/collectstatic_output.txt`
- Static files count in container: `647` files

## Caddy Routing Proof
- Caddy validation output: `OUT/caddy_validate.txt`
- Active Caddyfile snapshot: `OUT/Caddyfile.active`

## Domain Header Checks
- Root headers: `OUT/curl_root_headers.txt`
- Admin headers: `OUT/curl_admin_headers.txt`
- API root headers: `OUT/curl_api_headers.txt`

## One Domain, Multi-Upstream, Single Suite Summary
- Domain tested: `https://pgsims.alshifalab.pk`
- Evidence shows root, admin, and API routes are reachable through the same public domain with Caddy fronting backend/frontend upstreams.
- Compose runtime and Caddy configuration together demonstrate a single deployed suite serving multiple upstream app surfaces.
