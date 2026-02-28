# Verification Evidence Log

This log records commands executed during backend truth verification and their outputs.

## Command
```bash
pwd
```

### Output
```
/home/munaim/srv/apps/pgsims

```
EXIT_CODE: 0

## Command
```bash
git --no-pager status
```

### Output
```
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	OUT/28_VERIFICATION_EVIDENCE_LOG.md

nothing added to commit but untracked files present (use "git add" to track)

```
EXIT_CODE: 0

## Command
```bash
git rev-parse HEAD | tee OUT/git_head.txt
```

### Output
```
24e0ed35f2bdf8e7102e4b7f95721222a04034bd

```
EXIT_CODE: 0

## Command
```bash
git --no-pager status --short --branch | tee OUT/git_status.txt
```

### Output
```
## main...origin/main
?? OUT/28_VERIFICATION_EVIDENCE_LOG.md
?? OUT/git_head.txt
?? OUT/git_status.txt

```
EXIT_CODE: 0

## Command
```bash
docker compose -f docker/docker-compose.yml ps | tee OUT/docker_ps.txt
```

### Output
```
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
NAME                   IMAGE                COMMAND                  SERVICE    CREATED          STATUS                    PORTS
pgsims_backend_prod    docker-web           "sh -c 'python manag…"   web        31 minutes ago   Up 31 minutes (healthy)   127.0.0.1:8014->8014/tcp
pgsims_beat            docker-beat          "celery -A sims_proj…"   beat       21 hours ago     Up 21 hours               8014/tcp
pgsims_db_prod         postgres:15-alpine   "docker-entrypoint.s…"   db         31 minutes ago   Up 31 minutes (healthy)   5432/tcp
pgsims_frontend_prod   docker-frontend      "docker-entrypoint.s…"   frontend   21 hours ago     Up 21 hours (healthy)     127.0.0.1:8082->3000/tcp
pgsims_redis_prod      redis:7-alpine       "docker-entrypoint.s…"   redis      21 hours ago     Up 21 hours (healthy)     6379/tcp
pgsims_worker          docker-worker        "celery -A sims_proj…"   worker     21 hours ago     Up 21 hours               8014/tcp

```
EXIT_CODE: 0

## Command
```bash
docker compose -f docker/docker-compose.yml logs -n 80 backend | tee OUT/docker_logs_backend.txt
```

### Output
```
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
no such service: backend

```
EXIT_CODE: 0

## Command
```bash
docker compose -f docker/docker-compose.yml logs -n 80 web | tee OUT/docker_logs_web.txt
```

### Output
```
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:40:55+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
pgsims_backend_prod  | [2026-02-27 21:09:31 +0000] [17] [INFO] Listening at: http://0.0.0.0:8014 (17)
pgsims_backend_prod  | [2026-02-27 21:09:31 +0000] [17] [INFO] Using worker: sync
pgsims_backend_prod  | [2026-02-27 21:09:31 +0000] [19] [INFO] Booting worker with pid: 19
pgsims_backend_prod  | [2026-02-27 21:09:31 +0000] [17] [INFO] Control socket listening at /app/gunicorn.ctl
pgsims_backend_prod  | [2026-02-27 21:09:31 +0000] [20] [INFO] Booting worker with pid: 20
pgsims_backend_prod  | [2026-02-27 21:09:31 +0000] [21] [INFO] Booting worker with pid: 21
pgsims_backend_prod  | [2026-02-27 21:09:31 +0000] [22] [INFO] Booting worker with pid: 22
pgsims_backend_prod  | [INFO] 2026-02-27 21:09:32,398 sims.certificates Certificate periodic tasks setup completed
pgsims_backend_prod  | [INFO] 2026-02-27 21:09:32,412 sims.logbook Logbook periodic tasks setup completed
pgsims_backend_prod  | [INFO] 2026-02-27 21:09:32,460 sims.certificates Certificate periodic tasks setup completed
pgsims_backend_prod  | [INFO] 2026-02-27 21:09:32,473 sims.logbook Logbook periodic tasks setup completed
pgsims_backend_prod  | [INFO] 2026-02-27 21:09:32,497 sims.wsgi SIMS WSGI application initialized successfully
pgsims_backend_prod  | [INFO] 2026-02-27 21:09:32,580 sims.wsgi SIMS WSGI application initialized successfully
pgsims_backend_prod  | [INFO] 2026-02-27 21:09:32,594 sims.certificates Certificate periodic tasks setup completed
pgsims_backend_prod  | [INFO] 2026-02-27 21:09:32,608 sims.logbook Logbook periodic tasks setup completed
pgsims_backend_prod  | [INFO] 2026-02-27 21:09:32,696 sims.wsgi SIMS WSGI application initialized successfully
pgsims_backend_prod  | [INFO] 2026-02-27 21:09:32,720 sims.certificates Certificate periodic tasks setup completed
pgsims_backend_prod  | [INFO] 2026-02-27 21:09:32,730 sims.logbook Logbook periodic tasks setup completed
pgsims_backend_prod  | [INFO] 2026-02-27 21:09:32,781 sims.wsgi SIMS WSGI application initialized successfully
pgsims_backend_prod  | [WARNING] 2026-02-27 21:09:33,973 sims.performance Slow request: GET /healthz/ took 1473ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:10:05,425 sims.performance Slow request: GET /healthz/ took 1405ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:10:36,545 sims.performance Slow request: GET /healthz/ took 1074ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:11:07,598 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:11:38,655 sims.performance Slow request: GET /healthz/ took 1008ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:12:09,708 sims.performance Slow request: GET /healthz/ took 1006ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:12:40,767 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:13:11,826 sims.performance Slow request: GET /healthz/ took 1012ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:13:42,880 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:14:14,336 sims.performance Slow request: GET /healthz/ took 1402ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:14:45,387 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:15:16,446 sims.performance Slow request: GET /healthz/ took 1013ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:15:47,507 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:16:18,564 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:16:49,626 sims.performance Slow request: GET /healthz/ took 1018ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:17:20,681 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:17:51,742 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:18:22,794 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:18:53,847 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:19:24,905 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:19:55,966 sims.performance Slow request: GET /healthz/ took 1016ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:20:27,029 sims.performance Slow request: GET /healthz/ took 1017ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:20:58,126 sims.performance Slow request: GET /healthz/ took 1048ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:21:29,191 sims.performance Slow request: GET /healthz/ took 1017ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:22:00,243 sims.performance Slow request: GET /healthz/ took 1006ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:22:31,376 sims.performance Slow request: GET /healthz/ took 1060ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:23:02,430 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:23:33,484 sims.performance Slow request: GET /healthz/ took 1008ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:24:04,547 sims.performance Slow request: GET /healthz/ took 1014ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:24:35,600 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:25:06,660 sims.performance Slow request: GET /healthz/ took 1016ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:25:37,718 sims.performance Slow request: GET /healthz/ took 1006ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:26:08,774 sims.performance Slow request: GET /healthz/ took 1008ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:26:39,879 sims.performance Slow request: GET /healthz/ took 1058ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:27:10,936 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:27:41,992 sims.performance Slow request: GET /healthz/ took 1010ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:28:13,046 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:28:44,102 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:29:15,156 sims.performance Slow request: GET /healthz/ took 1006ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:29:46,208 sims.performance Slow request: GET /healthz/ took 1006ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:30:17,278 sims.performance Slow request: GET /healthz/ took 1025ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:30:48,331 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:31:19,385 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:31:50,443 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:32:21,498 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:32:52,559 sims.performance Slow request: GET /healthz/ took 1016ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:33:23,629 sims.performance Slow request: GET /healthz/ took 1022ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:33:54,725 sims.performance Slow request: GET /healthz/ took 1047ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:34:25,779 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:34:56,836 sims.performance Slow request: GET /healthz/ took 1006ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:35:27,902 sims.performance Slow request: GET /healthz/ took 1017ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:35:58,957 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:36:30,021 sims.performance Slow request: GET /healthz/ took 1009ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:37:01,074 sims.performance Slow request: GET /healthz/ took 1006ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:37:32,131 sims.performance Slow request: GET /healthz/ took 1006ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:38:03,195 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:38:34,251 sims.performance Slow request: GET /healthz/ took 1006ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:39:05,305 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:39:36,358 sims.performance Slow request: GET /healthz/ took 1006ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:40:07,431 sims.performance Slow request: GET /healthz/ took 1023ms
pgsims_backend_prod  | [WARNING] 2026-02-27 21:40:38,498 sims.performance Slow request: GET /healthz/ took 1008ms

```
EXIT_CODE: 0

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T backend python manage.py check
```

### Output
```
time="2026-02-28T02:41:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
service "backend" is not running

```
EXIT_CODE: 1

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T web python manage.py check | tee OUT/manage_check.txt
```

### Output
```
time="2026-02-28T02:41:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
[INFO] 2026-02-27 21:41:20,121 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-27 21:41:20,132 sims.logbook Logbook periodic tasks setup completed
System check identified no issues (0 silenced).

```
EXIT_CODE: 0

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T backend python manage.py showmigrations --plan > OUT/showmigrations_plan.txt
```

### Output
```
time="2026-02-28T02:41:20+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:20+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:20+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:20+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:20+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:20+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:20+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
service "backend" is not running

```
EXIT_CODE: 1

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T web python manage.py showmigrations --plan > OUT/showmigrations_plan.txt
```

### Output
```
time="2026-02-28T02:41:20+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:20+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:20+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:20+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:20+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:20+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:20+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
[INFO] 2026-02-27 21:41:22,111 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-27 21:41:22,121 sims.logbook Logbook periodic tasks setup completed

```
EXIT_CODE: 0

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T backend python manage.py shell -c "from django.apps import apps; print('
'.join(sorted([a.label for a in apps.get_app_configs()])))" > OUT/installed_apps.txt
```

### Output
```
time="2026-02-28T02:41:22+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:22+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:22+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:23+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:23+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:23+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:23+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
service "backend" is not running

```
EXIT_CODE: 1

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T web python manage.py shell -c "from django.apps import apps; print('
'.join(sorted([a.label for a in apps.get_app_configs()])))" > OUT/installed_apps.txt
```

### Output
```
time="2026-02-28T02:41:23+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:23+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:23+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:23+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:23+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:23+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:23+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
[INFO] 2026-02-27 21:41:24,233 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-27 21:41:24,244 sims.logbook Logbook periodic tasks setup completed

```
EXIT_CODE: 0

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T backend python manage.py shell -c "import django; print('DJANGO_VERSION', django.get_version())"
```

### Output
```
time="2026-02-28T02:41:24+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:24+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:24+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:24+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:24+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:24+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:24+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
service "backend" is not running

```
EXIT_CODE: 1

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T web python manage.py shell -c "import django; print('DJANGO_VERSION', django.get_version())" | tee OUT/django_version.txt
```

### Output
```
time="2026-02-28T02:41:24+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:24+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:24+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:24+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:24+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:24+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:41:24+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
[INFO] 2026-02-27 21:41:25,687 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-27 21:41:25,698 sims.logbook Logbook periodic tasks setup completed
DJANGO_VERSION 4.2.28

```
EXIT_CODE: 0

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T web python manage.py shell < OUT/models_inventory_dump.py > OUT/models_inventory.json
```

### Output
```
time="2026-02-28T02:48:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:48:02+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:48:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:48:02+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:48:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:48:02+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:48:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
[INFO] 2026-02-27 21:48:04,030 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-27 21:48:04,039 sims.logbook Logbook periodic tasks setup completed
Traceback (most recent call last):
  File "/app/manage.py", line 24, in <module>
    main()
  File "/app/manage.py", line 21, in main
    execute_from_command_line(sys.argv)
  File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
    utility.execute()
  File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/__init__.py", line 436, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/base.py", line 412, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/base.py", line 458, in execute
    output = self.handle(*args, **options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/commands/shell.py", line 127, in handle
    exec(sys.stdin.read(), globals())
  File "<string>", line 60, in <module>
  File "/usr/local/lib/python3.11/json/__init__.py", line 238, in dumps
    **kw).encode(obj)
          ^^^^^^^^^^^
  File "/usr/local/lib/python3.11/json/encoder.py", line 202, in encode
    chunks = list(chunks)
             ^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/json/encoder.py", line 430, in _iterencode
    yield from _iterencode_list(o, _current_indent_level)
  File "/usr/local/lib/python3.11/json/encoder.py", line 326, in _iterencode_list
    yield from chunks
  File "/usr/local/lib/python3.11/json/encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "/usr/local/lib/python3.11/json/encoder.py", line 326, in _iterencode_list
    yield from chunks
  File "/usr/local/lib/python3.11/json/encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "/usr/local/lib/python3.11/json/encoder.py", line 326, in _iterencode_list
    yield from chunks
  File "/usr/local/lib/python3.11/json/encoder.py", line 439, in _iterencode
    o = _default(o)
        ^^^^^^^^^^^
  File "/usr/local/lib/python3.11/json/encoder.py", line 180, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type ZoneInfo is not JSON serializable

```
EXIT_CODE: 1

## Command
```bash
python OUT/render_models_catalog.py
```

### Output
```
bash: python: command not found

```
EXIT_CODE: 127

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T web python manage.py shell < OUT/models_inventory_dump.py > OUT/models_inventory.json
```

### Output
```
time="2026-02-28T02:48:37+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:48:37+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:48:37+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:48:37+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:48:37+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:48:37+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:48:37+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
[INFO] 2026-02-27 21:48:38,958 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-27 21:48:38,968 sims.logbook Logbook periodic tasks setup completed

```
EXIT_CODE: 0

## Command
```bash
python3 OUT/render_models_catalog.py
```

### Output
```
Models: 62

```
EXIT_CODE: 0

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T web python manage.py shell -c "from django.contrib.admin.sites import site; print('REGISTRY_COUNT', len(site._registry)); print('
'.join(sorted([m._meta.label for m in site._registry.keys()])))" > OUT/admin_registry_models.txt
```

### Output
```
time="2026-02-28T02:52:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:52:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:52:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:52:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:52:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:52:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:52:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
[INFO] 2026-02-27 21:52:19,386 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-27 21:52:19,396 sims.logbook Logbook periodic tasks setup completed

```
EXIT_CODE: 0

## Command
```bash
python3 OUT/admin_audit.py
```

### Output
```
Generated admin audit outputs

```
EXIT_CODE: 0

## Command
```bash
rg -n --no-heading -S 'choices\s*=|TextChoices|IntegerChoices|Status|STATE|APPROV|SUBMIT|REVIEW|SEND_BACK|RETURN' backend > OUT/grep_status_states.txt
```

### Output
```
bash: rg: command not found

```
EXIT_CODE: 127

## Command
```bash
rg -n --no-heading -S 'transition|can_|allowed_|validate_|clean\(|perform_create|perform_update|serializer\.validate|utrmc-approve|verify' backend > OUT/grep_transitions.txt
```

### Output
```
bash: rg: command not found

