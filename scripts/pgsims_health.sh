#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

docker compose -f docker/docker-compose.yml --env-file .env ps

echo "Checking backend health..."
curl -fsS http://127.0.0.1:8014/healthz/

echo
echo "Checking frontend login page..."
curl -fsS http://127.0.0.1:8082/login >/dev/null

echo "PGSIMS health check passed."
