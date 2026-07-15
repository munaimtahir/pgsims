#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

require_file() {
  [[ -f "$1" ]] || fail "Missing required file: $1"
}

require_file "docs/LEGACY_DELETE_CANDIDATES.md"
require_file "docs/FRONTEND_DELETE_CANDIDATES.md"
require_file "docs/CANONICAL_FRONTEND_ROUTE_AUDIT.md"
require_file "docs/CANONICAL_FRONTEND_ROLE_MATRIX.md"
require_file "docs/CANONICAL_SOURCE_OF_TRUTH.md"
require_file "docs/CANONICAL_ROUTE_MAP.md"
require_file "docs/CANONICAL_API_MAP.md"
require_file "docs/DO_NOT_USE_LEGACY_PATHS.md"

for route_file in \
  frontend/app/dashboard/pg/page.tsx \
  frontend/app/dashboard/resident/progress/page.tsx \
  frontend/app/dashboard/resident/schedule/page.tsx \
  frontend/app/dashboard/resident/research/page.tsx \
  frontend/app/dashboard/resident/thesis/page.tsx \
  frontend/app/dashboard/resident/workshops/page.tsx \
  frontend/app/dashboard/resident/postings/page.tsx \
  frontend/app/dashboard/supervisor/research-approvals/page.tsx \
  frontend/app/dashboard/utrmc/users/page.tsx \
  frontend/app/dashboard/utrmc/supervisors/page.tsx \
  frontend/app/dashboard/utrmc/hospitals/page.tsx \
  frontend/app/dashboard/utrmc/departments/page.tsx \
  frontend/app/dashboard/utrmc/matrix/page.tsx \
  frontend/app/dashboard/utrmc/programs/page.tsx
do
  require_file "$route_file"
  if ! rg -n "redirect\\(" "$route_file" >/dev/null; then
    fail "Expected redirect-only legacy route file: $route_file"
  fi
done

for removed_helper in \
  frontend/lib/api/departments.ts \
  frontend/lib/api/hospitals.ts \
  frontend/lib/api/training.ts
do
  if [[ -e "$removed_helper" ]]; then
    fail "Deprecated helper still exists: $removed_helper"
  fi
done

if rg -n "from ['\\\"]@/lib/api/(departments|hospitals|training)['\\\"]|from ['\\\"].*/api/(departments|hospitals|training)['\\\"]" frontend -g '*.ts' -g '*.tsx' >/tmp/check_legacy_delete_candidates_frontend.txt; then
  cat /tmp/check_legacy_delete_candidates_frontend.txt
  fail "Frontend still references deleted helper modules"
fi

if rg -n "SupervisorResidentLink" backend/sims/users/admin.py backend/sims/users/userbase_views.py frontend/app frontend/components frontend/lib -g '*.py' -g '*.ts' -g '*.tsx' >/tmp/check_legacy_delete_candidates_supervisor_link.txt; then
  cat /tmp/check_legacy_delete_candidates_supervisor_link.txt
  fail "Active frontend/runtime code still references SupervisorResidentLink"
fi

echo "PASS: legacy delete candidate checks"
