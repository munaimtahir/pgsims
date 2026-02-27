# 00_CONTEXT

- Audit target: PGSIMS production stack and domain
- Timestamp (UTC): 2026-02-27T00:39:45.473672+00:00
- Git HEAD: 05e67ec290df24234f04d36aa47c3013376f3314
- Domain audited: https://pgsims.alshifalab.pk
- Compose file: /srv/apps/pgsims/docker/docker-compose.prod.yml
- Active Caddyfile: /etc/caddy/Caddyfile

## Scope executed
Phases A-M were executed with raw evidence captured under `evidence/`.

## Runtime/environment notes (redacted)
- Compose warnings indicate required vars are unset: `SECRET_KEY` (unset), `DB_PASSWORD` (unset).
- Secret values were not recorded in evidence.

## Audit-induced operational actions
- Docker stack commands were executed for observation (`docker compose ps/logs/config`, and health checks).
- API-level workflow simulation created/transitioned at least one logbook record (`entry_id=281`) to validate state machine behavior.
- No source code/config files were edited as part of this audit package generation.

## Known access limitations
- `iptables -S` and Caddy journal full output required root privileges; outputs captured as permission-limited evidence.
