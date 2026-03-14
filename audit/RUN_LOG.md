# PGSIMS Audit Run Log (Evidence)

## Environment setup / dependency behavior

```bash
python3 -m pip install -r backend/requirements.txt --dry-run
```

Result: failed with `externally-managed-environment` (PEP 668), requiring `--break-system-packages`.

```bash
python3 -m venv .audit-venv
```

Result: failed: `ensurepip is not available` / `python3.12-venv` missing.

## Backend runnability

```bash
cd backend && SECRET_KEY='audit-secret' DEBUG='True' python3 manage.py check
```

Result: failed with `PermissionError: ... backend/logs/sims_error.log` then `ValueError: Unable to configure handler 'file'`.

Permission evidence:

```bash
ls -ld backend/logs && ls -l backend/logs/sims_error.log
```

Result: `backend/logs/sims_error.log` owned by `ubuntu:ubuntu`, not current user.

```bash
cd backend && SECRET_KEY='audit-secret' DJANGO_SETTINGS_MODULE=sims_project.settings_test python3 manage.py check
cd backend && SECRET_KEY='audit-secret' DJANGO_SETTINGS_MODULE=sims_project.settings_test python3 manage.py migrate --noinput
```

Result: both succeeded; migrations: `No migrations to apply.`

```bash
cd backend && SECRET_KEY='audit-secret' DJANGO_SETTINGS_MODULE=sims_project.settings_test python3 manage.py runserver 127.0.0.1:18014
curl -i http://127.0.0.1:18014/healthz/
```

Result: `HTTP/1.1 200 OK`, JSON:

```json
{"status":"healthy","checks":{"database":"ok","cache":"ok","celery":"not available"}}
```

## Frontend runnability

```bash
cd frontend && npm run build
```

Result: successful production build.

```bash
cd frontend && npm run start -- -p 13000
```

Result: starts and serves 200, but warns:
`"next start" does not work with "output: standalone" configuration. Use "node .next/standalone/server.js" instead.`

```bash
cd frontend && PORT=13001 HOSTNAME=127.0.0.1 node .next/standalone/server.js
curl -I http://127.0.0.1:13001/
```

Result: `HTTP/1.1 200 OK`.

## E2E execution obstacle

```bash
cd frontend && npm run test:e2e:smoke
```

Result: failed before test assertions due filesystem permissions:
- `EACCES: permission denied, rmdir ... frontend/pw-test-results/...`
- `EACCES: permission denied, copyfile ... -> frontend/playwright-report/index.html`

Ownership evidence:

```bash
ls -ld frontend/playwright-report frontend/pw-test-results
```

Result: both owned by `root:root`.
