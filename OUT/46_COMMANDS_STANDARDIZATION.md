# Commands Standardization

## Before -> After (service token)
- `docker compose ... exec -T web python manage.py migrate`
  -> `docker compose ... exec -T backend python manage.py migrate`
- `docker compose ... logs web`
  -> `docker compose ... logs backend`
- `docker compose ... restart web worker beat`
  -> `docker compose ... restart backend worker beat`

## Updated Surfaces
- `Makefile`
- `scripts/e2e_seed.sh`
- `scripts/local_dev/backend.sh`
- `scripts/local_dev/both.sh`
- `README.md`
- `.github/copilot-instructions.md`
- `docs/contracts/RELEASE_NOTES_20260226.md`

## Canonical Operational Commands (prod)
- Health check:
  - `docker compose -f docker/docker-compose.prod.yml exec -T backend python manage.py check`
- Migrations:
  - `docker compose -f docker/docker-compose.prod.yml exec -T backend python manage.py migrate --noinput`
- Tests:
  - `docker compose -f docker/docker-compose.prod.yml exec -T backend python manage.py test --failfast`
- Logs:
  - `docker compose -f docker/docker-compose.prod.yml logs -n 200 backend`
- Restart:
  - `docker compose -f docker/docker-compose.prod.yml restart backend`
