# Docker Helper Scripts

## Added scripts

- `scripts/pgsims_up.sh`
- `scripts/pgsims_down.sh`
- `scripts/pgsims_restart.sh`
- `scripts/pgsims_ps.sh`
- `scripts/pgsims_logs.sh`
- `scripts/pgsims_health.sh`
- `scripts/pgsims_seed_e2e.sh`

## Behavior

- All stack commands use `docker compose -f docker/docker-compose.yml --env-file .env`.
- Down/restart commands do not delete volumes.
- The health script checks backend `/healthz/` and the frontend login page.
- The seed wrapper preserves the existing E2E seed flow.

## Notes

- Scripts are executable and rooted at the repo root before invoking compose.
- No compose or application code change was needed for this phase.
