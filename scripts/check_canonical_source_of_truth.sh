#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

for file in \
  "frontend/lib/navRegistry.ts" \
  "frontend/lib/api/supervision.ts" \
  "frontend/lib/api/academics.ts" \
  "frontend/lib/api/dataQuality.ts" \
  "frontend/lib/api/masters.ts" \
  "docs/CANONICAL_FRONTEND_ROLE_MATRIX.md" \
  "docs/CANONICAL_FRONTEND_ROUTE_AUDIT.md"
do
  [[ -f "$file" ]] || fail "Missing canonical source-of-truth artifact: $file"
done

if rg -n "SupervisorResidentLink|supervision_link|HOD|UTRMC_ADMIN|PGDashboard|pg-dashboard" frontend/app frontend/components frontend/lib frontend/middleware.ts -g '*.ts' -g '*.tsx' >/tmp/check_canonical_source_of_truth.out; then
  cat /tmp/check_canonical_source_of_truth.out
  fail "Legacy frontend source-of-truth references remain"
fi

echo "Canonical source-of-truth gate: PASS"
