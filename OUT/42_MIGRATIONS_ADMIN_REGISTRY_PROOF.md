# Migrations and Admin Registry Proof

## Compose Context
- Active compose file: `/srv/apps/pgsims/docker/docker-compose.prod.yml`
- Runtime backend service name: `web` (requested `backend` service name is not present in this compose profile)

## Migration and Health Gates
- Django check: `OUT/manage_check_phaseb.txt` (and latest re-run `OUT/manage_check_final.txt`)
- Migration plan: `OUT/showmigrations_plan.txt`
- Migration apply: `OUT/migrate_output.txt`
- Failfast tests: `OUT/test_failfast_output.txt` (latest: `OUT/test_failfast_final.txt`)

## Admin Registry Proof
- Registry dump: `OUT/admin_registry_models.txt`
- Final registry count: `OUT/admin_registry_count_final.txt` (value: 36)

## Gate Result
- `python manage.py check` -> PASS
- `python manage.py showmigrations --plan` -> PASS (captured)
- `python manage.py migrate --noinput` -> PASS
- `python manage.py test --failfast` -> PASS (`Ran 286 tests ... OK`)
- Django admin registry snapshot -> PASS
