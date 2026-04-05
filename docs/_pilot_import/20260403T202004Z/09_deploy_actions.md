# 09 Deploy Actions

## Actions Taken

1. Generated migration for year=5 support:
   - `backend/sims/users/migrations/0003_alter_historicaluser_year_alter_user_year.py`
2. Rebuilt backend-related images from current repo code:
   - backend
   - worker
   - beat
3. Recreated services with explicit env file to avoid unset-variable drift:
   - `docker compose --env-file .env -f docker/docker-compose.yml up -d --force-recreate ...`
4. Verified runtime now includes required pilot import commands/modules.
5. Completed import against running target DB.

## Important Recovery Event

- During restart, services briefly crash-looped because compose was run without explicit env-file binding, causing `SECRET_KEY` to appear unset at runtime.
- Recovered by recreating stack with `--env-file .env`.
- Health returned to green before import continuation.

## No Demo Reseed Evidence

- Post-import user scan found no demo/e2e/test-pattern users.
- Services run without auto-seed jobs adding demo records.