```
EXIT_CODE: 127

## Command
```bash
python3 - <<'PY'
import json
from pathlib import Path
inv = json.loads(Path('/home/munaim/srv/apps/pgsims/OUT/models_inventory.json').read_text())
lines=['# Models With Status-like Fields','']
for m in inv:
    if m.get('status_fields'):
        lines.append(f-
```

### Output
```
bash: warning: here-document at line 4 delimited by end-of-file (wanted `PY')
  File "<stdin>", line 7
    lines.append(f-
                ^
SyntaxError: '(' was never closed

```
EXIT_CODE: 1

## Command
```bash
grep -RniE 'choices\s*=|TextChoices|IntegerChoices|Status|STATE|APPROV|SUBMIT|REVIEW|SEND_BACK|RETURN' backend > OUT/grep_status_states.txt
```

### Output
```
grep: backend/__pycache__/test_frontend_create.cpython-312.pyc: binary file matches
grep: backend/__pycache__/test_admin_view.cpython-312.pyc: binary file matches
grep: backend/__pycache__/test_admin.cpython-312.pyc: binary file matches
grep: backend/db.sqlite3: binary file matches
grep: backend/sims/academics/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/academics/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/sims/academics/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/academics/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/sims/academics/migrations/__pycache__/0002_initial.cpython-312.pyc: binary file matches
grep: backend/sims/academics/migrations/__pycache__/0001_initial.cpython-312.pyc: binary file matches
grep: backend/sims/users/__pycache__/apps.cpython-312.pyc: binary file matches
grep: backend/sims/users/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/users/__pycache__/api_views.cpython-312.pyc: binary file matches
grep: backend/sims/users/__pycache__/test_registration_api.cpython-312.pyc: binary file matches
grep: backend/sims/users/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/users/__pycache__/tests.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/users/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/users/__pycache__/test_registration_api.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/users/management/commands/__pycache__/import_demo_cases.cpython-312.pyc: binary file matches
grep: backend/sims/users/management/commands/__pycache__/seed_demo_data.cpython-312.pyc: binary file matches
grep: backend/sims/users/management/commands/__pycache__/seed_e2e.cpython-312.pyc: binary file matches
grep: backend/sims/users/migrations/__pycache__/0002_historicaluser.cpython-312.pyc: binary file matches
grep: backend/sims/users/migrations/__pycache__/0001_initial.cpython-312.pyc: binary file matches
grep: backend/sims/attendance/__pycache__/services.cpython-312.pyc: binary file matches
grep: backend/sims/attendance/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/attendance/__pycache__/api_views.cpython-312.pyc: binary file matches
grep: backend/sims/attendance/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/attendance/__pycache__/tests.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/attendance/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/sims/attendance/migrations/__pycache__/0002_initial.cpython-312.pyc: binary file matches
grep: backend/sims/attendance/migrations/__pycache__/0001_initial.cpython-312.pyc: binary file matches
grep: backend/sims/__pycache__/common_permissions.cpython-312.pyc: binary file matches
grep: backend/sims/tests/factories/__pycache__/rotation_factories.cpython-312.pyc: binary file matches
grep: backend/sims/tests/factories/__pycache__/case_factories.cpython-312.pyc: binary file matches
grep: backend/sims/tests/factories/__pycache__/certificate_factories.cpython-312.pyc: binary file matches
grep: backend/sims/audit/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/audit/__pycache__/signals.cpython-312.pyc: binary file matches
grep: backend/sims/audit/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/sims/audit/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/results/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/results/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/sims/results/__pycache__/urls.cpython-312.pyc: binary file matches
grep: backend/sims/results/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/results/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/sims/results/migrations/__pycache__/0002_initial.cpython-312.pyc: binary file matches
grep: backend/sims/results/migrations/__pycache__/0001_initial.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/apps.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/api_serializers.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/test_api.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/api_views.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/tests.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/api_urls.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/test_api.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/urls.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/migrations/__pycache__/0002_initial.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/migrations/__pycache__/0001_initial.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/migrations/__pycache__/0003_alter_logbookentry_options_and_more.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/migrations/__pycache__/0005_historicallogbookreview_historicalprocedure_and_more.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/migrations/__pycache__/0006_remove_date_constraint.cpython-312.pyc: binary file matches
grep: backend/sims/cases/__pycache__/api_serializers.cpython-312.pyc: binary file matches
grep: backend/sims/cases/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/cases/__pycache__/test_api.cpython-312.pyc: binary file matches
grep: backend/sims/cases/__pycache__/api_views.cpython-312.pyc: binary file matches
grep: backend/sims/cases/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/cases/__pycache__/api_urls.cpython-312.pyc: binary file matches
grep: backend/sims/cases/__pycache__/test_api.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/cases/__pycache__/urls.cpython-312.pyc: binary file matches
grep: backend/sims/cases/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/cases/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/sims/cases/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/sims/cases/templatetags/__pycache__/case_filters.cpython-312.pyc: binary file matches
grep: backend/sims/cases/migrations/__pycache__/0002_initial.cpython-312.pyc: binary file matches
grep: backend/sims/cases/migrations/__pycache__/0001_initial.cpython-312.pyc: binary file matches
grep: backend/sims/cases/migrations/__pycache__/0002_historicalcasecategory_historicalclinicalcase_and_more.cpython-312.pyc: binary file matches
grep: backend/sims/domain/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/services.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/apps.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/api_serializers.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/test_canonical_migration_gate.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/api_views.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/test_canonical_migration_gate.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/tests.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/api_urls.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/migrations/__pycache__/0002_historicalrotation_historicalhospital_and_more.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/migrations/__pycache__/0002_initial.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/migrations/__pycache__/0003_hospitaldepartment_and_more.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/migrations/__pycache__/0001_initial.cpython-312.pyc: binary file matches
grep: backend/sims/reports/__pycache__/services.cpython-312.pyc: binary file matches
grep: backend/sims/reports/__pycache__/apps.cpython-312.pyc: binary file matches
grep: backend/sims/reports/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/reports/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/reports/__pycache__/tests.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/reports/__pycache__/registry.cpython-312.pyc: binary file matches
grep: backend/sims/reports/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/sims/reports/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/services.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/event_catalog.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/dashboard_v1.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/tests.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/dimensions.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/event_tracking.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/management/commands/__pycache__/rebuild_analytics_rollups.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/migrations/__pycache__/0001_initial.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/migrations/__pycache__/0001_add_performance_indexes.cpython-312.pyc: binary file matches
grep: backend/sims/bulk/__pycache__/services.cpython-312.pyc: binary file matches
grep: backend/sims/bulk/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/bulk/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/sims/bulk/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/bulk/__pycache__/tests.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/bulk/__pycache__/urls.cpython-312.pyc: binary file matches
grep: backend/sims/bulk/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/bulk/migrations/__pycache__/0001_initial.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/apps.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/api_serializers.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/api_views.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/urls.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/migrations/__pycache__/0002_initial.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/migrations/__pycache__/0001_initial.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/migrations/__pycache__/0002_historicalcertificatetype_historicalcertificate.cpython-312.pyc: binary file matches
grep: backend/sims/notifications/__pycache__/services.cpython-312.pyc: binary file matches
grep: backend/sims/notifications/__pycache__/apps.cpython-312.pyc: binary file matches
grep: backend/sims/notifications/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/notifications/__pycache__/signals.cpython-312.pyc: binary file matches
grep: backend/sims/notifications/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/notifications/__pycache__/tests.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/notifications/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/search/__pycache__/services.cpython-312.pyc: binary file matches
grep: backend/sims/search/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/search/__pycache__/signals.cpython-312.pyc: binary file matches
grep: backend/sims/search/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/search/__pycache__/tests.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/_devtools/tests/__pycache__/test_rbac_api.cpython-312.pyc: binary file matches
grep: backend/sims_project/__pycache__/settings.cpython-312.pyc: binary file matches
grep: backend/sims_project/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/sims_project/__pycache__/urls.cpython-312.pyc: binary file matches
grep: backend/sims_project/__pycache__/health.cpython-312.pyc: binary file matches
grep: backend/sims_project/__pycache__/wsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/liblcms2-cc10e42f.so.2.0.17: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libwebpmux-7f11e5ce.so.3.1.2: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libjpeg-32d42e18.so.62.4.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libzstd-761a17b6.so.1.5.7: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libharfbuzz-0692f733.so.0.61230.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libpng16-4a38ea05.so.16.53.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libtiff-295fd75c.so.6.2.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libwebp-d8b9687f.so.7.2.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libavif-01e67780.so.16.3.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libopenjp2-94e588ba.so.2.5.4: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libfreetype-ee1c40c4.so.6.20.4: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libbrotlicommon-c55a5f7a.so.1.2.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/poolmanager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/connectionpool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/filepost.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/_base_connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/_collections.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/_request_methods.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/http2/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/http2/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/http2/__pycache__/probe.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/request.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/ssl_.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/timeout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/ssltransport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/ssl_match_hostname.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/proxy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/wait.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/url.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/retry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/contrib/__pycache__/socks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/contrib/__pycache__/pyopenssl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/contrib/emscripten/__pycache__/request.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/contrib/emscripten/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/contrib/emscripten/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/contrib/emscripten/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/contrib/emscripten/__pycache__/fetch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/platformdirs/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/platformdirs/__pycache__/macos.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/platformdirs/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/platformdirs/__pycache__/android.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/platformdirs/__pycache__/unix.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/platformdirs/__pycache__/__main__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/platformdirs/__pycache__/_xdg.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/platformdirs/__pycache__/windows.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/iniconfig/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/iniconfig/__pycache__/_parse.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/iniconfig/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/__pycache__/cronlog.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/__pycache__/click_plugins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/__pycache__/crontabs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/__pycache__/pycodestyle.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/__pycache__/crontab.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/__pycache__/mccabe.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/__pycache__/mypy_extensions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/__pycache__/six.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/__pycache__/typing_extensions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/certifi/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/diff_match_patch/__pycache__/diff_match_patch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/whitenoise/__pycache__/responders.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/whitenoise/__pycache__/compress.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/whitenoise/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/whitenoise/__pycache__/media_types.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/whitenoise/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/whitenoise/__pycache__/storage.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/whitenoise/runserver_nostatic/management/commands/__pycache__/runserver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/__pycache__/processor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/__pycache__/style_guide.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/__pycache__/statistics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/__pycache__/checker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/__pycache__/violation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/__pycache__/discover_files.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/formatting/__pycache__/_windows_color.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/formatting/__pycache__/default.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/formatting/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/options/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/options/__pycache__/parse_args.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/options/__pycache__/aggregator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/options/__pycache__/manager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/api/__pycache__/legacy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/main/__pycache__/cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/main/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/main/__pycache__/application.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/main/__pycache__/options.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/plugins/__pycache__/pyflakes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/plugins/__pycache__/pycodestyle.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/plugins/__pycache__/finder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/flake8/plugins/__pycache__/reporter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/widget_tweaks/templatetags/__pycache__/widget_tweaks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytokens/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytokens/__pycache__/cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/fixtures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/live_server_helper.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/lazy_django.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/runner.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/live_server_helper.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/django_compat.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/django_compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/plugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/plugin.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/lazy_django.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/asserts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/fixtures.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blib2to3/__pycache__/pytree.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blib2to3/__pycache__/pygram.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blib2to3/pgen2/__pycache__/parse.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blib2to3/pgen2/__pycache__/grammar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blib2to3/pgen2/__pycache__/literals.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blib2to3/pgen2/__pycache__/tokenize.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blib2to3/pgen2/__pycache__/conv.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blib2to3/pgen2/__pycache__/driver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blib2to3/pgen2/__pycache__/token.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blib2to3/pgen2/__pycache__/pgen.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/__pycache__/__pip-runner__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/__pycache__/wheel_builder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/__pycache__/main.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/__pycache__/self_outdated_check.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/__pycache__/configuration.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/__pycache__/pyproject.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/__pycache__/build_env.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/index/__pycache__/package_finder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/index/__pycache__/sources.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/index/__pycache__/collector.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/compatibility_tags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/unpacking.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/deprecation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/setuptools_build.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/filesystem.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/direct_url_helpers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/appdirs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/_log.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/virtualenv.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/temp_dir.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/glibc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/hashes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/logging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/entrypoints.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/packaging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/encoding.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/datetime.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/egg_link.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/urls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/misc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/subprocess.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/filetypes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/resolution/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/resolution/legacy/__pycache__/resolver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/requirements.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/provider.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/factory.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/resolver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/found_candidates.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/reporter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/candidates.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/locations/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/locations/__pycache__/_sysconfig.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/locations/__pycache__/_distutils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/locations/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/models/__pycache__/scheme.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/models/__pycache__/installation_report.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/models/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/models/__pycache__/link.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/models/__pycache__/format_control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/models/__pycache__/candidate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/models/__pycache__/direct_url.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/models/__pycache__/target_python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/models/__pycache__/index.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/models/__pycache__/search_scope.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/models/__pycache__/selection_prefs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/req/__pycache__/constructors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/req/__pycache__/req_uninstall.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/req/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/req/__pycache__/req_file.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/req/__pycache__/req_install.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/req/__pycache__/req_set.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/cli/__pycache__/status_codes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/cli/__pycache__/main.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/cli/__pycache__/progress_bars.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/cli/__pycache__/cmdoptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/cli/__pycache__/req_command.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/cli/__pycache__/spinners.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/cli/__pycache__/autocompletion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/cli/__pycache__/parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/cli/__pycache__/base_command.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/cli/__pycache__/command_context.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/cli/__pycache__/main_parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/freeze.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/list.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/show.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/inspect.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/download.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/hash.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/check.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/completion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/install.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/configuration.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/search.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/help.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/index.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/uninstall.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/vcs/__pycache__/subversion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/vcs/__pycache__/mercurial.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/vcs/__pycache__/versioncontrol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/vcs/__pycache__/git.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/vcs/__pycache__/bazaar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/distributions/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/distributions/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/distributions/__pycache__/installed.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/distributions/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/distributions/__pycache__/sdist.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/metadata/__pycache__/_json.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/metadata/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/metadata/__pycache__/pkg_resources.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/metadata/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/metadata/importlib/__pycache__/_dists.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/metadata/importlib/__pycache__/_envs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/metadata/importlib/__pycache__/_compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/network/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/network/__pycache__/download.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/network/__pycache__/lazy_wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/network/__pycache__/session.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/network/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/network/__pycache__/auth.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/network/__pycache__/xmlrpc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/operations/__pycache__/freeze.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/operations/__pycache__/prepare.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/operations/__pycache__/check.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/operations/install/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/operations/install/__pycache__/editable_legacy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/operations/build/__pycache__/metadata_editable.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/operations/build/__pycache__/build_tracker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/operations/build/__pycache__/metadata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/operations/build/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/operations/build/__pycache__/metadata_legacy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/operations/build/__pycache__/wheel_editable.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/operations/build/__pycache__/wheel_legacy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/webencodings/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/testing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/results.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/helpers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/actions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pyparsing/diagram/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/poolmanager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/connectionpool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/filepost.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/_collections.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/packages/__pycache__/six.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/packages/backports/__pycache__/weakref_finalize.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/ssl_.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/timeout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/ssl_match_hostname.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/proxy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/wait.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/url.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/retry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/contrib/__pycache__/ntlmpool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/contrib/__pycache__/securetransport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/contrib/__pycache__/appengine.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/contrib/__pycache__/pyopenssl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/contrib/_securetransport/__pycache__/low_level.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/contrib/_securetransport/__pycache__/bindings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/platformdirs/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/platformdirs/__pycache__/macos.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/platformdirs/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/platformdirs/__pycache__/android.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/platformdirs/__pycache__/unix.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/platformdirs/__pycache__/__main__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/platformdirs/__pycache__/windows.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/__pycache__/six.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/__pycache__/typing_extensions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/sbcsgroupprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/eucjpprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/codingstatemachine.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/codingstatemachinedict.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/chardistribution.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/escsm.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/big5prober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/euckrprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/utf8prober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/hebrewprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/escprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/utf1632prober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/mbcsgroupprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/mbcssm.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/sjisprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/macromanprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/euctwprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/sbcharsetprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/jpcntx.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/universaldetector.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/charsetprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/gb2312prober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/johabprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/charsetgroupprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/mbcharsetprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/enums.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/cp949prober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/latin1prober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/cli/__pycache__/chardetect.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/metadata/__pycache__/languages.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/certifi/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/__pycache__/_impl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_in_process/__pycache__/_in_process.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/segment.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/live_render.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/style.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/prompt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/layout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/ansi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/traceback.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/abc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/theme.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/markup.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_inspect.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/emoji.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_log_render.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/progress.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/repr.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/cells.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/color.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_wrap.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/progress_bar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/scope.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_pick.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_loop.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_timer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/palette.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/color_triplet.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_fileno.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/measure.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/bar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/pager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/table.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/pretty.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/logging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/rule.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_ratio.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/styled.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/spinner.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/highlighter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_windows_renderer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_emoji_codes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/padding.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/columns.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_stack.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/console.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/filesize.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/protocol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_extension.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_null_file.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/terminal_theme.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/diagnose.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/constrain.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/tree.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_emoji_replace.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/align.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_windows.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/jupyter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_win32_console.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/default_styles.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/json.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/file_proxy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/status.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/syntax.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/screen.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/box.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/__main__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/panel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/containers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/live.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/packaging/__pycache__/tags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/packaging/__pycache__/requirements.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/packaging/__pycache__/specifiers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/packaging/__pycache__/_structures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/packaging/__pycache__/version.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/packaging/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/packaging/__pycache__/markers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/packaging/__pycache__/_musllinux.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/packaging/__pycache__/_manylinux.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distro/__pycache__/distro.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/serialize.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/filewrapper.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/wrapper.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/heuristics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/controller.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/adapter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/_cmd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/cachecontrol/caches/__pycache__/file_cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/cachecontrol/caches/__pycache__/redis_cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/tomli/__pycache__/_parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/tomli/__pycache__/_re.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/tornadoweb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/after.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/nap.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/before.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/stop.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/_asyncio.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/wait.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/before_sleep.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/retry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/colorama/__pycache__/initialise.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/colorama/__pycache__/ansitowin32.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/colorama/tests/__pycache__/initialise_test.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/colorama/tests/__pycache__/winterm_test.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/colorama/tests/__pycache__/ansitowin32_test.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/_internal_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/status_codes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/cookies.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/adapters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/structures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/certs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/auth.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/help.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/sessions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/idna/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/idna/__pycache__/codec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/idna/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/idna/__pycache__/intranges.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/idna/__pycache__/uts46data.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/resources.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/locators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/metadata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/manifest.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/scripts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/version.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/markers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/database.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/index.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_macos.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_openssl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_ssl_constants.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_windows.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/resolvelib/__pycache__/structs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/resolvelib/__pycache__/reporters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/resolvelib/__pycache__/providers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/resolvelib/__pycache__/resolvers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/msgpack/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/msgpack/__pycache__/fallback.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/msgpack/__pycache__/ext.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/__pycache__/formatter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/__pycache__/modeline.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/__pycache__/lexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/__pycache__/scanner.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/__pycache__/sphinxext.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/__pycache__/regexopt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/__pycache__/token.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/filters/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/styles/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/lexers/__pycache__/python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/lexers/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/lexers/__pycache__/_mapping.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/formatters/__pycache__/latex.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/formatters/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/formatters/__pycache__/img.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/formatters/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pkg_resources/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/timezone_field/__pycache__/choices.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/timezone_field/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/timezone_field/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/tags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/_parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/metadata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/requirements.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/_elffile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/specifiers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/_structures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/_tokenizer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/version.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/pylock.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/markers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/_musllinux.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/_manylinux.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/licenses/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/charset_normalizer/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/charset_normalizer/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/charset_normalizer/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/charset_normalizer/__pycache__/md.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/charset_normalizer/__pycache__/legacy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/charset_normalizer/__pycache__/cd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/charset_normalizer/cli/__pycache__/__main__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/charset_normalizer/md__mypyc.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/__pycache__/backend.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/__pycache__/_typing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/__pycache__/gitignore.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/__pycache__/pathspec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/__pycache__/pattern.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/_backends/__pycache__/_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/_backends/__pycache__/agg.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/_backends/simple/__pycache__/gitignore.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/_backends/simple/__pycache__/pathspec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/_backends/hyperscan/__pycache__/gitignore.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/_backends/hyperscan/__pycache__/pathspec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/_backends/re2/__pycache__/gitignore.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/_backends/re2/__pycache__/pathspec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/patterns/__pycache__/gitwildmatch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/patterns/gitignore/__pycache__/spec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/patterns/gitignore/__pycache__/basic.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/patterns/gitignore/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/wcwidth/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/wcwidth/__pycache__/bisearch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/wcwidth/__pycache__/grapheme.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/wcwidth/__pycache__/unicode_versions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/wcwidth/__pycache__/textwrap.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/wcwidth/__pycache__/wcwidth.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/wcwidth/__pycache__/sgr_state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/crispy_forms/__pycache__/layout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/crispy_forms/__pycache__/bootstrap.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/crispy_forms/__pycache__/layout_slice.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/crispy_forms/__pycache__/helper.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/crispy_forms/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/crispy_forms/templatetags/__pycache__/crispy_forms_filters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/crispy_forms/templatetags/__pycache__/crispy_forms_field.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/crispy_forms/templatetags/__pycache__/crispy_forms_tags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/drawing/__pycache__/image.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/drawing/__pycache__/geometry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/drawing/__pycache__/fill.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/drawing/__pycache__/spreadsheet_drawing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/utils/__pycache__/cell.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/utils/__pycache__/indexed_list.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/utils/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/packaging/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/packaging/__pycache__/workbook.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/packaging/__pycache__/relationship.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/chartsheet/__pycache__/chartsheet.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/chartsheet/__pycache__/custom.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/worksheet/__pycache__/header_footer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/worksheet/__pycache__/cell_range.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/worksheet/__pycache__/filters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/worksheet/__pycache__/_reader.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/worksheet/__pycache__/table.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/worksheet/__pycache__/protection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/worksheet/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/worksheet/__pycache__/dimensions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/worksheet/__pycache__/worksheet.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/worksheet/__pycache__/_writer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/worksheet/__pycache__/_read_only.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/chart/__pycache__/reference.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/pivot/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/pivot/__pycache__/table.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/descriptors/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/reader/__pycache__/workbook.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/reader/__pycache__/excel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/cell/__pycache__/cell.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/cell/__pycache__/rich_text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/formula/__pycache__/tokenizer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/formula/__pycache__/translate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/styles/__pycache__/numbers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/styles/__pycache__/differential.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/styles/__pycache__/proxy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/styles/__pycache__/named_styles.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/workbook/__pycache__/workbook.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/workbook/__pycache__/protection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/workbook/__pycache__/defined_name.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/workbook/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/workbook/__pycache__/_writer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/comments/__pycache__/comment_sheet.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/amqp/__pycache__/spec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/amqp/__pycache__/platform.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/amqp/__pycache__/abstract_channel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/amqp/__pycache__/serialization.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/amqp/__pycache__/protocol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/amqp/__pycache__/sasl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/amqp/__pycache__/channel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/amqp/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/amqp/__pycache__/method_framing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/PcfFontFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageStat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/JpegImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ContainerIO.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/TiffTags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/BufrStubImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/XVThumbImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/PSDraw.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/PpmImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/MpegImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/XbmImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/BlpImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/PcdImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageMorph.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/FitsImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageCms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/PcxImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/_typing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageChops.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/WalImageFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/GribStubImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageFilter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/QoiImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageDraw2.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImagePalette.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/JpegPresets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/SpiderImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/Jpeg2KImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/PalmImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/SunImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/MpoImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/PdfParser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageGrab.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/FontFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/GimpGradientFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/MspImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImtImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/GimpPaletteFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageTransform.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/IcoImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/PaletteFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/CurImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/EpsImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/TarIO.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/XpmImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageQt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/FpxImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/WebPImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageShow.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/AvifImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/_binary.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageWin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageColor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageFont.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/McIdasImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/MicImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/Image.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageOps.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/WmfImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ExifTags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/BdfFontFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageSequence.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/TiffImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/_deprecate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageEnhance.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/TgaImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/FliImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/PngImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/_util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/DcxImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/PdfImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageDraw.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageText.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/PsdImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/IptcImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageMode.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/BmpImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/GbrImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/GdImageFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageMath.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/FtexImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageTk.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/IcnsImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/SgiImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/DdsImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/PixarImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/GifImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/Hdf5StubImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/_imagingtk.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/_imaging.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/_avif.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/_imagingmorph.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/_webp.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/_imagingcms.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/_imagingft.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/_imagingmath.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dateutil/__pycache__/relativedelta.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dateutil/__pycache__/rrule.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dateutil/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dateutil/tz/__pycache__/tz.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dateutil/tz/__pycache__/win.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dateutil/tz/__pycache__/_common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dateutil/tz/__pycache__/_factories.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dateutil/zoneinfo/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dateutil/parser/__pycache__/_parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dateutil/parser/__pycache__/isoparser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/auth/__pycache__/idp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/auth/__pycache__/token_manager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/auth/__pycache__/token.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/ocsp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/typing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/event.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/lock.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/crc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/sentinel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/credentials.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/data_structure.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/background.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/cluster.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/retry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/backoff.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/driver_info.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/maint_notifications.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/observability/__pycache__/attributes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/observability/__pycache__/recorder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/observability/__pycache__/metrics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/observability/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/observability/__pycache__/registry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/observability/__pycache__/providers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/http/__pycache__/http_client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/multidb/__pycache__/circuit.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/multidb/__pycache__/failover.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/multidb/__pycache__/event.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/multidb/__pycache__/command_executor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/multidb/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/multidb/__pycache__/healthcheck.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/multidb/__pycache__/database.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/multidb/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/multidb/__pycache__/failure_detector.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/__pycache__/sentinel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/__pycache__/policies.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/__pycache__/helpers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/__pycache__/cluster.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/__pycache__/redismodules.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/timeseries/__pycache__/commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/bf/__pycache__/commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/json/__pycache__/commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/json/__pycache__/path.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/json/__pycache__/decoders.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/search/__pycache__/reducers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/search/__pycache__/aggregation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/search/__pycache__/commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/search/__pycache__/suggestion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/search/__pycache__/result.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/search/__pycache__/profile_information.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/search/__pycache__/hybrid_result.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/search/__pycache__/query.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/search/__pycache__/querystring.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/search/__pycache__/hybrid_query.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/vectorset/__pycache__/commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/vectorset/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/_parsers/__pycache__/resp3.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/_parsers/__pycache__/commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/_parsers/__pycache__/socket.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/_parsers/__pycache__/hiredis.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/_parsers/__pycache__/resp2.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/_parsers/__pycache__/encoders.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/_parsers/__pycache__/helpers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/_parsers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/__pycache__/lock.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/__pycache__/sentinel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/__pycache__/cluster.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/__pycache__/retry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/http/__pycache__/http_client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/multidb/__pycache__/failover.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/multidb/__pycache__/event.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/multidb/__pycache__/command_executor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/multidb/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/multidb/__pycache__/healthcheck.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/multidb/__pycache__/database.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/multidb/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/multidb/__pycache__/failure_detector.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/entity.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/matcher.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/message.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/abstract.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/serialization.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/compression.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/simple.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/pidbox.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/clocks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/messaging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/utils/__pycache__/uuid.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/utils/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/utils/__pycache__/functional.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/utils/__pycache__/text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/utils/__pycache__/time.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/utils/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/utils/__pycache__/div.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/utils/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/utils/__pycache__/url.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/utils/__pycache__/limits.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/filesystem.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/gcpubsub.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/pyro.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/SLMQ.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/azurestoragequeues.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/memory.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/qpid.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/consul.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/azureservicebus.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/mongodb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/confluentkafka.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/etcd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/redis.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/SQS.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/native_delayed_delivery.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/virtual/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/virtual/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/virtual/__pycache__/exchange.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/asynchronous/__pycache__/timer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/asynchronous/__pycache__/semaphore.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/asynchronous/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/asynchronous/__pycache__/hub.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/asynchronous/http/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/asynchronous/http/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/asynchronous/aws/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/asynchronous/aws/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/asynchronous/aws/__pycache__/ext.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/asynchronous/aws/sqs/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/__pycache__/rl_config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/__pycache__/rl_settings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/platypus/__pycache__/doctemplate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/platypus/__pycache__/frames.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/platypus/__pycache__/figures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/platypus/__pycache__/flowables.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/platypus/__pycache__/tables.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/platypus/__pycache__/paragraph.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/platypus/__pycache__/tableofcontents.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/platypus/__pycache__/xpreformatted.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/platypus/__pycache__/para.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/platypus/__pycache__/paraparser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/colors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/pdfencrypt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/testutils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/rl_accel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/corp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/rparsexml.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/boxstuff.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/pygments2xpre.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/arciv.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/randomtext.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/rl_safe_eval.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/normalDate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/geomutils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/codecharts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/attrmap.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/PyFontify.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/fontfinder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/styles.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/sequencer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/textsplit.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/__pycache__/renderSVG.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/__pycache__/widgetbase.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/__pycache__/shapes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/__pycache__/svgpath.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/__pycache__/renderPDF.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/__pycache__/transform.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/__pycache__/renderPM.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/__pycache__/renderbase.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/__pycache__/renderPS.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/widgets/__pycache__/eventcal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/widgets/__pycache__/grids.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/widgets/__pycache__/signsandsymbols.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/widgets/__pycache__/table.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/widgets/__pycache__/flags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/samples/__pycache__/stacked_column.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/samples/__pycache__/stacked_bar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/samples/__pycache__/scatter_lines.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/samples/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/samples/__pycache__/radar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/samples/__pycache__/filled_radar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/samples/__pycache__/linechart_with_markers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/samples/__pycache__/clustered_bar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/samples/__pycache__/simple_pie.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/samples/__pycache__/bubble.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/samples/__pycache__/line_chart.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/samples/__pycache__/scatter_lines_markers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/samples/__pycache__/clustered_column.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/samples/__pycache__/scatter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/samples/__pycache__/exploded_pie.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/usps4s.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/widgets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/lto.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/dmtx.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/fourstate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/test.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/charts/__pycache__/textlabels.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/charts/__pycache__/dotbox.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/charts/__pycache__/utils3d.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/charts/__pycache__/axes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/charts/__pycache__/lineplots.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/charts/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/charts/__pycache__/markers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/charts/__pycache__/barcharts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/charts/__pycache__/piecharts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/charts/__pycache__/spider.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/charts/__pycache__/linecharts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/charts/__pycache__/slidebox.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/charts/__pycache__/legends.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/pdfgen/__pycache__/canvas.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/pdfgen/__pycache__/pdfimages.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/pdfgen/__pycache__/textobject.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/pdfbase/__pycache__/_fontdata_enc_symbol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/pdfbase/__pycache__/_glyphlist.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/pdfbase/__pycache__/ttfonts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/pdfbase/__pycache__/pdfdoc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/pdfbase/__pycache__/_fontdata_widths_symbol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/pdfbase/__pycache__/cidfonts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/pdfbase/__pycache__/acroform.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/pdfbase/__pycache__/pdfmetrics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/pdfbase/__pycache__/pdfutils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/sy______.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/zx______.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/zy______.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/DarkGardenMK.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_celery_beat/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_celery_beat/__pycache__/schedulers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_celery_beat/__pycache__/clockedschedule.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_celery_beat/__pycache__/tzcrontab.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_celery_beat/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click_repl/__pycache__/_repl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/report.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/comments.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/numerics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/nodes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/lines.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/linegen.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/output.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/rusty.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/brackets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/ranges.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/trans.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/mode.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/files.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/strings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/concurrency.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/handle_ipynb_magics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/parsing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/process.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/einfo.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/spawn.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/forkserver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/popen_fork.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/heap.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/sharedctypes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/popen_spawn_win32.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/pool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/queues.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/resource_sharer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/_win.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/reduction.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/synchronize.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/popen_forkserver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/managers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/context.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/__pycache__/filters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/__pycache__/filterset.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/rest_framework/__pycache__/backends.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/rest_framework/__pycache__/filterset.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/locale/cs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/locale/bg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/locale/uk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/locale/be/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/locale/nl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/locale/sk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_filters/locale/el/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/patch_stdout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/history.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/mouse_events.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/cursor_shapes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/selection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/renderer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/document.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/validation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/buffer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/search.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/auto_suggest.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/win32_types.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/clipboard/__pycache__/pyperclip.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/clipboard/__pycache__/in_memory.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/clipboard/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/formatted_text/__pycache__/ansi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/formatted_text/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/formatted_text/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/formatted_text/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/formatted_text/__pycache__/pygments.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/widgets/__pycache__/menus.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/widgets/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/widgets/__pycache__/dialogs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/widgets/__pycache__/toolbars.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/shortcuts/__pycache__/prompt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/shortcuts/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/shortcuts/__pycache__/choice_input.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/shortcuts/__pycache__/dialogs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/shortcuts/progress_bar/__pycache__/formatters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/shortcuts/progress_bar/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/scroll.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/open_in_editor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/emacs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/named_commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/basic.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/completion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/mouse.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/cpr.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/page_navigation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/search.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/auto_suggest.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/vi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/focus.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/__pycache__/emacs_state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/__pycache__/defaults.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/__pycache__/key_bindings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/__pycache__/vi_state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/__pycache__/key_processor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/eventloop/__pycache__/inputhook.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/eventloop/__pycache__/async_generator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/eventloop/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/eventloop/__pycache__/win32.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/completion/__pycache__/fuzzy_completer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/completion/__pycache__/filesystem.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/completion/__pycache__/deduplicate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/completion/__pycache__/nested.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/completion/__pycache__/word_completer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/completion/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/filters/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/filters/__pycache__/app.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/filters/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/filters/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/layout/__pycache__/menus.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/layout/__pycache__/layout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/layout/__pycache__/controls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/layout/__pycache__/processors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/layout/__pycache__/dummy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/layout/__pycache__/margins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/layout/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/layout/__pycache__/scrollable_pane.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/layout/__pycache__/dimension.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/layout/__pycache__/screen.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/layout/__pycache__/mouse_handlers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/layout/__pycache__/containers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/input/__pycache__/ansi_escape_sequences.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/input/__pycache__/vt100_parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/input/__pycache__/vt100.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/input/__pycache__/defaults.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/input/__pycache__/posix_pipe.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/input/__pycache__/posix_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/input/__pycache__/typeahead.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/input/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/input/__pycache__/win32.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/input/__pycache__/win32_pipe.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/styles/__pycache__/style.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/styles/__pycache__/defaults.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/styles/__pycache__/style_transformation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/styles/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/styles/__pycache__/pygments.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/application/__pycache__/run_in_terminal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/application/__pycache__/dummy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/application/__pycache__/current.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/application/__pycache__/application.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/lexers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/lexers/__pycache__/pygments.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/contrib/completers/__pycache__/system.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/contrib/regular_languages/__pycache__/compiler.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/contrib/regular_languages/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/contrib/regular_languages/__pycache__/completion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/contrib/regular_languages/__pycache__/lexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/contrib/regular_languages/__pycache__/validation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/contrib/regular_languages/__pycache__/regex_parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/contrib/ssh/__pycache__/server.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/contrib/telnet/__pycache__/protocol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/contrib/telnet/__pycache__/server.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/output/__pycache__/flush_stdout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/output/__pycache__/vt100.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/output/__pycache__/defaults.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/output/__pycache__/plain_text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/output/__pycache__/color_depth.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/output/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/output/__pycache__/win32.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/output/__pycache__/conemu.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/output/__pycache__/windows10.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/corsheaders/__pycache__/apps.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/corsheaders/__pycache__/conf.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/corsheaders/__pycache__/checks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/corsheaders/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/simple_history/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/simple_history/__pycache__/template_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/simple_history/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/simple_history/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/simple_history/__pycache__/manager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/simple_history/management/commands/__pycache__/populate_history.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blackd/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blackd/__pycache__/middlewares.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blackd/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/__pycache__/formatter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/__pycache__/sql.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/__pycache__/cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/__pycache__/lexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/__pycache__/keywords.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/filters/__pycache__/aligned_indent.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/filters/__pycache__/reindent.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/filters/__pycache__/others.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/engine/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/engine/__pycache__/filter_stack.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/engine/__pycache__/statement_splitter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pluggy/__pycache__/_callers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pluggy/__pycache__/_manager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pluggy/__pycache__/_result.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pluggy/__pycache__/_tracing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pluggy/__pycache__/_hooks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/__pycache__/shortcuts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/__pycache__/context_processors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/__pycache__/loader.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/__pycache__/defaultfilters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/__pycache__/defaulttags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/__pycache__/engine.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/__pycache__/loader_tags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/__pycache__/library.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/__pycache__/smartif.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/__pycache__/context.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/loaders/__pycache__/filesystem.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/loaders/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/backends/__pycache__/django.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/template/backends/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/archive.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/log.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/safestring.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/module_loading.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/datastructures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/_os.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/timezone.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/deconstruct.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/functional.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/inspect.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/feedgenerator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/http.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/version.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/regex_helper.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/dateparse.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/numberformat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/topological_sort.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/termcolors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/jslex.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/timesince.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/ipv6.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/encoding.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/hashable.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/formats.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/lorem_ipsum.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/crypto.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/dateformat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/decorators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/tree.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/autoreload.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/translation/__pycache__/trans_real.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/http/__pycache__/request.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/http/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/http/__pycache__/cookie.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/http/__pycache__/multipartparser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/templatetags/__pycache__/static.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/templatetags/__pycache__/i18n.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/__pycache__/paginator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/__pycache__/asgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/__pycache__/signing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/__pycache__/wsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/cache/backends/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/checks/security/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/checks/__pycache__/registry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/checks/__pycache__/urls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/checks/__pycache__/model_checks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/servers/__pycache__/basehttp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/serializers/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/serializers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/serializers/__pycache__/xml_serializer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/__pycache__/templates.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/__pycache__/sql.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/__pycache__/color.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/flush.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/createcachetable.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/compilemessages.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/sqlflush.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/sqlmigrate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/inspectdb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/dbshell.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/migrate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/check.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/runserver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/makemessages.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/sqlsequencereset.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/loaddata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/optimizemigration.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/makemigrations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/mail/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/mail/__pycache__/message.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/mail/backends/__pycache__/smtp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/mail/backends/__pycache__/filebased.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/mail/backends/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/files/storage/__pycache__/memory.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/files/storage/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/files/__pycache__/uploadedfile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/files/__pycache__/uploadhandler.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/files/__pycache__/images.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/files/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/files/__pycache__/locks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/handlers/__pycache__/exception.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/handlers/__pycache__/asgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/handlers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/handlers/__pycache__/wsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/forms/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/forms/__pycache__/boundfield.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/forms/__pycache__/formsets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/forms/__pycache__/widgets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/forms/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/forms/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/forms/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/__pycache__/transaction.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/indexes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/expressions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/query_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/constraints.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/query.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/deletion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/options.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/enums.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/manager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/functions/__pycache__/comparison.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/functions/__pycache__/text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/functions/__pycache__/datetime.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/sql/__pycache__/compiler.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/sql/__pycache__/subqueries.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/sql/__pycache__/where.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/sql/__pycache__/query.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/fields/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/fields/__pycache__/related.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/fields/__pycache__/files.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/fields/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/fields/__pycache__/reverse_related.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/fields/__pycache__/related_descriptors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/__pycache__/writer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/__pycache__/loader.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/__pycache__/optimizer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/__pycache__/recorder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/__pycache__/executor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/__pycache__/questioner.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/__pycache__/migration.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/__pycache__/autodetector.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/__pycache__/graph.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/__pycache__/state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/operations/__pycache__/special.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/operations/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/operations/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/operations/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/operations/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/__pycache__/ddl_references.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/creation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/mysql/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/mysql/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/mysql/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/mysql/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/mysql/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/oracle/__pycache__/creation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/oracle/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/oracle/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/oracle/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/oracle/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/oracle/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/oracle/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/postgresql/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/postgresql/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/postgresql/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/postgresql/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/postgresql/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/base/__pycache__/creation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/base/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/base/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/base/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/base/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/base/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/middleware/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/middleware/__pycache__/csrf.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/middleware/__pycache__/http.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/middleware/__pycache__/common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/middleware/__pycache__/locale.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/apps/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/apps/__pycache__/registry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/test/__pycache__/runner.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/test/__pycache__/testcases.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/test/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/test/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/dispatch/__pycache__/dispatcher.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/urls/__pycache__/static.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/urls/__pycache__/i18n.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/eu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/uz/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/tt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/zh_Hans/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/os/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/id/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ga/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/cs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/vi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ckb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ky/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/bg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/he/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/pl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/pt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/dsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/mn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/uk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ast/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/pa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ne/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/be/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/hy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/nl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/es_VE/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ia/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/tg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/zh_Hant/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/gl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ml/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/sr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/is/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/lb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/udm/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/sk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/nb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/tr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/br/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/km/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/sl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/es_CO/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/lt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/sr_Latn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ms/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/gd/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/hsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ig/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ar_DZ/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ka/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/hi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ta/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/th/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ja/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/fi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/kk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/cy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/sq/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/fy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/nn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/te/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/mk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ro/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/bs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/es_AR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/hu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/sv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/lv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/az/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/kn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/en_GB/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/bn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/io/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/en_AU/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/es_MX/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/kab/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ur/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/tk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/sw/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/hr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/af/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ko/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/eo/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/et/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/el/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/da/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/urls/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/urls/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/urls/__pycache__/resolvers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/base_user.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/context_processors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/hashers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/backends.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/tokens.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/password_validation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/decorators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/management/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/management/commands/__pycache__/createsuperuser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/migrations/__pycache__/0001_initial.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/eu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/zh_Hans/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/os/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/id/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ga/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/cs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/vi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ckb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ky/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/bg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/he/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/pl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/pt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/dsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/mn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/uk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ast/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/pa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ne/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/be/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/hy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/nl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/es_VE/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ia/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/tg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/zh_Hant/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/gl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ml/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/sr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/is/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/sk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/nb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/tr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/km/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/sl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/es_CO/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/lt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/sr_Latn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ms/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/gd/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/hsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ar_DZ/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ka/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/hi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ta/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/th/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ja/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/fi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/kk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/cy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/sq/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/nn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/te/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/mk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ro/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/bs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/es_AR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/hu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/sv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/lv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/az/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/kn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/en_GB/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/bn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/en_AU/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/es_MX/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/kab/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/tk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/sw/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/hr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/af/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ko/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/eo/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/et/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/el/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/da/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/handlers/__pycache__/modwsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/sites/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/sites/__pycache__/shortcuts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/sites/__pycache__/managers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/humanize/templatetags/__pycache__/humanize.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/sessions/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/sessions/__pycache__/base_session.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/sessions/backends/__pycache__/file.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/sessions/backends/__pycache__/db.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/sessions/backends/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/__pycache__/shortcuts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/__pycache__/measure.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/__pycache__/feeds.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/utils/__pycache__/ogrinspect.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/utils/__pycache__/layermapping.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/datasource.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/libgdal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/field.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/srs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/layer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/geometries.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/feature.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/envelope.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/error.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/geomtype.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/driver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/prototypes/__pycache__/srs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/prototypes/__pycache__/generation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/prototypes/__pycache__/errcheck.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/raster/__pycache__/band.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/raster/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/gdal/raster/__pycache__/source.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geos/__pycache__/libgeos.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geos/__pycache__/collections.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geos/__pycache__/mutable_list.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geos/__pycache__/polygon.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geos/__pycache__/factory.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geos/__pycache__/io.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geos/__pycache__/geometry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geos/__pycache__/coordseq.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geos/__pycache__/point.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geos/__pycache__/linestring.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geos/prototypes/__pycache__/io.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geos/prototypes/__pycache__/coordseq.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geos/prototypes/__pycache__/geom.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geos/prototypes/__pycache__/misc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geos/prototypes/__pycache__/errcheck.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geoip2/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/forms/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/models/__pycache__/lookups.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/models/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/spatialite/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/spatialite/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/mysql/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/oracle/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/oracle/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/base/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/base/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/base/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/postgis/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/postgis/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/postgis/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/postgis/__pycache__/adapter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/sitemaps/__pycache__/kml.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/sitemaps/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/management/commands/__pycache__/ogrinspect.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/admin/__pycache__/options.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/postgres/__pycache__/indexes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/postgres/__pycache__/signals.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/postgres/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/postgres/__pycache__/constraints.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/postgres/forms/__pycache__/hstore.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/postgres/aggregates/__pycache__/general.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/postgres/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/sitemaps/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/contenttypes/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/contenttypes/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/contenttypes/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/syndication/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/__pycache__/sites.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/__pycache__/checks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/__pycache__/widgets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/__pycache__/filters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/__pycache__/decorators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/__pycache__/options.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/templatetags/__pycache__/log.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/templatetags/__pycache__/admin_modify.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/templatetags/__pycache__/admin_list.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/id/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/cs/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/bg/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/nl/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ia/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ca/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ru/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/fi/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/es_AR/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/sv/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/eo/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/views/__pycache__/main.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/views/__pycache__/autocomplete.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admindocs/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admindocs/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admindocs/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/messages/storage/__pycache__/fallback.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/messages/storage/__pycache__/session.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/messages/storage/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/messages/storage/__pycache__/cookie.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/messages/__pycache__/context_processors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/messages/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/messages/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/redirects/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/staticfiles/__pycache__/handlers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/staticfiles/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/staticfiles/__pycache__/urls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/staticfiles/__pycache__/finders.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/staticfiles/__pycache__/storage.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/staticfiles/management/commands/__pycache__/runserver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/staticfiles/management/commands/__pycache__/findstatic.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/flatpages/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/flatpages/templatetags/__pycache__/flatpages.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/views/__pycache__/defaults.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/views/__pycache__/csrf.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/views/__pycache__/static.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/views/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/views/__pycache__/i18n.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/views/generic/__pycache__/edit.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/views/generic/__pycache__/detail.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/views/generic/__pycache__/list.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/views/generic/__pycache__/dates.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/views/generic/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/views/decorators/__pycache__/http.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tzlocal/__pycache__/win32.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tzlocal/__pycache__/unix.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/__pycache__/hash_ring.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/__pycache__/pool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/client/__pycache__/sharded.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/client/__pycache__/herd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/client/__pycache__/default.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/serializers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/serializers/__pycache__/pickle.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/serializers/__pycache__/msgpack.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/serializers/__pycache__/json.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/compressors/__pycache__/zlib.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/compressors/__pycache__/lzma.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/compressors/__pycache__/lz4.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/compressors/__pycache__/zstd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/compressors/__pycache__/gzip.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/compressors/__pycache__/identity.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/compressors/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/reverse.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/request.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/renderers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/metadata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/settings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/routers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/filters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/permissions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/generics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/relations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/pagination.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/negotiation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/viewsets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/throttling.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/test.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/status.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/authentication.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/parsers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/utils/__pycache__/timezone.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/utils/__pycache__/model_meta.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/utils/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/utils/__pycache__/field_mapping.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/utils/__pycache__/encoders.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/utils/__pycache__/formatting.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/utils/__pycache__/mediatypes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/utils/__pycache__/urls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/utils/__pycache__/serializer_helpers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/utils/__pycache__/breadcrumbs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/schemas/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/schemas/__pycache__/coreapi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/schemas/__pycache__/generators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/schemas/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/schemas/__pycache__/openapi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/templatetags/__pycache__/rest_framework.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/ne_NP/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/zh_Hans/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/ru_RU/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/id/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/cs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/bg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/pl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/pt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/uk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/hy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/nl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/tr_TR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/zh_Hant/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/sk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/nb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/tr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/sl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/fa_IR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/en/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/zh_CN/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/th/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/ja/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/fi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/kk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/mk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/ro/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/hu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/sv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/ko_KR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/lv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/az/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/et/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/el/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/da/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/plugin_support.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/patch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/report.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/data.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/collector.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/cmdline.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/multiproc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/version.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/pytracer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/sysmon.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/results.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/regions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/lcovreport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/xmlreport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/types.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/templite.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/numbits.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/report_core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/jsonreport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/tomlconfig.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/plugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/execfile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/disposition.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/env.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/annotate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/bytecode.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/files.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/sqlitedb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/misc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/inorout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/sqldata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/phystokens.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/context.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/tracer.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/__pycache__/resources.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/__pycache__/widgets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/__pycache__/results.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/formats/__pycache__/base_formats.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/zh_Hans/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/cs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/bg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/he/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/pl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/uk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/kz/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/nl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/sk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/tr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/ja/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/fi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/es_AR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/ko/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/fd7dcdb10166ebd4db98__mypyc.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/__pycache__/arbiter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/__pycache__/errors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/__pycache__/sock.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/__pycache__/glogging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/__pycache__/systemd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/http2/__pycache__/request.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/http2/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/http2/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/http2/__pycache__/errors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/http2/__pycache__/async_connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/http2/__pycache__/stream.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/asgi/__pycache__/lifespan.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/asgi/__pycache__/unreader.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/asgi/__pycache__/uwsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/asgi/__pycache__/message.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/asgi/__pycache__/websocket.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/asgi/__pycache__/protocol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/http/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/http/__pycache__/message.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/http/__pycache__/parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/http/__pycache__/wsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/instrument/__pycache__/statsd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/workers/__pycache__/gasgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/workers/__pycache__/gthread.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/workers/__pycache__/ggevent.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/workers/__pycache__/base_async.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/workers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/dirty/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/dirty/__pycache__/arbiter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/dirty/__pycache__/app.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/dirty/__pycache__/errors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/dirty/__pycache__/stash.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/dirty/__pycache__/protocol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/dirty/__pycache__/worker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/dirty/__pycache__/tlv.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/dirty/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/ctl/__pycache__/cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/ctl/__pycache__/handlers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/ctl/__pycache__/protocol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/ctl/__pycache__/server.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/ctl/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dj_database_url/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2/__pycache__/_json.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2/__pycache__/sql.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2/__pycache__/extensions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2/__pycache__/tz.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2/__pycache__/extras.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2/__pycache__/errors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2/__pycache__/pool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2/__pycache__/errorcodes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2/__pycache__/_range.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2/_psycopg.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dotenv/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dotenv/__pycache__/main.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dotenv/__pycache__/cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dotenv/__pycache__/variables.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dotenv/__pycache__/parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/jwt/__pycache__/api_jwk.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/jwt/__pycache__/api_jws.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/jwt/__pycache__/jwk_set_cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/jwt/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/jwt/__pycache__/jwks_client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/jwt/__pycache__/algorithms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/jwt/__pycache__/help.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/jwt/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/jwt/__pycache__/api_jwt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/vine/__pycache__/funtools.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/vine/__pycache__/promises.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/factory/__pycache__/random.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/factory/__pycache__/builder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/factory/__pycache__/fuzzy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/factory/__pycache__/declarations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/factory/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/_internal_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/status_codes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/cookies.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/adapters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/structures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/certs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/auth.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/help.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/sessions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/et_xmlfile/__pycache__/incremental_tree.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/30fcd23745efe32ce681__mypyc.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libldap-1accf1ee.so.2.0.200: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libkrb5-fcafa220.so.3.3: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libcrypto-81d66ed9.so.3: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libssl-81ffa89e.so.3: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libselinux-0922c95c.so.1: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libk5crypto-b1f99d5c.so.3.1: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libkrb5support-d0bcff84.so.0.1: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libsasl2-883649fd.so.3.0.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libgssapi_krb5-497db0c6.so.2.2: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libpq-9b38f5e3.so.5.17: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/security/__pycache__/certificate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/local.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/schedules.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/canvas.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/states.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/bootsteps.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/_state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/platforms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/result.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/beat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/__main__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/timer2.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/log.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/sysinfo.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/imports.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/collections.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/functional.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/time.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/iso8601.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/serialization.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/quorum_queues.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/threads.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/graph.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/term.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/objects.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/nodenames.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/annotations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/saferepr.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/dispatch/__pycache__/signal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/__pycache__/request.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/__pycache__/loops.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/__pycache__/control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/__pycache__/components.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/__pycache__/heartbeat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/__pycache__/strategy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/__pycache__/autoscale.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/__pycache__/worker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/__pycache__/pidbox.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/__pycache__/state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/consumer/__pycache__/consumer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/consumer/__pycache__/delayed_delivery.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/consumer/__pycache__/tasks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/consumer/__pycache__/gossip.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/consumer/__pycache__/mingle.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/events/__pycache__/cursesmon.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/events/__pycache__/state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/events/__pycache__/snapshot.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/events/__pycache__/dispatcher.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/apps/__pycache__/multi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/apps/__pycache__/beat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/apps/__pycache__/worker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/concurrency/__pycache__/thread.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/concurrency/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/concurrency/__pycache__/asynpool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/concurrency/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/concurrency/__pycache__/prefork.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/fixups/__pycache__/django.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/bin/__pycache__/events.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/bin/__pycache__/celery.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/bin/__pycache__/control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/bin/__pycache__/migrate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/bin/__pycache__/multi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/bin/__pycache__/result.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/bin/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/bin/__pycache__/worker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/log.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/events.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/defaults.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/backends.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/registry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/task.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/amqp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/trace.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/cosmosdbsql.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/arangodb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/elasticsearch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/dynamodb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/rpc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/asynchronous.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/azureblockblob.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/mongodb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/redis.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/gcs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/cassandra.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/database/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/database/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/contrib/__pycache__/rdb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/contrib/__pycache__/migrate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/contrib/__pycache__/abortable.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/contrib/__pycache__/pytest.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/contrib/testing/__pycache__/app.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/contrib/testing/__pycache__/tasks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/contrib/testing/__pycache__/worker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/contrib/testing/__pycache__/mocks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/contrib/testing/__pycache__/manager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/contrib/django/__pycache__/task.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/asgiref/__pycache__/local.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/asgiref/__pycache__/typing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/asgiref/__pycache__/timeout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/asgiref/__pycache__/testing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/asgiref/__pycache__/current_thread_executor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/asgiref/__pycache__/compatibility.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/asgiref/__pycache__/sync.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/asgiref/__pycache__/server.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/asgiref/__pycache__/wsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tools/__pycache__/resx2po.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click_didyoumean/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click_plugins/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/backends.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/settings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/tokens.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/authentication.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/token_blacklist/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/token_blacklist/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/token_blacklist/management/commands/__pycache__/flushexpiredtokens.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_cov/__pycache__/engine.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/idna/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/idna/__pycache__/codec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/idna/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/idna/__pycache__/intranges.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/idna/__pycache__/uts46data.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/cron_descriptor/__pycache__/StringBuilder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/cron_descriptor/__pycache__/Options.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/cron_descriptor/__pycache__/GetText.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/cron_descriptor/__pycache__/Exception.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/cron_descriptor/__pycache__/ExpressionValidator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/cron_descriptor/__pycache__/ExpressionDescriptor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/cron_descriptor/__pycache__/ExpressionParser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/__pycache__/typing.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/__pycache__/cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/__pycache__/typing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/__pycache__/factory.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/__pycache__/generator.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/__pycache__/proxy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/__pycache__/factory.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/__pycache__/documentor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/__pycache__/proxy.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/__pycache__/generator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/__pycache__/exceptions.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/utils/__pycache__/text.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/utils/__pycache__/datasets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/utils/__pycache__/text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/utils/__pycache__/distribution.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/utils/__pycache__/decorators.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/utils/__pycache__/checksums.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/utils/__pycache__/datasets.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/utils/__pycache__/decorators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/utils/__pycache__/loading.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/utils/__pycache__/loading.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/utils/__pycache__/distribution.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/decode/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/decode/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/sphinx/__pycache__/validator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/passport/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/passport/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/passport/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/passport/it_IT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/passport/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/passport/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/isbn/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/isbn/__pycache__/isbn.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/isbn/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/isbn/__pycache__/isbn.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/lorem/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/lorem/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/lorem/cs_CZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/lorem/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/lorem/it_IT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/lorem/pl_PL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/lorem/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/lorem/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/el_GR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/nl_NL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/fr_CA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/ro_RO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/uk_UA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/cs_CZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/tr_TR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/ng_NG/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/fa_IR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/es_ES/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/uz_UZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/es_AR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/vi_VN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/pl_PL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/en_AU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/currency/pt_BR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/sbn/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/sbn/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/sbn/__pycache__/sbn.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/sbn/__pycache__/sbn.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/fr_FR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/ar_AA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/fr_CA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/ta_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/gu_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/hr_HR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/id_ID/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/hu_HU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/uz_UZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/no_NO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/ko_KR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/sl_SI/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/zh_TW/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/th_TH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/ja_JP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/date_time/hi_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/ar_PS/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/el_GR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/nl_NL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/ro_RO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/ar_SA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/uk_UA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/tr_TR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/ar_JO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/sk_SK/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/es_ES/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/es_AR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/vi_VN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/ko_KR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/pl_PL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/de_DE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/de_CH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/th_TH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/ja_JP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/automotive/az_AZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/profile/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/profile/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/job/fr_FR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/job/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/job/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/job/ro_RO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/job/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/job/cs_CZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/job/hu_HU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/job/sk_SK/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/job/vi_VN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/fr_FR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/ar_PS/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/en_NZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/ar_JO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/it_IT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/ar_AE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/en_GB/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/en_AU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/de_LU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/de_CH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/pt_BR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/phone_number/az_AZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/bank/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/bank/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/bank/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/bank/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/bank/en_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/bank/nl_BE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/bank/es_MX/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/bank/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/barcode/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/barcode/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/barcode/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/barcode/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/barcode/ja_JP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/fr_FR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/nl_NL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/fil_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/ro_RO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/fr_CH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/id_ID/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/tr_TR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/hu_HU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/fa_IR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/it_IT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/es_ES/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/vi_VN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/ko_KR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/pl_PL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/zh_TW/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/es_MX/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/fi_FI/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/th_TH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/ja_JP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/pt_BR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/az_AZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/fr_QC/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/pt_PT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/is_IS/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/uk_UA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/hu_HU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/fa_IR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/vi_VN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/pl_PL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/zh_TW/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/de_DE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/ja_JP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/or_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/et_EE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/person/az_AZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/emoji/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/emoji/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/geo/el_GR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/geo/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/geo/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/geo/pt_PT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/geo/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/geo/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/user_agent/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/user_agent/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/ne_NP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/fr_FR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/el_GR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/sv_SE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/nl_NL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/pt_PT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/zu_ZA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/fr_CA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/ro_RO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/da_DK/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/en_NZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/fr_CH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/ta_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/en_IE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/hr_HR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/ka_GE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/id_ID/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/uk_UA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/cs_CZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/en_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/hy_AM/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/en_CA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/es_CO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/hu_HU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/sk_SK/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/fa_IR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/en_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/en/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/en/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/it_IT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/es_ES/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/en_MS/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/nl_BE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/no_NO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/es_AR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/vi_VN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/ko_KR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/pl_PL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/sl_SI/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/en_GB/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/zh_TW/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/de_DE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/en_AU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/es_MX/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/fi_FI/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/he_IL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/de_CH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/th_TH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/ja_JP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/pt_BR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/az_AZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/address/hi_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/doi/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/doi/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/file/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/file/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/color/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/color/__pycache__/color.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/color/__pycache__/color.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/color/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/python/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/python/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/misc/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/misc/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/misc/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/internet/el_GR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/internet/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/internet/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/internet/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/internet/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/internet/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/internet/ja_JP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/fr_FR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/el_GR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/sv_SE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/el_CY/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/bg_BG/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/nl_NL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/pt_PT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/ro_RO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/fr_CH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/en_IE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/hr_HR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/mt_MT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/lv_LV/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/uk_UA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/cs_CZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/tr_TR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/lt_LT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/en_CA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/es_CO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/hu_HU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/sk_SK/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/en_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/it_IT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/es_ES/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/dk_DK/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/lb_LU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/nl_BE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/no_NO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/pl_PL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/sl_SI/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/en_GB/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/zh_TW/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/de_DE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/es_MX/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/fi_FI/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/he_IL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/th_TH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/pt_BR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/et_EE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/ssn/az_AZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/credit_card/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/credit_card/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/credit_card/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/credit_card/uk_UA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/credit_card/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/contrib/pytest/__pycache__/plugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/contrib/pytest/__pycache__/plugin.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/formats/__pycache__/_html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/formats/__pycache__/_latex.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/formats/__pycache__/_json.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/formats/__pycache__/_cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/formats/__pycache__/_csv.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/formats/__pycache__/_sql.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/formats/__pycache__/_xlsx.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/formats/__pycache__/_ods.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/formats/__pycache__/_df.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/formats/__pycache__/_rst.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/formats/__pycache__/_dbf.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/formats/__pycache__/_xls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/formats/__pycache__/_yaml.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/_vendor/dbfpy/__pycache__/header.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/_vendor/dbfpy/__pycache__/dbfnew.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/_vendor/dbfpy/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/_vendor/dbfpy/__pycache__/dbf.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/_vendor/dbfpy/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tablib/_vendor/dbfpy/__pycache__/record.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/shell_completion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/testing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/termui.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/_winconsole.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/types.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/_termui_impl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/_textwrap.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/formatting.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/_compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/decorators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/globals.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/__pycache__/formatter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/__pycache__/modeline.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/__pycache__/lexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/__pycache__/scanner.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/__pycache__/sphinxext.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/__pycache__/regexopt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/__pycache__/token.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/filters/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/styles/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/lisp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/haxe.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/solidity.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/forth.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_stan_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_qlik_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/matlab.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/sophia.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/graphics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/boa.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/c_like.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/supercollider.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_julia_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/d.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_tsql_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/blueprint.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/inferno.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_cocoa_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/ncl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_css_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/igor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/idl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_mysql_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/textedit.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/felix.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/pawn.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/markup.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/ampl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/fantom.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/devicetree.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/templates.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_googlesql_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_php_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/zig.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/sql.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/tact.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/spice.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/scdoc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/asm.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/macaulay2.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/slash.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/gsql.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/dsls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_ada_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/hdl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/business.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/verification.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/phix.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/theorem.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/scripting.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/basic.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/configs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/wgsl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/wren.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/dotnet.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_sourcemod_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_sql_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/c_cpp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/parasail.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/carbon.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_openedge_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/r.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/haskell.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/unicon.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/trafficscript.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/vyper.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_cl_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_lua_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/shell.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/wowtoc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/berry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/installers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/factor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/tcl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/praat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/jvm.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/javascript.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/esoteric.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/hare.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/fortran.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/ecl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/varnish.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/grammar_notation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/chapel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/perl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_lilypond_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/snobol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/modeling.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_stata_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_postgres_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/dax.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/func.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_lasso_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/console.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/algebra.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/openscad.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/arrow.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/qvt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/kuin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/textfmts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/tnt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/ptx.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_mql_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/ooc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/typst.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/maple.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_scilab_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/pony.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/webassembly.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/teal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/actionscript.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/comal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/mojo.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/urbi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/crystal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/oberon.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/graph.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/yang.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/nimrod.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/pascal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/clean.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/monte.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/int_fiction.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/sas.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/dylan.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/rust.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/go.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/gdscript.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/php.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/x10.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/rebol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/modula2.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_vim_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/automation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/mosel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/objective.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/apdlexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/csound.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/qlik.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/whiley.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/robotframework.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/dalvik.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/ruby.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/arturo.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_csound_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/nit.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_scheme_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/j.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_mapping.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/css.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/teraterm.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/webmisc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/parsers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/erlang.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/foxpro.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/formatters/__pycache__/latex.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/formatters/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/formatters/__pycache__/img.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/formatters/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pyflakes/__pycache__/messages.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pyflakes/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pyflakes/__pycache__/checker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pyflakes/test/__pycache__/test_match.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pyflakes/test/__pycache__/test_builtin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pyflakes/test/__pycache__/test_type_annotations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pyflakes/test/__pycache__/test_undefined_names.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pyflakes/test/__pycache__/test_api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pyflakes/test/__pycache__/test_other.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pyflakes/test/__pycache__/test_doctests.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pyflakes/test/__pycache__/test_imports.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/_io/__pycache__/pprint.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/_io/__pycache__/terminalwriter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/_io/__pycache__/wcwidth.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/_io/__pycache__/saferepr.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/python_api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/tracemalloc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/terminal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/fixtures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/outcomes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/tmpdir.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/runner.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/monkeypatch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/main.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/stepwise.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/unraisableexception.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/faulthandler.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/terminalprogress.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/debugging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/skipping.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/hookspec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/doctest.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/pytester.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/setuponly.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/pytester_assertions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/setupplan.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/subtests.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/timing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/nodes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/scope.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/warnings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/recwarn.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/warning_types.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/unittest.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/reports.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/logging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/stash.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/capture.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/freeze_support.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/_argcomplete.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/deprecated.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/pathlib.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/threadexception.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/junitxml.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/raises.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/cacheprovider.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/pastebin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/legacypath.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/helpconfig.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/_code/__pycache__/code.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/_code/__pycache__/source.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/_py/__pycache__/path.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/_py/__pycache__/error.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/config/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/config/__pycache__/findpaths.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/config/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/config/__pycache__/argparsing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/mark/__pycache__/expression.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/mark/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/mark/__pycache__/structures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/assertion/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/assertion/__pycache__/truncate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/assertion/__pycache__/rewrite.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/assertion/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/liblcms2-cc10e42f.so.2.0.17: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libwebpmux-7f11e5ce.so.3.1.2: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libjpeg-32d42e18.so.62.4.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libzstd-761a17b6.so.1.5.7: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libharfbuzz-0692f733.so.0.61230.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libpng16-4a38ea05.so.16.53.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libtiff-295fd75c.so.6.2.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libwebp-d8b9687f.so.7.2.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libavif-01e67780.so.16.3.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libopenjp2-94e588ba.so.2.5.4: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libfreetype-ee1c40c4.so.6.20.4: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libbrotlicommon-c55a5f7a.so.1.2.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/poolmanager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/connectionpool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/filepost.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/_base_connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/_collections.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/_request_methods.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/http2/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/http2/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/http2/__pycache__/probe.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/request.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/ssl_.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/timeout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/ssltransport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/ssl_match_hostname.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/proxy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/wait.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/url.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/retry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/contrib/__pycache__/socks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/contrib/__pycache__/pyopenssl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/contrib/emscripten/__pycache__/request.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/contrib/emscripten/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/contrib/emscripten/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/contrib/emscripten/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/contrib/emscripten/__pycache__/fetch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/platformdirs/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/platformdirs/__pycache__/macos.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/platformdirs/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/platformdirs/__pycache__/android.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/platformdirs/__pycache__/unix.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/platformdirs/__pycache__/__main__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/platformdirs/__pycache__/_xdg.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/platformdirs/__pycache__/windows.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/iniconfig/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/iniconfig/__pycache__/_parse.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/iniconfig/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/__pycache__/cronlog.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/__pycache__/click_plugins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/__pycache__/crontabs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/__pycache__/pycodestyle.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/__pycache__/crontab.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/__pycache__/mccabe.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/__pycache__/mypy_extensions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/__pycache__/six.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/__pycache__/typing_extensions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/certifi/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/diff_match_patch/__pycache__/diff_match_patch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/whitenoise/__pycache__/responders.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/whitenoise/__pycache__/compress.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/whitenoise/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/whitenoise/__pycache__/media_types.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/whitenoise/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/whitenoise/__pycache__/storage.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/whitenoise/runserver_nostatic/management/commands/__pycache__/runserver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/__pycache__/processor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/__pycache__/style_guide.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/__pycache__/statistics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/__pycache__/checker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/__pycache__/violation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/__pycache__/discover_files.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/formatting/__pycache__/_windows_color.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/formatting/__pycache__/default.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/formatting/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/options/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/options/__pycache__/parse_args.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/options/__pycache__/aggregator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/options/__pycache__/manager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/api/__pycache__/legacy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/main/__pycache__/cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/main/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/main/__pycache__/application.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/main/__pycache__/options.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/plugins/__pycache__/pyflakes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/plugins/__pycache__/pycodestyle.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/plugins/__pycache__/finder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/flake8/plugins/__pycache__/reporter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/widget_tweaks/templatetags/__pycache__/widget_tweaks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytokens/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytokens/__pycache__/cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/fixtures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/live_server_helper.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/lazy_django.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/runner.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/live_server_helper.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/django_compat.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/django_compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/plugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/plugin.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/lazy_django.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/asserts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/fixtures.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blib2to3/__pycache__/pytree.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blib2to3/__pycache__/pygram.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blib2to3/pgen2/__pycache__/parse.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blib2to3/pgen2/__pycache__/grammar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blib2to3/pgen2/__pycache__/literals.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blib2to3/pgen2/__pycache__/tokenize.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blib2to3/pgen2/__pycache__/conv.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blib2to3/pgen2/__pycache__/driver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blib2to3/pgen2/__pycache__/token.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blib2to3/pgen2/__pycache__/pgen.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/__pycache__/__pip-runner__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/__pycache__/wheel_builder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/__pycache__/main.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/__pycache__/self_outdated_check.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/__pycache__/configuration.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/__pycache__/pyproject.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/__pycache__/build_env.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/index/__pycache__/package_finder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/index/__pycache__/sources.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/index/__pycache__/collector.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/compatibility_tags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/unpacking.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/deprecation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/setuptools_build.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/filesystem.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/direct_url_helpers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/appdirs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/_log.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/virtualenv.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/temp_dir.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/glibc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/hashes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/logging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/entrypoints.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/packaging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/encoding.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/datetime.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/egg_link.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/urls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/misc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/subprocess.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/filetypes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/resolution/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/resolution/legacy/__pycache__/resolver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/requirements.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/provider.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/factory.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/resolver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/found_candidates.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/reporter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/candidates.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/locations/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/locations/__pycache__/_sysconfig.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/locations/__pycache__/_distutils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/locations/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/models/__pycache__/scheme.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/models/__pycache__/installation_report.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/models/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/models/__pycache__/link.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/models/__pycache__/format_control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/models/__pycache__/candidate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/models/__pycache__/direct_url.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/models/__pycache__/target_python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/models/__pycache__/index.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/models/__pycache__/search_scope.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/models/__pycache__/selection_prefs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/req/__pycache__/constructors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/req/__pycache__/req_uninstall.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/req/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/req/__pycache__/req_file.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/req/__pycache__/req_install.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/req/__pycache__/req_set.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/cli/__pycache__/status_codes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/cli/__pycache__/main.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/cli/__pycache__/progress_bars.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/cli/__pycache__/cmdoptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/cli/__pycache__/req_command.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/cli/__pycache__/spinners.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/cli/__pycache__/autocompletion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/cli/__pycache__/parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/cli/__pycache__/base_command.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/cli/__pycache__/command_context.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/cli/__pycache__/main_parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/freeze.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/list.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/show.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/inspect.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/download.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/hash.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/check.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/completion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/install.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/configuration.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/search.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/help.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/index.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/uninstall.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/vcs/__pycache__/subversion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/vcs/__pycache__/mercurial.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/vcs/__pycache__/versioncontrol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/vcs/__pycache__/git.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/vcs/__pycache__/bazaar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/distributions/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/distributions/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/distributions/__pycache__/installed.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/distributions/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/distributions/__pycache__/sdist.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/metadata/__pycache__/_json.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/metadata/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/metadata/__pycache__/pkg_resources.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/metadata/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/metadata/importlib/__pycache__/_dists.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/metadata/importlib/__pycache__/_envs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/metadata/importlib/__pycache__/_compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/network/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/network/__pycache__/download.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/network/__pycache__/lazy_wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/network/__pycache__/session.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/network/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/network/__pycache__/auth.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/network/__pycache__/xmlrpc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/operations/__pycache__/freeze.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/operations/__pycache__/prepare.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/operations/__pycache__/check.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/operations/install/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/operations/install/__pycache__/editable_legacy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/operations/build/__pycache__/metadata_editable.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/operations/build/__pycache__/build_tracker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/operations/build/__pycache__/metadata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/operations/build/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/operations/build/__pycache__/metadata_legacy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/operations/build/__pycache__/wheel_editable.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/operations/build/__pycache__/wheel_legacy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/webencodings/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/testing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/results.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/helpers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/actions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pyparsing/diagram/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/poolmanager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/connectionpool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/filepost.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/_collections.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/packages/__pycache__/six.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/packages/backports/__pycache__/weakref_finalize.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/ssl_.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/timeout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/ssl_match_hostname.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/proxy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/wait.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/url.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/retry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/contrib/__pycache__/ntlmpool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/contrib/__pycache__/securetransport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/contrib/__pycache__/appengine.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/contrib/__pycache__/pyopenssl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/contrib/_securetransport/__pycache__/low_level.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/contrib/_securetransport/__pycache__/bindings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/platformdirs/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/platformdirs/__pycache__/macos.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/platformdirs/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/platformdirs/__pycache__/android.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/platformdirs/__pycache__/unix.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/platformdirs/__pycache__/__main__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/platformdirs/__pycache__/windows.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/__pycache__/six.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/__pycache__/typing_extensions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/sbcsgroupprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/eucjpprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/codingstatemachine.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/codingstatemachinedict.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/chardistribution.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/escsm.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/big5prober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/euckrprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/utf8prober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/hebrewprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/escprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/utf1632prober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/mbcsgroupprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/mbcssm.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/sjisprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/macromanprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/euctwprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/sbcharsetprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/jpcntx.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/universaldetector.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/charsetprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/gb2312prober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/johabprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/charsetgroupprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/mbcharsetprober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/enums.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/cp949prober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/latin1prober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/cli/__pycache__/chardetect.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/metadata/__pycache__/languages.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/certifi/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pyproject_hooks/__pycache__/_impl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pyproject_hooks/_in_process/__pycache__/_in_process.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/segment.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/live_render.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/style.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/prompt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/layout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/ansi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/traceback.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/abc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/theme.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/markup.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_inspect.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/emoji.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_log_render.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/progress.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/repr.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/cells.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/color.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_wrap.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/progress_bar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/scope.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_pick.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_loop.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_timer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/palette.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/color_triplet.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_fileno.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/measure.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/bar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/pager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/table.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/pretty.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/logging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/rule.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_ratio.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/styled.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/spinner.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/highlighter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_windows_renderer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_emoji_codes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/padding.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/columns.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_stack.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/console.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/filesize.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/protocol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_extension.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_null_file.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/terminal_theme.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/diagnose.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/constrain.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/tree.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_emoji_replace.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/align.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_windows.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/jupyter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_win32_console.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/default_styles.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/json.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/file_proxy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/status.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/syntax.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/screen.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/box.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/__main__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/panel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/containers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/live.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/packaging/__pycache__/tags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/packaging/__pycache__/requirements.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/packaging/__pycache__/specifiers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/packaging/__pycache__/_structures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/packaging/__pycache__/version.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/packaging/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/packaging/__pycache__/markers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/packaging/__pycache__/_musllinux.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/packaging/__pycache__/_manylinux.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distro/__pycache__/distro.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/serialize.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/filewrapper.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/wrapper.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/heuristics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/controller.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/adapter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/_cmd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/cachecontrol/caches/__pycache__/file_cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/cachecontrol/caches/__pycache__/redis_cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/tomli/__pycache__/_parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/tomli/__pycache__/_re.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/tornadoweb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/after.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/nap.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/before.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/stop.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/_asyncio.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/wait.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/before_sleep.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/tenacity/__pycache__/retry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/colorama/__pycache__/initialise.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/colorama/__pycache__/ansitowin32.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/colorama/tests/__pycache__/initialise_test.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/colorama/tests/__pycache__/winterm_test.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/colorama/tests/__pycache__/ansitowin32_test.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/_internal_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/status_codes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/cookies.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/adapters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/structures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/certs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/auth.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/help.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/sessions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/idna/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/idna/__pycache__/codec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/idna/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/idna/__pycache__/intranges.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/idna/__pycache__/uts46data.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/resources.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/locators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/metadata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/manifest.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/scripts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/version.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/markers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/database.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/index.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_macos.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_openssl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_ssl_constants.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_windows.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/resolvelib/__pycache__/structs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/resolvelib/__pycache__/reporters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/resolvelib/__pycache__/providers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/resolvelib/__pycache__/resolvers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/msgpack/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/msgpack/__pycache__/fallback.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/msgpack/__pycache__/ext.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/__pycache__/formatter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/__pycache__/modeline.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/__pycache__/lexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/__pycache__/scanner.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/__pycache__/sphinxext.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/__pycache__/regexopt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/__pycache__/token.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/filters/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/styles/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/lexers/__pycache__/python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/lexers/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/lexers/__pycache__/_mapping.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/formatters/__pycache__/latex.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/formatters/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/formatters/__pycache__/img.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/formatters/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pkg_resources/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/timezone_field/__pycache__/choices.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/timezone_field/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/timezone_field/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/tags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/_parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/metadata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/requirements.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/_elffile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/specifiers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/_structures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/_tokenizer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/version.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/pylock.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/markers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/_musllinux.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/_manylinux.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/licenses/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/charset_normalizer/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/charset_normalizer/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/charset_normalizer/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/charset_normalizer/__pycache__/md.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/charset_normalizer/__pycache__/legacy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/charset_normalizer/__pycache__/cd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/charset_normalizer/cli/__pycache__/__main__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/charset_normalizer/md__mypyc.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/__pycache__/backend.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/__pycache__/_typing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/__pycache__/gitignore.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/__pycache__/pathspec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/__pycache__/pattern.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/_backends/__pycache__/_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/_backends/__pycache__/agg.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/_backends/simple/__pycache__/gitignore.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/_backends/simple/__pycache__/pathspec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/_backends/hyperscan/__pycache__/gitignore.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/_backends/hyperscan/__pycache__/pathspec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/_backends/re2/__pycache__/gitignore.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/_backends/re2/__pycache__/pathspec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/patterns/__pycache__/gitwildmatch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/patterns/gitignore/__pycache__/spec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/patterns/gitignore/__pycache__/basic.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/patterns/gitignore/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/wcwidth/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/wcwidth/__pycache__/bisearch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/wcwidth/__pycache__/grapheme.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/wcwidth/__pycache__/unicode_versions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/wcwidth/__pycache__/textwrap.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/wcwidth/__pycache__/wcwidth.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/wcwidth/__pycache__/sgr_state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/crispy_forms/__pycache__/layout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/crispy_forms/__pycache__/bootstrap.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/crispy_forms/__pycache__/layout_slice.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/crispy_forms/__pycache__/helper.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/crispy_forms/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/crispy_forms/templatetags/__pycache__/crispy_forms_filters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/crispy_forms/templatetags/__pycache__/crispy_forms_field.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/crispy_forms/templatetags/__pycache__/crispy_forms_tags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/drawing/__pycache__/image.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/drawing/__pycache__/geometry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/drawing/__pycache__/fill.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/drawing/__pycache__/spreadsheet_drawing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/utils/__pycache__/cell.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/utils/__pycache__/indexed_list.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/utils/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/packaging/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/packaging/__pycache__/workbook.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/packaging/__pycache__/relationship.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/chartsheet/__pycache__/chartsheet.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/chartsheet/__pycache__/custom.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/worksheet/__pycache__/header_footer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/worksheet/__pycache__/cell_range.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/worksheet/__pycache__/filters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/worksheet/__pycache__/_reader.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/worksheet/__pycache__/table.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/worksheet/__pycache__/protection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/worksheet/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/worksheet/__pycache__/dimensions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/worksheet/__pycache__/worksheet.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/worksheet/__pycache__/_writer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/worksheet/__pycache__/_read_only.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/chart/__pycache__/reference.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/pivot/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/pivot/__pycache__/table.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/descriptors/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/reader/__pycache__/workbook.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/reader/__pycache__/excel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/cell/__pycache__/cell.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/cell/__pycache__/rich_text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/formula/__pycache__/tokenizer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/formula/__pycache__/translate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/styles/__pycache__/numbers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/styles/__pycache__/differential.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/styles/__pycache__/proxy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/styles/__pycache__/named_styles.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/workbook/__pycache__/workbook.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/workbook/__pycache__/protection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/workbook/__pycache__/defined_name.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/workbook/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/workbook/__pycache__/_writer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/comments/__pycache__/comment_sheet.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/amqp/__pycache__/spec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/amqp/__pycache__/platform.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/amqp/__pycache__/abstract_channel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/amqp/__pycache__/serialization.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/amqp/__pycache__/protocol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/amqp/__pycache__/sasl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/amqp/__pycache__/channel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/amqp/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/amqp/__pycache__/method_framing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/PcfFontFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageStat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/JpegImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ContainerIO.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/TiffTags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/BufrStubImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/XVThumbImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/PSDraw.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/PpmImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/MpegImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/XbmImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/BlpImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/PcdImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageMorph.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/FitsImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageCms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/PcxImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/_typing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageChops.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/WalImageFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/GribStubImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageFilter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/QoiImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageDraw2.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImagePalette.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/JpegPresets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/SpiderImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/Jpeg2KImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/PalmImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/SunImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/MpoImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/PdfParser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageGrab.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/FontFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/GimpGradientFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/MspImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImtImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/GimpPaletteFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageTransform.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/IcoImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/PaletteFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/CurImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/EpsImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/TarIO.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/XpmImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageQt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/FpxImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/WebPImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageShow.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/AvifImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/_binary.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageWin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageColor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageFont.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/McIdasImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/MicImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/Image.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageOps.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/WmfImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ExifTags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/BdfFontFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageSequence.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/TiffImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/_deprecate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageEnhance.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/TgaImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/FliImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/PngImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/_util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/DcxImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/PdfImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageDraw.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageText.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/PsdImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/IptcImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageMode.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/BmpImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/GbrImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/GdImageFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageMath.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/FtexImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageTk.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/IcnsImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/SgiImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/DdsImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/PixarImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/GifImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/Hdf5StubImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/_imagingtk.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/_imaging.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/_avif.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/_imagingmorph.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/_webp.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/_imagingcms.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/_imagingft.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/_imagingmath.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dateutil/__pycache__/relativedelta.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dateutil/__pycache__/rrule.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dateutil/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dateutil/tz/__pycache__/tz.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dateutil/tz/__pycache__/win.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dateutil/tz/__pycache__/_common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dateutil/tz/__pycache__/_factories.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dateutil/zoneinfo/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dateutil/parser/__pycache__/_parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dateutil/parser/__pycache__/isoparser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/auth/__pycache__/idp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/auth/__pycache__/token_manager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/auth/__pycache__/token.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/ocsp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/typing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/event.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/lock.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/crc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/sentinel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/credentials.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/data_structure.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/background.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/cluster.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/retry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/backoff.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/driver_info.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/maint_notifications.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/observability/__pycache__/attributes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/observability/__pycache__/recorder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/observability/__pycache__/metrics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/observability/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/observability/__pycache__/registry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/observability/__pycache__/providers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/http/__pycache__/http_client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/multidb/__pycache__/circuit.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/multidb/__pycache__/failover.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/multidb/__pycache__/event.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/multidb/__pycache__/command_executor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/multidb/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/multidb/__pycache__/healthcheck.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/multidb/__pycache__/database.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/multidb/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/multidb/__pycache__/failure_detector.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/__pycache__/sentinel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/__pycache__/policies.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/__pycache__/helpers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/__pycache__/cluster.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/__pycache__/redismodules.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/timeseries/__pycache__/commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/bf/__pycache__/commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/json/__pycache__/commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/json/__pycache__/path.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/json/__pycache__/decoders.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/search/__pycache__/reducers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/search/__pycache__/aggregation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/search/__pycache__/commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/search/__pycache__/suggestion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/search/__pycache__/result.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/search/__pycache__/profile_information.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/search/__pycache__/hybrid_result.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/search/__pycache__/query.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/search/__pycache__/querystring.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/search/__pycache__/hybrid_query.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/vectorset/__pycache__/commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/vectorset/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/_parsers/__pycache__/resp3.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/_parsers/__pycache__/commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/_parsers/__pycache__/socket.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/_parsers/__pycache__/hiredis.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/_parsers/__pycache__/resp2.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/_parsers/__pycache__/encoders.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/_parsers/__pycache__/helpers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/_parsers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/__pycache__/lock.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/__pycache__/sentinel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/__pycache__/cluster.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/__pycache__/retry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/http/__pycache__/http_client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/multidb/__pycache__/failover.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/multidb/__pycache__/event.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/multidb/__pycache__/command_executor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/multidb/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/multidb/__pycache__/healthcheck.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/multidb/__pycache__/database.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/multidb/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/multidb/__pycache__/failure_detector.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/entity.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/matcher.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/message.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/abstract.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/serialization.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/compression.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/simple.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/pidbox.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/clocks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/messaging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/utils/__pycache__/uuid.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/utils/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/utils/__pycache__/functional.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/utils/__pycache__/text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/utils/__pycache__/time.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/utils/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/utils/__pycache__/div.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/utils/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/utils/__pycache__/url.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/utils/__pycache__/limits.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/filesystem.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/gcpubsub.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/pyro.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/SLMQ.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/azurestoragequeues.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/memory.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/qpid.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/consul.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/azureservicebus.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/mongodb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/confluentkafka.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/etcd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/redis.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/SQS.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/native_delayed_delivery.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/virtual/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/virtual/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/virtual/__pycache__/exchange.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/asynchronous/__pycache__/timer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/asynchronous/__pycache__/semaphore.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/asynchronous/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/asynchronous/__pycache__/hub.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/asynchronous/http/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/asynchronous/http/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/asynchronous/aws/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/asynchronous/aws/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/asynchronous/aws/__pycache__/ext.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/asynchronous/aws/sqs/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/__pycache__/rl_config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/__pycache__/rl_settings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/platypus/__pycache__/doctemplate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/platypus/__pycache__/frames.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/platypus/__pycache__/figures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/platypus/__pycache__/flowables.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/platypus/__pycache__/tables.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/platypus/__pycache__/paragraph.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/platypus/__pycache__/tableofcontents.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/platypus/__pycache__/xpreformatted.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/platypus/__pycache__/para.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/platypus/__pycache__/paraparser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/colors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/pdfencrypt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/testutils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/rl_accel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/corp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/rparsexml.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/boxstuff.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/pygments2xpre.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/arciv.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/randomtext.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/rl_safe_eval.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/normalDate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/geomutils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/codecharts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/attrmap.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/PyFontify.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/fontfinder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/styles.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/sequencer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/textsplit.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/__pycache__/renderSVG.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/__pycache__/widgetbase.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/__pycache__/shapes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/__pycache__/svgpath.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/__pycache__/renderPDF.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/__pycache__/transform.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/__pycache__/renderPM.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/__pycache__/renderbase.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/__pycache__/renderPS.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/widgets/__pycache__/eventcal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/widgets/__pycache__/grids.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/widgets/__pycache__/signsandsymbols.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/widgets/__pycache__/table.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/widgets/__pycache__/flags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/samples/__pycache__/stacked_column.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/samples/__pycache__/stacked_bar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/samples/__pycache__/scatter_lines.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/samples/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/samples/__pycache__/radar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/samples/__pycache__/filled_radar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/samples/__pycache__/linechart_with_markers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/samples/__pycache__/clustered_bar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/samples/__pycache__/simple_pie.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/samples/__pycache__/bubble.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/samples/__pycache__/line_chart.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/samples/__pycache__/scatter_lines_markers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/samples/__pycache__/clustered_column.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/samples/__pycache__/scatter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/samples/__pycache__/exploded_pie.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/usps4s.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/widgets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/lto.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/dmtx.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/fourstate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/barcode/__pycache__/test.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/charts/__pycache__/textlabels.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/charts/__pycache__/dotbox.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/charts/__pycache__/utils3d.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/charts/__pycache__/axes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/charts/__pycache__/lineplots.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/charts/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/charts/__pycache__/markers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/charts/__pycache__/barcharts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/charts/__pycache__/piecharts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/charts/__pycache__/spider.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/charts/__pycache__/linecharts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/charts/__pycache__/slidebox.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/charts/__pycache__/legends.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/pdfgen/__pycache__/canvas.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/pdfgen/__pycache__/pdfimages.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/pdfgen/__pycache__/textobject.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/pdfbase/__pycache__/_fontdata_enc_symbol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/pdfbase/__pycache__/_glyphlist.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/pdfbase/__pycache__/ttfonts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/pdfbase/__pycache__/pdfdoc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/pdfbase/__pycache__/_fontdata_widths_symbol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/pdfbase/__pycache__/cidfonts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/pdfbase/__pycache__/acroform.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/pdfbase/__pycache__/pdfmetrics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/pdfbase/__pycache__/pdfutils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/sy______.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/zx______.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/zy______.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/DarkGardenMK.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_celery_beat/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_celery_beat/__pycache__/schedulers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_celery_beat/__pycache__/clockedschedule.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_celery_beat/__pycache__/tzcrontab.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_celery_beat/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click_repl/__pycache__/_repl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/report.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/comments.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/numerics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/nodes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/lines.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/linegen.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/output.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/rusty.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/brackets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/ranges.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/trans.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/mode.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/files.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/strings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/concurrency.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/handle_ipynb_magics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/parsing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/process.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/einfo.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/spawn.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/forkserver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/popen_fork.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/heap.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/sharedctypes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/popen_spawn_win32.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/pool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/queues.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/resource_sharer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/_win.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/reduction.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/synchronize.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/popen_forkserver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/managers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/context.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/__pycache__/filters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/__pycache__/filterset.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/rest_framework/__pycache__/backends.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/rest_framework/__pycache__/filterset.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/locale/cs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/locale/bg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/locale/uk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/locale/be/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/locale/nl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/locale/sk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_filters/locale/el/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/patch_stdout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/history.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/mouse_events.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/cursor_shapes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/selection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/renderer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/document.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/validation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/buffer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/search.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/auto_suggest.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/win32_types.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/clipboard/__pycache__/pyperclip.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/clipboard/__pycache__/in_memory.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/clipboard/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/formatted_text/__pycache__/ansi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/formatted_text/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/formatted_text/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/formatted_text/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/formatted_text/__pycache__/pygments.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/widgets/__pycache__/menus.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/widgets/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/widgets/__pycache__/dialogs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/widgets/__pycache__/toolbars.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/shortcuts/__pycache__/prompt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/shortcuts/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/shortcuts/__pycache__/choice_input.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/shortcuts/__pycache__/dialogs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/shortcuts/progress_bar/__pycache__/formatters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/shortcuts/progress_bar/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/scroll.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/open_in_editor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/emacs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/named_commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/basic.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/completion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/mouse.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/cpr.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/page_navigation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/search.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/auto_suggest.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/vi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/focus.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/__pycache__/emacs_state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/__pycache__/defaults.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/__pycache__/key_bindings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/__pycache__/vi_state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/__pycache__/key_processor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/eventloop/__pycache__/inputhook.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/eventloop/__pycache__/async_generator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/eventloop/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/eventloop/__pycache__/win32.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/completion/__pycache__/fuzzy_completer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/completion/__pycache__/filesystem.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/completion/__pycache__/deduplicate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/completion/__pycache__/nested.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/completion/__pycache__/word_completer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/completion/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/filters/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/filters/__pycache__/app.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/filters/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/filters/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/layout/__pycache__/menus.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/layout/__pycache__/layout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/layout/__pycache__/controls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/layout/__pycache__/processors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/layout/__pycache__/dummy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/layout/__pycache__/margins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/layout/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/layout/__pycache__/scrollable_pane.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/layout/__pycache__/dimension.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/layout/__pycache__/screen.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/layout/__pycache__/mouse_handlers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/layout/__pycache__/containers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/input/__pycache__/ansi_escape_sequences.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/input/__pycache__/vt100_parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/input/__pycache__/vt100.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/input/__pycache__/defaults.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/input/__pycache__/posix_pipe.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/input/__pycache__/posix_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/input/__pycache__/typeahead.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/input/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/input/__pycache__/win32.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/input/__pycache__/win32_pipe.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/styles/__pycache__/style.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/styles/__pycache__/defaults.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/styles/__pycache__/style_transformation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/styles/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/styles/__pycache__/pygments.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/application/__pycache__/run_in_terminal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/application/__pycache__/dummy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/application/__pycache__/current.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/application/__pycache__/application.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/lexers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/lexers/__pycache__/pygments.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/contrib/completers/__pycache__/system.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/contrib/regular_languages/__pycache__/compiler.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/contrib/regular_languages/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/contrib/regular_languages/__pycache__/completion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/contrib/regular_languages/__pycache__/lexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/contrib/regular_languages/__pycache__/validation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/contrib/regular_languages/__pycache__/regex_parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/contrib/ssh/__pycache__/server.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/contrib/telnet/__pycache__/protocol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/contrib/telnet/__pycache__/server.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/output/__pycache__/flush_stdout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/output/__pycache__/vt100.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/output/__pycache__/defaults.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/output/__pycache__/plain_text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/output/__pycache__/color_depth.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/output/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/output/__pycache__/win32.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/output/__pycache__/conemu.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/output/__pycache__/windows10.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/corsheaders/__pycache__/apps.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/corsheaders/__pycache__/conf.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/corsheaders/__pycache__/checks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/corsheaders/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/simple_history/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/simple_history/__pycache__/template_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/simple_history/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/simple_history/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/simple_history/__pycache__/manager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/simple_history/management/commands/__pycache__/populate_history.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blackd/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blackd/__pycache__/middlewares.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blackd/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/__pycache__/formatter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/__pycache__/sql.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/__pycache__/cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/__pycache__/lexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/__pycache__/keywords.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/filters/__pycache__/aligned_indent.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/filters/__pycache__/reindent.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/filters/__pycache__/others.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/engine/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/engine/__pycache__/filter_stack.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/engine/__pycache__/statement_splitter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pluggy/__pycache__/_callers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pluggy/__pycache__/_manager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pluggy/__pycache__/_result.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pluggy/__pycache__/_tracing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pluggy/__pycache__/_hooks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/__pycache__/shortcuts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/__pycache__/context_processors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/__pycache__/loader.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/__pycache__/defaultfilters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/__pycache__/defaulttags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/__pycache__/engine.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/__pycache__/loader_tags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/__pycache__/library.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/__pycache__/smartif.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/__pycache__/context.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/loaders/__pycache__/filesystem.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/loaders/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/backends/__pycache__/django.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/template/backends/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/archive.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/log.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/safestring.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/module_loading.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/datastructures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/_os.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/timezone.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/deconstruct.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/functional.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/inspect.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/feedgenerator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/http.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/version.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/regex_helper.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/dateparse.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/numberformat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/topological_sort.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/termcolors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/jslex.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/timesince.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/ipv6.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/encoding.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/hashable.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/formats.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/lorem_ipsum.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/crypto.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/dateformat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/decorators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/tree.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/autoreload.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/translation/__pycache__/trans_real.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/http/__pycache__/request.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/http/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/http/__pycache__/cookie.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/http/__pycache__/multipartparser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/templatetags/__pycache__/static.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/templatetags/__pycache__/i18n.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/__pycache__/paginator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/__pycache__/asgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/__pycache__/signing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/__pycache__/wsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/cache/backends/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/checks/security/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/checks/__pycache__/registry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/checks/__pycache__/urls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/checks/__pycache__/model_checks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/servers/__pycache__/basehttp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/serializers/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/serializers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/serializers/__pycache__/xml_serializer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/__pycache__/templates.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/__pycache__/sql.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/__pycache__/color.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/flush.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/createcachetable.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/compilemessages.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/sqlflush.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/sqlmigrate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/inspectdb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/dbshell.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/migrate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/check.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/runserver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/makemessages.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/sqlsequencereset.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/loaddata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/optimizemigration.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/makemigrations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/mail/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/mail/__pycache__/message.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/mail/backends/__pycache__/smtp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/mail/backends/__pycache__/filebased.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/mail/backends/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/files/storage/__pycache__/memory.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/files/storage/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/files/__pycache__/uploadedfile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/files/__pycache__/uploadhandler.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/files/__pycache__/images.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/files/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/files/__pycache__/locks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/handlers/__pycache__/exception.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/handlers/__pycache__/asgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/handlers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/handlers/__pycache__/wsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/forms/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/forms/__pycache__/boundfield.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/forms/__pycache__/formsets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/forms/__pycache__/widgets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/forms/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/forms/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/forms/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/__pycache__/transaction.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/indexes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/expressions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/query_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/constraints.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/query.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/deletion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/options.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/enums.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/manager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/functions/__pycache__/comparison.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/functions/__pycache__/text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/functions/__pycache__/datetime.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/sql/__pycache__/compiler.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/sql/__pycache__/subqueries.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/sql/__pycache__/where.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/sql/__pycache__/query.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/fields/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/fields/__pycache__/related.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/fields/__pycache__/files.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/fields/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/fields/__pycache__/reverse_related.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/fields/__pycache__/related_descriptors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/__pycache__/writer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/__pycache__/loader.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/__pycache__/optimizer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/__pycache__/recorder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/__pycache__/executor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/__pycache__/questioner.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/__pycache__/migration.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/__pycache__/autodetector.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/__pycache__/graph.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/__pycache__/state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/operations/__pycache__/special.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/operations/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/operations/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/operations/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/operations/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/__pycache__/ddl_references.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/creation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/mysql/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/mysql/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/mysql/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/mysql/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/mysql/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/oracle/__pycache__/creation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/oracle/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/oracle/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/oracle/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/oracle/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/oracle/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/oracle/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/postgresql/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/postgresql/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/postgresql/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/postgresql/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/postgresql/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/base/__pycache__/creation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/base/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/base/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/base/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/base/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/base/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/middleware/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/middleware/__pycache__/csrf.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/middleware/__pycache__/http.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/middleware/__pycache__/common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/middleware/__pycache__/locale.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/apps/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/apps/__pycache__/registry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/test/__pycache__/runner.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/test/__pycache__/testcases.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/test/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/test/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/dispatch/__pycache__/dispatcher.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/urls/__pycache__/static.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/urls/__pycache__/i18n.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/eu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/uz/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/tt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/zh_Hans/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/os/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/id/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ga/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/cs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/vi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ckb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ky/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/bg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/he/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/pl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/pt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/dsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/mn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/uk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ast/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/pa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ne/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/be/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/hy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/nl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/es_VE/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ia/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/tg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/zh_Hant/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/gl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ml/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/sr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/is/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/lb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/udm/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/sk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/nb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/tr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/br/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/km/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/sl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/es_CO/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/lt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/sr_Latn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ms/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/gd/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/hsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ig/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ar_DZ/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ka/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/hi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ta/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/th/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ja/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/fi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/kk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/cy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/sq/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/fy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/nn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/te/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/mk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ro/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/bs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/es_AR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/hu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/sv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/lv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/az/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/kn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/en_GB/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/bn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/io/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/en_AU/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/es_MX/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/kab/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ur/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/tk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/sw/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/hr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/af/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ko/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/eo/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/et/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/el/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/da/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/urls/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/urls/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/urls/__pycache__/resolvers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/base_user.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/context_processors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/hashers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/backends.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/tokens.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/password_validation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/decorators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/management/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/management/commands/__pycache__/createsuperuser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/migrations/__pycache__/0001_initial.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/eu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/zh_Hans/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/os/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/id/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ga/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/cs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/vi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ckb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ky/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/bg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/he/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/pl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/pt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/dsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/mn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/uk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ast/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/pa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ne/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/be/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/hy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/nl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/es_VE/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ia/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/tg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/zh_Hant/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/gl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ml/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/sr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/is/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/sk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/nb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/tr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/km/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/sl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/es_CO/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/lt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/sr_Latn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ms/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/gd/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/hsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ar_DZ/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ka/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/hi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ta/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/th/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ja/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/fi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/kk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/cy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/sq/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/nn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/te/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/mk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ro/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/bs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/es_AR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/hu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/sv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/lv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/az/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/kn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/en_GB/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/bn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/en_AU/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/es_MX/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/kab/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/tk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/sw/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/hr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/af/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ko/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/eo/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/et/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/el/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/da/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/handlers/__pycache__/modwsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/sites/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/sites/__pycache__/shortcuts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/sites/__pycache__/managers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/humanize/templatetags/__pycache__/humanize.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/sessions/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/sessions/__pycache__/base_session.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/sessions/backends/__pycache__/file.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/sessions/backends/__pycache__/db.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/sessions/backends/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/__pycache__/shortcuts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/__pycache__/measure.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/__pycache__/feeds.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/utils/__pycache__/ogrinspect.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/utils/__pycache__/layermapping.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/datasource.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/libgdal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/field.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/srs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/layer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/geometries.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/feature.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/envelope.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/error.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/geomtype.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/__pycache__/driver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/prototypes/__pycache__/srs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/prototypes/__pycache__/generation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/prototypes/__pycache__/errcheck.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/raster/__pycache__/band.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/raster/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/gdal/raster/__pycache__/source.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geos/__pycache__/libgeos.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geos/__pycache__/collections.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geos/__pycache__/mutable_list.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geos/__pycache__/polygon.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geos/__pycache__/factory.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geos/__pycache__/io.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geos/__pycache__/geometry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geos/__pycache__/coordseq.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geos/__pycache__/point.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geos/__pycache__/linestring.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geos/prototypes/__pycache__/io.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geos/prototypes/__pycache__/coordseq.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geos/prototypes/__pycache__/geom.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geos/prototypes/__pycache__/misc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geos/prototypes/__pycache__/errcheck.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geoip2/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/forms/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/models/__pycache__/lookups.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/models/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/spatialite/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/spatialite/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/mysql/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/oracle/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/oracle/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/base/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/base/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/base/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/postgis/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/postgis/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/postgis/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/postgis/__pycache__/adapter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/sitemaps/__pycache__/kml.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/sitemaps/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/management/commands/__pycache__/ogrinspect.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/admin/__pycache__/options.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/postgres/__pycache__/indexes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/postgres/__pycache__/signals.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/postgres/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/postgres/__pycache__/constraints.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/postgres/forms/__pycache__/hstore.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/postgres/aggregates/__pycache__/general.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/postgres/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/sitemaps/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/contenttypes/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/contenttypes/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/contenttypes/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/syndication/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/__pycache__/sites.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/__pycache__/checks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/__pycache__/widgets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/__pycache__/filters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/__pycache__/decorators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/__pycache__/options.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/templatetags/__pycache__/log.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/templatetags/__pycache__/admin_modify.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/templatetags/__pycache__/admin_list.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/id/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/cs/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/bg/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/nl/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ia/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ca/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ru/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/fi/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/es_AR/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/sv/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/eo/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/views/__pycache__/main.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/views/__pycache__/autocomplete.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admindocs/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admindocs/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admindocs/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/messages/storage/__pycache__/fallback.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/messages/storage/__pycache__/session.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/messages/storage/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/messages/storage/__pycache__/cookie.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/messages/__pycache__/context_processors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/messages/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/messages/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/redirects/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/staticfiles/__pycache__/handlers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/staticfiles/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/staticfiles/__pycache__/urls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/staticfiles/__pycache__/finders.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/staticfiles/__pycache__/storage.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/staticfiles/management/commands/__pycache__/runserver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/staticfiles/management/commands/__pycache__/findstatic.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/flatpages/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/flatpages/templatetags/__pycache__/flatpages.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/views/__pycache__/defaults.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/views/__pycache__/csrf.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/views/__pycache__/static.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/views/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/views/__pycache__/i18n.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/views/generic/__pycache__/edit.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/views/generic/__pycache__/detail.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/views/generic/__pycache__/list.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/views/generic/__pycache__/dates.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/views/generic/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/views/decorators/__pycache__/http.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tzlocal/__pycache__/win32.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tzlocal/__pycache__/unix.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/__pycache__/hash_ring.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/__pycache__/pool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/client/__pycache__/sharded.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/client/__pycache__/herd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/client/__pycache__/default.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/serializers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/serializers/__pycache__/pickle.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/serializers/__pycache__/msgpack.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/serializers/__pycache__/json.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/compressors/__pycache__/zlib.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/compressors/__pycache__/lzma.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/compressors/__pycache__/lz4.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/compressors/__pycache__/zstd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/compressors/__pycache__/gzip.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/compressors/__pycache__/identity.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/compressors/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/reverse.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/request.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/renderers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/metadata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/settings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/routers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/filters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/permissions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/generics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/relations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/pagination.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/negotiation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/viewsets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/throttling.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/test.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/status.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/authentication.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/parsers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/utils/__pycache__/timezone.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/utils/__pycache__/model_meta.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/utils/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/utils/__pycache__/field_mapping.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/utils/__pycache__/encoders.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/utils/__pycache__/formatting.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/utils/__pycache__/mediatypes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/utils/__pycache__/urls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/utils/__pycache__/serializer_helpers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/utils/__pycache__/breadcrumbs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/schemas/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/schemas/__pycache__/coreapi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/schemas/__pycache__/generators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/schemas/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/schemas/__pycache__/openapi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/templatetags/__pycache__/rest_framework.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/ne_NP/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/zh_Hans/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/ru_RU/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/id/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/cs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/bg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/pl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/pt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/uk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/hy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/nl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/tr_TR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/zh_Hant/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/sk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/nb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/tr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/sl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/fa_IR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/en/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/zh_CN/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/th/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/ja/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/fi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/kk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/mk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/ro/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/hu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/sv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/ko_KR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/lv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/az/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/et/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/el/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/da/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/plugin_support.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/patch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/report.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/data.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/collector.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/cmdline.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/multiproc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/version.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/pytracer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/sysmon.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/results.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/regions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/lcovreport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/xmlreport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/types.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/templite.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/numbits.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/report_core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/jsonreport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/tomlconfig.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/plugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/execfile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/disposition.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/env.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/annotate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/bytecode.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/files.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/sqlitedb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/misc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/inorout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/sqldata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/phystokens.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/context.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/tracer.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/__pycache__/resources.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/__pycache__/widgets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/__pycache__/results.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/formats/__pycache__/base_formats.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/zh_Hans/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/cs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/bg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/he/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/pl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/uk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/kz/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/nl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/sk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/tr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/ja/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/fi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/es_AR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/ko/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/fd7dcdb10166ebd4db98__mypyc.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/__pycache__/arbiter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/__pycache__/errors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/__pycache__/sock.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/__pycache__/glogging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/__pycache__/systemd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/http2/__pycache__/request.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/http2/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/http2/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/http2/__pycache__/errors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/http2/__pycache__/async_connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/http2/__pycache__/stream.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/asgi/__pycache__/lifespan.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/asgi/__pycache__/unreader.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/asgi/__pycache__/uwsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/asgi/__pycache__/message.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/asgi/__pycache__/websocket.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/asgi/__pycache__/protocol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/http/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/http/__pycache__/message.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/http/__pycache__/parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/http/__pycache__/wsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/instrument/__pycache__/statsd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/workers/__pycache__/gasgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/workers/__pycache__/gthread.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/workers/__pycache__/ggevent.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/workers/__pycache__/base_async.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/workers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/dirty/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/dirty/__pycache__/arbiter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/dirty/__pycache__/app.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/dirty/__pycache__/errors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/dirty/__pycache__/stash.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/dirty/__pycache__/protocol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/dirty/__pycache__/worker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/dirty/__pycache__/tlv.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/dirty/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/ctl/__pycache__/cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/ctl/__pycache__/handlers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/ctl/__pycache__/protocol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/ctl/__pycache__/server.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/ctl/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dj_database_url/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2/__pycache__/_json.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2/__pycache__/sql.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2/__pycache__/extensions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2/__pycache__/tz.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2/__pycache__/extras.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2/__pycache__/errors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2/__pycache__/pool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2/__pycache__/errorcodes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2/__pycache__/_range.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2/_psycopg.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dotenv/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dotenv/__pycache__/main.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dotenv/__pycache__/cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dotenv/__pycache__/variables.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dotenv/__pycache__/parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/jwt/__pycache__/api_jwk.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/jwt/__pycache__/api_jws.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/jwt/__pycache__/jwk_set_cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/jwt/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/jwt/__pycache__/jwks_client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/jwt/__pycache__/algorithms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/jwt/__pycache__/help.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/jwt/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/jwt/__pycache__/api_jwt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/vine/__pycache__/funtools.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/vine/__pycache__/promises.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/factory/__pycache__/random.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/factory/__pycache__/builder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/factory/__pycache__/fuzzy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/factory/__pycache__/declarations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/factory/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/_internal_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/status_codes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/cookies.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/adapters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/structures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/certs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/auth.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/help.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/sessions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/et_xmlfile/__pycache__/incremental_tree.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/30fcd23745efe32ce681__mypyc.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libldap-1accf1ee.so.2.0.200: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libkrb5-fcafa220.so.3.3: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libcrypto-81d66ed9.so.3: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libssl-81ffa89e.so.3: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libselinux-0922c95c.so.1: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libk5crypto-b1f99d5c.so.3.1: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libkrb5support-d0bcff84.so.0.1: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libsasl2-883649fd.so.3.0.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libgssapi_krb5-497db0c6.so.2.2: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libpq-9b38f5e3.so.5.17: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/security/__pycache__/certificate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/local.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/schedules.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/canvas.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/states.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/bootsteps.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/_state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/platforms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/result.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/beat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/__main__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/timer2.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/log.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/sysinfo.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/imports.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/collections.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/functional.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/time.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/debug.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/iso8601.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/serialization.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/quorum_queues.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/threads.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/graph.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/term.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/objects.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/nodenames.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/annotations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/saferepr.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/dispatch/__pycache__/signal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/__pycache__/request.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/__pycache__/loops.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/__pycache__/control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/__pycache__/components.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/__pycache__/heartbeat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/__pycache__/strategy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/__pycache__/autoscale.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/__pycache__/worker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/__pycache__/pidbox.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/__pycache__/state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/consumer/__pycache__/consumer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/consumer/__pycache__/delayed_delivery.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/consumer/__pycache__/tasks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/consumer/__pycache__/gossip.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/consumer/__pycache__/mingle.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/events/__pycache__/cursesmon.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/events/__pycache__/state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/events/__pycache__/snapshot.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/events/__pycache__/dispatcher.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/apps/__pycache__/multi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/apps/__pycache__/beat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/apps/__pycache__/worker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/concurrency/__pycache__/thread.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/concurrency/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/concurrency/__pycache__/asynpool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/concurrency/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/concurrency/__pycache__/prefork.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/fixups/__pycache__/django.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/bin/__pycache__/events.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/bin/__pycache__/celery.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/bin/__pycache__/control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/bin/__pycache__/migrate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/bin/__pycache__/multi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/bin/__pycache__/result.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/bin/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/bin/__pycache__/worker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/log.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/events.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/defaults.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/backends.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/registry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/task.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/amqp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/trace.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/cosmosdbsql.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/arangodb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/elasticsearch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/dynamodb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/rpc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/asynchronous.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/azureblockblob.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/mongodb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/redis.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/gcs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/cassandra.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/database/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/database/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/contrib/__pycache__/rdb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/contrib/__pycache__/migrate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/contrib/__pycache__/abortable.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/contrib/__pycache__/pytest.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/contrib/testing/__pycache__/app.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/contrib/testing/__pycache__/tasks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/contrib/testing/__pycache__/worker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/contrib/testing/__pycache__/mocks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/contrib/testing/__pycache__/manager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/contrib/django/__pycache__/task.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/asgiref/__pycache__/local.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/asgiref/__pycache__/typing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/asgiref/__pycache__/timeout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/asgiref/__pycache__/testing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/asgiref/__pycache__/current_thread_executor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/asgiref/__pycache__/compatibility.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/asgiref/__pycache__/sync.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/asgiref/__pycache__/server.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/asgiref/__pycache__/wsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tools/__pycache__/resx2po.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click_didyoumean/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click_plugins/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/backends.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/settings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/tokens.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/authentication.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/token_blacklist/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/token_blacklist/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/token_blacklist/management/commands/__pycache__/flushexpiredtokens.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_cov/__pycache__/engine.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/idna/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/idna/__pycache__/codec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/idna/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/idna/__pycache__/intranges.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/idna/__pycache__/uts46data.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/cron_descriptor/__pycache__/StringBuilder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/cron_descriptor/__pycache__/Options.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/cron_descriptor/__pycache__/GetText.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/cron_descriptor/__pycache__/Exception.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/cron_descriptor/__pycache__/ExpressionValidator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/cron_descriptor/__pycache__/ExpressionDescriptor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/cron_descriptor/__pycache__/ExpressionParser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/__pycache__/typing.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/__pycache__/cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/__pycache__/typing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/__pycache__/factory.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/__pycache__/generator.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/__pycache__/proxy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/__pycache__/factory.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/__pycache__/documentor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/__pycache__/proxy.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/__pycache__/generator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/__pycache__/exceptions.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/utils/__pycache__/text.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/utils/__pycache__/datasets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/utils/__pycache__/text.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/utils/__pycache__/distribution.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/utils/__pycache__/decorators.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/utils/__pycache__/checksums.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/utils/__pycache__/datasets.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/utils/__pycache__/decorators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/utils/__pycache__/loading.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/utils/__pycache__/loading.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/utils/__pycache__/distribution.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/decode/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/decode/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/sphinx/__pycache__/validator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/passport/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/passport/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/passport/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/passport/it_IT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/passport/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/passport/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/isbn/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/isbn/__pycache__/isbn.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/isbn/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/isbn/__pycache__/isbn.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/lorem/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/lorem/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/lorem/cs_CZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/lorem/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/lorem/it_IT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/lorem/pl_PL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/lorem/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/lorem/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/el_GR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/nl_NL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/fr_CA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/ro_RO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/uk_UA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/cs_CZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/tr_TR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/ng_NG/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/fa_IR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/es_ES/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/uz_UZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/es_AR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/vi_VN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/pl_PL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/en_AU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/currency/pt_BR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/sbn/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/sbn/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/sbn/__pycache__/sbn.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/sbn/__pycache__/sbn.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/fr_FR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/ar_AA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/fr_CA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/ta_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/gu_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/hr_HR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/id_ID/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/hu_HU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/uz_UZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/no_NO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/ko_KR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/sl_SI/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/zh_TW/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/th_TH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/ja_JP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/date_time/hi_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/ar_PS/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/el_GR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/nl_NL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/ro_RO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/ar_SA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/uk_UA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/tr_TR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/ar_JO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/sk_SK/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/es_ES/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/es_AR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/vi_VN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/ko_KR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/pl_PL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/de_DE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/de_CH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/th_TH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/ja_JP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/automotive/az_AZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/profile/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/profile/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/job/fr_FR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/job/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/job/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/job/ro_RO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/job/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/job/cs_CZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/job/hu_HU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/job/sk_SK/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/job/vi_VN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/fr_FR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/ar_PS/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/en_NZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/ar_JO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/it_IT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/ar_AE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/en_GB/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/en_AU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/de_LU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/de_CH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/pt_BR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/phone_number/az_AZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/bank/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/bank/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/bank/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/bank/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/bank/en_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/bank/nl_BE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/bank/es_MX/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/bank/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/barcode/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/barcode/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/barcode/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/barcode/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/barcode/ja_JP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/fr_FR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/nl_NL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/fil_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/ro_RO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/fr_CH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/id_ID/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/tr_TR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/hu_HU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/fa_IR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/it_IT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/es_ES/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/vi_VN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/ko_KR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/pl_PL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/zh_TW/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/es_MX/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/fi_FI/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/th_TH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/ja_JP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/pt_BR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/az_AZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/fr_QC/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/pt_PT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/is_IS/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/uk_UA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/hu_HU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/fa_IR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/vi_VN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/pl_PL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/zh_TW/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/de_DE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/ja_JP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/or_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/et_EE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/person/az_AZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/emoji/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/emoji/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/geo/el_GR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/geo/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/geo/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/geo/pt_PT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/geo/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/geo/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/user_agent/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/user_agent/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/ne_NP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/fr_FR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/el_GR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/sv_SE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/nl_NL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/pt_PT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/zu_ZA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/fr_CA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/ro_RO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/da_DK/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/en_NZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/fr_CH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/ta_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/en_IE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/hr_HR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/ka_GE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/id_ID/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/uk_UA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/cs_CZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/en_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/hy_AM/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/en_CA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/es_CO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/hu_HU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/sk_SK/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/fa_IR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/en_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/en/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/en/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/it_IT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/es_ES/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/en_MS/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/nl_BE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/no_NO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/es_AR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/vi_VN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/ko_KR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/pl_PL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/sl_SI/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/en_GB/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/zh_TW/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/de_DE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/en_AU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/es_MX/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/fi_FI/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/he_IL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/de_CH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/bn_BD/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/th_TH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/ja_JP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/pt_BR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/az_AZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/address/hi_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/doi/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/doi/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/file/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/file/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/color/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/color/__pycache__/color.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/color/__pycache__/color.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/color/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/python/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/python/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/misc/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/misc/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/misc/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/internet/el_GR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/internet/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/internet/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/internet/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/internet/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/internet/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/internet/ja_JP/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/fr_FR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/el_GR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/sv_SE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/el_CY/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/bg_BG/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/nl_NL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/pt_PT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/ro_RO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/fr_CH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/es_CL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/en_IE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/de_AT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/hr_HR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/mt_MT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/lv_LV/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/uk_UA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/cs_CZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/tr_TR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/en_PH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/lt_LT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/en_CA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/es_CO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/hu_HU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/sk_SK/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/en_IN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/it_IT/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/es_ES/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/dk_DK/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/lb_LU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/nl_BE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/no_NO/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/pl_PL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/sl_SI/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/en_GB/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/zh_TW/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/de_DE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/es_MX/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/fi_FI/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/he_IL/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/th_TH/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/pt_BR/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/et_EE/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/ssn/az_AZ/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/credit_card/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/credit_card/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/credit_card/ru_RU/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/credit_card/uk_UA/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/credit_card/zh_CN/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/contrib/pytest/__pycache__/plugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/contrib/pytest/__pycache__/plugin.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/formats/__pycache__/_html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/formats/__pycache__/_latex.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/formats/__pycache__/_json.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/formats/__pycache__/_cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/formats/__pycache__/_csv.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/formats/__pycache__/_sql.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/formats/__pycache__/_xlsx.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/formats/__pycache__/_ods.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/formats/__pycache__/_df.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/formats/__pycache__/_rst.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/formats/__pycache__/_dbf.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/formats/__pycache__/_xls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/formats/__pycache__/_yaml.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/_vendor/dbfpy/__pycache__/header.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/_vendor/dbfpy/__pycache__/dbfnew.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/_vendor/dbfpy/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/_vendor/dbfpy/__pycache__/dbf.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/_vendor/dbfpy/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tablib/_vendor/dbfpy/__pycache__/record.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/shell_completion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/testing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/_utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/termui.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/_winconsole.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/types.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/_termui_impl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/_textwrap.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/formatting.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/_compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/decorators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/parser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/globals.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/__pycache__/formatter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/__pycache__/modeline.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/__pycache__/lexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/__pycache__/scanner.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/__pycache__/sphinxext.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/__pycache__/regexopt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/__pycache__/token.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/filters/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/styles/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/lisp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/haxe.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/solidity.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/forth.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_stan_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_qlik_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/matlab.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/sophia.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/graphics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/boa.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/c_like.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/supercollider.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_julia_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/d.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_tsql_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/blueprint.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/inferno.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_cocoa_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/ncl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_css_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/igor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/idl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_mysql_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/textedit.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/felix.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/pawn.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/markup.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/ampl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/fantom.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/devicetree.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/templates.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_googlesql_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_php_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/zig.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/sql.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/tact.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/spice.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/scdoc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/asm.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/macaulay2.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/slash.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/gsql.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/dsls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_ada_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/hdl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/business.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/verification.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/phix.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/theorem.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/scripting.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/basic.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/configs.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/wgsl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/wren.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/dotnet.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_sourcemod_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_sql_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/c_cpp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/parasail.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/carbon.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_openedge_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/r.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/haskell.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/unicon.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/trafficscript.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/vyper.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_cl_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_lua_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/shell.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/wowtoc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/berry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/installers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/factor.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/tcl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/praat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/jvm.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/javascript.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/esoteric.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/hare.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/fortran.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/ecl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/varnish.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/grammar_notation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/chapel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/perl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_lilypond_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/snobol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/modeling.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_stata_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_postgres_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/dax.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/func.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_lasso_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/console.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/algebra.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/openscad.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/arrow.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/qvt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/kuin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/textfmts.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/tnt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/ptx.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_mql_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/ooc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/typst.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/maple.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_scilab_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/pony.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/webassembly.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/teal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/actionscript.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/comal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/mojo.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/urbi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/crystal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/oberon.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/graph.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/yang.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/nimrod.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/pascal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/clean.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/monte.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/int_fiction.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/sas.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/dylan.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/rust.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/go.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/gdscript.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/php.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/x10.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/rebol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/modula2.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_vim_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/automation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/mosel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/objective.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/apdlexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/csound.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/qlik.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/whiley.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/robotframework.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/dalvik.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/ruby.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/arturo.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_csound_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/nit.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_scheme_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/j.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_mapping.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/css.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/teraterm.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/webmisc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/parsers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/erlang.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/foxpro.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/formatters/__pycache__/latex.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/formatters/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/formatters/__pycache__/img.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/formatters/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pyflakes/__pycache__/messages.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pyflakes/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pyflakes/__pycache__/checker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pyflakes/test/__pycache__/test_match.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pyflakes/test/__pycache__/test_builtin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pyflakes/test/__pycache__/test_type_annotations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pyflakes/test/__pycache__/test_undefined_names.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pyflakes/test/__pycache__/test_api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pyflakes/test/__pycache__/test_other.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pyflakes/test/__pycache__/test_doctests.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pyflakes/test/__pycache__/test_imports.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/_io/__pycache__/pprint.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/_io/__pycache__/terminalwriter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/_io/__pycache__/wcwidth.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/_io/__pycache__/saferepr.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/python_api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/tracemalloc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/terminal.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/fixtures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/outcomes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/tmpdir.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/runner.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/monkeypatch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/main.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/stepwise.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/unraisableexception.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/faulthandler.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/terminalprogress.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/debugging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/skipping.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/hookspec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/doctest.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/pytester.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/setuponly.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/pytester_assertions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/setupplan.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/subtests.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/timing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/nodes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/scope.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/warnings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/recwarn.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/warning_types.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/unittest.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/reports.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/logging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/stash.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/capture.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/freeze_support.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/_argcomplete.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/deprecated.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/pathlib.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/threadexception.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/junitxml.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/raises.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/cacheprovider.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/pastebin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/legacypath.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/helpconfig.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/_code/__pycache__/code.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/_code/__pycache__/source.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/_py/__pycache__/path.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/_py/__pycache__/error.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/config/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/config/__pycache__/findpaths.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/config/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/config/__pycache__/argparsing.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/mark/__pycache__/expression.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/mark/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/mark/__pycache__/structures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/assertion/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/assertion/__pycache__/truncate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/assertion/__pycache__/rewrite.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/assertion/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/bin/python3: binary file matches
grep: backend/.venv/bin/python: binary file matches
grep: backend/.venv/bin/python3.12: binary file matches

```
EXIT_CODE: 0

## Command
```bash
grep -RniE 'transition|can_|allowed_|validate_|clean\(|perform_create|perform_update|update\(|save\(|serializer\.validate|utrmc-approve|verify' backend > OUT/grep_transitions.txt
```

### Output
```
grep: backend/db.sqlite3: binary file matches
grep: backend/.coverage: binary file matches
grep: backend/sims/academics/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/sims/users/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/sims/users/__pycache__/api_views.cpython-312.pyc: binary file matches
grep: backend/sims/users/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/users/__pycache__/tests.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/users/__pycache__/decorators.cpython-312.pyc: binary file matches
grep: backend/sims/users/management/commands/__pycache__/seed_demo_data.cpython-312.pyc: binary file matches
grep: backend/sims/__pycache__/common_permissions.cpython-312.pyc: binary file matches
grep: backend/sims/results/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/sims/results/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/apps.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/api_serializers.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/test_api.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/api_views.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/tests.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/api_urls.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/test_api.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/logbook/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/sims/cases/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/cases/__pycache__/test_api.cpython-312.pyc: binary file matches
grep: backend/sims/cases/__pycache__/api_views.cpython-312.pyc: binary file matches
grep: backend/sims/cases/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/cases/__pycache__/test_api.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/cases/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/domain/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/services.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/apps.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/api_views.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/tests.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/api_urls.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/sims/rotations/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/sims/reports/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/services.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/event_catalog.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/dashboard_v1.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/tests.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/analytics/__pycache__/event_tracking.cpython-312.pyc: binary file matches
grep: backend/sims/bulk/__pycache__/services.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/apps.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/urls.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/migrations/__pycache__/0001_initial.cpython-312.pyc: binary file matches
grep: backend/sims/certificates/migrations/__pycache__/0002_historicalcertificatetype_historicalcertificate.cpython-312.pyc: binary file matches
grep: backend/sims/_devtools/tests/__pycache__/test_rbac_api.cpython-312.pyc: binary file matches
grep: backend/sims_project/__pycache__/settings.cpython-312.pyc: binary file matches
grep: backend/sims_project/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libxcb-64009ff3.so.1.1.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libharfbuzz-0692f733.so.0.61230.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libtiff-295fd75c.so.6.2.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libfreetype-ee1c40c4.so.6.20.4: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libbrotlicommon-c55a5f7a.so.1.2.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/poolmanager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/connectionpool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/_collections.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/http2/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/ssl_.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/timeout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/ssltransport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/ssl_match_hostname.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/url.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/util/__pycache__/retry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/contrib/__pycache__/pyopenssl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/urllib3/contrib/emscripten/__pycache__/fetch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/platformdirs/__pycache__/windows.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/__pycache__/pycodestyle.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/__pycache__/typing_extensions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/whitenoise/__pycache__/responders.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/fixtures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/live_server_helper.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/live_server_helper.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/plugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/plugin.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_django/__pycache__/fixtures.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blib2to3/__pycache__/pytree.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blib2to3/pgen2/__pycache__/parse.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blib2to3/pgen2/__pycache__/grammar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/blib2to3/pgen2/__pycache__/driver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/__pycache__/wheel_builder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/index/__pycache__/package_finder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/index/__pycache__/sources.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/compatibility_tags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/utils/__pycache__/entrypoints.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/resolution/legacy/__pycache__/resolver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/resolver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/found_candidates.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/models/__pycache__/format_control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/models/__pycache__/direct_url.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/req/__pycache__/req_uninstall.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/req/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/cli/__pycache__/cmdoptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/cli/__pycache__/req_command.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/check.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/commands/__pycache__/install.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/vcs/__pycache__/git.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_internal/network/__pycache__/session.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/actions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/poolmanager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/connectionpool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/ssl_.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/timeout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/ssltransport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/ssl_match_hostname.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/url.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/retry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/contrib/__pycache__/securetransport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/contrib/__pycache__/appengine.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/contrib/__pycache__/pyopenssl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/urllib3/contrib/_securetransport/__pycache__/bindings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/__pycache__/typing_extensions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/codingstatemachine.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/chardet/__pycache__/utf1632prober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/prompt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/progress.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/_emoji_codes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/rich/__pycache__/live.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/serialize.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/adapter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/adapters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/requests/__pycache__/sessions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/idna/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/metadata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/distlib/__pycache__/index.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_macos.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/truststore/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_openssl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_ssl_constants.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_windows.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/__pycache__/cmdline.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/__pycache__/lexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pygments/lexers/__pycache__/python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pip/_vendor/pkg_resources/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/version.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/pylock.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/packaging/__pycache__/_manylinux.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/charset_normalizer/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/_backends/__pycache__/agg.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/_backends/hyperscan/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pathspec/_backends/hyperscan/__pycache__/pathspec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/crispy_forms/templatetags/__pycache__/crispy_forms_tags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/packaging/__pycache__/workbook.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/worksheet/__pycache__/properties.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/worksheet/__pycache__/copier.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/reader/__pycache__/excel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/openpyxl/formula/__pycache__/tokenizer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/amqp/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/amqp/__pycache__/transport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/amqp/__pycache__/abstract_channel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/amqp/__pycache__/channel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/JpegImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageCms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/JpegPresets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/Jpeg2KImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/PdfParser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/Image.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/TiffImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/ImageFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/__pycache__/PngImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/_imaging.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/_avif.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/_imagingft.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dateutil/__pycache__/rrule.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dateutil/tz/__pycache__/tz.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dateutil/tz/__pycache__/win.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dateutil/tz/__pycache__/_common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/auth/__pycache__/token.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/ocsp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/cluster.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/driver_info.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/http/__pycache__/http_client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/multidb/__pycache__/healthcheck.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/commands/__pycache__/cluster.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/_parsers/__pycache__/socket.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/_parsers/__pycache__/hiredis.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/_parsers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/__pycache__/cluster.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/redis/asyncio/multidb/__pycache__/healthcheck.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/entity.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/abstract.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/pidbox.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/utils/__pycache__/limits.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/gcpubsub.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/pyamqp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/azurestoragequeues.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/qpid.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/consul.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/azureservicebus.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/librabbitmq.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/mongodb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/confluentkafka.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/etcd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/redis.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/__pycache__/SQS.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/virtual/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/transport/sqlalchemy/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/asynchronous/http/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/asynchronous/http/__pycache__/curl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/asynchronous/aws/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/kombu/asynchronous/aws/sqs/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/rl_safe_eval.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/lib/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/__pycache__/widgetbase.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/graphics/__pycache__/shapes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/pdfgen/__pycache__/canvas.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/pdfbase/__pycache__/_can_cmap_data.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/pdfbase/__pycache__/pdfdoc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_celery_beat/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_celery_beat/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_celery_beat/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/lines.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/linegen.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/trans.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/black/__pycache__/handle_ipynb_magics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/billiard/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/validation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/__pycache__/buffer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/shortcuts/__pycache__/prompt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/named_commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/search.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/key_binding/__pycache__/key_bindings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/layout/__pycache__/controls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/prompt_toolkit/application/__pycache__/application.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/corsheaders/__pycache__/conf.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/corsheaders/__pycache__/checks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/corsheaders/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/__pycache__/formatter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/sqlparse/__pycache__/cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pluggy/__pycache__/_manager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pluggy/__pycache__/_hooks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/http.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/utils/__pycache__/crypto.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/http/__pycache__/request.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/http/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/__pycache__/paginator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/cache/backends/__pycache__/db.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/cache/backends/__pycache__/locmem.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/cache/backends/__pycache__/dummy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/cache/backends/__pycache__/filebased.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/cache/backends/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/cache/backends/__pycache__/memcached.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/cache/backends/__pycache__/redis.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/checks/security/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/checks/__pycache__/model_checks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/serializers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/__pycache__/templates.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/createcachetable.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/sqlmigrate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/migrate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/runserver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/squashmigrations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/showmigrations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/management/commands/__pycache__/optimizemigration.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/files/storage/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/files/__pycache__/uploadedfile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/files/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/core/handlers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/forms/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/forms/__pycache__/formsets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/forms/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/forms/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/forms/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/__pycache__/transaction.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/expressions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/lookups.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/query.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/deletion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/__pycache__/options.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/sql/__pycache__/compiler.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/sql/__pycache__/subqueries.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/sql/__pycache__/query.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/fields/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/fields/__pycache__/related.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/fields/__pycache__/files.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/fields/__pycache__/json.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/models/fields/__pycache__/related_descriptors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/__pycache__/loader.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/__pycache__/graph.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/operations/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/migrations/operations/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/mysql/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/mysql/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/mysql/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/oracle/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/oracle/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/postgresql/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/base/__pycache__/creation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/base/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/base/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/base/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/base/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/db/backends/base/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/middleware/__pycache__/csrf.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/middleware/__pycache__/common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/test/__pycache__/testcases.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/test/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/test/__pycache__/selenium.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/__pycache__/global_settings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/uz/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/zh_Hans/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/id/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/cs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ckb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ky/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/bg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/he/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/pl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/dsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/uk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/be/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/nl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ia/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/gl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ml/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/sr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/is/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/sk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/nb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/tr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/sr_Latn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ms/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/gd/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/hsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ig/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ar_DZ/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ja/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/fi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/sq/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/nn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/es_AR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/hu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/sv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/lv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/az/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/en_AU/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/tk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/af/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ko/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/eo/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/et/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/el/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/da/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/base_user.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/hashers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/backends.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/password_validation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/management/commands/__pycache__/changepassword.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/management/commands/__pycache__/createsuperuser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/sites/__pycache__/requests.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/sessions/backends/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/sessions/backends/__pycache__/signed_cookies.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/utils/__pycache__/layermapping.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/geoip2/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/spatialite/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/spatialite/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/mysql/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/oracle/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/base/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/gis/db/backends/base/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/postgres/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/contenttypes/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/contenttypes/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/contenttypes/management/commands/__pycache__/remove_stale_contenttypes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/__pycache__/checks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/__pycache__/widgets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/__pycache__/decorators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/__pycache__/options.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/templatetags/__pycache__/admin_modify.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/templatetags/__pycache__/admin_list.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/eu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/tt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/zh_Hans/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/os/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/id/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ga/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/cs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/vi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ckb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ky/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/bg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/he/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/pl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/pt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/dsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/mn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/uk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/pa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ne/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/be/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/hy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/nl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/es_VE/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ia/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/tg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/zh_Hant/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/gl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ml/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/sr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/is/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/sk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/nb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/tr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/km/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/sl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/es_CO/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/lt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/sr_Latn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ms/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/gd/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/hsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ar_DZ/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ka/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/hi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ta/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/th/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ja/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/fi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/kk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/cy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/sq/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/nn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/te/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/mk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ro/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/bs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/es_AR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/hu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/sv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/lv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/az/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/kn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/en_GB/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/bn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/io/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/en_AU/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/es_MX/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ur/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/sw/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/hr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/af/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ko/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/eo/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/et/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/el/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/da/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/views/__pycache__/main.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/staticfiles/__pycache__/finders.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/staticfiles/management/commands/__pycache__/collectstatic.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/views/__pycache__/i18n.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/views/generic/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/client/__pycache__/sharded.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_redis/client/__pycache__/default.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/renderers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/metadata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/settings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/urlpatterns.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/versioning.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/decorators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/__pycache__/viewsets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/utils/__pycache__/field_mapping.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/schemas/__pycache__/generators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/authtoken/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/plugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/coverage/__pycache__/sqldata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/__pycache__/resources.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/formats/__pycache__/base_formats.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/__pycache__/sock.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/http2/__pycache__/stream.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/asgi/__pycache__/uwsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/asgi/__pycache__/protocol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/http/__pycache__/wsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/uwsgi/__pycache__/message.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/gunicorn/workers/__pycache__/gthread.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2/__pycache__/errorcodes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/jwt/__pycache__/api_jws.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/jwt/__pycache__/types.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/jwt/__pycache__/jwks_client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/jwt/__pycache__/algorithms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/jwt/__pycache__/api_jwt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/factory/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/adapters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/requests/__pycache__/sessions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/30fcd23745efe32ce681__mypyc.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libldap-1accf1ee.so.2.0.200: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libkrb5-fcafa220.so.3.3: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libcrypto-81d66ed9.so.3: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libssl-81ffa89e.so.3: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libselinux-0922c95c.so.1: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libk5crypto-b1f99d5c.so.3.1: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libsasl2-883649fd.so.3.0.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libgssapi_krb5-497db0c6.so.2.2: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libpq-9b38f5e3.so.5.17: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/security/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/security/__pycache__/serialization.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/security/__pycache__/certificate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/canvas.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/platforms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/result.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/__pycache__/beat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/collections.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/utils/__pycache__/time.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/consumer/__pycache__/consumer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/consumer/__pycache__/delayed_delivery.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/worker/consumer/__pycache__/tasks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/events/__pycache__/snapshot.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/apps/__pycache__/worker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/concurrency/__pycache__/thread.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/concurrency/__pycache__/solo.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/concurrency/__pycache__/asynpool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/concurrency/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/fixups/__pycache__/django.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/bin/__pycache__/control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/bin/__pycache__/multi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/task.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/app/__pycache__/amqp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/arangodb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/dynamodb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/backends/__pycache__/rpc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/celery/contrib/__pycache__/sphinx.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/backends.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/settings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/tokens.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework_simplejwt/__pycache__/state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_cov/__pycache__/plugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pytest_cov/__pycache__/plugin.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/idna/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/cron_descriptor/__pycache__/ExpressionValidator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/sphinx/__pycache__/validator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/lorem/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/lorem/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/company/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/color/__pycache__/color.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/color/__pycache__/color.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/python/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/python/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/misc/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/faker/providers/misc/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/click/__pycache__/termui.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/__pycache__/cmdline.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/__pycache__/lexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/lisp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_cocoa_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_css_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/ride.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_mysql_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_php_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/macaulay2.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/dsls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/phix.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/scripting.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/basic.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/shell.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/installers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/praat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/fortran.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/varnish.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_lilypond_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/_lasso_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/julia.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/actionscript.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/bibtex.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/sas.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/rebol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/apdlexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pygments/lexers/__pycache__/webmisc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pyflakes/__pycache__/checker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pyflakes/test/__pycache__/test_type_annotations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pyflakes/test/__pycache__/test_other.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/monkeypatch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/main.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/debugging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/pytester.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/__pycache__/raises.cpython-312.pyc: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/_pytest/config/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libxcb-64009ff3.so.1.1.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libharfbuzz-0692f733.so.0.61230.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libtiff-295fd75c.so.6.2.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libfreetype-ee1c40c4.so.6.20.4: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libbrotlicommon-c55a5f7a.so.1.2.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/poolmanager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/connectionpool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/_collections.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/http2/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/ssl_.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/timeout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/ssltransport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/ssl_match_hostname.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/url.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/util/__pycache__/retry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/contrib/__pycache__/pyopenssl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/urllib3/contrib/emscripten/__pycache__/fetch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/platformdirs/__pycache__/windows.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/__pycache__/pycodestyle.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/__pycache__/typing_extensions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/whitenoise/__pycache__/responders.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/fixtures.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/live_server_helper.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/live_server_helper.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/plugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/plugin.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_django/__pycache__/fixtures.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blib2to3/__pycache__/pytree.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blib2to3/pgen2/__pycache__/parse.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blib2to3/pgen2/__pycache__/grammar.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/blib2to3/pgen2/__pycache__/driver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/__pycache__/wheel_builder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/__pycache__/exceptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/index/__pycache__/package_finder.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/index/__pycache__/sources.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/compatibility_tags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/utils/__pycache__/entrypoints.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/resolution/legacy/__pycache__/resolver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/resolver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/resolution/resolvelib/__pycache__/found_candidates.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/models/__pycache__/format_control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/models/__pycache__/direct_url.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/req/__pycache__/req_uninstall.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/req/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/cli/__pycache__/cmdoptions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/cli/__pycache__/req_command.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/check.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/commands/__pycache__/install.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/vcs/__pycache__/git.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_internal/network/__pycache__/session.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pyparsing/__pycache__/actions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/poolmanager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/__pycache__/connectionpool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/ssl_.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/timeout.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/ssltransport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/ssl_match_hostname.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/url.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/util/__pycache__/retry.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/contrib/__pycache__/securetransport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/contrib/__pycache__/appengine.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/contrib/__pycache__/pyopenssl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/urllib3/contrib/_securetransport/__pycache__/bindings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/__pycache__/typing_extensions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/codingstatemachine.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/chardet/__pycache__/utf1632prober.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/prompt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/progress.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/_emoji_codes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/rich/__pycache__/live.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/serialize.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/cachecontrol/__pycache__/adapter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/adapters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/requests/__pycache__/sessions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/idna/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/metadata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/wheel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/compat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/distlib/__pycache__/index.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_macos.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/truststore/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_openssl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_ssl_constants.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/truststore/__pycache__/_windows.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/__pycache__/cmdline.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/__pycache__/lexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pygments/lexers/__pycache__/python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pip/_vendor/pkg_resources/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/version.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/pylock.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/packaging/__pycache__/_manylinux.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/charset_normalizer/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/__pycache__/util.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/_backends/__pycache__/agg.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/_backends/hyperscan/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pathspec/_backends/hyperscan/__pycache__/pathspec.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/crispy_forms/templatetags/__pycache__/crispy_forms_tags.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/packaging/__pycache__/workbook.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/worksheet/__pycache__/properties.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/worksheet/__pycache__/copier.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/reader/__pycache__/excel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/openpyxl/formula/__pycache__/tokenizer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/amqp/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/amqp/__pycache__/transport.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/amqp/__pycache__/abstract_channel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/amqp/__pycache__/channel.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/JpegImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageCms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/JpegPresets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/Jpeg2KImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/PdfParser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/Image.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/TiffImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/ImageFile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/__pycache__/PngImagePlugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/_imaging.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/_avif.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/_imagingft.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dateutil/__pycache__/rrule.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dateutil/tz/__pycache__/tz.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dateutil/tz/__pycache__/win.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dateutil/tz/__pycache__/_common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/auth/__pycache__/token.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/ocsp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/cluster.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/driver_info.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/http/__pycache__/http_client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/multidb/__pycache__/healthcheck.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/commands/__pycache__/cluster.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/_parsers/__pycache__/socket.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/_parsers/__pycache__/hiredis.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/_parsers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/__pycache__/cluster.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/__pycache__/client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/redis/asyncio/multidb/__pycache__/healthcheck.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/entity.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/abstract.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/pidbox.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/utils/__pycache__/limits.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/gcpubsub.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/pyamqp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/azurestoragequeues.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/qpid.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/consul.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/azureservicebus.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/librabbitmq.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/mongodb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/confluentkafka.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/etcd.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/redis.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/__pycache__/SQS.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/virtual/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/transport/sqlalchemy/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/asynchronous/http/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/asynchronous/http/__pycache__/curl.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/asynchronous/aws/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/kombu/asynchronous/aws/sqs/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/rl_safe_eval.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/lib/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/__pycache__/widgetbase.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/graphics/__pycache__/shapes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/pdfgen/__pycache__/canvas.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/pdfbase/__pycache__/_can_cmap_data.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/pdfbase/__pycache__/pdfdoc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_celery_beat/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_celery_beat/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_celery_beat/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/lines.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/linegen.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/trans.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/black/__pycache__/handle_ipynb_magics.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/billiard/__pycache__/connection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/validation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/__pycache__/buffer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/shortcuts/__pycache__/prompt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/named_commands.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/bindings/__pycache__/search.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/key_binding/__pycache__/key_bindings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/layout/__pycache__/controls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/prompt_toolkit/application/__pycache__/application.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/corsheaders/__pycache__/conf.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/corsheaders/__pycache__/checks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/corsheaders/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/__pycache__/formatter.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/sqlparse/__pycache__/cli.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pluggy/__pycache__/_manager.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pluggy/__pycache__/_hooks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/http.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/utils/__pycache__/crypto.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/http/__pycache__/request.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/http/__pycache__/response.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/__pycache__/paginator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/cache/backends/__pycache__/db.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/cache/backends/__pycache__/locmem.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/cache/backends/__pycache__/dummy.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/cache/backends/__pycache__/filebased.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/cache/backends/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/cache/backends/__pycache__/memcached.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/cache/backends/__pycache__/redis.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/checks/security/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/checks/__pycache__/model_checks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/serializers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/__pycache__/templates.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/createcachetable.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/sqlmigrate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/migrate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/runserver.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/squashmigrations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/showmigrations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/management/commands/__pycache__/optimizemigration.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/files/storage/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/files/__pycache__/uploadedfile.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/files/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/core/handlers/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/forms/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/forms/__pycache__/formsets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/forms/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/forms/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/forms/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/__pycache__/transaction.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/expressions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/lookups.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/query.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/deletion.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/__pycache__/options.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/sql/__pycache__/compiler.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/sql/__pycache__/subqueries.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/sql/__pycache__/query.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/fields/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/fields/__pycache__/related.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/fields/__pycache__/files.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/fields/__pycache__/json.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/models/fields/__pycache__/related_descriptors.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/__pycache__/loader.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/__pycache__/graph.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/operations/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/migrations/operations/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/sqlite3/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/mysql/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/mysql/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/mysql/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/oracle/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/oracle/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/postgresql/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/base/__pycache__/creation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/base/__pycache__/schema.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/base/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/base/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/base/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/db/backends/base/__pycache__/introspection.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/middleware/__pycache__/csrf.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/middleware/__pycache__/common.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/test/__pycache__/testcases.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/test/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/test/__pycache__/selenium.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/__pycache__/global_settings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/uz/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/zh_Hans/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/id/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/cs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ckb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ky/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/bg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/he/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/pl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/dsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/uk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/be/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/nl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ia/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/gl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ml/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/sr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/is/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/sk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/nb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/tr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/sr_Latn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ms/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/gd/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/hsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ig/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ar_DZ/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ja/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/fi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/sq/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/nn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/es_AR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/hu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/sv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/lv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/az/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/en_AU/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/tk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/af/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ko/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/eo/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/et/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/el/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/da/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/base_user.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/hashers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/models.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/backends.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/password_validation.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/management/commands/__pycache__/changepassword.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/management/commands/__pycache__/createsuperuser.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/sites/__pycache__/requests.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/sessions/backends/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/sessions/backends/__pycache__/signed_cookies.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/utils/__pycache__/layermapping.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/geoip2/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/spatialite/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/spatialite/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/mysql/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/oracle/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/base/__pycache__/features.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/gis/db/backends/base/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/postgres/__pycache__/operations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/contenttypes/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/contenttypes/__pycache__/admin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/contenttypes/management/commands/__pycache__/remove_stale_contenttypes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/__pycache__/checks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/__pycache__/widgets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/__pycache__/decorators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/__pycache__/options.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/templatetags/__pycache__/admin_modify.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/templatetags/__pycache__/admin_list.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/eu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/tt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/zh_Hans/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/os/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/id/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ga/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/cs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/vi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ckb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ky/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/bg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/he/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/pl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/pt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/it/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/dsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/mn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/uk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/pa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ne/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/be/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/hy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/nl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/es_VE/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ia/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/tg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/zh_Hant/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/gl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ml/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/sr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/is/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/sk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/nb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/tr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/km/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/sl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/es_CO/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/lt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/sr_Latn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ms/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/gd/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/hsb/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ar_DZ/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ka/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/hi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ta/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/th/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ja/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/fi/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/kk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/cy/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/sq/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/nn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/te/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/mk/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ro/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/bs/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/es_AR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/hu/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/sv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/lv/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/az/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/kn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/en_GB/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/bn/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/io/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/en_AU/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/es_MX/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ur/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/sw/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/hr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/af/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ko/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/eo/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/et/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/el/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/da/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/views/__pycache__/main.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/staticfiles/__pycache__/finders.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/staticfiles/management/commands/__pycache__/collectstatic.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/views/__pycache__/i18n.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/views/generic/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/__pycache__/cache.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/client/__pycache__/sharded.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_redis/client/__pycache__/default.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/renderers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/metadata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/settings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/validators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/urlpatterns.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/versioning.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/fields.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/decorators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/__pycache__/viewsets.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/utils/__pycache__/field_mapping.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/schemas/__pycache__/generators.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/authtoken/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/html.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/plugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/coverage/__pycache__/sqldata.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/__pycache__/resources.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/__pycache__/mixins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/__pycache__/forms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/formats/__pycache__/base_formats.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/__pycache__/config.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/__pycache__/sock.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/http2/__pycache__/stream.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/asgi/__pycache__/uwsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/asgi/__pycache__/protocol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/http/__pycache__/wsgi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/uwsgi/__pycache__/message.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/gunicorn/workers/__pycache__/gthread.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2/__pycache__/errorcodes.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/jwt/__pycache__/api_jws.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/jwt/__pycache__/types.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/jwt/__pycache__/jwks_client.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/jwt/__pycache__/algorithms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/jwt/__pycache__/api_jwt.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/factory/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/api.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/adapters.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/utils.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/requests/__pycache__/sessions.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/30fcd23745efe32ce681__mypyc.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libldap-1accf1ee.so.2.0.200: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libkrb5-fcafa220.so.3.3: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libcrypto-81d66ed9.so.3: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libssl-81ffa89e.so.3: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libselinux-0922c95c.so.1: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libk5crypto-b1f99d5c.so.3.1: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libsasl2-883649fd.so.3.0.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libgssapi_krb5-497db0c6.so.2.2: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libpq-9b38f5e3.so.5.17: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/security/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/security/__pycache__/serialization.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/security/__pycache__/certificate.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/canvas.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/platforms.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/result.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/__pycache__/beat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/collections.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/utils/__pycache__/time.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/consumer/__pycache__/consumer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/consumer/__pycache__/delayed_delivery.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/worker/consumer/__pycache__/tasks.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/events/__pycache__/snapshot.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/apps/__pycache__/worker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/concurrency/__pycache__/thread.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/concurrency/__pycache__/solo.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/concurrency/__pycache__/asynpool.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/concurrency/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/fixups/__pycache__/django.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/bin/__pycache__/control.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/bin/__pycache__/multi.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/base.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/task.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/app/__pycache__/amqp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/arangodb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/dynamodb.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/backends/__pycache__/rpc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/celery/contrib/__pycache__/sphinx.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/serializers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/backends.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/settings.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/tokens.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/views.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework_simplejwt/__pycache__/state.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_cov/__pycache__/plugin.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pytest_cov/__pycache__/plugin.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/idna/__pycache__/core.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/cron_descriptor/__pycache__/ExpressionValidator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/sphinx/__pycache__/validator.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/lorem/en_US/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/lorem/en_US/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/company/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/color/__pycache__/color.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/color/__pycache__/color.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/python/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/python/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/misc/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/faker/providers/misc/__pycache__/__init__.cpython-312-pytest-9.0.2.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/click/__pycache__/termui.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/__pycache__/cmdline.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/__pycache__/lexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/lisp.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_cocoa_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_css_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/ride.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_mysql_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_php_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/macaulay2.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/dsls.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/phix.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/scripting.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/basic.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/shell.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/installers.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/praat.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/fortran.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/varnish.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_lilypond_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/_lasso_builtins.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/julia.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/actionscript.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/bibtex.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/sas.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/rebol.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/apdlexer.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pygments/lexers/__pycache__/webmisc.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pyflakes/__pycache__/checker.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pyflakes/test/__pycache__/test_type_annotations.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pyflakes/test/__pycache__/test_other.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/python.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/monkeypatch.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/main.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/debugging.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/pytester.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/__pycache__/raises.cpython-312.pyc: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/_pytest/config/__pycache__/__init__.cpython-312.pyc: binary file matches
grep: backend/.venv/bin/python3: binary file matches
grep: backend/.venv/bin/python: binary file matches
grep: backend/.venv/bin/python3.12: binary file matches

```
EXIT_CODE: 0

## Command
```bash
python3 OUT/models_status_extract.py
```

### Output
```
Generated models_status_fields.txt

```
EXIT_CODE: 0

## Command
```bash
grep -RniE --exclude-dir=migrations --exclude-dir=__pycache__ --exclude='test*.py' 'choices\s*=|TextChoices|IntegerChoices|Status|STATE|APPROV|SUBMIT|REVIEW|SEND_BACK|RETURN' backend/sims > OUT/grep_status_states.txt
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
grep -RniE --exclude-dir=migrations --exclude-dir=__pycache__ --exclude='test*.py' 'transition|can_|allowed_|validate_|clean\(|perform_create|perform_update|update\(|save\(|serializer\.validate|utrmc-approve|verify' backend/sims > OUT/grep_transitions.txt
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
grep -RniE 'AUTH_USER_MODEL|MIDDLEWARE|REST_FRAMEWORK' backend/sims_project > OUT/rbac_settings_refs.txt
```

### Output
```
grep: backend/sims_project/__pycache__/settings.cpython-312.pyc: binary file matches
grep: backend/sims_project/__pycache__/tests.cpython-312.pyc: binary file matches
grep: backend/sims_project/__pycache__/middleware.cpython-312.pyc: binary file matches
grep: backend/sims_project/__pycache__/wsgi.cpython-312.pyc: binary file matches

```
EXIT_CODE: 0

## Command
```bash
grep -RniE --exclude-dir=migrations --exclude-dir=__pycache__ 'permission_classes\s*=|BasePermission|IsAuthenticated|has_permission|has_object_permission' backend/sims > OUT/rbac_permission_classes.txt
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
grep -RniE --exclude-dir=migrations --exclude-dir=__pycache__ 'role\s*==|role\s*in|is_superuser|allowed_roles|PermissionDenied|groups|Group|has_perm|can_' backend/sims > OUT/rbac_role_checks.txt
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
grep -RniE --exclude-dir=migrations --exclude-dir=__pycache__ 'decorator|@action|@permission_classes|middleware|login_required|user_passes_test' backend/sims > OUT/rbac_decorators_middleware.txt
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T web python manage.py spectacular --file /tmp/openapi.json
```

### Output
```
time="2026-02-28T02:57:02+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:02+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:02+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
[INFO] 2026-02-27 21:57:03,319 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-27 21:57:03,330 sims.logbook Logbook periodic tasks setup completed
Unknown command: 'spectacular'
Type 'manage.py help' for usage.

```
EXIT_CODE: 1

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T web cat /tmp/openapi.json > OUT/openapi.json
```

### Output
```
time="2026-02-28T02:57:03+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:03+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:03+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:03+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:03+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:03+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:03+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
cat: /tmp/openapi.json: No such file or directory

```
EXIT_CODE: 1

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T web python manage.py shell -c "from rest_framework.schemas.openapi import SchemaGenerator; from rest_framework.renderers import JSONOpenAPIRenderer; schema=SchemaGenerator(title='PGSIMS API').get_schema(request=None, public=True); print(JSONOpenAPIRenderer().render(schema, renderer_context={}).decode())" > OUT/openapi_fallback.json
```

### Output
```
time="2026-02-28T02:57:03+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:03+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:03+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:03+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:03+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:03+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:03+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
[INFO] 2026-02-27 21:57:04,851 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-27 21:57:04,861 sims.logbook Logbook periodic tasks setup completed
Traceback (most recent call last):
  File "/app/manage.py", line 24, in <module>
    main()
  File "/app/manage.py", line 21, in main
    execute_from_command_line(sys.argv)
  File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
    utility.execute()
  File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/__init__.py", line 436, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/base.py", line 412, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/base.py", line 458, in execute
    output = self.handle(*args, **options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/commands/shell.py", line 117, in handle
    exec(options["command"], globals())
  File "<string>", line 1, in <module>
  File "/home/sims/.local/lib/python3.11/site-packages/rest_framework/schemas/openapi.py", line 78, in get_schema
    operation = view.schema.get_operation(path, method)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/sims/.local/lib/python3.11/site-packages/rest_framework/schemas/openapi.py", line 144, in get_operation
    operation['operationId'] = self.get_operation_id(path, method)
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/sims/.local/lib/python3.11/site-packages/rest_framework/schemas/openapi.py", line 265, in get_operation_id
    name = self.get_operation_id_base(path, method, action)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/sims/.local/lib/python3.11/site-packages/rest_framework/schemas/openapi.py", line 248, in get_operation_id_base
    assert inflection, '`inflection` must be installed for OpenAPI schema support.'
           ^^^^^^^^^^
AssertionError: `inflection` must be installed for OpenAPI schema support.

```
EXIT_CODE: 1

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T web python manage.py shell < OUT/api_endpoints_dump.py > OUT/api_endpoints.json
```

### Output
```
time="2026-02-28T02:57:05+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:05+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:05+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:05+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:05+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:05+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:05+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
[INFO] 2026-02-27 21:57:06,666 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-27 21:57:06,675 sims.logbook Logbook periodic tasks setup completed

```
EXIT_CODE: 0

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T web python manage.py shell < OUT/serializers_dump.py > OUT/serializers_inventory.json
```

### Output
```
time="2026-02-28T02:57:07+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:07+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:07+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:07+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:07+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:07+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:57:07+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
[INFO] 2026-02-27 21:57:08,475 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-27 21:57:08,485 sims.logbook Logbook periodic tasks setup completed
/home/sims/.local/lib/python3.11/site-packages/rest_framework/fields.py:990: UserWarning: max_value should be an integer or Decimal instance.
  warnings.warn("max_value should be an integer or Decimal instance.")
/home/sims/.local/lib/python3.11/site-packages/rest_framework/fields.py:992: UserWarning: min_value should be an integer or Decimal instance.
  warnings.warn("min_value should be an integer or Decimal instance.")

```
EXIT_CODE: 0

## Command
```bash
python3 OUT/render_api_catalogs.py
```

### Output
```
Endpoints: 208, Serializers: 54

```
EXIT_CODE: 0

## Command
```bash
python3 OUT/render_api_catalogs.py
```

### Output
```
Endpoints normalized: 151

```
EXIT_CODE: 0

## Command
```bash
grep -RniE --exclude-dir=migrations --exclude-dir=__pycache__ 'import|export|csv|xlsx|bulk|upload|download|tablib|resource' backend/sims > OUT/grep_import_export.txt
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
grep -RniE --exclude-dir=migrations --exclude-dir=__pycache__ 'celery|beat|crontab|schedule|rq|apscheduler|@shared_task|PeriodicTask' backend > OUT/grep_jobs.txt
```

### Output
```
grep: backend/db.sqlite3: binary file matches
grep: backend/static/images/fmu-logo.png: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/liblzma-61b1002e.so.5.8.2: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libzstd-761a17b6.so.1.5.7: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libharfbuzz-0692f733.so.0.61230.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libwebp-d8b9687f.so.7.2.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libavif-01e67780.so.16.3.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libopenjp2-94e588ba.so.2.5.4: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libfreetype-ee1c40c4.so.6.20.4: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/pillow.libs/libbrotlicommon-c55a5f7a.so.1.2.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/_imaging.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/PIL/_imagingft.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/tzdata/zoneinfo/Asia/Irkutsk: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/dateutil/zoneinfo/dateutil-zoneinfo.tar.gz: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/_ebi____.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/sy______.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/zx______.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/_eb_____.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/VeraBI.ttf: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/zy______.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/zd______.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/cobo____.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/_ei_____.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/VeraIt.ttf: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/_ab_____.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/_ai_____.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/_abi____.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/VeraBd.ttf: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/com_____.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/cob_____.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/coo_____.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/_a______.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/DarkGardenMK.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/_er_____.pfb: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/reportlab/fonts/Vera.ttf: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_celery_beat/locale/zh_Hans/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_celery_beat/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_celery_beat/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_celery_beat/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_celery_beat/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_celery_beat/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django_celery_beat/locale/ko/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/id/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/pt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ast/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ne/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/es_VE/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ia/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/tg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/gl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/es_CO/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ar_DZ/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/es_AR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/az/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/en_AU/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/es_MX/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/et/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/conf/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/es_VE/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/es_CO/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/auth/common-passwords.txt.gz: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/uz/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/pt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/es_VE/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ia/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/gl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/es_CO/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/es_AR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/es_MX/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admin/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/django/contrib/admindocs/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/static/rest_framework/fonts/glyphicons-halflings-regular.woff2: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/static/rest_framework/fonts/glyphicons-halflings-regular.eot: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/static/rest_framework/fonts/fontawesome-webfont.ttf: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/static/rest_framework/fonts/fontawesome-webfont.eot: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/static/rest_framework/fonts/glyphicons-halflings-regular.woff: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/static/rest_framework/fonts/fontawesome-webfont.woff: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/pt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/rest_framework/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/import_export/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/30fcd23745efe32ce681__mypyc.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libldap-1accf1ee.so.2.0.200: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libkrb5-fcafa220.so.3.3: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libcrypto-81d66ed9.so.3: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libpcre-9513aab5.so.1.2.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libssl-81ffa89e.so.3: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libk5crypto-b1f99d5c.so.3.1: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libsasl2-883649fd.so.3.0.0: binary file matches
grep: backend/.venv/lib/python3.12/site-packages/psycopg2_binary.libs/libpq-9b38f5e3.so.5.17: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/liblzma-61b1002e.so.5.8.2: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libzstd-761a17b6.so.1.5.7: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libharfbuzz-0692f733.so.0.61230.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libwebp-d8b9687f.so.7.2.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libavif-01e67780.so.16.3.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libopenjp2-94e588ba.so.2.5.4: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libfreetype-ee1c40c4.so.6.20.4: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/pillow.libs/libbrotlicommon-c55a5f7a.so.1.2.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/_imaging.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/PIL/_imagingft.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/tzdata/zoneinfo/Asia/Irkutsk: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/dateutil/zoneinfo/dateutil-zoneinfo.tar.gz: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/_ebi____.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/sy______.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/zx______.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/_eb_____.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/VeraBI.ttf: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/zy______.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/zd______.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/cobo____.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/_ei_____.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/VeraIt.ttf: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/_ab_____.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/_ai_____.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/_abi____.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/VeraBd.ttf: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/com_____.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/cob_____.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/coo_____.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/_a______.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/DarkGardenMK.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/_er_____.pfb: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/reportlab/fonts/Vera.ttf: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_celery_beat/locale/zh_Hans/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_celery_beat/locale/de/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_celery_beat/locale/fa/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_celery_beat/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_celery_beat/locale/ru/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_celery_beat/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django_celery_beat/locale/ko/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/id/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/pt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ast/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ne/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/es_VE/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ia/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/tg/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/gl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/es_CO/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ar_DZ/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/es_AR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/az/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/en_AU/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/es_MX/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/et/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/conf/locale/ar/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/es_VE/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/es_CO/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/auth/common-passwords.txt.gz: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/uz/LC_MESSAGES/djangojs.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/pt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/es_VE/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ia/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/ca/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/gl/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/es/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/es_CO/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/es_AR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/es_MX/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admin/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/django/contrib/admindocs/locale/fr/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/static/rest_framework/fonts/glyphicons-halflings-regular.woff2: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/static/rest_framework/fonts/glyphicons-halflings-regular.eot: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/static/rest_framework/fonts/fontawesome-webfont.ttf: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/static/rest_framework/fonts/fontawesome-webfont.eot: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/static/rest_framework/fonts/glyphicons-halflings-regular.woff: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/static/rest_framework/fonts/fontawesome-webfont.woff: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/pt/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/rest_framework/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/import_export/locale/pt_BR/LC_MESSAGES/django.mo: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/30fcd23745efe32ce681__mypyc.cpython-312-x86_64-linux-gnu.so: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libldap-1accf1ee.so.2.0.200: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libkrb5-fcafa220.so.3.3: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libcrypto-81d66ed9.so.3: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libpcre-9513aab5.so.1.2.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libssl-81ffa89e.so.3: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libk5crypto-b1f99d5c.so.3.1: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libsasl2-883649fd.so.3.0.0: binary file matches
grep: backend/.venv/lib64/python3.12/site-packages/psycopg2_binary.libs/libpq-9b38f5e3.so.5.17: binary file matches
grep: backend/.venv/bin/python3: binary file matches
grep: backend/.venv/bin/python: binary file matches
grep: backend/.venv/bin/python3.12: binary file matches
grep: backend/staticfiles/rest_framework/css/bootstrap-theme.min.css.map.gz: binary file matches
grep: backend/staticfiles/rest_framework/css/bootstrap-theme.min.css.51806092cc05.map.gz: binary file matches
grep: backend/staticfiles/rest_framework/css/bootstrap.min.css.cafbda9c0e9e.map.gz: binary file matches
grep: backend/staticfiles/rest_framework/css/bootstrap.min.css.gz: binary file matches
grep: backend/staticfiles/rest_framework/css/bootstrap.min.css.map.gz: binary file matches
grep: backend/staticfiles/rest_framework/docs/js/highlight.pack.js.gz: binary file matches
grep: backend/staticfiles/rest_framework/docs/js/highlight.pack.479b5f21dcba.js.gz: binary file matches
grep: backend/staticfiles/rest_framework/js/jquery-3.7.1.min.2c872dbe60f4.js.gz: binary file matches
grep: backend/staticfiles/rest_framework/js/jquery-3.7.1.min.js.gz: binary file matches
grep: backend/staticfiles/rest_framework/js/coreapi-0.1.1.e580e3854595.js.gz: binary file matches
grep: backend/staticfiles/rest_framework/js/coreapi-0.1.1.js.gz: binary file matches
grep: backend/staticfiles/rest_framework/fonts/fontawesome-webfont.svg.gz: binary file matches
grep: backend/staticfiles/rest_framework/fonts/glyphicons-halflings-regular.woff2: binary file matches
grep: backend/staticfiles/rest_framework/fonts/glyphicons-halflings-regular.448c34a56d69.woff2: binary file matches
grep: backend/staticfiles/rest_framework/fonts/fontawesome-webfont.3293616ec0c6.woff: binary file matches
grep: backend/staticfiles/rest_framework/fonts/fontawesome-webfont.83e37a11f9d7.svg.gz: binary file matches
grep: backend/staticfiles/rest_framework/fonts/fontawesome-webfont.8b27bc96115c.eot: binary file matches
grep: backend/staticfiles/rest_framework/fonts/glyphicons-halflings-regular.eot: binary file matches
grep: backend/staticfiles/rest_framework/fonts/fontawesome-webfont.ttf: binary file matches
grep: backend/staticfiles/rest_framework/fonts/fontawesome-webfont.dcb26c7239d8.ttf: binary file matches
grep: backend/staticfiles/rest_framework/fonts/fontawesome-webfont.dcb26c7239d8.ttf.gz: binary file matches
grep: backend/staticfiles/rest_framework/fonts/glyphicons-halflings-regular.fa2772327f55.woff: binary file matches
grep: backend/staticfiles/rest_framework/fonts/glyphicons-halflings-regular.svg.gz: binary file matches
grep: backend/staticfiles/rest_framework/fonts/fontawesome-webfont.eot: binary file matches
grep: backend/staticfiles/rest_framework/fonts/fontawesome-webfont.ttf.gz: binary file matches
grep: backend/staticfiles/rest_framework/fonts/glyphicons-halflings-regular.e18bbf611f2a.ttf.gz: binary file matches
grep: backend/staticfiles/rest_framework/fonts/glyphicons-halflings-regular.woff: binary file matches
grep: backend/staticfiles/rest_framework/fonts/glyphicons-halflings-regular.ttf.gz: binary file matches
grep: backend/staticfiles/rest_framework/fonts/glyphicons-halflings-regular.f4769f9bdb74.eot: binary file matches
grep: backend/staticfiles/rest_framework/fonts/glyphicons-halflings-regular.08eda92397ae.svg.gz: binary file matches
grep: backend/staticfiles/rest_framework/fonts/fontawesome-webfont.woff: binary file matches
grep: backend/staticfiles/admin/css/responsive.css.gz: binary file matches
grep: backend/staticfiles/admin/css/responsive.f6533dab034d.css.gz: binary file matches
grep: backend/staticfiles/admin/js/vendor/xregexp/xregexp.js.gz: binary file matches
grep: backend/staticfiles/admin/js/vendor/xregexp/xregexp.efda034b9537.js.gz: binary file matches
grep: backend/staticfiles/admin/js/vendor/xregexp/xregexp.min.b0439563a5d3.js.gz: binary file matches
grep: backend/staticfiles/admin/js/vendor/xregexp/xregexp.min.js.gz: binary file matches
grep: backend/staticfiles/admin/js/vendor/jquery/jquery.js.gz: binary file matches
grep: backend/staticfiles/admin/js/vendor/jquery/jquery.min.js.gz: binary file matches
grep: backend/staticfiles/admin/js/vendor/jquery/jquery.0208b96062ba.js.gz: binary file matches
grep: backend/staticfiles/admin/js/vendor/jquery/jquery.min.641dd1437010.js.gz: binary file matches
grep: backend/staticfiles/admin/js/vendor/select2/select2.full.c2afdeda3058.js.gz: binary file matches
grep: backend/staticfiles/admin/js/vendor/select2/i18n/lv.08e62128eac1.js.gz: binary file matches
grep: backend/staticfiles/admin/js/vendor/select2/i18n/lv.js.gz: binary file matches
grep: backend/staticfiles/admin/js/vendor/select2/i18n/it.be4fe8d365b5.js.gz: binary file matches
grep: backend/staticfiles/admin/js/vendor/select2/i18n/it.js.gz: binary file matches
grep: backend/staticfiles/admin/js/vendor/select2/select2.full.js.gz: binary file matches
grep: backend/staticfiles/admin/js/inlines.js.gz: binary file matches
grep: backend/staticfiles/admin/js/nav_sidebar.js.gz: binary file matches
grep: backend/staticfiles/admin/js/nav_sidebar.3b9190d420b1.js.gz: binary file matches
grep: backend/staticfiles/admin/js/inlines.22d4d93c00b4.js.gz: binary file matches
grep: backend/staticfiles/admin/js/admin/DateTimeShortcuts.9f6e209cebca.js.gz: binary file matches
grep: backend/staticfiles/admin/js/admin/DateTimeShortcuts.js.gz: binary file matches
grep: backend/staticfiles/images/fmu-logo.png: binary file matches
grep: backend/staticfiles/images/fmu-logo.d3148120c45e.png: binary file matches

```
EXIT_CODE: 0

## Command
```bash
grep -RniE --exclude-dir=migrations --exclude-dir=__pycache__ 'NotificationService|notification|recipient|verb|body|metadata|channels' backend/sims > OUT/grep_notifications.txt
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
grep -RniE --exclude-dir=migrations --exclude-dir=__pycache__ --exclude-dir=.venv --exclude-dir=templates --exclude-dir=tests --exclude='test*.py' 'export|csv|xlsx|bulk|upload|download|tablib|resource|import_' backend/sims backend/sims_project > OUT/grep_import_export.txt
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
grep -RniE --exclude-dir=migrations --exclude-dir=__pycache__ --exclude-dir=.venv --exclude-dir=templates --exclude-dir=tests --exclude='test*.py' 'celery|beat|crontab|schedule|@shared_task|PeriodicTask|run_scheduled_reports|ScheduledReportRunner' backend/sims backend/sims_project > OUT/grep_jobs.txt
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
grep -RniE --exclude-dir=migrations --exclude-dir=__pycache__ --exclude-dir=tests --exclude='test*.py' 'NotificationService|Notification\.objects\.create|recipient=|verb=|body=|metadata=|CHANNEL_' backend/sims > OUT/grep_notifications.txt
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T backend python manage.py test --failfast
```

### Output
```
time="2026-02-28T02:59:46+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:59:46+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:59:46+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:59:46+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:59:46+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:59:46+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:59:46+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
service "backend" is not running

```
EXIT_CODE: 1

## Command
```bash
docker compose -f docker/docker-compose.yml exec -T web python manage.py test --failfast
```

### Output
```
time="2026-02-28T02:59:47+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:59:47+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:59:47+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:59:47+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:59:47+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:59:47+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T02:59:47+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
[INFO] 2026-02-27 21:59:48,263 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-27 21:59:48,273 sims.logbook Logbook periodic tasks setup completed
Status: 200
ErrorNote: Please correct the error below.
FieldError: Supervisor is required for PGs
Form initialized successfully. dict_keys(['username', 'email', 'first_name', 'last_name', 'role', 'specialty', 'year', 'supervisor', 'password1', 'password2'])
GET /admin/users/user/add/ Status Code: 200
Found 286 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.............Rebuilding analytics rollups for 2026-02-26 -> 2026-02-26
Rollup rows updated: 1
Rebuilding analytics rollups for 2026-02-26 -> 2026-02-26
Rollup rows updated: 1
....................[WARNING] 2026-02-27 22:00:01,252 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:01,256 sims.analytics.event_tracking analytics_event_dropped
.[WARNING] 2026-02-27 22:00:01,313 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:01,318 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:01,322 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:01,331 sims.analytics.event_tracking analytics_event_dropped
.[WARNING] 2026-02-27 22:00:01,390 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:01,393 sims.analytics.event_tracking analytics_event_dropped
..[WARNING] 2026-02-27 22:00:01,491 sims.analytics.event_tracking analytics_event_dropped
/home/sims/.local/lib/python3.11/site-packages/django/db/models/fields/__init__.py:1535: RuntimeWarning: DateTimeField User.date_joined received a naive datetime (2024-02-01 00:00:00) while time zone support is active.
  warnings.warn(
[WARNING] 2026-02-27 22:00:01,512 sims.analytics.event_tracking analytics_event_dropped
...[WARNING] 2026-02-27 22:00:01,620 sims.analytics.event_tracking analytics_event_dropped
/home/sims/.local/lib/python3.11/site-packages/django/db/models/fields/__init__.py:1535: RuntimeWarning: DateTimeField User.date_joined received a naive datetime (2024-01-10 00:00:00) while time zone support is active.
  warnings.warn(
[WARNING] 2026-02-27 22:00:01,639 sims.analytics.event_tracking analytics_event_dropped
...................................................................[WARNING] 2026-02-27 22:00:06,293 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:06,298 sims.analytics.event_tracking analytics_event_dropped
....................[WARNING] 2026-02-27 22:00:08,142 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:08,147 sims.analytics.event_tracking analytics_event_dropped
...[WARNING] 2026-02-27 22:00:08,464 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:08,465 sims.analytics.event_tracking analytics_event_dropped
.[WARNING] 2026-02-27 22:00:08,545 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:08,546 sims.analytics.event_tracking analytics_event_dropped
.[WARNING] 2026-02-27 22:00:08,620 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:08,621 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:08,633 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:08,634 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:08,645 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:08,646 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:08,668 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:08,669 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:08,679 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-27 22:00:08,681 sims.analytics.event_tracking analytics_event_dropped
...........................................................................Processed 1 scheduled reports
.Processed 0 scheduled reports
.Processed 1 scheduled reports
................................................................[WARNING] 2026-02-27 22:00:16,030 sims.analytics.event_tracking analytics_event_dropped
.....[WARNING] 2026-02-27 22:00:16,456 sims.analytics.event_tracking analytics_event_dropped
..[WARNING] 2026-02-27 22:00:16,632 sims.analytics.event_tracking analytics_event_dropped
......
----------------------------------------------------------------------
Ran 286 tests in 19.578s

OK
Destroying test database for alias 'default'...

```
EXIT_CODE: 0

## Command
```bash
curl -I --max-time 30 https://pgsims.alshifalab.pk/api/health
```

### Output
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0  0   179    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
HTTP/2 404 
alt-svc: h3=":443"; ma=2592000
content-type: text/html; charset=utf-8
cross-origin-opener-policy: same-origin
date: Fri, 27 Feb 2026 22:00:18 GMT
permissions-policy: camera=(), microphone=(), geolocation=()
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=31536000; includeSubDomains; preload
vary: Cookie, origin
via: 1.1 Caddy
x-content-type-options: nosniff
x-frame-options: SAMEORIGIN
x-request-id: c6189d991433441ab3c93da9254b8858
x-response-time: 13ms
content-length: 179


```
EXIT_CODE: 0

## Command
```bash
curl -I --max-time 30 https://pgsims.alshifalab.pk/health
```

### Output
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
HTTP/2 404 
alt-svc: h3=":443"; ma=2592000
cache-control: private, no-cache, no-store, max-age=0, must-revalidate
content-type: text/html; charset=utf-8
date: Fri, 27 Feb 2026 22:00:18 GMT
link: </_next/static/media/4473ecc91f70f139-s.p.woff>; rel=preload; as="font"; crossorigin=""; type="font/woff", </_next/static/media/463dafcda517f24f-s.p.woff>; rel=preload; as="font"; crossorigin=""; type="font/woff"
permissions-policy: camera=(), microphone=(), geolocation=()
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=31536000; includeSubDomains; preload
vary: RSC, Next-Router-State-Tree, Next-Router-Prefetch, Accept-Encoding
via: 1.1 Caddy
x-content-type-options: nosniff
x-frame-options: SAMEORIGIN
x-powered-by: Next.js


```
EXIT_CODE: 0

## Command
```bash
curl -I --max-time 30 https://pgsims.alshifalab.pk/healthz/
```

### Output
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
HTTP/2 405 
allow: GET
alt-svc: h3=":443"; ma=2592000
cache-control: max-age=0, no-cache, no-store, must-revalidate, private
content-type: text/html; charset=utf-8
cross-origin-opener-policy: same-origin
date: Fri, 27 Feb 2026 22:00:18 GMT
expires: Fri, 27 Feb 2026 22:00:18 GMT
permissions-policy: camera=(), microphone=(), geolocation=()
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=31536000; includeSubDomains; preload
vary: origin
via: 1.1 Caddy
x-content-type-options: nosniff
x-frame-options: SAMEORIGIN
x-request-id: 30f786c37931447dae8bf42eeee6ed65
x-response-time: 0ms
content-length: 0


```
EXIT_CODE: 0

## Command
```bash
curl -I --max-time 30 https://pgsims.alshifalab.pk/admin/
```

### Output
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
HTTP/2 302 
alt-svc: h3=":443"; ma=2592000
cache-control: max-age=0, no-cache, no-store, must-revalidate, private
content-type: text/html; charset=utf-8
cross-origin-opener-policy: same-origin
date: Fri, 27 Feb 2026 22:00:18 GMT
expires: Fri, 27 Feb 2026 22:00:18 GMT
location: /admin/login/?next=/admin/
permissions-policy: camera=(), microphone=(), geolocation=()
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=31536000; includeSubDomains; preload
vary: Cookie, origin
via: 1.1 Caddy
x-content-type-options: nosniff
x-frame-options: SAMEORIGIN
x-request-id: b912cc826c1f452391e464ef8420c352
x-response-time: 54ms
content-length: 0


```
EXIT_CODE: 0

## Command
```bash
ls -1 OUT/20_BACKEND_TRUTH_MAP.md OUT/21_MODELS_CATALOG.md OUT/22_WORKFLOWS_STATE_MACHINES.md OUT/23_RBAC_PERMISSIONS_MAP.md OUT/24_API_ENDPOINTS_CATALOG.md OUT/25_SERIALIZERS_PAYLOAD_SHAPES.md OUT/26_IMPORT_EXPORT_AND_JOBS.md OUT/27_GAPS_AND_FIX_RECOMMENDATIONS.md OUT/28_VERIFICATION_EVIDENCE_LOG.md OUT/models_graph.dot OUT/openapi.json
```

### Output
```
OUT/20_BACKEND_TRUTH_MAP.md
OUT/21_MODELS_CATALOG.md
OUT/22_WORKFLOWS_STATE_MACHINES.md
OUT/23_RBAC_PERMISSIONS_MAP.md
OUT/24_API_ENDPOINTS_CATALOG.md
OUT/25_SERIALIZERS_PAYLOAD_SHAPES.md
OUT/26_IMPORT_EXPORT_AND_JOBS.md
OUT/27_GAPS_AND_FIX_RECOMMENDATIONS.md
OUT/28_VERIFICATION_EVIDENCE_LOG.md
OUT/models_graph.dot
OUT/openapi.json

```
EXIT_CODE: 0

## Command
```bash
git --no-pager status --short --branch
```

### Output
```
## main...origin/main
?? OUT/20_BACKEND_TRUTH_MAP.md
?? OUT/21_MODELS_CATALOG.md
?? OUT/22_WORKFLOWS_STATE_MACHINES.md
?? OUT/23_RBAC_PERMISSIONS_MAP.md
?? OUT/24_API_ENDPOINTS_CATALOG.md
?? OUT/25_SERIALIZERS_PAYLOAD_SHAPES.md
?? OUT/26_IMPORT_EXPORT_AND_JOBS.md
?? OUT/27_GAPS_AND_FIX_RECOMMENDATIONS.md
?? OUT/28_VERIFICATION_EVIDENCE_LOG.md
?? OUT/admin_audit.py
?? OUT/admin_files_audit.txt
?? OUT/admin_models_gap.txt
?? OUT/admin_registry_models.txt
?? OUT/api_endpoints.json
?? OUT/api_endpoints_dump.py
?? OUT/django_version.txt
?? OUT/docker_logs_backend.txt
?? OUT/docker_logs_web.txt
?? OUT/docker_ps.txt
?? OUT/git_head.txt
?? OUT/git_status.txt
?? OUT/grep_import_export.txt
?? OUT/grep_jobs.txt
?? OUT/grep_notifications.txt
?? OUT/grep_status_states.txt
?? OUT/grep_transitions.txt
?? OUT/installed_apps.txt
?? OUT/manage_check.txt
?? OUT/models_graph.dot
?? OUT/models_inventory.json
?? OUT/models_inventory_dump.py
?? OUT/models_status_extract.py
?? OUT/models_status_fields.txt
?? OUT/openapi.json
?? OUT/openapi_fallback.json
?? OUT/rbac_decorators_middleware.txt
?? OUT/rbac_permission_classes.txt
?? OUT/rbac_role_checks.txt
?? OUT/rbac_settings_refs.txt
?? OUT/render_api_catalogs.py
?? OUT/render_models_catalog.py
?? OUT/serializers_dump.py
?? OUT/serializers_inventory.json
?? OUT/showmigrations_plan.txt

```
EXIT_CODE: 0

## Command
```bash
cat OUT/active_compose_files.txt
```

### Output
```
/srv/apps/pgsims/docker/docker-compose.prod.yml

```
EXIT_CODE: 0

## Command
```bash
cat OUT/active_compose_primary.txt
```

### Output
```
/srv/apps/pgsims/docker/docker-compose.prod.yml

```
EXIT_CODE: 0

## Command
```bash
docker compose -f /srv/apps/pgsims/docker/docker-compose.prod.yml config > OUT/compose_rendered.yml
```

### Output
```
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"

```
EXIT_CODE: 0

## Command
```bash
docker compose -f /srv/apps/pgsims/docker/docker-compose.prod.yml ps > OUT/docker_ps.txt
```

### Output
```
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"

```
EXIT_CODE: 0

## Command
```bash
docker compose -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput > OUT/collectstatic_output.txt
```

### Output
```
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:18+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
[INFO] 2026-02-28 07:14:19,686 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-28 07:14:19,695 sims.logbook Logbook periodic tasks setup completed

```
EXIT_CODE: 0

## Command
```bash
docker compose -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T web sh -lc 'find /app/staticfiles -type f | wc -l' > OUT/staticfiles_count.txt
```

### Output
```
time="2026-02-28T12:14:20+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:20+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:20+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:20+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:20+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:20+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:20+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:14:20+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"

```
EXIT_CODE: 0

## Command
```bash
sudo -n caddy validate --config /etc/caddy/Caddyfile > OUT/caddy_validate.txt 2>&1 || caddy validate --config /etc/caddy/Caddyfile > OUT/caddy_validate.txt 2>&1
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
sudo -n cat /etc/caddy/Caddyfile > OUT/Caddyfile.active 2>/dev/null || cat /etc/caddy/Caddyfile > OUT/Caddyfile.active
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
curl -I --max-time 30 https://pgsims.alshifalab.pk/ > OUT/curl_root_headers.txt
```

### Output
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0  0  6100    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

```
EXIT_CODE: 0

## Command
```bash
curl -I --max-time 30 https://pgsims.alshifalab.pk/admin/ > OUT/curl_admin_headers.txt
```

### Output
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

```
EXIT_CODE: 0

## Command
```bash
curl -I --max-time 30 https://pgsims.alshifalab.pk/api/ > OUT/curl_api_headers.txt
```

### Output
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0  0   179    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

```
EXIT_CODE: 0

## Command
```bash
docker compose -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T backend python manage.py check
```

### Output
```
time="2026-02-28T12:15:02+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:02+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:02+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:02+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
service "backend" is not running

```
EXIT_CODE: 1

## Command
```bash
docker compose -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T web python manage.py check > OUT/manage_check_phaseb.txt
```

### Output
```
time="2026-02-28T12:15:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:02+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:02+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:02+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:02+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:02+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
[INFO] 2026-02-28 07:15:03,253 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-28 07:15:03,262 sims.logbook Logbook periodic tasks setup completed

```
EXIT_CODE: 0

## Command
```bash
docker compose -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T backend python manage.py showmigrations --plan > OUT/showmigrations_plan.txt
```

### Output
```
time="2026-02-28T12:15:03+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:03+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:03+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:03+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:03+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:03+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:03+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:04+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
service "backend" is not running

```
EXIT_CODE: 1

## Command
```bash
docker compose -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T web python manage.py showmigrations --plan > OUT/showmigrations_plan.txt
```

### Output
```
time="2026-02-28T12:15:04+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:04+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:04+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:04+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:04+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:04+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:04+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:04+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
[INFO] 2026-02-28 07:15:05,203 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-28 07:15:05,214 sims.logbook Logbook periodic tasks setup completed

```
EXIT_CODE: 0

## Command
```bash
docker compose -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T backend python manage.py migrate --noinput
```

### Output
```
time="2026-02-28T12:15:06+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:06+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:06+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:06+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:06+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:06+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:06+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:06+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
service "backend" is not running

```
EXIT_CODE: 1

## Command
```bash
docker compose -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T web python manage.py migrate --noinput > OUT/migrate_output.txt
```

### Output
```
time="2026-02-28T12:15:06+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:06+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:06+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:06+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:06+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:06+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:06+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:06+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
[INFO] 2026-02-28 07:15:07,229 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-28 07:15:07,239 sims.logbook Logbook periodic tasks setup completed

```
EXIT_CODE: 0

## Command
```bash
docker compose -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T backend python manage.py test --failfast
```

### Output
```
time="2026-02-28T12:15:08+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:08+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:08+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:08+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:08+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:08+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:08+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:08+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
service "backend" is not running

```
EXIT_CODE: 1

## Command
```bash
docker compose -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T web python manage.py test --failfast > OUT/test_failfast_output.txt
```

### Output
```
time="2026-02-28T12:15:08+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:08+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:08+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:08+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:08+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:08+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:08+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:08+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
[INFO] 2026-02-28 07:15:09,579 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-28 07:15:09,589 sims.logbook Logbook periodic tasks setup completed
Creating test database for alias 'default'...
.................................[WARNING] 2026-02-28 07:15:22,281 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:22,285 sims.analytics.event_tracking analytics_event_dropped
.[WARNING] 2026-02-28 07:15:22,340 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:22,345 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:22,349 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:22,358 sims.analytics.event_tracking analytics_event_dropped
.[WARNING] 2026-02-28 07:15:22,416 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:22,419 sims.analytics.event_tracking analytics_event_dropped
..[WARNING] 2026-02-28 07:15:22,516 sims.analytics.event_tracking analytics_event_dropped
/home/sims/.local/lib/python3.11/site-packages/django/db/models/fields/__init__.py:1535: RuntimeWarning: DateTimeField User.date_joined received a naive datetime (2024-02-01 00:00:00) while time zone support is active.
  warnings.warn(
[WARNING] 2026-02-28 07:15:22,536 sims.analytics.event_tracking analytics_event_dropped
...[WARNING] 2026-02-28 07:15:22,647 sims.analytics.event_tracking analytics_event_dropped
/home/sims/.local/lib/python3.11/site-packages/django/db/models/fields/__init__.py:1535: RuntimeWarning: DateTimeField User.date_joined received a naive datetime (2024-01-10 00:00:00) while time zone support is active.
  warnings.warn(
[WARNING] 2026-02-28 07:15:22,665 sims.analytics.event_tracking analytics_event_dropped
...................................................................[WARNING] 2026-02-28 07:15:27,080 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:27,085 sims.analytics.event_tracking analytics_event_dropped
....................[WARNING] 2026-02-28 07:15:28,881 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:28,886 sims.analytics.event_tracking analytics_event_dropped
...[WARNING] 2026-02-28 07:15:29,176 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:29,177 sims.analytics.event_tracking analytics_event_dropped
.[WARNING] 2026-02-28 07:15:29,254 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:29,255 sims.analytics.event_tracking analytics_event_dropped
.[WARNING] 2026-02-28 07:15:29,325 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:29,326 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:29,337 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:29,338 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:29,348 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:29,349 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:29,369 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:29,370 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:29,379 sims.analytics.event_tracking analytics_event_dropped
[WARNING] 2026-02-28 07:15:29,380 sims.analytics.event_tracking analytics_event_dropped
.............................................................................................................................................[WARNING] 2026-02-28 07:15:36,366 sims.analytics.event_tracking analytics_event_dropped
.....[WARNING] 2026-02-28 07:15:36,869 sims.analytics.event_tracking analytics_event_dropped
..[WARNING] 2026-02-28 07:15:37,021 sims.analytics.event_tracking analytics_event_dropped
......
----------------------------------------------------------------------
Ran 286 tests in 18.677s

OK
Destroying test database for alias 'default'...

```
EXIT_CODE: 0

## Command
```bash
docker compose -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T backend python manage.py shell -c "from django.contrib.admin.sites import site; print(len(site._registry)); print('
'.join(sorted([m._meta.label for m in site._registry.keys()])))" > OUT/admin_registry_models.txt
```

### Output
```
time="2026-02-28T12:15:38+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:38+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:38+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:38+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:38+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:38+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:38+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:38+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
service "backend" is not running

```
EXIT_CODE: 1

## Command
```bash
docker compose -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T web python manage.py shell -c "from django.contrib.admin.sites import site; print(len(site._registry)); print('
'.join(sorted([m._meta.label for m in site._registry.keys()])))" > OUT/admin_registry_models.txt
```

### Output
```
time="2026-02-28T12:15:38+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:38+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:38+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:38+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:38+05:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:38+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:38+05:00" level=warning msg="The \"DB_PASSWORD\" variable is not set. Defaulting to a blank string."
time="2026-02-28T12:15:38+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
[INFO] 2026-02-28 07:15:39,866 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-28 07:15:39,876 sims.logbook Logbook periodic tasks setup completed

```
EXIT_CODE: 0

## Command
```bash
docker compose --env-file /srv/apps/pgsims/.env -f /srv/apps/pgsims/docker/docker-compose.prod.yml logs -n 200 backend > OUT/backend_logs_tail.txt 2>&1
```

### Output
```

```
EXIT_CODE: 1

## Command
```bash
docker compose --env-file /srv/apps/pgsims/.env -f /srv/apps/pgsims/docker/docker-compose.prod.yml logs -n 200 web > OUT/backend_logs_tail.txt 2>&1
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
docker compose --env-file /srv/apps/pgsims/.env -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T web python manage.py shell -c "import os; from django.conf import settings; print('SECRET_KEY_LEN', len(settings.SECRET_KEY or '')); print('DATABASE_URL_SET', bool(os.environ.get('DATABASE_URL'))); print('DB_PASSWORD_SET', bool(os.environ.get('DB_PASSWORD')));" > OUT/runtime_env_check.txt
```

### Output
```
time="2026-02-28T12:16:42+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
[INFO] 2026-02-28 07:16:43,436 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-28 07:16:43,446 sims.logbook Logbook periodic tasks setup completed

```
EXIT_CODE: 0

## Command
```bash
docker compose --env-file /srv/apps/pgsims/.env -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T web python manage.py shell -c "from django.utils import timezone; from sims.users.models import User; from sims.logbook.models import LogbookEntry; sup,_=User.objects.get_or_create(username='integrity_sup', defaults={'email':'integrity_sup@example.com','role':'supervisor','specialty':'medicine','first_name':'Integrity','last_name':'Supervisor','is_active':True}); sup.role='supervisor'; sup.specialty='medicine'; sup.is_active=True; sup.set_password('Integrityprint(GET
```

### Output
```
bash: unexpected EOF while looking for matching `"'

```
EXIT_CODE: 2

## Command
```bash
curl -sS -D OUT/api_root_unauth_headers.txt -o OUT/api_root_unauth_body.txt https://pgsims.alshifalab.pk/api/
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
curl -sS -D OUT/auth_login_pg_headers.txt -H 'Content-Type: application/json' -d '{"username":"integrity_pg","password":"Integrityprint(GET
```

### Output
```
bash: unexpected EOF while looking for matching `''

```
EXIT_CODE: 2

## Command
```bash
curl -sS -D OUT/auth_login_sup_headers.txt -H 'Content-Type: application/json' -d '{"username":"integrity_sup","password":"Integrityprint(GET
```

### Output
```
bash: unexpected EOF while looking for matching `''

```
EXIT_CODE: 2

## Command
```bash
curl -sS -D OUT/logbook_my_headers.txt -H 'Authorization: Bearer ' https://pgsims.alshifalab.pk/api/logbook/my > OUT/logbook_my_body.json
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
curl -sS -D OUT/pending_queue_headers.txt -H 'Authorization: Bearer ' https://pgsims.alshifalab.pk/api/logbook/pending > OUT/pending_queue_body.json
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
curl -sS -D OUT/notifications_unread_headers.txt -H 'Authorization: Bearer ' https://pgsims.alshifalab.pk/api/notifications/unread-count > OUT/notifications_unread_body.json
```

### Output
```

```
EXIT_CODE: 0

## Command
```bash
docker compose --env-file /srv/apps/pgsims/.env -f /srv/apps/pgsims/docker/docker-compose.prod.yml exec -T web python manage.py shell -c "...seed integrity smoke users/entry..." > OUT/api_smoke_seed.txt
```

### Output
```
time="2026-02-28T12:18:30+05:00" level=warning msg="/srv/apps/pgsims/docker/docker-compose.prod.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
[INFO] 2026-02-28 07:18:32,021 sims.certificates Certificate periodic tasks setup completed
[INFO] 2026-02-28 07:18:32,031 sims.logbook Logbook periodic tasks setup completed
Traceback (most recent call last):
  File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 918, in get_or_create
    return self.get(**kwargs), False
           ^^^^^^^^^^^^^^^^^^
  File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 639, in get
    raise self.model.DoesNotExist(
sims.users.models.User.DoesNotExist: User matching query does not exist.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/app/manage.py", line 24, in <module>
    main()
  File "/app/manage.py", line 21, in main
    execute_from_command_line(sys.argv)
  File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
    utility.execute()
  File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/__init__.py", line 436, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/base.py", line 412, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/base.py", line 458, in execute
    output = self.handle(*args, **options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/commands/shell.py", line 117, in handle
    exec(options["command"], globals())
  File "<string>", line 1, in <module>
  File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 925, in get_or_create
    return self.create(**params), True
           ^^^^^^^^^^^^^^^^^^^^^
  File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/query.py", line 660, in create
    obj.save(force_insert=True, using=self.db)
  File "/app/sims/users/models.py", line 212, in save
    self.full_clean()
  File "/home/sims/.local/lib/python3.11/site-packages/django/db/models/base.py", line 1502, in full_clean
    raise ValidationError(errors)
django.core.exceptions.ValidationError: {'password': ['This field cannot be blank.']}
```
EXIT_CODE: 1

## Command
```bash
curl -sS -D OUT/api_root_unauth_headers.txt -o OUT/api_root_unauth_body.txt https://pgsims.alshifalab.pk/api/
```

### Output
```
```
EXIT_CODE: 0

## Command
```bash
curl -sS -D OUT/auth_login_pg_headers.txt -H 'Content-Type: application/json' -d '{"username":"integrity_pg","password":"IntegrityPass234"}' https://pgsims.alshifalab.pk/api/auth/login/ > OUT/auth_login_pg_body.json
```

### Output
```
body_saved=OUT/auth_login_pg_body.json
```
EXIT_CODE: 0

## Command
```bash
curl -sS -D OUT/auth_login_sup_headers.txt -H 'Content-Type: application/json' -d '{"username":"integrity_sup","password":"IntegrityPass234"}' https://pgsims.alshifalab.pk/api/auth/login/ > OUT/auth_login_sup_body.json
```

### Output
```
body_saved=OUT/auth_login_sup_body.json
```
EXIT_CODE: 0

## Command
```bash
curl -sS -D OUT/logbook_my_headers.txt -H 'Authorization: Bearer <PG_TOKEN>' https://pgsims.alshifalab.pk/api/logbook/my/ > OUT/logbook_my_body.json
```

### Output
```
body_saved=OUT/logbook_my_body.json
```
EXIT_CODE: 0

## Command
```bash
curl -sS -D OUT/pending_queue_headers.txt -H 'Authorization: Bearer <SUP_TOKEN>' https://pgsims.alshifalab.pk/api/logbook/pending/ > OUT/pending_queue_body.json
```

### Output
```
body_saved=OUT/pending_queue_body.json
```
EXIT_CODE: 0

## Command
```bash
curl -sS -D OUT/notifications_unread_headers.txt -H 'Authorization: Bearer <PG_TOKEN>' https://pgsims.alshifalab.pk/api/notifications/unread-count/ > OUT/notifications_unread_body.json
```

### Output
```
body_saved=OUT/notifications_unread_body.json
```
EXIT_CODE: 0

## Command
```bash
curl -sS -D OUT/api_root_unauth_headers.txt -o OUT/api_root_unauth_body.txt https://pgsims.alshifalab.pk/api/
curl -sS -D OUT/logbook_my_headers.txt -H 'Authorization: Bearer <PG_TOKEN>' https://pgsims.alshifalab.pk/api/logbook/my/ > OUT/logbook_my_body.json
curl -sS -D OUT/pending_queue_headers.txt -H 'Authorization: Bearer <SUP_TOKEN>' https://pgsims.alshifalab.pk/api/logbook/pending/ > OUT/pending_queue_body.json
curl -sS -D OUT/notifications_unread_headers.txt -H 'Authorization: Bearer <PG_TOKEN>' https://pgsims.alshifalab.pk/api/notifications/unread-count/ > OUT/notifications_unread_body.json
```

### Output
```
See generated files:
- OUT/api_root_unauth_headers.txt, OUT/api_root_unauth_body.txt
- OUT/logbook_my_headers.txt, OUT/logbook_my_body.json
- OUT/pending_queue_headers.txt, OUT/pending_queue_body.json
- OUT/notifications_unread_headers.txt, OUT/notifications_unread_body.json
```
EXIT_CODE: 0

## Command
```bash
docker compose --env-file <env> -f <compose> exec -T web pip install inflection
docker compose --env-file <env> -f <compose> exec -T web python manage.py generateschema --format openapi-json > OUT/openapi.json
docker compose --env-file <env> -f <compose> exec -T web python manage.py shell -c "disable drifting PeriodicTask entries"
docker compose --env-file <env> -f <compose> exec -T worker python - <<'PY' ... list celery registered tasks ...
```
### Output
```
See:
- OUT/pip_install_inflection.txt
- OUT/openapi_generation_strict.txt
- OUT/openapi_size_strict.txt
- OUT/periodic_tasks_disable.txt
- OUT/celery_registered_tasks.txt
```
EXIT_CODE: 0

## Command
```bash
python manage.py check
python manage.py test --failfast
python manage.py generateschema / drf-spectacular runtime generation
```
### Output
```
See:
- OUT/manage_check_final.txt
- OUT/test_failfast_final.txt
- OUT/openapi_generation_strict.txt
- OUT/openapi_size_strict.txt
- OUT/openapi.json
```
EXIT_CODE: 0
