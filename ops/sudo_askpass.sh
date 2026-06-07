#!/usr/bin/env bash
set -euo pipefail

# Terminal-based askpass helper for sudo -A.
# Prefers an explicit password env var, then a password file, then falls back
# to /dev/tty so it works from an SSH or local terminal session.

if [[ -n "${PGSIMS_SUDO_PASSWORD:-}" ]]; then
  printf '%s\n' "${PGSIMS_SUDO_PASSWORD}"
  exit 0
fi

if [[ -n "${PGSIMS_SUDO_PASSWORD_FILE:-}" ]]; then
  if [[ ! -r "${PGSIMS_SUDO_PASSWORD_FILE}" ]]; then
    echo "PGSIMS_SUDO_PASSWORD_FILE is set but not readable: ${PGSIMS_SUDO_PASSWORD_FILE}" >&2
    exit 1
  fi

  IFS= read -r password < "${PGSIMS_SUDO_PASSWORD_FILE}"
  printf '%s\n' "${password}"
  exit 0
fi

if [[ ! -r /dev/tty ]]; then
  echo "PGSIMS_SUDO_PASSWORD is not set and /dev/tty is unavailable" >&2
  exit 1
fi

printf 'Sudo password: ' > /dev/tty
stty -echo < /dev/tty
IFS= read -r password < /dev/tty
stty echo < /dev/tty
printf '\n' > /dev/tty

printf '%s\n' "${password}"
