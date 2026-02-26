#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

docker compose -f docker/docker-compose.yml exec -T web python manage.py migrate --noinput
docker compose -f docker/docker-compose.yml exec -T web python manage.py seed_e2e

echo "E2E seed completed."
