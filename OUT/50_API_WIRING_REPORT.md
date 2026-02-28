# 50 API Wiring Report (PGSIMS)

Date: 2026-02-28
Repo: /home/munaim/srv/apps/pgsims (main)
Domain: https://pgsims.alshifalab.pk
Active Caddyfile: /etc/caddy/Caddyfile
Active compose: docker/docker-compose.prod.yml

## Executive Result
Current routing is already Caddy-first for browser traffic.
- Caddy proxies `/api/*` and `/admin/*` to host loopback `127.0.0.1:8014`.
- Caddy proxies frontend `/` to `127.0.0.1:8082`.
- Docker internal backend service is reachable as `http://backend:8014` (not `:8000`).

Standardization performed:
- Browser/client calls standardized to same-origin API paths (effective `/api/...` through Caddy).
- Server-side fallback standardized to `http://backend:8014`.

## Phase A: Caddy Listeners and Upstreams
Evidence:
- `OUT/Caddyfile.current`
- `OUT/Caddyfile.current.numbered.txt`
- `OUT/listeners_filtered.txt`

Findings:
- Site block: `pgsims.alshifalab.pk`.
- Caddy listens on `*:80` and `*:443`.
- Upstreams:
  - `/api/*` -> `127.0.0.1:8014`
  - `/admin/*` -> `127.0.0.1:8014`
  - `/healthz*` -> `127.0.0.1:8014`
  - catch-all `/` -> `127.0.0.1:8082`
- Upstream address type is host loopback (`127.0.0.1:<port>`), not docker DNS.

## Phase B: Compose Networking and Ports
Evidence:
- `OUT/compose.rendered.yml`
- `OUT/compose.rendered.numbered.txt`
- `OUT/docker_network_inspect_docker_sims_network.json`

Findings:
- Backend service name: `backend`.
- Backend process binds `0.0.0.0:8014` in container.
- Backend is published to host only on loopback: `127.0.0.1:8014:8014`.
- Frontend service name: `frontend`, published as `127.0.0.1:8082:3000`.
- Container-network reachability: `http://backend:8014` from other containers on `docker_sims_network`.

Reachability statements:
- Backend reachable from host on: `http://127.0.0.1:8014`
- Backend reachable from containers via: `http://backend:8014`

## Phase C: Frontend API Base Usage
Evidence:
- `OUT/frontend_api_refs.txt`
- `OUT/frontend_apiclient_usage.txt`
- `frontend/lib/api/client.ts`
- `frontend/next.config.mjs`

Findings before standardization:
- Frontend API methods mostly call endpoint paths like `/api/...`.
- Axios base URL came from `NEXT_PUBLIC_API_URL` and prod compose set it to `https://pgsims.alshifalab.pk`.
- This worked, but was absolute-domain style, not the requested client-relative convention.

## Phase D: Runtime Truth Checks
Evidence:
- `OUT/docker_ps_table.txt`
- `OUT/runtime_backend_localhost8000_head.txt`
- `OUT/runtime_backend_localhost8014_head.txt`
- `OUT/runtime_backend_backend8000_head.txt`
- `OUT/runtime_backend_backend8014_head.txt`
- `OUT/runtime_frontend_wget_backend8000_admin.txt`
- `OUT/runtime_frontend_wget_backend8014_admin.txt`
- `OUT/runtime_frontend_wget_domain_api_auth_profile.txt`
- `OUT/runtime_host_to_domain_admin_head.txt`
- `OUT/runtime_host_to_domain_api_head.txt`
- `OUT/runtime_host_to_domain_api_auth_profile_head.txt`

Observed runtime truth:
- `127.0.0.1:8000` in backend container: connection refused.
- `127.0.0.1:8014` in backend container: responds (200).
- `backend:8000` on docker network: connection refused.
- `backend:8014` on docker network: responds (HTTP from Django/Gunicorn).
- `https://pgsims.alshifalab.pk/admin/`: proxied and responds (302 to admin login).
- `https://pgsims.alshifalab.pk/api/auth/profile/`: proxied and responds (401 unauthenticated, expected).
- `https://pgsims.alshifalab.pk/api/`: 404 (endpoint not defined), but still routed through Caddy to backend.

## Phase E: Standardization Changes Applied
Target standard:
- Client-side -> same-origin `/api` pathing through Caddy.
- Server-side (if needed) -> internal URL `http://backend:8014`.

Changes made:
1. `frontend/lib/api/client.ts`
- Browser default now uses same-origin pathing (empty axios base with `/api/...` endpoints).
- Added server fallback base URL: `SERVER_API_URL` or `http://backend:8014`.
- Added guard so if `NEXT_PUBLIC_API_URL=/api`, it does not produce `/api/api/...` duplication.

2. `frontend/next.config.mjs`
- Default `NEXT_PUBLIC_API_URL` changed to `/api`.

3. `frontend/Dockerfile`
- Build arg default changed to `NEXT_PUBLIC_API_URL=/api`.

Compose and Caddy did not require wiring changes for this standardization.

## Final Wiring Diagram
```text
Browser
  -> https://pgsims.alshifalab.pk/api/*
  -> Caddy (:443)
  -> reverse_proxy 127.0.0.1:8014
  -> docker backend container (service: backend, port 8014)

Browser
  -> https://pgsims.alshifalab.pk/* (non-api)
  -> Caddy (:443)
  -> reverse_proxy 127.0.0.1:8082
  -> docker frontend container (service: frontend, port 3000)

Server-side frontend code (if used)
  -> http://backend:8014 (docker DNS, internal network)
```

## PASS Criteria Check
- Browser can call `/api` without CORS issues: PASS (same-origin via Caddy, verified with `/api/auth/profile/` returning 401, not CORS failure).
- Frontend pages load: PASS (frontend container healthy; root/admin routes respond).
- API login works (200): NOT EXECUTED in this run (no login credential flow executed here).

## Notes
- Real backend internal port is `8014`, not `8000`; all standardization was aligned to the actual running service.
