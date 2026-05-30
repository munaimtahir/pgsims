# PREFLIGHT — Backup Center Final Verification

Date (UTC): 2026-05-30

## Repo state (evidence)
- CWD: `/home/munaim/srv/apps/pgsims`
- Branch: `main`
- HEAD: `5861184352634d8a75b5709ae6e32c935d4126ed`
- `git log -1`: `5861184 chore(backup): gap closure and final verification`
- Working tree: clean (`git status --porcelain` empty)

## App status (docs)
- `docs/CURRENT_FINAL_STATE.md` reports Pilot Baseline v1.0 and a different “latest commit hash” (dated 2026-05-29T11:00:00Z). This file is currently out-of-sync with `HEAD` and will be updated in this sprint.

## Mandatory governance docs (availability)
- `docs/PROD_GATE_CLOSURE/00_README.md`: present and read (2026-04-23).
- `docs/ANTI_DRIFT_GUARDRAILS.md`: **missing** at expected path.
  - Found archived copy at `docs/ARCHIVE/ANTI_DRIFT_GUARDRAILS.md` (read for this session).
  - Action in this sprint: restore canonical path `docs/ANTI_DRIFT_GUARDRAILS.md` from the archived source to satisfy governance references.

## Framework & structure (audit)
- Backend: Django project in `backend/` (`backend/manage.py`, `backend/sims_project/settings.py`).
- Frontend: Next.js app in `frontend/` (`frontend/package.json`, Next `14.2.33`).
- Media root (backend): `backend/sims_project/settings.py` sets `MEDIA_ROOT = BASE_DIR / "media"`.
- Docker/Compose: compose files exist under `docker/` (e.g. `docker/docker-compose.yml`).

## Backup Center implementation (presence check)
Backend (present under `backend/sims/backup_center/`):
- `models.py`, `services.py`, `views.py`, `urls.py`, `admin.py`
- management commands: `management/commands/create_system_backup.py`, `validate_system_backup.py`, `restore_system_backup.py`
- tests: `tests.py`

Frontend (present):
- Page: `frontend/app/dashboard/utrmc/backup/page.tsx` (+ `page.test.tsx`)
- Components: `frontend/components/backup/BackupList.tsx`, `CreateBackupModal.tsx`, `RestoreModal.tsx`
- Entry link: `frontend/app/dashboard/utrmc/page.tsx` links to `/dashboard/utrmc/backup`

## Required commands to run (planned)
Runtime:
- `docker compose -f docker/docker-compose.yml ps`
- `docker compose -f docker/docker-compose.yml logs --tail=200`

Backend:
- `cd backend && python manage.py check`
- `cd backend && python manage.py showmigrations`
- `cd backend && python manage.py makemigrations --check --dry-run`

Frontend:
- `cd frontend && npm install`
- `cd frontend && npm run lint`
- `cd frontend && npm run typecheck`
- `cd frontend && npm run build`
- `cd frontend && npm run test`


## Runtime preflight outputs

### docker compose ps
NAME              IMAGE                COMMAND                  SERVICE    CREATED        STATUS                 PORTS
pgsims_backend    docker-backend       "sh -c 'python manag…"   backend    15 hours ago   Up 8 hours (healthy)   127.0.0.1:8014->8014/tcp
pgsims_beat       docker-beat          "celery -A sims_proj…"   beat       41 hours ago   Up 8 hours             8014/tcp
pgsims_db         postgres:15-alpine   "docker-entrypoint.s…"   db         15 hours ago   Up 8 hours (healthy)   5432/tcp
pgsims_frontend   docker-frontend      "docker-entrypoint.s…"   frontend   16 hours ago   Up 8 hours (healthy)   127.0.0.1:8082->3000/tcp
pgsims_redis      redis:7-alpine       "docker-entrypoint.s…"   redis      41 hours ago   Up 8 hours (healthy)   6379/tcp
pgsims_worker     docker-worker        "celery -A sims_proj…"   worker     41 hours ago   Up 8 hours             8014/tcp

