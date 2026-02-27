# Release Lock Context

- Date: 2026-02-27
- Repo: /srv/apps/pgsims
- Domain: https://pgsims.alshifalab.pk
- Prod compose: /srv/apps/pgsims/docker/docker-compose.prod.yml
- Repo canonical Caddy: /srv/apps/pgsims/deploy/Caddyfile.pgsims
- Active Caddy: /etc/caddy/Caddyfile
- Caddy sync script: /srv/apps/pgsims/ops/caddy_sync_reload.sh
- Expected upstream binds: backend 127.0.0.1:8014, frontend 127.0.0.1:8082

## Scope
This run performed release-lock verification only, with one-shot test checks and evidence capture. No remediation loops were executed.

## Hard Constraints Applied
- No DB wipe and no production data mutation.
- If verification fails, stop further remediation and provide TruthMap + Final Verdict.
- Secrets/tokens redacted by avoiding value dumps of sensitive environment variables.

## Baseline Evidence
- /srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/00_time.txt
- /srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/00_uname.txt
- /srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/00_git_head.txt
- /srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/00_git_status.txt
