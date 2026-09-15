# Authenticated Android parity acceptance — 2026-09-15

**CONDITIONAL GO: backend/account prerequisites closed; device matrix incomplete.**

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
- Staff: confirmed fresh login to profile gate; dashboard visible after authorized profile completion.
  Final dashboard/Inbox/restoration matrix is not claimed complete.
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

## Current blocking condition and remaining gates

The emulator repeatedly changed foreground to `pk.vexel.medsims/.MainActivity` during this run,
including after explicitly bringing PGR Companion forward. Final dumpsys focus showed MedSIMS
(task209), and the package-filtered PGR helper timed out. Device automation was paused and the
owner was asked to pause the competing session. Do not operate the other app or claim these
interrupted checks as passes.

1. Once `pgsims` is exclusively available, run four-role dashboard, Inbox and profile navigation,
   logout/relogin/restoration after the now-complete demo profiles. ADMIN device login still pending.
2. Full onboarding/password-first/schema-change tests need an isolated candidate backend and
   deliberate fixture states; the completed production demo profiles are not substitutes.
3. Run role-scoped workflow transitions, notification target/read/unread isolation, and authenticated
   offline draft/upload recovery. Earlier synthetic recovery gates remain valid but are separate.
4. Continue unchecked roadmap rows, signed/physical-device/release gates in `android.md`.

Evidence is in `evidence/`; no credentials or tokens are retained there.
