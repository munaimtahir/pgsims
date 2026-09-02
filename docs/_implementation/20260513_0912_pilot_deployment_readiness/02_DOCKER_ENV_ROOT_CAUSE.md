# Docker Env Root Cause

## Classification

- **Stale container issue**

## Evidence

- `docker compose -f docker/docker-compose.yml --env-file .env config` resolves `SECRET_KEY` correctly.
- `docker inspect pgsims_backend` shows `SECRET_KEY=` empty in the live container environment.
- `docker inspect pgsims_worker` and `docker inspect pgsims_beat` also show `SECRET_KEY=` empty.
- Runtime logs for backend, worker, and beat all fail with `RuntimeError: SECRET_KEY environment variable is required`.
- The repo `.env` file does define `SECRET_KEY`.

## Interpretation

The compose file and `.env` are aligned, but the running containers were created earlier without the needed env value. Recreating the stack through the env-file aware helper scripts should clear the restart loop.
