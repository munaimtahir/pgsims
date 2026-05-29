# Deployment Actions

Target deployment:
- Compose project `docker`
- Compose file `docker/docker-compose.yml`

Actions taken:
1. Removed `python manage.py create_superadmin` from the backend startup command in compose.
2. Recreated `backend`, `worker`, and `beat` services with:

```bash
docker compose --env-file .env -f docker/docker-compose.yml up -d --force-recreate backend worker beat
```

3. Verified the running backend command no longer contains `create_superadmin`.

Current backend container command:

```text
["sh","-c","python manage.py migrate --noinput &&
       python manage.py collectstatic --noinput &&
       gunicorn sims_project.wsgi:application --bind 0.0.0.0:8014 --workers 4 --timeout 60"]
```

Deployment choices intentionally avoided:
- No full backend image rebuild
- No frontend rebuild
- No database volume replacement
- No destructive compose down / volume prune

Reason for conservative deployment:
- The working tree contains many unrelated pre-existing user changes.
- A rebuild from the current worktree would not have been a controlled pilot-safe deployment.

Deployment result:
- Startup behavior was corrected so backend boot does not auto-create admin users.
- Existing cleaned database stayed attached.
- Services remained reachable after recreate.

