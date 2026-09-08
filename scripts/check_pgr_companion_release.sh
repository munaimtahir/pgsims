#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# As of 2026-09-07 the published pk.vexel.pgrcompanion listing is built from android/app-portal
# (a login-gated PGR SIMS client), which supersedes the offline-only android/app-companion module
# at versionCode 2 / 1.0.2. This is an explicit repository-level decision — see
# builds/companion/build-info.json and SPRINT_STATE.md.
build="$root/android/app-portal/build.gradle.kts"
manifest="$root/android/app-portal/src/main/AndroidManifest.xml"
strings="$root/android/app-portal/src/main/res/values/strings.xml"
grep -q 'applicationId = "pk.vexel.pgrcompanion"' "$build"
grep -q 'versionCode = 3' "$build"
grep -q 'versionName = "1.1.3"' "$build"
grep -q 'PGR Companion' "$strings"
grep -q 'android.permission.INTERNET' "$manifest"
grep -q 'INSTITUTIONAL_API_BASE_URL' "$build"
grep -q 'https://android.pgsims.alshifalab.pk/' "$build"
# Release must be signed with the actual Companion upload key, not the debug/staging key.
grep -q 'signingConfig = signingConfigs.getByName("release")' "$build"
! grep -rn -E 'localhost|10\.0\.2\.2|example\.com|TODO endpoint|fake|mock' "$root/android/app-portal/src/main" >/dev/null
test -f "$root/docs/android/pgr-companion-1.0.0/VERIFICATION.md"
test -f "$root/ANDROID_CURRENT_STATE.md"
test -f "$root/PGR_SIMS_ANDROID_API_INTEGRATION.md"
test -f "$root/ANDROID_RELEASE_VERIFICATION.md"
echo "PGR Companion release checks passed"
