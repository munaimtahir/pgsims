#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"
fail=0
check() { if rg -q "$2" "$1"; then echo "PASS $3"; else echo "FAIL $3"; fail=1; fi; }
check backend/sims/users/models.py "class ResidentDocument" "generic resident document model"
check backend/sims/users/models.py "class ResidentDocumentRequirement" "configurable document requirements"
check backend/sims/supervision/models.py "class PendingSupervisorAssignment" "pending supervisor model"
check backend/sims/users/onboarding_api.py "pending_uploads" "specific pending upload state"
check backend/sims/users/services.py "create_supervisor_assignment" "canonical manual supervisor assignment"
check frontend/app/dashboard/resident/documents/page.tsx "Upload Later" "resident document center"
check frontend/app/admin/pending-supervisor-links/page.tsx "Pending Supervisor Links" "admin pending supervisor queue"
test -f ONBOARDING_ARCHITECTURE_FINAL.md && echo "PASS final architecture documentation" || { echo "FAIL final architecture documentation"; fail=1; }
exit "$fail"
