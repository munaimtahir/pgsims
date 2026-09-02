#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/munaim/srv/apps/pgsims"
cd "$ROOT"

fail() {
  echo "Brick 9-10 academic workflows gate: FAIL"
  echo "$1"
  exit 1
}

# 1. File checks
for path in \
  backend/sims/academics/models.py \
  backend/sims/academics/services.py \
  backend/sims/academics/serializers.py \
  backend/sims/academics/views.py \
  backend/sims/academics/workflow_urls.py \
  backend/sims/academics/management/commands/seed_pilot_academic_workflows.py \
  frontend/lib/api/academics.ts \
  frontend/app/academics/evaluations/page.tsx \
  frontend/app/academics/evaluations/new/page.tsx \
  frontend/app/academics/evaluations/[id]/page.tsx \
  frontend/app/academics/evaluations/[id]/review/page.tsx \
  frontend/app/academics/logbook/page.tsx \
  frontend/app/academics/logbook/new/page.tsx \
  frontend/app/academics/logbook/[id]/page.tsx \
  frontend/app/academics/logbook/[id]/review/page.tsx \
  frontend/app/academics/my-progress/page.tsx \
  frontend/app/academics/supervisor-workload/page.tsx \
  frontend/app/academics/workflow-overview/page.tsx \
  frontend/app/academics/workflow-data-quality/page.tsx \
  docs/implementation/20260718_brick_9_10_academic_workflows/DISCOVERY.md \
  docs/implementation/20260718_brick_9_10_academic_workflows/FINAL_VERDICT.md
do
  [[ -f "$path" ]] || fail "Missing required file: $path"
done

# 2. Content check for models
grep -n "class EvaluationSubmission" backend/sims/academics/models.py >/dev/null \
  || fail "Missing EvaluationSubmission model"
grep -n "class EvaluationResponse" backend/sims/academics/models.py >/dev/null \
  || fail "Missing EvaluationResponse model"
grep -n "class LogbookEntry" backend/sims/academics/models.py >/dev/null \
  || fail "Missing LogbookEntry model"
grep -n "class ProcedureRecord" backend/sims/academics/models.py >/dev/null \
  || fail "Missing ProcedureRecord model"

# 3. Content check for frontend API helpers
grep -n "listEvaluationSubmissions" frontend/lib/api/academics.ts >/dev/null \
  || fail "Frontend evaluations API helpers missing"
grep -n "listLogbookEntries" frontend/lib/api/academics.ts >/dev/null \
  || fail "Frontend logbook API helpers missing"

# 4. Old role checks on new evaluation pages
if grep -rn "UTRMC_ADMIN\|SUPER_ADMIN\|SYSTEM_ADMIN\|TEACHER\|STUDENT\|TRAINEE\|DATA_ENTRY\|OFFICE_STAFF\|CLERK\|HOD" \
  frontend/app/academics/evaluations/ \
  frontend/app/academics/logbook/ >/dev/null; then
  fail "Old legacy roles found in new evaluation/logbook page directories"
fi

echo "Brick 9-10 academic workflows gate: PASS"
