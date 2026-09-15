# Authenticated recovery and workflow verification — 2026-09-15

**PASS for the exercised recovery and logbook correction cycle.** Broader parity release remains
CONDITIONAL GO; this report does not certify every roadmap workflow or UI action.

Baseline `70dbb85`, unchanged Android runtime from `800f7ac`. App `pk.vexel.pgrcompanion.debug`,
1.1.10/code10, emulator `pgsims` / emulator-5554 / API36. Production remains on `aef3bd2`.
The checkout stayed on main and the emulator stayed in PGR Companion during this resumed run.
The final signed candidate was subsequently retargeted to 1.1.9/code9 after the owner confirmed
code9 remains unused in Play; that change affects release metadata only, not this tested runtime.

## Results

Seven opt-in instrumentation methods in `AuthenticatedParityRecoveryTest` passed:

| Method | Evidence | Seconds |
| --- | --- | --- |
| prepare | Real resident session, ownership/marker checks on seed leave20, logbook32 and demo document2; no writes | 8.933 |
| stageOffline | With Wi-Fi/data disabled, two encrypted drafts and encrypted synthetic PDF staged | 0.203 |
| verifyAfterRestart | Force-stop followed by fresh instrumentation process retained exact retry keys and PDF bytes | 0.138 |
| replayAndSubmit | Reconnect, recovery replay, empty queues, two further create replays per draft returned same IDs, leave/logbook submitted | 10.951 |
| supervisorReturn | UI login as assigned supervisor; returned synthetic logbook for correction | 6.099 |
| residentCorrectAndResubmit | UI relogin as resident; updated reflection persisted and resubmission succeeded | 2.178 |
| discardAndLogoutOffline | Explicit encrypted-upload discard, restaging plus two drafts, offline application sign-out purged queues and tokens | 0.451 |

Instrumentation calls the installed app repository/recovery service; workflow form entry, the
Android document picker and all transitions are not claimed as UI-tested by these methods.
The previously committed four-role shell matrix remains separate evidence.

## Retained authorized server fixtures

- Leave21: marker `ANDROID-PARITY-20260915-RECOVERY`, submitted, dates2026-11-10 through2026-11-11;
  key `fb7f76c5-dd25-42d7-bb3d-c924260c3e9c`.
- Logbook33: same marker, submitted after supervisor return and resident correction;
  key `786c751e-0134-4784-8d7e-a3caba22b339`.
- Existing synthetic document2 replaced with `ANDROID-PARITY-20260915-RECOVERY.pdf`, 125 bytes,
  SHA256 `034360b8929e7273d543cf892ed752d6f6add7cf407ab271cbdd5a6d290fe5a0`.

Server queries before reconnect found zero matching new records; after retries, exactly one row
exists per key. After offline logout and reconnect, both `-PURGE` record counts remain zero and
original_filename/file hash are unchanged from the successful recovery upload. No unrelated
workflow records were changed. These are deliberately synthetic records without patient data.

## Reproduction and limitations

Build `./gradlew :app-companion:assembleDebugAndroidTest` passed (final build6s); install only its
test APK over the existing matching debug application. Each method is invoked individually:

```sh
adb -s emulator-5554 shell am instrument -w   -e parityAcceptance authorized-demo   -e class pk.vexel.pgrcompanion.AuthenticatedParityRecoveryTest#METHOD   pk.vexel.pgrcompanion.debug.test/androidx.test.runner.AndroidJUnitRunner
```

Use methods in table order, with authorized resident login before prepare, supervisor login before
supervisorReturn, resident login before residentCorrectAndResubmit. Disable both Wi-Fi/data before
stageOffline and discardAndLogoutOffline; force-stop before verifyAfterRestart; reconnect before
replayAndSubmit. The tests skip without explicit opt-in. prepare refuses to overwrite an existing
fixture, validates seed markers/ownership and refuses pre-existing queue contents. Do not run this
sequence against arbitrary identities or document IDs.

An initial UI wait used a nonexistent resident Home label and timed out; the authenticated prepare
method verified the actual resident role. Some first sign-out attempts after instrumentation did
not complete within the helper timeout, including an expired-session error screen. Explicit retry
recovered and subsequent role assertions passed. These attempts are not counted as UI logout
successes, and the complete expired-session/lifecycle UI matrix remains open. The helper now
rejects disabled controls rather than silently tapping them. No app-runtime change was made.

Final state: Wi-Fi/data enabled, app restarted signed out, synthetic host fixture exported to
`evidence/recovery-fixture.json` and removed from app cache, all encrypted recovery queues empty.
Backend healthy. No deployment, Caddy, FCM or Play changes. Existing unit/backend suite evidence
was not rerun because this change only adds opt-in instrumentation and a helper guard.

Still open: evaluation/full review payloads and transitions, full UI workflow forms, remaining
notification target/read/unread and lifecycle/expired-session cases, isolated password/schema
states, unimplemented roadmap rows, and physical-device/release gates.
