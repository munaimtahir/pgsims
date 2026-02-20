#!/usr/bin/env bash
set -euo pipefail

PROJECT="pgsims"
docker compose -p "$PROJECT" logs --tail=200
