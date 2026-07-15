#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/munaim/srv/apps/pgsims"
cd "$ROOT"

for path in \
  docs/implementation/20260708_brick_6_masters_directory_data_quality/FINAL_VERDICT.md \
  backend/sims/academics/models.py \
  frontend/app/dashboard/utrmc/hospitals/page.tsx \
  frontend/app/dashboard/utrmc/departments/page.tsx \
  frontend/app/dashboard/utrmc/data-quality/page.tsx
do
  [[ -f "$path" ]] || { echo "Brick 6 masters/data-quality gate: FAIL"; echo "Missing $path"; exit 1; }
done

echo "Brick 6 masters/data-quality gate: PASS"
