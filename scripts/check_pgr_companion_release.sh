#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
build="$root/android/app/build.gradle.kts"
manifest="$root/android/app/src/main/AndroidManifest.xml"
strings="$root/android/app/src/main/res/values/strings.xml"
grep -q 'applicationId = "pk.vexel.pgrcompanion"' "$build"
grep -q 'versionCode = 1' "$build"
grep -q 'versionName = "1.0.0"' "$build"
grep -q 'PGR Companion' "$strings"
grep -q 'POST_NOTIFICATIONS' "$manifest"
! grep -q 'INTERNET\|ACCESS_NETWORK_STATE\|fmu_logo\|networkSecurityConfig' "$manifest"
! find "$root/android/app/src/main" -type f -print0 | xargs -0 rg -l 'fmu\.pg\.sims|Faisalabad Medical University|PGR SIMS|FMU' >/dev/null
test -f "$root/docs/android/pgr-companion-1.0.0/VERIFICATION.md"
echo "PGR Companion release checks passed"
