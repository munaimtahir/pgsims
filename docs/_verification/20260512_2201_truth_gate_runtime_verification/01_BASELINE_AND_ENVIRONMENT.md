# Baseline and Environment

| Item | Evidence | Result |
|---|---|---|
| Working directory | `pwd` | `/home/munaim/srv/apps/pgsims` |
| Branch | `git branch --show-current` | `main` |
| Commit | `git log -1 --oneline` | `1c0639f (HEAD -> main, origin/main, origin/HEAD) audit` |
| Repo status | `git status --short` | clean |
| Env files | `find . -maxdepth 3 -name '.env*' -type f -print` | `.env`, `backend/.env.example`, `frontend/.env.local`, examples |

## Non-secret environment keys

| File | Keys present |
|---|---|
| `.env` | `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`, `DB_PASSWORD`, `DEBUG`, `NEXT_PUBLIC_API_URL`, `SECRET_KEY`, `SECURE_SSL_REDIRECT` |
| `frontend/.env.local` | `NEXT_PUBLIC_API_URL` |

## Runtime settings inside backend container

Command:

```bash
docker compose -f docker/docker-compose.yml --env-file .env exec -T backend python manage.py shell
```

Observed:

| Setting | Value |
|---|---|
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | includes `localhost`, `127.0.0.1`, `backend`, `pgsims_backend` |
| `CORS_ALLOWED_ORIGINS` | configured |
| `CSRF_TRUSTED_ORIGINS` | configured |
| DB engine | PostgreSQL |
| DB connection | OK |

## Environment notes

- The first compose start emitted unresolved-variable warnings for `SECRET_KEY` and `DB_PASSWORD`.
- That warning did not block the local runtime after the stack was started with `--env-file .env`.
- The earlier audit’s `DEBUG=True` observation is not true for the current runtime.
