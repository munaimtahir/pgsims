# SPRINT_STATE.md — PGR Companion identity migration to the Portal build

## Scope

**Repository-level decision (2026-09-07):** the `pk.vexel.pgrcompanion` Play listing is now built
from `android/app-portal` (a login-gated postgraduate management client) instead of the
offline-only `android/app-companion` module. Explicit, confirmed decision to supersede the
existing Play listing, not an accidental rename. Current release: `versionCode 3` /
`versionName 1.1.3`.

## Completed work

- **Signing-key continuity gate: PASS**, verified against the actual last-accepted Play artifact
  (rebuilt from tag `play-closed-testing-baseline-1.0.0` since no binary of it exists locally or
  in git history; cert extracted independently with `apksigner` and `keytool`, both APK and AAB):
  `a858f42c4460feab688e3e9fce28b3e9e0d5af03a555133e5e134f890b61f010`. The `1.1.3` build is signed
  with this same key — uploads as a normal update, not a new app.
- `android/app-portal/build.gradle.kts` retargeted: `applicationId` → `pk.vexel.pgrcompanion`,
  `versionCode` → `3`, `versionName` → `1.1.3`, real `release` signingConfig wired to
  `-PpgrCompanionSigningPropertiesFile` (previously used the debug key — a deliberate placeholder
  from when this was a dev-only track).
- **Wording swept end-to-end** (final, verified-in-binary state as of the last rebuild): no
  in-app text describes the app as "institutional" anywhere. Screen titles
  ("Institutional Workspace") → "PGR Companion"; disclaimer → "PGR Companion is a login-gated
  postgraduate management client..."; footer "Everything in Portal..." → "Everything in PGR
  Companion..."; error copy "Could not load institutional information" → "...your PGR SIMS
  information"; removed a stale reference to nonexistent "Home/Training/Documents/Profile tabs";
  removed the "Faisalabad Medical University" heading from the **login screen** specifically
  (post-login screens still show it — that's real per-user server data, not a hardcoded label).
  Each wording pass was rebuilt and re-verified by unpacking the actual APK's dex and grepping for
  the old/new strings — not just source-level trust.
- Built, tested, linted, and signed the final `1.1.3` release:
  `builds/companion/PGR-Companion-1.1.3.aab` (SHA-256
  `04674c09af765a2d947f98368b91065e29471d9617fe1d731ca21838eee6f068`) and matching `.apk` (SHA-256
  `71b4d8723f255a054d8b739e593607dd022814c888dc5d9c5680170e155da305`). This is the artifact to
  upload — earlier hashes recorded in chat/docs from intermediate rebuilds are superseded.
- Rewrote `scripts/check_pgr_companion_release.sh` to gate `android/app-portal` instead of the
  superseded `app-companion` checks; passes. `builds/companion/build-info.json` records the full
  supersession and both artifact hashes.
- Corrected `data_safety_export.csv`: personal data collection = true, encrypted in transit =
  true, account creation = none (institution-issued credentials), data deletion supported.
  Name/Email/User IDs/Phone = **Required** (app unusable without signing in, no offline mode left
  in this listing); Files & docs = **Optional**. All Collected-only, never Shared.
- Captured fresh store-listing screenshots on `AdForge_API_36`, logged in live as the reviewer
  demo account, saved to `store_listing_screenshots/pgr-companion-1.1.3/` (login screen,
  onboarding-status screen, documents screen — real production data). These replace the stale
  `pgr-companion-1.0.0/` set, which showed the retired offline app.
- Reset the password for the existing production demo account `android.demo.resident1` (synthetic
  test account, not a real person) and confirmed a live `200` login against
  `https://android.pgsims.alshifalab.pk/`, for use as the Play Console reviewer account. Credential
  given to the user out-of-band (chat only) — never committed to git.
- User has completed, directly in Play Console: store listing/description update, Data Safety form
  update, and adding the reviewer/tester account (App access flow). See
  `docs/ANDROID_PLAY_STORE_UPLOAD_CHECKLIST.md` for the checked-off items.
- Confirmed no installed users exist of the prior `1.0.2` offline build, so the "silent upgrade"
  concern for existing users doesn't apply — no migration/warning screen needed.
- `android/app-companion` (the prior `1.0.2` offline-only build) still exists and still builds, but
  is no longer gated by the release script and has no Play listing of its own — frozen/historical.
- **API-36 release smoke: PASS (2026-09-08).** The signed `1.1.3` Portal APK installed over the
  same-package release on `AdForge_API_36` (Android 16/API 36, x86_64), launched
  `pk.vexel.pgrportal.PortalActivity`, restored the existing encrypted reviewer-demo session, and
  rendered live onboarding/profile data. Home/back exited cleanly; foreground relaunch restored
  the same connected session; the crash buffer remained empty. No credential was read or written.
- Replaced the obsolete `android/README.md` module map and marked the old `:app` verification/state
  files as historical provenance, so the documented canonical build is `:app-portal` 1.1.3.
- Canonical source baseline committed and pushed as `Stabilize PGR Companion Portal release
  baseline`; the tracked project tree is clean at that commit.

## Pending work

1. **User's chosen rollout sequence (2026-09-08): `1.0.2` (`versionCode 2`, the offline
   `app-companion` build — its first-ever Play upload) was uploaded first and is awaiting Play
   review approval. `1.1.3` (`versionCode 3`, the login-gated `app-portal` build that actually
   supersedes it) will be uploaded only after `1.0.2` is approved — not in parallel.** Until then,
   do not treat `1.1.3` upload as ready-to-go without checking back in on `1.0.2`'s review status
   first.
2. Once `1.0.2` is approved: upload `builds/companion/PGR-Companion-1.1.3.aab` (verify SHA-256
   `04674c09af765a2d947f98368b91065e29471d9617fe1d731ca21838eee6f068` before selecting it) — the
   new `store_listing_screenshots/pgr-companion-1.1.3/` set and Data Safety/listing updates are
   already in place in Play Console, so this step alone should complete the `1.1.3` rollout.
3. Optional production-demo closure: use the owner-approved demo credentials to verify one
   successful document upload/resubmission and logout, then re-login and verify uninstall/session
   isolation. Do not mutate the reviewer account without those credentials and explicit approval.
