# Authenticated Android parity acceptance — 2026-09-15

**CONDITIONAL GO: final signed 1.1.9/code9 candidate and four-role shell matrix pass; broader
workflow matrix remains.**

Candidate source `595e415` (runtime `800f7ac`), branch `feature/android-parity-stages-1-6`.
Device `pgsims`, emulator-5554, API36; `pk.vexel.pgrcompanion.debug`, 1.1.10/code10.
APK SHA256 `fbf446cee92b7b80c0c363194f072316c4aba9fbec2cc5f136fffd7f7e2afbdf`.
Production checkout `aef3bd2`; healthy backend image
`sha256:7fe0b71e2c2d5e87e7e36e1ded9deaeab9f74995b9ae965497c3547dba8401e3`.
The parity backend routing changes are not deployed; these are compatibility checks against the
current production backend, not complete certification of the combined backend candidate.

## Authorized demo setup

The owner supplied ADMIN credentials and explicitly authorized demo profile values/backend repair.
Credentials are retained only in the owner-controlled private JSON (mode 600), never in this report.

Initial device routing correctly prevented dashboard access for staff (phone/email), resident
(academic session), and supervisor (phone/email/designation). ADMIN API reported missing phone.
The session/designation options endpoint returned fallback codes without stored lookup rows;
submitting the offered resident session returned 400. Two explicitly labeled master lookup records
were created transactionally on the VPS, with `ANDROID_ACCEPTANCE_LOOKUP_CREATED` audit entries:

- AcademicSession id1, code `ANDROID-DEMO-2026`, name `ANDROID PARITY DEMO 2026-2027`.
- Designation id1, code `ANDROID-DEMO`, name `ANDROID PARITY DEMO Supervisor`.

Only the four authorized demo profiles were completed through `POST /api/auth/complete-profile/`:

| Account | Assigned demo fields |
| --- | --- |
| staff | phone +923000000101; email android-parity-staff@example.invalid |
| resident | academic_session_ref ANDROID-DEMO-2026 |
| supervisor | phone +923000000103; email android-parity-supervisor@example.invalid; designation_ref ANDROID-DEMO |
| admin | phone +923000000104 |

Subsequent complete-profile and auth/me checks show no missing required fields for all four roles.
Existing nonmissing values, passwords and unrelated workflow records were not changed. Demo fields
and lookup records are intentionally retained to support the next acceptance run. No deployment,
Caddy, FCM, notification delivery or Play changes were made.

## Completed verification

- Resident: confirmed fresh login to dynamic required-profile gate; force-stop/restart restores that
  gate; logout reaches login form. Forced 401 → real refresh → retried snapshot and notification
  endpoint reads PASS (1 test, 8.777s).
- Supervisor: confirmed fresh login to required-profile gate; restored session retains gate and
  logout reaches login form. Same forced-refresh check PASS (1 test, 4.910s).
- Final four-role shell run after profile completion:
  - SUPPORT_STAFF: Home, Inbox, Profile, force-stop/session restoration and logout PASS.
  - RESIDENT: Home, Inbox, Profile, force-stop/session restoration and logout PASS.
  - SUPERVISOR: Home, Inbox, Profile, force-stop/session restoration and logout PASS.
  - ADMIN: Home, paged Users directory, universal-create dialog (opened/cancelled without mutation),
    Inbox, Profile, force-stop/session restoration and logout PASS.
- All four roles: authenticated notification reads succeed. Resident/supervisor each see their own
  three labeled notification fixtures; no other role's labeled fixtures appear. Staff/admin have
  no labeled fixtures, so their empty result alone does not prove cross-recipient isolation.
- Staff, resident and supervisor: GET users lists exactly their own identity; another identity
  returns404; forged POST users is denied403. ADMIN directory API returns200.

