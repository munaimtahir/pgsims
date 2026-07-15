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

require_file "docs/CANONICAL_FRONTEND_ROLE_MATRIX.md"
require_file "docs/CANONICAL_FRONTEND_ROUTE_AUDIT.md"
require_file "docs/FRONTEND_DELETE_CANDIDATES.md"
require_file "frontend/app/supervision/page.tsx"
require_file "frontend/app/supervision/assignments/page.tsx"
require_file "frontend/app/supervision/assignments/new/page.tsx"
require_file "frontend/app/supervision/import/page.tsx"
require_file "frontend/app/supervision/data-quality/page.tsx"
require_file "frontend/app/academics/page.tsx"
require_file "frontend/app/academics/training-records/page.tsx"
require_file "frontend/app/academics/data-quality/page.tsx"

ACTIVE_PATHS=(
  "frontend/app"
  "frontend/components"
  "frontend/lib"
  "frontend/middleware.ts"
)

FORBIDDEN_PATTERN='HOD|UTRMC_ADMIN|SupervisorResidentLink|supervision_link|resident_supervisor_link|supervisor_resident|pg-dashboard|PGDashboard'
if rg -n "$FORBIDDEN_PATTERN" "${ACTIVE_PATHS[@]}" -g '*.ts' -g '*.tsx' >/tmp/check_canonical_frontend_roles_forbidden.txt; then
  cat /tmp/check_canonical_frontend_roles_forbidden.txt
  fail "Forbidden legacy frontend references remain"
fi

if rg -n "/dashboard/resident/(progress|schedule|research|thesis|workshops|postings)" frontend/lib/navRegistry.ts >/tmp/check_canonical_frontend_roles_nav_legacy.txt; then
  cat /tmp/check_canonical_frontend_roles_nav_legacy.txt
  fail "Resident navigation still exposes legacy workflow routes"
fi

if rg -n "/dashboard/supervisor/research-approvals|/dashboard/supervisor/residents/.*/progress" frontend/lib/navRegistry.ts >/tmp/check_canonical_frontend_roles_nav_supervisor_legacy.txt; then
  cat /tmp/check_canonical_frontend_roles_nav_supervisor_legacy.txt
  fail "Supervisor navigation still exposes legacy workflow routes"
fi

python3 - <<'PY'
from pathlib import Path
text = Path("frontend/lib/navRegistry.ts").read_text()
checks = {
    "admin_users": "/users",
    "admin_masters": "/masters",
    "admin_supervision": "/supervision",
    "admin_academics": "/academics",
    "resident_dashboard": "/dashboard/resident",
    "resident_profile": "/complete-profile",
    "supervisor_dashboard": "/dashboard/supervisor",
    "support_dashboard": "/dashboard/utrmc",
}
missing = [name for name, needle in checks.items() if needle not in text]
if missing:
    raise SystemExit(f"Missing nav entries: {', '.join(missing)}")

support_block = text.split("title: 'Support Staff'", 1)[1].split("},", 1)[0]
for forbidden in ["/users", "/masters", "/supervision", "/academics"]:
    if forbidden in support_block:
        raise SystemExit(f"Support staff nav exposes forbidden route: {forbidden}")
PY

echo "PASS: canonical frontend role checks"
