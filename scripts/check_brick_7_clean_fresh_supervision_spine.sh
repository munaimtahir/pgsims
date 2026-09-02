#!/usr/bin/env bash
set -u
set -o pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failures=0

check_file() {
  local path="$1"
  if [[ -f "$path" ]]; then
    printf 'PASS %s\n' "$path"
  else
    printf 'FAIL %s\n' "$path"
    failures=1
  fi
}

check_absent() {
  local path="$1"
  if [[ -e "$path" ]]; then
    printf 'FAIL unexpectedly present %s\n' "$path"
    failures=1
  else
    printf 'PASS absent %s\n' "$path"
  fi
}

echo "Brick 7 supervision spine gate"

check_file "backend/sims/supervision/models.py"
check_file "backend/sims/supervision/services.py"
check_file "backend/sims/supervision/views.py"
check_file "backend/sims/supervision/serializers.py"
check_file "docs/implementation/20260708_brick_7_clean_fresh_supervision_spine/FRONTEND_VERIFICATION.md"
check_file "docs/implementation/20260708_brick_7_clean_fresh_supervision_spine/IMPORT_SPEC.md"
check_file "docs/implementation/20260708_brick_7_clean_fresh_supervision_spine/DATA_QUALITY_SPEC.md"
check_file "docs/implementation/20260708_brick_7_clean_fresh_supervision_spine/PILOT_SEED_DATA.md"
check_file "docs/implementation/20260708_brick_7_clean_fresh_supervision_spine/BUSINESS_RULES.md"
check_file "docs/implementation/20260708_brick_7_clean_fresh_supervision_spine/MODEL_SPEC.md"
check_file "docs/implementation/20260708_brick_7_clean_fresh_supervision_spine/COMPATIBILITY_REVIEW.md"

check_file "frontend/app/dashboard/utrmc/supervision/page.tsx"
check_file "frontend/app/dashboard/utrmc/data-quality/page.tsx"
check_file "frontend/app/supervision/page.tsx"
check_file "frontend/app/supervision/assignments/page.tsx"
check_file "frontend/app/supervision/assignments/new/page.tsx"
check_file "frontend/app/supervision/assignments/[id]/page.tsx"
check_file "frontend/app/supervision/import/page.tsx"
check_file "frontend/app/supervision/data-quality/page.tsx"

legacy_hits="$(rg -n "SupervisorResidentLink" \
  backend/sims/training/views.py \
  backend/sims/users/userbase_views.py \
  backend/sims/users/userbase_serializers.py \
  backend/sims/bulk/services.py \
  backend/sims/bulk/userbase_engine.py \
  frontend/lib/api/departments.ts \
  frontend/lib/api/userbase.ts \
  frontend/lib/api/supervision.ts \
  frontend/app/dashboard/resident/page.tsx \
  frontend/app/dashboard/supervisor/page.tsx \
  frontend/app/dashboard/utrmc/supervision/page.tsx \
  frontend/app/dashboard/utrmc/data-quality/page.tsx \
  frontend/app/supervision \
  -g '!frontend/coverage/**' -g '!**/.next/**' || true)"
if [[ -n "$legacy_hits" ]]; then
  echo "FAIL legacy SupervisorResidentLink references remain:"
  printf '%s\n' "$legacy_hits"
  failures=1
else
  echo "PASS no SupervisorResidentLink references found"
fi

if [[ $failures -ne 0 ]]; then
  echo "Brick 7 supervision spine gate: FAIL"
  exit 1
fi

echo "Brick 7 supervision spine gate: PASS"
