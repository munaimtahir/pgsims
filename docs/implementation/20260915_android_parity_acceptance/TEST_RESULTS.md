# Authenticated Android parity acceptance — 2026-09-15

Verdict: **CONDITIONAL GO — profile prerequisites and ADMIN credentials required**.
Candidate branch `feature/android-parity-stages-1-6`, source `595e415` (runtime `800f7ac`).
Device: `pgsims`, emulator-5554, API36; package `pk.vexel.pgrcompanion.debug`, 1.1.10/code10.
APK SHA256: `fbf446cee92b7b80c0c363194f072316c4aba9fbec2cc5f136fffd7f7e2afbdf`.
Production checkout remains `aef3bd2`, backend healthy, image
`sha256:7fe0b71e2c2d5e87e7e36e1ded9deaeab9f74995b9ae965497c3547dba8401e3`.
This run uses the production API with authorized demo accounts. The parity backend routing
changes are not deployed; do not infer full candidate-backend acceptance from this compatibility run.

## Observed account routing

| Role | Fresh login result | Remaining prerequisite |
| --- | --- | --- |
| SUPPORT_STAFF | Dynamic complete-profile form; no dashboard bypass | Phone Number, Email |
| RESIDENT | Dynamic complete-profile form; no dashboard bypass | Academic Session / Induction |
| SUPERVISOR | Dynamic complete-profile form; no dashboard bypass | Phone Number, Email, Supervisor Designation |
| ADMIN | Not run | Authorized credential file/entry not supplied |

Resident forced real 401 → refresh → retried snapshot and notification endpoint reads: PASS,
1 instrumentation test, 8.777s. Supervisor same: PASS, 1 test, 4.910s.
Resident process restart restores the session to the required-profile gate; logout reaches
login form. Remaining staff/supervisor restart/logout checks are being completed.

Reproduction: use `scripts/android_acceptance_ui.py` with `PGR_ACCEPTANCE_CREDENTIALS` pointing
to the owner-controlled JSON. Wait for `Forgot password?` before entering credentials, and the
role-specific completion label before further actions. A transient label containing “Sign in”
is not sufficient to establish completed logout.
Refresh command: `adb -s emulator-5554 shell am instrument -w -e releaseAcceptance authorized-demo
-e expectedRole RESIDENT -e class pk.vexel.pgrcompanion.ReleaseAcceptanceTest#forceRefresh
pk.vexel.pgrcompanion.debug.test/androidx.test.runner.AndroidJUnitRunner` (repeat for SUPERVISOR).

An initial resident refresh invocation failed its stored-token precondition after logout; it did
not exercise refresh. A confirmed fresh resident session was then established and the test passed.
The precondition failure is retained separately and is not represented as an application defect.

## Gates that remain open

- ADMIN login and its authorized UI/actions.
- Complete required demo profile data using owner-provided valid values; then all-role dashboard,
  Inbox isolation/targets and profile action acceptance.
- Password-first/profile-schema change matrix against a disposable candidate backend, plus invalid,
  disabled/revoked session cases. Current production profile values were not altered.
- Role-scoped workflow transitions and offline create/retry/purge with populated authenticated queues.
  Prior synthetic recovery tests pass but do not substitute for these authenticated checks.
- Remaining unchecked roadmap actions in `android.md`; physical-device and signed release gates.

No workflow records, account profile data, passwords, FCM, production services or Caddy were changed.
Only authorized login/refresh/logout sessions and read requests were exercised. No credentials or
tokens are included in evidence.

## Signed 1.1.10 release candidate and final isolated backend gates

- Owner signing configuration produced APK and AAB successfully. Package metadata is
  `pk.vexel.pgrcompanion`, version `1.1.10`, code `10`.
- APK and AAB signatures pass. Certificate SHA-256
  `a858f42c4460feab688e3e9fce28b3e9e0d5af03a555133e5e134f890b61f010` matches the verified
  1.1.9/1.1.3 Play upload certificate.
- APK SHA-256: `d5808f628b84da2575a9b5806a834d6250a2c7aa595b0e243e88c3cc36a91e1a`.
- AAB SHA-256: `46ce93a195d75e334040a176ab11314a133f5928ab10f675e8fe9f0362a6a715`.
- Artifacts are stored locally under `builds/companion/1.1.10/`; signing properties and keys remain
  owner-controlled and are not committed.
- Fetched-candidate VPS isolation passes: SQLite 929 tests in 74.338s with one PostgreSQL-only skip;
  the skipped simultaneous-retry test passes separately on disposable PostgreSQL in 0.671s.
  Migration drift, migrate-from-zero, Django check and repository-aware deployment tests pass.

Play upload/publication and production deployment were not performed. Authenticated dashboard and
workflow acceptance remains blocked by backend-required demo profile values and the absence of an
approved ADMIN credential, not by signing or build failure.
