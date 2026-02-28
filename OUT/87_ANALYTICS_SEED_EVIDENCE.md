# Analytics Seed Evidence

No new analytics seed command was added in this fix.

For deterministic local/docker-backed execution, existing idempotent seed command was used:

```bash
cd /home/munaim/srv/apps/pgsims
docker compose --env-file .env -f docker/docker-compose.prod.yml exec -T backend python manage.py seed_e2e
```

Observed output:
- `seed_e2e completed successfully.`

Additional contract/data probe (auth + live feed access):

```bash
curl -X POST https://pgsims.alshifalab.pk/api/auth/login/ ... (admin)
curl -H "Authorization: Bearer <token>" https://pgsims.alshifalab.pk/api/analytics/events/live?limit=5&event_type_prefix=logbook.case
curl -X POST https://pgsims.alshifalab.pk/api/auth/login/ ... (pg)
curl -H "Authorization: Bearer <token>" https://pgsims.alshifalab.pk/api/analytics/events/live?limit=5
```

Observed statuses:
- `admin_live_status=200`
- `pg_live_status=403`
