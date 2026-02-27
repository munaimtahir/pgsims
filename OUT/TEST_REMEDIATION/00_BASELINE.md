# Test Remediation Baseline

Date: 2026-02-27
Repo: `/srv/apps/pgsims`
Compose file: `/srv/apps/pgsims/docker/docker-compose.prod.yml`
Backend service: `web`

## Captured Baseline Artifacts
- `00_ps.txt`
- `00_python.txt`
- `00_pip_freeze.txt`
- `01_test_failures_raw.txt`

## Baseline Test Command
`docker compose -f docker/docker-compose.prod.yml exec -T web python manage.py test -v 2`

## Baseline Result
- Status: **FAILED**
- Total tests discovered: `158`
- Failures: `3`
- Errors: `5`

## Baseline Failure Summary
- Import/dependency errors due to missing `factory` module.
- One import-time script (`test_frontend_create`) executed during discovery and failed model validation.
- User search service tests failed for short query term under PostgreSQL full-text behavior.
