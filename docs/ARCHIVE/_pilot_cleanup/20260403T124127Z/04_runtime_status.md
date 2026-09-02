# Runtime Status

Repository state at execution time:
- Working directory: `/home/munaim/srv/apps/pgsims`
- Branch: `main`
- Commit: `72e96cc40ab753fb98e75d01717e6aa908a5eab4`
- Working tree: dirty before this task with many unrelated user changes already present

Active deployment discovered:
- Compose project: `docker`
- Compose file: `/home/munaim/srv/apps/pgsims/docker/docker-compose.yml`
- Backend URL used for health verification: `http://127.0.0.1:8014/healthz/`
- Frontend URL used for UI verification: `http://127.0.0.1:8082`

Safety artifacts created before destructive work:
- active env copy
- compose file copy
- rendered compose config copy
- compose project listing
- compose service status
- docker ps snapshot
- backend health snapshot
- frontend HTTP snapshot
- full live database dump
- live schema dump
- schema table listing
- pre-cleanup row counts
- backend / worker / beat log tails

Current deployment status after conservative service recreate:
- `pgsims_backend`: healthy
- `pgsims_frontend`: healthy
- `pgsims_db`: healthy
- `pgsims_redis`: healthy
- `pgsims_worker`: running
- `pgsims_beat`: running

Health checks validated:
- Backend health response: `{"status":"healthy","checks":{"database":"ok","cache":"ok","celery":"ok"}}`
- Frontend root responded with HTTP `200`
- `admin` login still works

Important deployment constraint observed:
- The repository is not clean.
- To avoid deploying unrelated unreviewed user changes, services were recreated without a full image rebuild.
- Result: compose startup change is live, but new repo-only management commands are not present inside the running backend image yet.

