# Smoke Tests

## Root (frontend)
- `curl -I https://pgsims.alshifalab.pk/`
- Expected: `HTTP/2 200` or `HTTP/2 304`

## Health Endpoint
- `curl -I https://pgsims.alshifalab.pk/healthz/`
- Expected: `HTTP/2 200`
- Current lock run observed: `HTTP/2 405` (blocker)

## Local Upstream Probes
- `curl -I http://127.0.0.1:8082/` expected `200`
- `curl -I http://127.0.0.1:8014/healthz/` expected `200`

## Auth Login Endpoint (behavioral)
- `curl -i -X POST https://pgsims.alshifalab.pk/api/auth/login/ -H 'Content-Type: application/json' -d '{"email":"invalid@example.com","password":"invalid"}'`
- Expected:
  - endpoint reachable through proxy
  - authentication failure response (4xx) for invalid credentials
  - no 5xx from proxy/upstream
