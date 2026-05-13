# Backup and Rollback Readiness

## Backup artifact

- Path: `docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_pilot_readiness_backup.sql`
- Size: 552 KB

## Backup command

- `docker compose -f docker/docker-compose.yml --env-file .env exec -T db pg_dump -U sims_user sims_db`

## Restore procedure

```bash
docker compose -f docker/docker-compose.yml --env-file .env exec -T db psql -U sims_user sims_db < backups/pgsims_pilot_readiness_backup.sql
```

## Rollback procedure

1. Stop the stack.
2. Check out the previous commit.
3. Rebuild and start the stack with the helper scripts.
4. Verify health.
5. Restore the DB backup only if needed.

## Result

- Backup created successfully.
- No secrets were printed.
