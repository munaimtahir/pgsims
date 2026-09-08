#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
android_dir="$repo_root/android"
commit="$(git -C "$repo_root" rev-parse HEAD)"
branch="$(git -C "$repo_root" branch --show-current)"
timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

build_track() {
  local module="$1" label="$2" output="$repo_root/builds/$3" app_id="$4" version="$5"
  mkdir -p "$output"
  (cd "$android_dir" && ./gradlew ":$module:testDebugUnitTest" ":$module:lintDebug" ":$module:assembleRelease" ":$module:bundleRelease")
  cp "$android_dir/$module/build/outputs/apk/release/$module-release.apk" "$output/$label-$version.apk"
  cp "$android_dir/$module/build/outputs/bundle/release/$module-release.aab" "$output/$label-$version.aab"
  printf '{\n  "applicationId": "%s",\n  "version": "%s",\n  "commit": "%s",\n  "branch": "%s",\n  "timestamp": "%s",\n  "compileSdk": 36,\n  "targetSdk": 36,\n  "buildType": "release"\n}\n' "$app_id" "$version" "$commit" "$branch" "$timestamp" > "$output/build-info.json"
  printf '# %s verification\n\nBuilt with unit tests, lint, release APK and release AAB via `scripts/build_android_tracks.sh`.\n' "$label" > "$output/verification-report.md"
}

# As of 2026-09-07, android/app-portal builds the published pk.vexel.pgrcompanion listing
# (login-gated PGR SIMS client), superseding the offline-only android/app-companion module below.
# Both write to builds/companion — see builds/companion/build-info.json for the supersession
# record. android/app-companion is kept building for reference but is frozen/historical and has
# no Play listing of its own.
build_track app-companion PGR-Companion companion pk.vexel.pgrcompanion 1.0.2
build_track app-portal PGR-Companion companion pk.vexel.pgrcompanion 1.1.3
cp "$repo_root/docs/PORTAL_WEB_PARITY_MATRIX.md" "$repo_root/builds/portal/parity-report.md" 2>/dev/null || true
cp "$repo_root/docs/PGR_SIMS_ANDROID_API_INTEGRATION.md" "$repo_root/builds/portal/api-verification.md" 2>/dev/null || true
