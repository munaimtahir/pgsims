# Monitoring and Healthcheck Readiness

## Available checks

- `./scripts/pgsims_ps.sh`
- `./scripts/pgsims_health.sh`
- `./scripts/pgsims_logs.sh backend`
- `./scripts/pgsims_logs.sh frontend`
- `./scripts/pgsims_logs.sh worker`
- `./scripts/pgsims_logs.sh beat`

## Operator flow

1. Run the health script.
2. Confirm backend `/healthz/` responds.
3. Confirm the frontend login page loads.
4. Inspect service logs only if a health check fails.

## Escalation cues

- Backend restart loop
- Frontend unavailable
- Database unhealthy
- Redis unhealthy
- Celery worker or beat unavailable

## Readiness note

The current stack can be checked quickly with the helper scripts and the health endpoint returned a healthy response during this sprint.
