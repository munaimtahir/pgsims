#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="/srv/apps/pgsims"
CANONICAL_CADDYFILE="${REPO_ROOT}/deploy/Caddyfile.pgsims"
ACTIVE_CADDYFILE="/etc/caddy/Caddyfile"

if [[ ! -f "${CANONICAL_CADDYFILE}" ]]; then
  echo "Missing canonical caddy file: ${CANONICAL_CADDYFILE}" >&2
  exit 1
fi

echo "Syncing ${CANONICAL_CADDYFILE} -> ${ACTIVE_CADDYFILE}"
sudo cp "${CANONICAL_CADDYFILE}" "${ACTIVE_CADDYFILE}"

echo "Validating Caddy config..."
sudo caddy validate --config "${ACTIVE_CADDYFILE}"

echo "Reloading Caddy..."
sudo systemctl reload caddy

cat <<'EOF'

Verification checklist:
  [ ] curl -I https://<domain>/
  [ ] curl -I https://<domain>/api/health/
  [ ] curl -I https://<domain>/admin/
  [ ] curl -I https://<domain>/static/admin/css/base.css
  [ ] curl -I https://<domain>/media/

EOF
