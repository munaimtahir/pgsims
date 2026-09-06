# PGR SIMS staging environment

## Boundary

The canonical remote hostname is `https://staging.pgsims.alshifalab.pk/`. It has no DNS record at
the start of this closure sprint, so it must not be presented as publicly available. Staging may
never use the production database, Redis data, Django secret, or resident accounts.

`docker/docker-compose.staging.yml` is the repository-side isolated target. It uses a distinct
`pgsims-staging` Compose project, its own Postgres/Redis/media volumes, unique database and Redis
namespaces, and binds the backend to loopback port `18014` only. It has no production container or
volume names.

## Provision and verify

Copy `docker/.env.staging.example` to the ignored `docker/.env.staging.local`, generate unique
values, then run:

```bash
docker compose --project-name pgsims-staging --env-file docker/.env.staging.local \
  -f docker/docker-compose.staging.yml up -d --build
docker compose --project-name pgsims-staging --env-file docker/.env.staging.local \
  -f docker/docker-compose.staging.yml exec backend python manage.py check
curl http://127.0.0.1:18014/healthz/
```

For public staging, a deployment operator must create the staging DNS record and add the supplied
`deploy/Caddyfile.pgsims.staging.example` block to the real multi-tenant Caddy configuration. Do
not overwrite the host Caddyfile with that fragment. Enable proxy/secure-cookie/HTTPS variables
only after that edge is active, then verify `https://staging.pgsims.alshifalab.pk/healthz/`.

## Test data and local emulator

Run `seed_org_data`, then `seed_android_e2e_demo`, only in staging. The latter requires
`PGSIMS_ENVIRONMENT=staging` and a 12+ character password in
`PGSIMS_STAGING_ANDROID_DEMO_PASSWORD`; it neither stores nor prints credentials.

For isolated emulator testing, `portalStaging` may use
`-PpgrPortalStagingBaseUrl=http://10.0.2.2:18014/`. Its staging-only network-security policy
permits cleartext only to the emulator host. Normal Portal builds remain HTTPS-only.

## Rollback

Use `docker compose ... down` to stop staging. Retain volumes for diagnosis. Removing the explicit
staging volumes is a deliberate destructive reset and must never target production volumes.
