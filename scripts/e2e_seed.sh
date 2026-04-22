#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

COMPOSE_ARGS=(--env-file .env -f docker/docker-compose.yml)

for _ in {1..60}; do
  if docker compose "${COMPOSE_ARGS[@]}" exec -T backend python manage.py check >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

docker compose "${COMPOSE_ARGS[@]}" exec -T backend python manage.py seed_org_data
docker compose "${COMPOSE_ARGS[@]}" exec -T backend python manage.py seed_active_surface_baseline
docker compose "${COMPOSE_ARGS[@]}" exec -T backend python manage.py seed_e2e
docker compose "${COMPOSE_ARGS[@]}" exec -T backend python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('E2E cache cleared.')"

echo "E2E seed completed."