Reproduction: `scripts/android_acceptance_ui.py`, with `PGR_ACCEPTANCE_CREDENTIALS` set to the
private JSON; wait for `Forgot password?` before login and the exact role's destination afterward.
Use explicit `adb shell am start -n pk.vexel.pgrcompanion.debug/pk.vexel.pgrcompanion.CompanionActivity`
for launches rather than a random Monkey event. Helper now re-reads field coordinates after IME
changes, verifies username input without logging it, and only reads nodes in the target package.
Refresh: `adb -s emulator-5554 shell am instrument -w -e releaseAcceptance authorized-demo
-e expectedRole RESIDENT -e class pk.vexel.pgrcompanion.ReleaseAcceptanceTest#forceRefresh
pk.vexel.pgrcompanion.debug.test/androidx.test.runner.AndroidJUnitRunner` (repeat SUPERVISOR).

Initial refresh invocation had no stored session and failed its precondition; after confirmed
resident login it passed. Preserve that log separately rather than treating it as a product failure.
The routing timeout logs are likewise retained and not counted as passing tests.

## Final Play-version retarget and signed artifacts

The owner confirmed versionCode 9 has not been uploaded to Play. The merged parity runtime was
therefore rebuilt with final package metadata `pk.vexel.pgrcompanion`, version 1.1.9/code9. The
complete Gradle gate passed: 41 unit tests, lint (0 errors), debug APK, Android-test APK, signed
release APK and signed AAB. APK signature and AAB JAR verification pass; certificate SHA-256
`a858f42c4460feab688e3e9fce28b3e9e0d5af03a555133e5e134f890b61f010` matches the established
release identity.

- APK: `builds/companion/1.1.9-parity-main/PGR-Companion-1.1.9-parity.apk`, SHA-256
  `376ecbda92761f76b5eab39820d4063348ba1e9508b7ce98c88fbf8807ba1b94`.
- AAB: `builds/companion/1.1.9-parity-main/PGR-Companion-1.1.9-parity.aab`, SHA-256
  `3ff3d81a4de04875dab7c665feae70185e34a5af4364c174611df796e7846432`.

The previous `builds/companion/1.1.9/` binaries and superseded 1.1.10 candidate remain preserved;
neither was overwritten. Emulator acceptance above was run on 1.1.10/code10 before the owner's
clarification. The only subsequent source change was version metadata, and the full build/test gate
was rerun after that change.

The rebuilt debug APK initially met Android's expected downgrade rejection because code10 remained
installed on the emulator. It was then installed on the test-only `pgsims` emulator using `adb -d`;
`dumpsys` confirmed 1.1.9/code9. The matching test APK installed and the default, noncredentialed
instrumentation invocation completed `OK (29 tests)` in 23.66 seconds. Authenticated destructive
acceptance methods remain opt-in and were not rerun during this metadata-only retarget.

## Remaining gates

Fetched-candidate VPS isolation also passes: SQLite 929 tests (one PostgreSQL-only skip) and the
separate disposable PostgreSQL concurrency test pass; migration drift, migrate-from-zero, Django
check and repository-aware deployment tests pass. No production database or volume was used.

1. Full onboarding/password-first/schema-change tests need an isolated candidate backend and
   deliberate fixture states; the completed production demo profiles are not substitutes.
2. Run role-scoped workflow transitions, notification target/read/unread isolation, and authenticated
   offline draft/upload recovery. Earlier synthetic recovery gates remain valid but are separate.
3. Continue unchecked roadmap rows and physical-device/Play release gates in `android.md`.

Evidence is in `evidence/`; no credentials or tokens are retained there.
The candidate was merged directly and pushed to `main`; production deployment and Play upload were
not performed.

## Resumed authenticated recovery run

[Recovery and workflow results](RECOVERY_WORKFLOW_RESULTS.md): seven opt-in device tests PASS for
restart/replay, server exactly-once records, PDF hash, supervisor return/resident correction and
offline discard/logout purge. These repository/service-level tests do not close every UI workflow
or expired-session lifecycle gate. Production remains unchanged.
