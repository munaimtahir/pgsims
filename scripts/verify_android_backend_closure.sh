#!/usr/bin/env bash
# Run from a committed VPS checkout. No production database/env/volume is used.
set -euo pipefail
image=${1:?pass the existing backend image digest}
mode=${2:-sqlite}
root=$(git rev-parse --show-toplevel)
cd "$root"
network=none
pg_name="android-closure-pg-$$"
net_name="android-closure-net-$$"
cleanup() {
  if [[ "$mode" == postgres ]]; then
    docker rm -f "$pg_name" >/dev/null 2>&1 || true
    docker network rm "$net_name" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT
if [[ "$mode" == postgres ]]; then
  docker network create --internal "$net_name" >/dev/null
  network=$net_name
  docker run -d --rm --name "$pg_name" --network "$network" --network-alias verification-db \
    --memory=512m --cpus=1 --pids-limit=128 --tmpfs /var/lib/postgresql/data \
    -e POSTGRES_PASSWORD=disposable-only -e POSTGRES_USER=verification -e POSTGRES_DB=verification postgres:15 >/dev/null
  for attempt in {1..30}; do
    if docker exec "$pg_name" pg_isready -U verification >/dev/null 2>&1; then break; fi
    sleep 1
  done
fi
git archive HEAD backend deploy/Caddyfile.pgsims docker docs/DEPLOYMENT.md README.md scripts/verify_android_backend_closure.sh |
 docker run --rm -i --network "$network" --memory=1500m --cpus=1 --pids-limit=256 \
 -e SECRET_KEY=disposable-verification-only -e DATABASE_URL=sqlite:////tmp/verification.sqlite3 \
 -e DJANGO_SETTINGS_MODULE=verification_settings -e FCM_ENABLED=False -e VERIFY_MODE="$mode" \
 --entrypoint sh "$image" -c '
set -eu
mkdir -p /tmp/repo
tar -xf - -C /tmp/repo
cd /tmp/repo/backend
cat > /tmp/verification_settings.py <<"PY"
from sims_project.settings_test import *
import os
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "/tmp/verification.sqlite3", "TEST": {"NAME": "/tmp/test-verification.sqlite3"}}}
if os.environ["VERIFY_MODE"] == "postgres":
    DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql", "NAME": "verification", "USER": "verification", "PASSWORD": "disposable-only", "HOST": "verification-db", "PORT": "5432"}}
CELERY_BROKER_URL = "memory://"
CELERY_RESULT_BACKEND = "cache+memory://"
FCM_ENABLED = False
PY
export PYTHONPATH=/tmp:/tmp/repo/backend
if [ "$VERIFY_MODE" = postgres ]; then
 python manage.py test sims.training.tests.LeaveIdempotencyConcurrencyTest --noinput --verbosity=2
else
 python manage.py makemigrations --check --dry-run
 python manage.py migrate --noinput
 python manage.py check
 python manage.py test --noinput --verbosity=2
fi
'
