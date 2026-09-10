# Android Play Store upload checklist

**Repository-level decision (2026-09-07): the `pk.vexel.pgrcompanion` Play listing is now built
from `android/app-companion` — the login-gated postgraduate management client — and this release
(`versionCode 3` / `1.1.3`) supersedes the prior offline-only `1.0.2` build
the previous offline-only implementation, which has been removed.** There is no second Android
track or separate application.
file's git history — that policy applied until this decision was made.

Reviewer/tester login credentials are **never committed to Git**. They're provided out-of-band
(chat/secure channel) — see the note at the bottom of this checklist for where to find them for
this release.

## Release candidate

- App name: PGR Companion
- Application ID: `pk.vexel.pgrcompanion`
- Version: `1.1.3` (versionCode `3`)
- Source module: `android/app-companion`
- Artifact: `builds/companion/PGR-Companion-1.1.3.aab`
- Target/min SDK: 36 / 26
- Network/authentication: **required** — the app is login-gated end-to-end; there is no offline
  mode in this listing. In-app copy describes it as a "login-gated postgraduate management client"
  (avoid the word "institutional" in any store-listing copy that quotes app text — see below).
- Signing: same upload key as the prior `1.0.2` release (`SHA-256
  a858f42c4460feab688e3e9fce28b3e9e0d5af03a555133e5e134f890b61f010`), so this uploads as a normal
  update to the existing listing rather than a new app.

## Before upload

- [ ] Confirm the upload-key certificate in Play Console matches
      `a858f42c4460feab688e3e9fce28b3e9e0d5af03a555133e5e134f890b61f010` (see
      `ANDROID_RELEASE_VERIFICATION.md` / `docs/COMPANION_CURRENT_STATE.md` for how this was
      independently verified against the actual last-accepted `1.0.0` upload).
- [ ] Confirm versionCode `3` has not already been uploaded for this listing.
- [x] Store listing description — updated by the user directly in Play Console (2026-09-08).
- [x] Data Safety declaration — updated by the user directly from `data_safety_export.csv`
      (2026-09-08). Name/Email/User IDs/Phone are **Required** (app cannot be used without signing
      in); Files & docs remains Optional.
- [x] Reviewer/tester login added by the user in Play Console's App access flow (2026-09-08), using
      the `android.demo.resident1` credential provided out-of-band (synthetic production demo
      account, not a real person).
- [x] **Store listing screenshots** — replaced by the user in Play Console (2026-09-08) with the
      fresh `1.1.3` set from `store_listing_screenshots/pgr-companion-1.1.3/` (login screen,
      onboarding-status screen, documents screen — real production data from the
      `android.demo.resident1` account), replacing the old `pgr-companion-1.0.0/` set.
- [ ] Upload only the frozen AAB above; compare its SHA-256 before selecting it in Play Console:
      `04674c09af765a2d947f98368b91065e29471d9617fe1d731ca21838eee6f068`
- [x] Existing-installed-users concern — **closed 2026-09-07**: confirmed there are no installed
      users of the prior `1.0.2` build, so no migration/warning screen is needed.

## Wording fixed in this release (2026-09-08)

Per explicit instruction, all in-app copy was swept to stop describing the app as "institutional"
and to drop the "Faisalabad Medical University" heading from the login screen specifically
(post-login screens still show the institution name, since that's real per-user data from the
server, not a hardcoded heading):
- Login/error/connected screen titles: "Institutional Workspace" → "PGR Companion"
- Disclaimer: "...is an institutional PGR SIMS client..." → "...is a login-gated postgraduate
  management client..."
- Footer: "Everything in Portal comes from..." → "Everything in PGR Companion comes from..."
- "Could not load institutional information" → "Could not load your PGR SIMS information"
- Removed a stale reference to "Home, Training, Documents and Profile tabs" (leftover copy from an
  earlier single-app design that no longer exists in this module)
- Removed the "Faisalabad Medical University" heading from the sign-in card

## Where the prior offline build stands

The old offline-only implementation has been removed; `scripts/check_pgr_companion_release.sh`
targets the single `app-companion` module — see
`builds/companion/build-info.json` for the full supersession record. It is not currently uploaded
anywhere and has no separate Play listing of its own.
