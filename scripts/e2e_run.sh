#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR/frontend"

export E2E_BASE_URL="${E2E_BASE_URL:-http://localhost:8082}"
export E2E_API_URL="${E2E_API_URL:-http://localhost:8014}"
npm run test:e2e
