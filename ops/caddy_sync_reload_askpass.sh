#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export SUDO_ASKPASS="${SCRIPT_DIR}/sudo_askpass.sh"

sudo -A bash "${SCRIPT_DIR}/caddy_sync_reload.sh"
