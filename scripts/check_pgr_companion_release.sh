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
grep -q 'versionCode = 4' "$build"
grep -q 'versionName = "1.1.4"' "$build"
grep -q 'PGR Companion' "$strings"
grep -q 'android.permission.INTERNET' "$manifest"
grep -q 'INSTITUTIONAL_API_BASE_URL' "$build"
grep -q 'https://android.pgsims.alshifalab.pk/' "$build"
# Release must be signed with the actual Companion upload key, not the debug/staging key.
grep -q 'signingConfig = signingConfigs.getByName("release")' "$build"
forbidden='localhost|10\.0\.2\.2|example\.com|TODO endpoint|fake|mock'
if command -v rg >/dev/null 2>&1; then
    if rg -n -i "$forbidden" "$root/android/app-portal/src/main" >/dev/null; then
        echo "Forbidden release pattern found in app-portal main source." >&2
        exit 1
    fi
else
    if grep -RniE "$forbidden" "$root/android/app-portal/src/main" >/dev/null; then
        echo "Forbidden release pattern found in app-portal main source." >&2
        exit 1
    fi
fi
test -f "$root/docs/android/pgr-companion-1.0.0/VERIFICATION.md"
test -f "$root/ANDROID_CURRENT_STATE.md"
test -f "$root/PGR_SIMS_ANDROID_API_INTEGRATION.md"
test -f "$root/ANDROID_RELEASE_VERIFICATION.md"
echo "PGR Companion release checks passed"