### docker compose logs --tail=200
pgsims_frontend  |   ▲ Next.js 14.2.33
pgsims_frontend  |   - Local:        http://localhost:3000
pgsims_frontend  |   - Network:      http://0.0.0.0:3000
pgsims_frontend  | 
pgsims_frontend  |  ✓ Starting...
pgsims_frontend  |  ✓ Ready in 124ms
pgsims_frontend  |   ▲ Next.js 14.2.33
pgsims_frontend  |   - Local:        http://localhost:3000
pgsims_frontend  |   - Network:      http://0.0.0.0:3000
pgsims_frontend  | 
pgsims_frontend  |  ✓ Starting...
pgsims_frontend  |  ✓ Ready in 5.2s
pgsims_frontend  | TypeError: Cannot read properties of null (reading 'digest')
pgsims_frontend  |     at /app/node_modules/next/dist/compiled/next-server/app-page.runtime.prod.js:13:19722
pgsims_frontend  |     at AsyncLocalStorage.run (node:async_hooks:346:14)
pgsims_frontend  |     at e_ (/app/node_modules/next/dist/compiled/next-server/app-page.runtime.prod.js:12:141421)
pgsims_frontend  |     at /app/node_modules/next/dist/compiled/next-server/app-page.runtime.prod.js:12:138763
pgsims_frontend  |     at process.processTicksAndRejections (node:internal/process/task_queues:95:5)
pgsims_frontend  | TypeError: Cannot read properties of null (reading 'digest')
pgsims_frontend  |     at /app/node_modules/next/dist/compiled/next-server/app-page.runtime.prod.js:13:19722
pgsims_frontend  |     at AsyncLocalStorage.run (node:async_hooks:346:14)
pgsims_frontend  |     at e_ (/app/node_modules/next/dist/compiled/next-server/app-page.runtime.prod.js:12:141421)
pgsims_frontend  |     at /app/node_modules/next/dist/compiled/next-server/app-page.runtime.prod.js:12:138763
pgsims_frontend  |     at process.processTicksAndRejections (node:internal/process/task_queues:95:5)
pgsims_worker    |  
pgsims_worker    |  -------------- celery@5641a52dfb25 v5.6.3 (recovery)
pgsims_worker    | --- ***** ----- 
pgsims_worker    | -- ******* ---- Linux-6.17.0-1016-gcp-x86_64-with-glibc2.41 2026-05-29 05:14:21
pgsims_worker    | - *** --- * --- 
pgsims_worker    | - ** ---------- [config]
pgsims_worker    | - ** ---------- .> app:         sims:0x7b8b92d9c710
pgsims_worker    | - ** ---------- .> transport:   redis://redis:6379/1
pgsims_worker    | - ** ---------- .> results:     redis://redis:6379/1
pgsims_worker    | - *** --- * --- .> concurrency: 2 (prefork)
pgsims_worker    | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
pgsims_worker    | --- ***** ----- 
pgsims_worker    |  -------------- [queues]
pgsims_worker    |                 .> celery           exchange=celery(direct) key=celery
pgsims_worker    |                 
pgsims_worker    | 
pgsims_worker    | [tasks]
pgsims_worker    |   . sims_project.celery.debug_task
pgsims_worker    | 
pgsims_worker    | [2026-05-29 05:14:22,157: INFO/MainProcess] Connected to redis://redis:6379/1
pgsims_worker    | [2026-05-29 05:14:22,170: INFO/MainProcess] mingle: searching for neighbors
pgsims_worker    | [2026-05-29 05:14:23,189: INFO/MainProcess] mingle: all alone
pgsims_worker    | [2026-05-29 05:14:23,211: INFO/MainProcess] celery@5641a52dfb25 ready.
pgsims_worker    | [2026-05-30 04:00:00,757: INFO/MainProcess] Task celery.backend_cleanup[994818d6-c85d-4bee-8854-cf077525476c] received
pgsims_worker    | [2026-05-30 04:00:00,836: INFO/ForkPoolWorker-2] Task celery.backend_cleanup[994818d6-c85d-4bee-8854-cf077525476c] succeeded in 0.0593651060044067s: None
pgsims_worker    | 
pgsims_worker    | worker: Warm shutdown (MainProcess)
pgsims_worker    |  
pgsims_worker    |  -------------- celery@5641a52dfb25 v5.6.3 (recovery)
pgsims_worker    | --- ***** ----- 
pgsims_worker    | -- ******* ---- Linux-6.17.0-1018-gcp-x86_64-with-glibc2.41 2026-05-30 13:52:21
pgsims_worker    | - *** --- * --- 
pgsims_worker    | - ** ---------- [config]
pgsims_worker    | - ** ---------- .> app:         sims:0x7ef1ddec1ad0
pgsims_worker    | - ** ---------- .> transport:   redis://redis:6379/1
pgsims_worker    | - ** ---------- .> results:     redis://redis:6379/1
pgsims_worker    | - *** --- * --- .> concurrency: 2 (prefork)
pgsims_worker    | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
pgsims_worker    | --- ***** ----- 
pgsims_worker    |  -------------- [queues]
pgsims_worker    |                 .> celery           exchange=celery(direct) key=celery
pgsims_worker    |                 
pgsims_worker    | 
pgsims_worker    | [tasks]
pgsims_worker    |   . sims_project.celery.debug_task
pgsims_worker    | 
pgsims_worker    | [2026-05-30 13:52:22,204: INFO/MainProcess] Connected to redis://redis:6379/1
pgsims_worker    | [2026-05-30 13:52:22,212: INFO/MainProcess] mingle: searching for neighbors
pgsims_worker    | [2026-05-30 13:52:23,229: INFO/MainProcess] mingle: all alone
pgsims_worker    | [2026-05-30 13:52:23,259: INFO/MainProcess] celery@5641a52dfb25 ready.
pgsims_redis     | 1:M 30 May 2026 17:11:03.530 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 17:11:03.531 * Background saving started by pid 7243
pgsims_redis     | 7243:C 30 May 2026 17:11:03.537 * DB saved on disk
pgsims_redis     | 7243:C 30 May 2026 17:11:03.538 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 17:11:03.632 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 17:18:49.846 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 17:18:49.847 * Background saving started by pid 7524
pgsims_redis     | 7524:C 30 May 2026 17:18:49.853 * DB saved on disk
pgsims_redis     | 7524:C 30 May 2026 17:18:49.854 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 17:18:49.949 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 17:26:36.074 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 17:26:36.075 * Background saving started by pid 7807
pgsims_redis     | 7807:C 30 May 2026 17:26:36.081 * DB saved on disk
pgsims_redis     | 7807:C 30 May 2026 17:26:36.081 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 17:26:36.176 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 17:33:54.254 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 17:33:54.255 * Background saving started by pid 8069
pgsims_redis     | 8069:C 30 May 2026 17:33:54.261 * DB saved on disk
pgsims_redis     | 8069:C 30 May 2026 17:33:54.262 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 17:33:54.356 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 17:42:08.711 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 17:42:08.712 * Background saving started by pid 8367
pgsims_redis     | 8367:C 30 May 2026 17:42:08.718 * DB saved on disk
pgsims_redis     | 8367:C 30 May 2026 17:42:08.719 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 17:42:08.813 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 17:49:55.028 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 17:49:55.029 * Background saving started by pid 8653
pgsims_redis     | 8653:C 30 May 2026 17:49:55.035 * DB saved on disk
pgsims_redis     | 8653:C 30 May 2026 17:49:55.036 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 17:49:55.130 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 17:57:41.231 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 17:57:41.232 * Background saving started by pid 8931
pgsims_redis     | 8931:C 30 May 2026 17:57:41.238 * DB saved on disk
pgsims_redis     | 8931:C 30 May 2026 17:57:41.238 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 17:57:41.333 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 18:05:27.578 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 18:05:27.579 * Background saving started by pid 9216
pgsims_redis     | 9216:C 30 May 2026 18:05:27.585 * DB saved on disk
pgsims_redis     | 9216:C 30 May 2026 18:05:27.586 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 18:05:27.679 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 18:13:13.809 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 18:13:13.809 * Background saving started by pid 9494
pgsims_redis     | 9494:C 30 May 2026 18:13:13.815 * DB saved on disk
pgsims_redis     | 9494:C 30 May 2026 18:13:13.816 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 18:13:13.911 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 18:21:00.145 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 18:21:00.146 * Background saving started by pid 9773
pgsims_redis     | 9773:C 30 May 2026 18:21:00.152 * DB saved on disk
pgsims_redis     | 9773:C 30 May 2026 18:21:00.152 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 18:21:00.247 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 18:28:46.491 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 18:28:46.491 * Background saving started by pid 10058
pgsims_redis     | 10058:C 30 May 2026 18:28:46.497 * DB saved on disk
pgsims_redis     | 10058:C 30 May 2026 18:28:46.498 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 18:28:46.592 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 18:36:32.737 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 18:36:32.738 * Background saving started by pid 10336
pgsims_redis     | 10336:C 30 May 2026 18:36:32.744 * DB saved on disk
pgsims_redis     | 10336:C 30 May 2026 18:36:32.745 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 18:36:32.839 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 18:44:18.968 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 18:44:18.969 * Background saving started by pid 10614
pgsims_redis     | 10614:C 30 May 2026 18:44:18.974 * DB saved on disk
pgsims_redis     | 10614:C 30 May 2026 18:44:18.975 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 18:44:19.070 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 18:52:05.305 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 18:52:05.306 * Background saving started by pid 10898
pgsims_redis     | 10898:C 30 May 2026 18:52:05.312 * DB saved on disk
pgsims_redis     | 10898:C 30 May 2026 18:52:05.312 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 18:52:05.407 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 18:59:51.542 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 18:59:51.543 * Background saving started by pid 11176
pgsims_redis     | 11176:C 30 May 2026 18:59:51.549 * DB saved on disk
pgsims_redis     | 11176:C 30 May 2026 18:59:51.550 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 18:59:51.644 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 19:07:15.173 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 19:07:15.174 * Background saving started by pid 11442
pgsims_redis     | 11442:C 30 May 2026 19:07:15.209 * DB saved on disk
pgsims_redis     | 11442:C 30 May 2026 19:07:15.210 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 19:07:15.275 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 19:14:54.023 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 19:14:54.023 * Background saving started by pid 11719
pgsims_redis     | 11719:C 30 May 2026 19:14:54.029 * DB saved on disk
pgsims_redis     | 11719:C 30 May 2026 19:14:54.030 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 19:14:54.125 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 19:22:40.330 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 19:22:40.331 * Background saving started by pid 12001
pgsims_redis     | 12001:C 30 May 2026 19:22:40.337 * DB saved on disk
pgsims_redis     | 12001:C 30 May 2026 19:22:40.338 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 19:22:40.432 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 19:30:25.618 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 19:30:25.619 * Background saving started by pid 12281
pgsims_redis     | 12281:C 30 May 2026 19:30:25.626 * DB saved on disk
pgsims_redis     | 12281:C 30 May 2026 19:30:25.626 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 19:30:25.721 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 19:38:11.928 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 19:38:11.929 * Background saving started by pid 12568
pgsims_redis     | 12568:C 30 May 2026 19:38:11.934 * DB saved on disk
pgsims_redis     | 12568:C 30 May 2026 19:38:11.935 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 19:38:12.029 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 19:45:58.219 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 19:45:58.220 * Background saving started by pid 12846
pgsims_redis     | 12846:C 30 May 2026 19:45:58.226 * DB saved on disk
pgsims_redis     | 12846:C 30 May 2026 19:45:58.227 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 19:45:58.322 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 19:53:44.410 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 19:53:44.411 * Background saving started by pid 13131
pgsims_redis     | 13131:C 30 May 2026 19:53:44.417 * DB saved on disk
pgsims_redis     | 13131:C 30 May 2026 19:53:44.418 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 19:53:44.512 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 20:01:30.713 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 20:01:30.714 * Background saving started by pid 13409
pgsims_redis     | 13409:C 30 May 2026 20:01:30.720 * DB saved on disk
pgsims_redis     | 13409:C 30 May 2026 20:01:30.720 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 20:01:30.814 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 20:08:55.733 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 20:08:55.733 * Background saving started by pid 13677
pgsims_redis     | 13677:C 30 May 2026 20:08:55.739 * DB saved on disk
pgsims_redis     | 13677:C 30 May 2026 20:08:55.740 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 20:08:55.835 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 20:16:33.268 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 20:16:33.269 * Background saving started by pid 13955
pgsims_redis     | 13955:C 30 May 2026 20:16:33.275 * DB saved on disk
pgsims_redis     | 13955:C 30 May 2026 20:16:33.275 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 20:16:33.370 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 20:24:18.488 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 20:24:18.489 * Background saving started by pid 14233
pgsims_redis     | 14233:C 30 May 2026 20:24:18.494 * DB saved on disk
pgsims_redis     | 14233:C 30 May 2026 20:24:18.495 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 20:24:18.590 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 20:32:04.816 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 20:32:04.817 * Background saving started by pid 14513
pgsims_redis     | 14513:C 30 May 2026 20:32:04.823 * DB saved on disk
pgsims_redis     | 14513:C 30 May 2026 20:32:04.823 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 20:32:04.918 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 20:39:51.060 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 20:39:51.060 * Background saving started by pid 14794
pgsims_redis     | 14794:C 30 May 2026 20:39:51.066 * DB saved on disk
pgsims_redis     | 14794:C 30 May 2026 20:39:51.067 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 20:39:51.161 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 20:47:37.395 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 20:47:37.396 * Background saving started by pid 15070
pgsims_redis     | 15070:C 30 May 2026 20:47:37.402 * DB saved on disk
pgsims_redis     | 15070:C 30 May 2026 20:47:37.403 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 20:47:37.497 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 20:55:23.596 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 20:55:23.596 * Background saving started by pid 15347
pgsims_redis     | 15347:C 30 May 2026 20:55:23.604 * DB saved on disk
pgsims_redis     | 15347:C 30 May 2026 20:55:23.604 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 20:55:23.697 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 21:03:09.923 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 21:03:09.924 * Background saving started by pid 15629
pgsims_redis     | 15629:C 30 May 2026 21:03:09.930 * DB saved on disk
pgsims_redis     | 15629:C 30 May 2026 21:03:09.930 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 21:03:10.025 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 21:10:56.147 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 21:10:56.148 * Background saving started by pid 15907
pgsims_redis     | 15907:C 30 May 2026 21:10:56.154 * DB saved on disk
pgsims_redis     | 15907:C 30 May 2026 21:10:56.154 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 21:10:56.249 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 21:18:42.472 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 21:18:42.473 * Background saving started by pid 16186
pgsims_redis     | 16186:C 30 May 2026 21:18:42.479 * DB saved on disk
pgsims_redis     | 16186:C 30 May 2026 21:18:42.480 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 21:18:42.574 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 21:26:28.693 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 21:26:28.693 * Background saving started by pid 16472
pgsims_redis     | 16472:C 30 May 2026 21:26:28.699 * DB saved on disk
pgsims_redis     | 16472:C 30 May 2026 21:26:28.700 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 21:26:28.795 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 21:33:56.540 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 21:33:56.541 * Background saving started by pid 16738
pgsims_redis     | 16738:C 30 May 2026 21:33:56.547 * DB saved on disk
pgsims_redis     | 16738:C 30 May 2026 21:33:56.547 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 21:33:56.642 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 21:41:31.234 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 21:41:31.234 * Background saving started by pid 17010
pgsims_redis     | 17010:C 30 May 2026 21:41:31.241 * DB saved on disk
pgsims_redis     | 17010:C 30 May 2026 21:41:31.242 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 21:41:31.335 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 21:48:16.152 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 21:48:16.152 * Background saving started by pid 17254
pgsims_redis     | 17254:C 30 May 2026 21:48:16.158 * DB saved on disk
pgsims_redis     | 17254:C 30 May 2026 21:48:16.159 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 21:48:16.254 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 21:54:59.423 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 21:54:59.424 * Background saving started by pid 17499
pgsims_redis     | 17499:C 30 May 2026 21:54:59.431 * DB saved on disk
pgsims_redis     | 17499:C 30 May 2026 21:54:59.431 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 21:54:59.530 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 22:02:46.143 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 22:02:46.144 * Background saving started by pid 17779
pgsims_redis     | 17779:C 30 May 2026 22:02:46.153 * DB saved on disk
pgsims_redis     | 17779:C 30 May 2026 22:02:46.154 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 22:02:46.246 * Background saving terminated with success
pgsims_redis     | 1:M 30 May 2026 22:10:36.975 * 100 changes in 300 seconds. Saving...
pgsims_redis     | 1:M 30 May 2026 22:10:36.976 * Background saving started by pid 18065
pgsims_redis     | 18065:C 30 May 2026 22:10:36.982 * DB saved on disk
pgsims_redis     | 18065:C 30 May 2026 22:10:36.983 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
pgsims_redis     | 1:M 30 May 2026 22:10:37.078 * Background saving terminated with success
pgsims_backend   | [WARNING] 2026-05-30 20:27:57,070 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 20:28:28,165 sims.performance Slow request: GET /healthz/ took 1024ms
pgsims_backend   | [WARNING] 2026-05-30 20:28:59,254 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:29:30,333 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:30:01,412 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:30:32,497 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:31:03,596 sims.performance Slow request: GET /healthz/ took 1025ms
pgsims_backend   | [WARNING] 2026-05-30 20:31:34,682 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:32:05,760 sims.performance Slow request: GET /healthz/ took 1008ms
pgsims_backend   | [WARNING] 2026-05-30 20:32:36,838 sims.performance Slow request: GET /healthz/ took 1008ms
pgsims_backend   | [WARNING] 2026-05-30 20:33:07,933 sims.performance Slow request: GET /healthz/ took 1023ms
pgsims_backend   | [WARNING] 2026-05-30 20:33:39,014 sims.performance Slow request: GET /healthz/ took 1012ms
pgsims_backend   | [WARNING] 2026-05-30 20:34:10,095 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:34:41,181 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:35:12,260 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 20:35:43,342 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 20:36:14,426 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:36:45,509 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:37:16,594 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:37:47,676 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:38:18,761 sims.performance Slow request: GET /healthz/ took 1013ms
pgsims_backend   | [WARNING] 2026-05-30 20:38:49,844 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:39:20,927 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 20:39:52,031 sims.performance Slow request: GET /healthz/ took 1029ms
pgsims_backend   | [WARNING] 2026-05-30 20:40:23,111 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 20:40:54,191 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:41:25,286 sims.performance Slow request: GET /healthz/ took 1024ms
pgsims_backend   | [WARNING] 2026-05-30 20:41:56,370 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 20:42:27,452 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:42:58,536 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:43:29,636 sims.performance Slow request: GET /healthz/ took 1025ms
pgsims_backend   | [WARNING] 2026-05-30 20:44:00,716 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 20:44:31,801 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:45:02,881 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 20:45:33,961 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:46:05,044 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:46:36,125 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 20:47:07,221 sims.performance Slow request: GET /healthz/ took 1024ms
pgsims_backend   | [WARNING] 2026-05-30 20:47:38,303 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 20:48:09,382 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:48:40,466 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:49:11,553 sims.performance Slow request: GET /healthz/ took 1012ms
pgsims_backend   | [WARNING] 2026-05-30 20:49:42,638 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 20:50:13,733 sims.performance Slow request: GET /healthz/ took 1023ms
pgsims_backend   | [WARNING] 2026-05-30 20:50:44,813 sims.performance Slow request: GET /healthz/ took 1008ms
pgsims_backend   | [WARNING] 2026-05-30 20:51:15,895 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 20:51:46,986 sims.performance Slow request: GET /healthz/ took 1022ms
pgsims_backend   | [WARNING] 2026-05-30 20:52:18,070 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 20:52:49,156 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:53:20,240 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:53:51,322 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 20:54:22,405 sims.performance Slow request: GET /healthz/ took 1014ms
pgsims_backend   | [WARNING] 2026-05-30 20:54:53,488 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 20:55:24,568 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 20:55:55,648 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 20:56:26,731 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 20:56:57,813 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:57:28,913 sims.performance Slow request: GET /healthz/ took 1024ms
pgsims_backend   | [WARNING] 2026-05-30 20:57:59,997 sims.performance Slow request: GET /healthz/ took 1014ms
pgsims_backend   | [WARNING] 2026-05-30 20:58:31,080 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 20:59:02,175 sims.performance Slow request: GET /healthz/ took 1024ms
pgsims_backend   | [WARNING] 2026-05-30 20:59:33,258 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:00:04,345 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 21:00:35,424 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:01:06,503 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:01:37,582 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:02:08,682 sims.performance Slow request: GET /healthz/ took 1025ms
pgsims_backend   | [WARNING] 2026-05-30 21:02:39,761 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:03:10,852 sims.performance Slow request: GET /healthz/ took 1015ms
pgsims_backend   | [WARNING] 2026-05-30 21:03:41,945 sims.performance Slow request: GET /healthz/ took 1024ms
pgsims_backend   | [WARNING] 2026-05-30 21:04:13,029 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:04:44,116 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 21:05:15,199 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:05:46,281 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:06:17,365 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 21:06:48,446 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:07:19,527 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:07:50,605 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:08:21,689 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:08:52,774 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:09:23,868 sims.performance Slow request: GET /healthz/ took 1023ms
pgsims_backend   | [WARNING] 2026-05-30 21:09:54,953 sims.performance Slow request: GET /healthz/ took 1013ms
pgsims_backend   | [WARNING] 2026-05-30 21:10:26,044 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:10:57,147 sims.performance Slow request: GET /healthz/ took 1024ms
pgsims_backend   | [WARNING] 2026-05-30 21:11:28,226 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:11:59,312 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:12:30,407 sims.performance Slow request: GET /healthz/ took 1024ms
pgsims_backend   | [WARNING] 2026-05-30 21:13:01,489 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:13:32,567 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:14:03,647 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:14:34,733 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 21:15:05,814 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:15:36,919 sims.performance Slow request: GET /healthz/ took 1023ms
pgsims_backend   | [WARNING] 2026-05-30 21:16:08,001 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:16:39,089 sims.performance Slow request: GET /healthz/ took 1012ms
pgsims_backend   | [WARNING] 2026-05-30 21:17:10,173 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:17:41,252 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 21:18:12,337 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:18:43,418 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:19:14,504 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:19:45,586 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:20:16,669 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:20:47,764 sims.performance Slow request: GET /healthz/ took 1023ms
pgsims_backend   | [WARNING] 2026-05-30 21:21:18,848 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:21:49,928 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:22:21,008 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:22:52,102 sims.performance Slow request: GET /healthz/ took 1024ms
pgsims_backend   | [WARNING] 2026-05-30 21:23:23,182 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:23:54,265 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:24:25,348 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:24:56,431 sims.performance Slow request: GET /healthz/ took 1013ms
pgsims_backend   | [WARNING] 2026-05-30 21:25:27,533 sims.performance Slow request: GET /healthz/ took 1025ms
pgsims_backend   | [WARNING] 2026-05-30 21:25:58,613 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:26:29,698 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 21:27:00,783 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:27:31,867 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:28:02,948 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:28:34,030 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:29:05,140 sims.performance Slow request: GET /healthz/ took 1034ms
pgsims_backend   | [WARNING] 2026-05-30 21:29:36,218 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:30:07,297 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:30:38,382 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 21:31:09,462 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:31:40,547 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:32:11,627 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:32:42,709 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 21:33:13,812 sims.performance Slow request: GET /healthz/ took 1027ms
pgsims_backend   | [WARNING] 2026-05-30 21:33:44,893 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:34:15,989 sims.performance Slow request: GET /healthz/ took 1024ms
pgsims_backend   | [WARNING] 2026-05-30 21:34:47,069 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:35:18,151 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:35:49,248 sims.performance Slow request: GET /healthz/ took 1024ms
pgsims_backend   | [WARNING] 2026-05-30 21:36:20,370 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:36:51,453 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:37:22,536 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:37:53,617 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:38:24,700 sims.performance Slow request: GET /healthz/ took 1013ms
pgsims_backend   | [WARNING] 2026-05-30 21:38:55,804 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 21:39:26,885 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:39:57,970 sims.performance Slow request: GET /healthz/ took 1013ms
pgsims_backend   | [WARNING] 2026-05-30 21:40:29,051 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:41:00,136 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:41:31,235 sims.performance Slow request: GET /healthz/ took 1026ms
pgsims_backend   | [WARNING] 2026-05-30 21:42:02,324 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:42:33,408 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:43:04,498 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 21:43:35,634 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:44:06,735 sims.performance Slow request: GET /healthz/ took 1025ms
pgsims_backend   | [WARNING] 2026-05-30 21:44:37,898 sims.performance Slow request: GET /healthz/ took 1013ms
pgsims_backend   | [WARNING] 2026-05-30 21:45:09,030 sims.performance Slow request: GET /healthz/ took 1020ms
pgsims_backend   | [WARNING] 2026-05-30 21:45:40,317 sims.performance Slow request: GET /healthz/ took 1186ms
pgsims_backend   | [WARNING] 2026-05-30 21:46:11,608 sims.performance Slow request: GET /healthz/ took 1031ms
pgsims_backend   | [WARNING] 2026-05-30 21:46:42,739 sims.performance Slow request: GET /healthz/ took 1016ms
pgsims_backend   | [WARNING] 2026-05-30 21:47:13,870 sims.performance Slow request: GET /healthz/ took 1033ms
pgsims_backend   | [WARNING] 2026-05-30 21:47:44,963 sims.performance Slow request: GET /healthz/ took 1014ms
pgsims_backend   | [WARNING] 2026-05-30 21:48:16,052 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:48:47,189 sims.performance Slow request: GET /healthz/ took 1012ms
pgsims_backend   | [WARNING] 2026-05-30 21:49:18,310 sims.performance Slow request: GET /healthz/ took 1012ms
pgsims_backend   | [WARNING] 2026-05-30 21:49:49,406 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:50:20,495 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:50:51,577 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:51:22,665 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:51:53,787 sims.performance Slow request: GET /healthz/ took 1012ms
pgsims_backend   | [WARNING] 2026-05-30 21:52:24,892 sims.performance Slow request: GET /healthz/ took 1016ms
pgsims_backend   | [WARNING] 2026-05-30 21:52:55,976 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:53:27,068 sims.performance Slow request: GET /healthz/ took 1014ms
pgsims_backend   | [WARNING] 2026-05-30 21:53:58,153 sims.performance Slow request: GET /healthz/ took 1008ms
pgsims_backend   | [WARNING] 2026-05-30 21:54:29,236 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:55:00,336 sims.performance Slow request: GET /healthz/ took 1025ms
pgsims_backend   | [WARNING] 2026-05-30 21:55:31,424 sims.performance Slow request: GET /healthz/ took 1012ms
pgsims_backend   | [WARNING] 2026-05-30 21:56:02,554 sims.performance Slow request: GET /healthz/ took 1042ms
pgsims_backend   | [WARNING] 2026-05-30 21:56:33,727 sims.performance Slow request: GET /healthz/ took 1027ms
pgsims_backend   | [WARNING] 2026-05-30 21:57:05,003 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:57:36,120 sims.performance Slow request: GET /healthz/ took 1033ms
pgsims_backend   | [WARNING] 2026-05-30 21:58:07,203 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 21:58:38,287 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:59:09,370 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 21:59:40,473 sims.performance Slow request: GET /healthz/ took 1027ms
pgsims_backend   | [WARNING] 2026-05-30 22:00:11,562 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 22:00:42,649 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 22:01:13,735 sims.performance Slow request: GET /healthz/ took 1013ms
pgsims_backend   | [WARNING] 2026-05-30 22:01:44,816 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 22:02:15,946 sims.performance Slow request: GET /healthz/ took 1012ms
pgsims_backend   | [WARNING] 2026-05-30 22:02:47,067 sims.performance Slow request: GET /healthz/ took 1014ms
pgsims_backend   | [WARNING] 2026-05-30 22:03:18,154 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 22:03:49,251 sims.performance Slow request: GET /healthz/ took 1011ms
pgsims_backend   | [WARNING] 2026-05-30 22:04:20,332 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 22:04:51,418 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 22:05:22,497 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 22:05:53,581 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend   | [WARNING] 2026-05-30 22:06:24,678 sims.performance Slow request: GET /healthz/ took 1024ms
pgsims_backend   | [WARNING] 2026-05-30 22:06:55,772 sims.performance Slow request: GET /healthz/ took 1012ms
pgsims_backend   | [WARNING] 2026-05-30 22:07:26,869 sims.performance Slow request: GET /healthz/ took 1026ms
pgsims_backend   | [WARNING] 2026-05-30 22:07:57,953 sims.performance Slow request: GET /healthz/ took 1012ms
pgsims_backend   | [WARNING] 2026-05-30 22:08:29,052 sims.performance Slow request: GET /healthz/ took 1024ms
pgsims_backend   | [WARNING] 2026-05-30 22:09:00,134 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 22:09:31,221 sims.performance Slow request: GET /healthz/ took 1012ms
pgsims_backend   | [WARNING] 2026-05-30 22:10:02,305 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend   | [WARNING] 2026-05-30 22:10:33,399 sims.performance Slow request: GET /healthz/ took 1024ms
pgsims_backend   | [WARNING] 2026-05-30 22:11:04,489 sims.performance Slow request: GET /healthz/ took 1014ms
pgsims_db        | 2026-05-30 21:38:42.738 UTC [20326] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:38:52.806 UTC [20334] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:39:02.867 UTC [20341] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:39:12.926 UTC [20348] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:39:22.989 UTC [20355] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:39:33.052 UTC [20362] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:39:43.115 UTC [20369] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:39:53.177 UTC [20377] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:40:03.242 UTC [20384] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:40:13.306 UTC [20391] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:40:23.366 UTC [20398] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:40:33.429 UTC [20405] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:40:43.497 UTC [20412] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:40:53.558 UTC [20420] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:41:03.624 UTC [20427] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:41:13.688 UTC [20434] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:41:23.748 UTC [20441] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:41:33.809 UTC [20449] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:41:43.873 UTC [20456] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:41:53.934 UTC [20464] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:42:03.995 UTC [20471] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:42:14.054 UTC [20478] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:42:24.113 UTC [20485] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:42:34.177 UTC [20492] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:42:44.240 UTC [20500] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:42:54.299 UTC [20508] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:43:04.365 UTC [20515] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:43:14.430 UTC [20522] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:43:24.490 UTC [20529] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:43:34.600 UTC [20536] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:43:44.666 UTC [20544] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:43:54.730 UTC [20551] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:44:04.804 UTC [20558] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:44:14.976 UTC [20566] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:44:25.047 UTC [20573] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:44:35.180 UTC [20580] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:44:45.286 UTC [20587] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:44:55.364 UTC [20594] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:45:05.454 UTC [20602] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:45:15.545 UTC [20608] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:45:25.660 UTC [20615] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:45:35.742 UTC [20623] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:45:45.962 UTC [20631] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:45:56.107 UTC [20639] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:46:06.275 UTC [20646] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:46:16.390 UTC [20653] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:46:26.451 UTC [20660] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:46:29.202 UTC [34] LOG:  checkpoint starting: time
pgsims_db        | 2026-05-30 21:46:32.935 UTC [34] LOG:  checkpoint complete: wrote 38 buffers (0.2%); 0 WAL file(s) added, 0 removed, 0 recycled; write=3.717 s, sync=0.007 s, total=3.733 s; sync files=37, longest=0.004 s, average=0.001 s; distance=81 kB, estimate=265 kB
pgsims_db        | 2026-05-30 21:46:36.520 UTC [20667] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:46:46.591 UTC [20675] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:46:56.679 UTC [20682] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:47:06.742 UTC [20689] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:47:16.808 UTC [20697] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:47:26.869 UTC [20704] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:47:37.006 UTC [20711] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:47:47.080 UTC [20719] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:47:57.152 UTC [20726] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:48:07.215 UTC [20733] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:48:17.280 UTC [20740] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:48:27.342 UTC [20747] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:48:37.427 UTC [20754] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:48:47.500 UTC [20763] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:48:57.561 UTC [20770] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:49:07.643 UTC [20777] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:49:17.723 UTC [20785] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:49:27.796 UTC [20793] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:49:37.862 UTC [20800] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:49:47.925 UTC [20808] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:49:57.984 UTC [20815] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:50:08.046 UTC [20822] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:50:18.107 UTC [20829] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:50:28.193 UTC [20836] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:50:38.260 UTC [20843] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:50:48.325 UTC [20851] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:50:58.390 UTC [20858] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:51:08.449 UTC [20865] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:51:18.519 UTC [20872] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:51:28.587 UTC [20879] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:51:30.035 UTC [34] LOG:  checkpoint starting: time
pgsims_db        | 2026-05-30 21:51:38.656 UTC [20886] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:51:38.783 UTC [34] LOG:  checkpoint complete: wrote 89 buffers (0.5%); 0 WAL file(s) added, 0 removed, 0 recycled; write=8.732 s, sync=0.007 s, total=8.749 s; sync files=83, longest=0.003 s, average=0.001 s; distance=150 kB, estimate=254 kB
pgsims_db        | 2026-05-30 21:51:48.726 UTC [20894] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:51:58.793 UTC [20901] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:52:08.858 UTC [20908] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:52:18.923 UTC [20915] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:52:28.985 UTC [20922] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:52:39.051 UTC [20930] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:52:49.118 UTC [20938] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:52:59.184 UTC [20946] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:53:09.261 UTC [20953] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:53:19.322 UTC [20960] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:53:29.381 UTC [20967] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:53:39.442 UTC [20974] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:53:49.511 UTC [20982] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:53:59.583 UTC [20989] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:54:09.649 UTC [20996] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:54:19.718 UTC [21003] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:54:29.786 UTC [21010] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:54:39.868 UTC [21017] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:54:49.932 UTC [21025] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:54:59.993 UTC [21033] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:55:10.052 UTC [21040] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:55:20.112 UTC [21047] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:55:30.175 UTC [21055] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:55:40.238 UTC [21062] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:55:50.305 UTC [21070] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:56:00.368 UTC [21077] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:56:10.429 UTC [21085] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:56:20.573 UTC [21092] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:56:30.674 UTC [21099] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:56:40.750 UTC [21106] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:56:50.840 UTC [21114] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:57:00.906 UTC [21121] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:57:10.970 UTC [21128] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:57:21.031 UTC [21135] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:57:31.104 UTC [21142] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:57:41.170 UTC [21150] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:57:51.235 UTC [21158] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:58:01.296 UTC [21165] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:58:11.359 UTC [21172] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:58:21.446 UTC [21179] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:58:31.509 UTC [21186] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:58:41.573 UTC [21193] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:58:51.636 UTC [21201] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:59:01.696 UTC [21208] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:59:11.761 UTC [21216] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:59:21.823 UTC [21223] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:59:31.887 UTC [21230] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:59:41.946 UTC [21239] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 21:59:52.011 UTC [21247] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:00:02.081 UTC [21253] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:00:12.147 UTC [21260] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:00:22.209 UTC [21268] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:00:32.275 UTC [21275] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:00:42.338 UTC [21282] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:00:52.403 UTC [21290] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:01:02.465 UTC [21297] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:01:12.529 UTC [21304] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:01:22.591 UTC [21311] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:01:32.653 UTC [21318] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:01:42.712 UTC [21325] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:01:52.775 UTC [21333] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:02:02.838 UTC [21340] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:02:12.920 UTC [21347] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:02:22.995 UTC [21354] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:02:33.075 UTC [21361] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:02:43.170 UTC [21369] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:02:53.253 UTC [21377] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:03:03.332 UTC [21384] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:03:13.400 UTC [21391] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:03:23.461 UTC [21398] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:03:33.525 UTC [21405] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:03:43.585 UTC [21412] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:03:53.649 UTC [21420] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:04:03.713 UTC [21427] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:04:13.773 UTC [21434] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:04:23.834 UTC [21441] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:04:33.894 UTC [21448] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:04:43.954 UTC [21455] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:04:54.017 UTC [21463] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:05:04.082 UTC [21470] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:05:14.146 UTC [21477] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:05:24.209 UTC [21484] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:05:34.271 UTC [21491] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:05:44.332 UTC [21498] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:05:54.398 UTC [21506] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:06:04.458 UTC [21513] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:06:14.521 UTC [21520] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:06:24.580 UTC [21528] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:06:34.644 UTC [21535] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:06:44.704 UTC [21542] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:06:54.776 UTC [21550] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:07:04.846 UTC [21557] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:07:14.905 UTC [21564] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:07:24.964 UTC [21571] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:07:35.026 UTC [21579] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:07:45.092 UTC [21587] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:07:55.154 UTC [21595] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:08:05.213 UTC [21602] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:08:15.270 UTC [21609] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:08:25.338 UTC [21616] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:08:35.399 UTC [21624] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:08:45.466 UTC [21631] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:08:55.530 UTC [21639] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:09:05.598 UTC [21646] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:09:15.664 UTC [21653] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:09:25.726 UTC [21660] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:09:35.789 UTC [21667] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:09:45.848 UTC [21675] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:09:55.909 UTC [21682] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:10:05.973 UTC [21689] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:10:16.035 UTC [21696] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:10:26.094 UTC [21703] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:10:36.157 UTC [21711] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:10:46.220 UTC [21719] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:10:56.281 UTC [21726] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:11:06.344 UTC [21733] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:11:16.410 UTC [21740] FATAL:  database "sims_user" does not exist
pgsims_db        | 2026-05-30 22:11:26.474 UTC [21747] FATAL:  database "sims_user" does not exist
pgsims_beat      | 	This probably means the server terminated abnormally
pgsims_beat      | 	before or while processing the request.
pgsims_beat      | 
pgsims_beat      | [2026-05-30 06:43:31,926: ERROR/MainProcess] Database gave error: OperationalError('server closed the connection unexpectedly\n\tThis probably means the server terminated abnormally\n\tbefore or while processing the request.\n')
pgsims_beat      | Traceback (most recent call last):
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
pgsims_beat      |     return self.cursor.execute(sql, params)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      | psycopg2.OperationalError: server closed the connection unexpectedly
pgsims_beat      | 	This probably means the server terminated abnormally
pgsims_beat      | 	before or while processing the request.
pgsims_beat      | 
pgsims_beat      | 
pgsims_beat      | The above exception was the direct cause of the following exception:
pgsims_beat      | 
pgsims_beat      | Traceback (most recent call last):
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django_celery_beat/schedulers.py", line 421, in schedule_changed
pgsims_beat      |     last, ts = self._last_timestamp, self.Changes.last_change()
pgsims_beat      |                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django_celery_beat/models.py", line 427, in last_change
pgsims_beat      |     return cls.objects.get(ident=1).last_update
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
pgsims_beat      |     return getattr(self.get_queryset(), name)(*args, **kwargs)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 635, in get
pgsims_beat      |     num = len(clone)
pgsims_beat      |           ^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 382, in __len__
pgsims_beat      |     self._fetch_all()
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 1886, in _fetch_all
pgsims_beat      |     self._result_cache = list(self._iterable_class(self))
pgsims_beat      |                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 93, in __iter__
pgsims_beat      |     results = compiler.execute_sql(
pgsims_beat      |               ^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1562, in execute_sql
pgsims_beat      |     cursor.execute(sql, params)
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
pgsims_beat      |     return self._execute_with_wrappers(
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
pgsims_beat      |     return executor(sql, params, many, context)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
pgsims_beat      |     with self.db.wrap_database_errors:
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
pgsims_beat      |     raise dj_exc_value.with_traceback(traceback) from exc_value
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
pgsims_beat      |     return self.cursor.execute(sql, params)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      | django.db.utils.OperationalError: server closed the connection unexpectedly
pgsims_beat      | 	This probably means the server terminated abnormally
pgsims_beat      | 	before or while processing the request.
pgsims_beat      | 
pgsims_beat      | [2026-05-30 06:43:36,949: ERROR/MainProcess] Database gave error: OperationalError('could not translate host name "db" to address: Temporary failure in name resolution\n')
pgsims_beat      | Traceback (most recent call last):
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 288, in ensure_connection
pgsims_beat      |     self.connect()
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
pgsims_beat      |     return func(*args, **kwargs)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 269, in connect
pgsims_beat      |     self.connection = self.get_new_connection(conn_params)
pgsims_beat      |                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
pgsims_beat      |     return func(*args, **kwargs)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/postgresql/base.py", line 275, in get_new_connection
pgsims_beat      |     connection = self.Database.connect(**conn_params)
pgsims_beat      |                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
pgsims_beat      |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      | psycopg2.OperationalError: could not translate host name "db" to address: Temporary failure in name resolution
pgsims_beat      | 
pgsims_beat      | 
pgsims_beat      | The above exception was the direct cause of the following exception:
pgsims_beat      | 
pgsims_beat      | Traceback (most recent call last):
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django_celery_beat/schedulers.py", line 421, in schedule_changed
pgsims_beat      |     last, ts = self._last_timestamp, self.Changes.last_change()
pgsims_beat      |                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django_celery_beat/models.py", line 427, in last_change
pgsims_beat      |     return cls.objects.get(ident=1).last_update
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
pgsims_beat      |     return getattr(self.get_queryset(), name)(*args, **kwargs)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 635, in get
pgsims_beat      |     num = len(clone)
pgsims_beat      |           ^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 382, in __len__
pgsims_beat      |     self._fetch_all()
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 1886, in _fetch_all
pgsims_beat      |     self._result_cache = list(self._iterable_class(self))
pgsims_beat      |                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 93, in __iter__
pgsims_beat      |     results = compiler.execute_sql(
pgsims_beat      |               ^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1560, in execute_sql
pgsims_beat      |     cursor = self.connection.cursor()
pgsims_beat      |              ^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
pgsims_beat      |     return func(*args, **kwargs)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 329, in cursor
pgsims_beat      |     return self._cursor()
pgsims_beat      |            ^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 305, in _cursor
pgsims_beat      |     self.ensure_connection()
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
pgsims_beat      |     return func(*args, **kwargs)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 287, in ensure_connection
pgsims_beat      |     with self.wrap_database_errors:
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
pgsims_beat      |     raise dj_exc_value.with_traceback(traceback) from exc_value
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 288, in ensure_connection
pgsims_beat      |     self.connect()
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
pgsims_beat      |     return func(*args, **kwargs)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/base/base.py", line 269, in connect
pgsims_beat      |     self.connection = self.get_new_connection(conn_params)
pgsims_beat      |                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/utils/asyncio.py", line 26, in inner
pgsims_beat      |     return func(*args, **kwargs)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/postgresql/base.py", line 275, in get_new_connection
pgsims_beat      |     connection = self.Database.connect(**conn_params)
pgsims_beat      |                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/psycopg2/__init__.py", line 122, in connect
pgsims_beat      |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      | django.db.utils.OperationalError: could not translate host name "db" to address: Temporary failure in name resolution
pgsims_beat      | 
pgsims_beat      | [2026-05-30 06:44:57,617: ERROR/MainProcess] Database gave error: OperationalError('server closed the connection unexpectedly\n\tThis probably means the server terminated abnormally\n\tbefore or while processing the request.\n')
pgsims_beat      | Traceback (most recent call last):
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
pgsims_beat      |     return self.cursor.execute(sql, params)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      | psycopg2.OperationalError: server closed the connection unexpectedly
pgsims_beat      | 	This probably means the server terminated abnormally
pgsims_beat      | 	before or while processing the request.
pgsims_beat      | 
pgsims_beat      | 
pgsims_beat      | The above exception was the direct cause of the following exception:
pgsims_beat      | 
pgsims_beat      | Traceback (most recent call last):
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django_celery_beat/schedulers.py", line 421, in schedule_changed
pgsims_beat      |     last, ts = self._last_timestamp, self.Changes.last_change()
pgsims_beat      |                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django_celery_beat/models.py", line 427, in last_change
pgsims_beat      |     return cls.objects.get(ident=1).last_update
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
pgsims_beat      |     return getattr(self.get_queryset(), name)(*args, **kwargs)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 635, in get
pgsims_beat      |     num = len(clone)
pgsims_beat      |           ^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 382, in __len__
pgsims_beat      |     self._fetch_all()
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 1886, in _fetch_all
pgsims_beat      |     self._result_cache = list(self._iterable_class(self))
pgsims_beat      |                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 93, in __iter__
pgsims_beat      |     results = compiler.execute_sql(
pgsims_beat      |               ^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/sql/compiler.py", line 1562, in execute_sql
pgsims_beat      |     cursor.execute(sql, params)
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
pgsims_beat      |     return self._execute_with_wrappers(
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
pgsims_beat      |     return executor(sql, params, many, context)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
pgsims_beat      |     with self.db.wrap_database_errors:
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
pgsims_beat      |     raise dj_exc_value.with_traceback(traceback) from exc_value
pgsims_beat      |   File "/home/sims/.local/lib/python3.11/site-packages/django/db/backends/utils.py", line 89, in _execute
pgsims_beat      |     return self.cursor.execute(sql, params)
pgsims_beat      |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_beat      | django.db.utils.OperationalError: server closed the connection unexpectedly
pgsims_beat      | 	This probably means the server terminated abnormally
pgsims_beat      | 	before or while processing the request.
pgsims_beat      | 
pgsims_beat      | celery beat v5.6.3 (recovery) is starting.
pgsims_beat      | __    -    ... __   -        _
pgsims_beat      | LocalTime -> 2026-05-30 13:52:21
pgsims_beat      | Configuration ->
pgsims_beat      |     . broker -> redis://redis:6379/1
pgsims_beat      |     . loader -> celery.loaders.app.AppLoader
pgsims_beat      |     . scheduler -> django_celery_beat.schedulers.DatabaseScheduler
pgsims_beat      | 
pgsims_beat      |     . logfile -> [stderr]@%INFO
pgsims_beat      |     . maxinterval -> 5.00 seconds (5s)
pgsims_beat      | [2026-05-30 13:52:21,435: INFO/MainProcess] beat: Starting...

## Backend preflight outputs

### python manage.py check

### python manage.py showmigrations

### python manage.py makemigrations --check --dry-run

NOTE: 'python' not found in PATH; using 'python3' (Python 3.12.3).

## Backend preflight outputs (python3)

### python3 manage.py check
System check identified no issues (0 silenced).

### python3 manage.py showmigrations
academics
 [X] 0001_initial
 [X] 0002_initial
 [X] 0003_remove_studentprofile_batch_and_more
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
 [X] 0003_logentry_add_action_flag_choices
audit
 [X] 0001_initial
 [X] 0002_initial
auth
 [X] 0001_initial
 [X] 0002_alter_permission_name_max_length
 [X] 0003_alter_user_email_max_length
 [X] 0004_alter_user_username_opts
 [X] 0005_alter_user_last_login_null
 [X] 0006_require_contenttypes_0002
 [X] 0007_alter_validators_add_error_messages
 [X] 0008_alter_user_username_max_length
 [X] 0009_alter_user_last_name_max_length
 [X] 0010_alter_group_name_max_length
 [X] 0011_update_proxy_permissions
 [X] 0012_alter_user_first_name_max_length
backup_center
 [ ] 0001_initial
bulk
 [X] 0001_initial
 [X] 0002_initial
 [X] 0003_historicalmappingpreset_and_more
contenttypes
 [X] 0001_initial
 [X] 0002_remove_content_type_name
django_celery_beat
 [X] 0001_initial
 [X] 0002_auto_20161118_0346
 [X] 0003_auto_20161209_0049
 [X] 0004_auto_20170221_0000
 [X] 0005_add_solarschedule_events_choices
 [X] 0006_auto_20180322_0932
 [X] 0007_auto_20180521_0826
 [X] 0008_auto_20180914_1922
 [X] 0006_auto_20180210_1226
 [X] 0006_periodictask_priority
 [X] 0009_periodictask_headers
 [X] 0010_auto_20190429_0326
 [X] 0011_auto_20190508_0153
 [X] 0012_periodictask_expire_seconds
 [X] 0013_auto_20200609_0727
 [X] 0014_remove_clockedschedule_enabled
 [X] 0015_edit_solarschedule_events_choices
 [X] 0016_alter_crontabschedule_timezone
 [X] 0017_alter_crontabschedule_month_of_year
 [X] 0018_improve_crontab_helptext
 [X] 0019_alter_periodictasks_options
notifications
 [X] 0001_initial
 [X] 0002_initial
rotations
 [X] 0001_initial
 [X] 0002_initial
 [X] 0003_alter_hospitaldepartment_options
sessions
 [X] 0001_initial
training
 [X] 0001_initial
 [X] 0002_phase6_academic_core
 [X] 0003_residenttrainingrecord_has_default_dates
 [X] 0004_historicalresidenttrainingrecord_has_default_dates
 [X] 0005_logbookentry_logbookthresholdconfig_and_more
 [X] 0006_alter_historicalrotationassignment_options_and_more
users
 [X] 0001_initial
 [X] 0002_alter_historicaluser_role_and_more
 [X] 0003_alter_historicaluser_year_alter_user_year
 [X] 0004_data_correction_flags
 [X] 0005_historicaluser_data_quality_and_index_names
 [X] 0006_alter_departmentmembership_options_and_more

### python3 manage.py makemigrations --check --dry-run
No changes detected
