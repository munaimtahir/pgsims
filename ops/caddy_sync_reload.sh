#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${PGSIMS_REPO_ROOT:-$(cd "${SCRIPT_DIR}/.." && pwd)}"
CANONICAL_CADDYFILE="${REPO_ROOT}/deploy/Caddyfile.pgsims"
ACTIVE_CADDYFILE="/etc/caddy/Caddyfile"

if [[ ! -f "${CANONICAL_CADDYFILE}" ]]; then
  echo "Missing canonical caddy file: ${CANONICAL_CADDYFILE}" >&2
  echo "Set PGSIMS_REPO_ROOT to the repo root if this checkout lives elsewhere." >&2
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
  [ ] curl -I https://pg.fmu.edu.pk/
  [ ] curl -I https://pgsims.alshifalab.pk/
  [ ] curl -I https://pg.fmu.edu.pk/healthz/
  [ ] curl -I https://pg.fmu.edu.pk/admin/
  [ ] curl -I https://pg.fmu.edu.pk/static/admin/css/base.css
  [ ] curl -I https://pg.fmu.edu.pk/media/

EOF
