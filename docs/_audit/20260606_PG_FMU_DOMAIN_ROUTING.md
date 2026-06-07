# 2026-06-06 PG.FMU.EDU.PK Routing Update

## Scope

Added `pg.fmu.edu.pk` as a production hostname for the existing PGSIMS application while keeping `pgsims.alshifalab.pk` active as an alias.

## Files Updated

- `deploy/Caddyfile.pgsims`
- `backend/sims_project/settings.py`
- `docker/docker-compose.yml`
- `docker/docker-compose.dev.yml`
- `docker/docker-compose.prod.yml`
- `docker/docker-compose.phc.yml`
- `backend/.env.example`
- `backend/.env.coolify.example`
- `docs/DEPLOYMENT.md`
- `README.md`
- `backend/sims/tests/test_deployment_domain_config.py`

## What Changed

- Caddy now serves both `pg.fmu.edu.pk` and `pgsims.alshifalab.pk` from the same application stack.
- Django host allowlists now include the new domain by default.
- CSRF and CORS origin examples/defaults now include both production domains.
- Production frontend API defaults now point at `https://pg.fmu.edu.pk`.
- Added a regression test that checks the domain wiring across the canonical deployment files.

## Validation

Pending runtime validation on the target host:

```bash
cd /home/munaim/srv/apps/pgsims
./ops/caddy_sync_reload.sh
```

If `sudo` needs askpass handling in a non-interactive context:

```bash
cd /home/munaim/srv/apps/pgsims
./ops/caddy_sync_reload_askpass.sh
```

Then verify:

```bash
curl -I https://pg.fmu.edu.pk/
curl -I https://pgsims.alshifalab.pk/
curl -I https://pg.fmu.edu.pk/api/health/
curl -I https://pg.fmu.edu.pk/admin/
```
