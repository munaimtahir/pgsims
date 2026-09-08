# Production deployment

Production checkout: `/home/munaim/srv/apps/pgsims`; Compose definition:
`docker/docker-compose.yml`. The backend image is not a source bind mount, so the backend was
rebuilt and restarted after pulling the pushed fixture support commit. The deployment introduced no
migration. Before restart, Django checks, migration consistency and migration plan passed; the
database container has `pg_dump` available for established recovery operations. Health at
`http://127.0.0.1:8014/healthz/` returned 200 after restart.

Rollback is a fast-forward-safe checkout to the preceding deployed commit followed by the same
backend image rebuild/restart. No production configuration, secrets or signing material changed.
