#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"
files=(backend/sims/users/services.py backend/sims/users/userbase_views.py backend/sims/users/views.py backend/sims/training/views.py backend/sims/bulk/userbase_engine.py backend/sims/bulk/services.py)
if rg -n '(^|[^.[:alnum:]_])user\.supervisor\s*=|(^|[^.[:alnum:]_])supervisor\s*=\s*user\b|__resident_user__supervisor' "${files[@]}"; then
  echo "FAIL: active onboarding/supervision code still writes or queries User.supervisor"
  exit 1
fi
echo "PASS: active onboarding/supervision code has no direct User.supervisor dependency"
