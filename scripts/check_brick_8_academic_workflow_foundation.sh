#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/munaim/srv/apps/pgsims"
cd "$ROOT"

fail() {
  echo "Brick 8 academic workflow foundation gate: FAIL"
  echo "$1"
  exit 1
}

for path in \
  backend/sims/academics/models.py \
  backend/sims/academics/services.py \
  backend/sims/academics/permissions.py \
  backend/sims/academics/workflow_urls.py \
  frontend/app/academics/page.tsx \
  frontend/app/academics/training-records/page.tsx \
  frontend/app/academics/periods/page.tsx \
  frontend/app/academics/rotation-templates/page.tsx \
  frontend/app/academics/evaluation-templates/page.tsx \
  frontend/app/academics/logbook-categories/page.tsx \
  frontend/app/academics/review-queue/page.tsx \
  frontend/app/academics/data-quality/page.tsx \
  backend/sims/academics/management/commands/seed_pilot_academics.py \
  docs/implementation/20260713_brick_8_academic_workflow_foundation/DISCOVERY.md \
  docs/implementation/20260713_brick_8_academic_workflow_foundation/FINAL_VERDICT.md
do
  [[ -f "$path" ]] || fail "Missing required file: $path"
done

rg -n "class ResidentTrainingRecord|class AcademicPeriod|class RotationTemplate|class EvaluationFormTemplate|class LogbookCategory|class SupervisorReviewQueueItem" backend/sims/academics/models.py >/dev/null \
  || fail "Missing Brick 8 models"

rg -n "/api/academics/" frontend/lib/api/academics.ts >/dev/null \
  || fail "Frontend academics API helper not wired"

rg -n "My Training" frontend/app/dashboard/resident/page.tsx >/dev/null \
  || fail "Resident dashboard missing My Training section"

rg -n "Academic Review Queue" frontend/app/dashboard/supervisor/page.tsx >/dev/null \
  || fail "Supervisor dashboard missing Academic Review Queue section"

[[ -f frontend/app/residents/[id]/page.tsx && -f frontend/app/supervisors/[id]/page.tsx ]] \
  || fail "Resident/supervisor detail routes missing"

rg -n "ADMIN|RESIDENT|SUPERVISOR|SUPPORT_STAFF" backend/sims/users/models.py frontend/app/users/new/page.tsx >/dev/null \
  || fail "Canonical role surfaces not found"

if rg -n "UTRMC_ADMIN|SUPER_ADMIN|SYSTEM_ADMIN|TEACHER|STUDENT|TRAINEE|DATA_ENTRY|OFFICE_STAFF|CLERK" \
  frontend/app/users/new/page.tsx \
  frontend/lib/navRegistry.ts \
  backend/sims/users/models.py \
  backend/sims/users/services.py >/tmp/brick8_role_hits.txt; then
  fail "Old role references remain in active role surfaces"
fi

echo "Brick 8 academic workflow foundation gate: PASS"
