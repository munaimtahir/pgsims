#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

export DB_PASSWORD="${DB_PASSWORD:-pgsims}"
export SECRET_KEY="${SECRET_KEY:-e2e-secret-key}"
export DEBUG="${DEBUG:-True}"
export ALLOWED_HOSTS="${ALLOWED_HOSTS:-localhost,127.0.0.1}"
export CORS_ALLOWED_ORIGINS="${CORS_ALLOWED_ORIGINS:-http://localhost:8082,http://localhost:3000}"
export CSRF_TRUSTED_ORIGINS="${CSRF_TRUSTED_ORIGINS:-http://localhost:8082,http://localhost:3000}"
export NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL:-http://localhost:8014}"
export SECURE_SSL_REDIRECT="${SECURE_SSL_REDIRECT:-False}"
export SESSION_COOKIE_SECURE="${SESSION_COOKIE_SECURE:-False}"
export CSRF_COOKIE_SECURE="${CSRF_COOKIE_SECURE:-False}"
export LOGIN_RATE_LIMIT="${LOGIN_RATE_LIMIT:-500/minute}"

docker compose -f docker/docker-compose.yml up -d --build
docker compose -f docker/docker-compose.yml ps

echo "E2E stack is up."
