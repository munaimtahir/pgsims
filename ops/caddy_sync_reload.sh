#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${PGSIMS_REPO_ROOT:-$(cd "${SCRIPT_DIR}/.." && pwd)}"
CANONICAL_CADDYFILE="${REPO_ROOT}/deploy/Caddyfile.pgsims"
MAINTAINED_CADDYFILE="${PGSIMS_SHARED_CADDYFILE:-/home/munaim/srv/proxy/caddy/Caddyfile}"
ACTIVE_CADDYFILE="${PGSIMS_ACTIVE_CADDYFILE:-/etc/caddy/Caddyfile}"

candidate="$(mktemp)"
trap 'rm -f "$candidate"' EXIT
python3 "${SCRIPT_DIR}/caddy_update_site.py" "$MAINTAINED_CADDYFILE" "$CANONICAL_CADDYFILE" > "$candidate"
sudo caddy validate --config "$candidate" --adapter caddyfile
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
sudo cp -p "$MAINTAINED_CADDYFILE" "${MAINTAINED_CADDYFILE}.${stamp}.bak"
sudo cp -p "$ACTIVE_CADDYFILE" "${ACTIVE_CADDYFILE}.${stamp}.bak"
sudo install -m 644 "$candidate" "$MAINTAINED_CADDYFILE"
sudo install -m 644 "$candidate" "$ACTIVE_CADDYFILE"
if ! sudo systemctl reload caddy; then
  sudo cp -p "${MAINTAINED_CADDYFILE}.${stamp}.bak" "$MAINTAINED_CADDYFILE"
  sudo cp -p "${ACTIVE_CADDYFILE}.${stamp}.bak" "$ACTIVE_CADDYFILE"
  sudo systemctl reload caddy
  echo 'Reload failed; restored previous shared configuration' >&2
  exit 1
fi
printf 'Updated only the PGSIMS site; shared backups: %s\n' "$stamp"
curl --fail --silent --show-error --retry 12 --retry-all-errors --retry-delay 2 --max-time 10 https://pg.vexel.pk/healthz/
