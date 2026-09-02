#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"

for path in \
  docs/implementation/20260626_update_0_universal_identity_dynamic_onboarding/FINAL_VERDICT.md \
  backend/sims/users/management/commands/repair_identity_profiles.py \
  frontend/app/users/new/page.tsx \
  frontend/app/complete-profile/page.tsx
do
  [[ -f "$path" ]] || { echo "Update 0 identity cleanup gate: FAIL"; echo "Missing $path"; exit 1; }
done

echo "Update 0 identity cleanup gate: PASS"
