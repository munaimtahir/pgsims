# Android gap-closure test results — 2026-09-20

## Source-level gate

Command:

```bash
cd android
./gradlew :app-companion:testDebugUnitTest :app-companion:lintDebug :app-companion:assembleDebug
```

Result: PASS. 39 unit tests passed, lint reported 0 errors, and debug APK assembly succeeded.
Lint warnings are existing dependency/resource warnings and are not release errors.

## Emulator gate

Environment context was reviewed at `docs/PROJECT_ENVIRONMENT_CONTEXT.md`. No `.docx` copy of that
document exists in the repository. The documented dedicated AVD `pgsims` was started locally and
reported API 36 as `emulator-5554`.

Command:

```bash
cd android
./gradlew :app-companion:connectedDebugAndroidTest
```

Result: PASS — 51 tests executed, 22 intentionally skipped by credential/storage acceptance
guards, 0 failures. The isolated `InboxUiTest` run passed 3/3 tests.

The initial run exposed stale fixtures that expected `/api/notifications/` without the new
`page=1` query. The fixtures were corrected to match the endpoint path independent of query
parameters; the full suite then passed.

## Synthetic process-death gate

Command:

```bash
python3 scripts/verify_android_process_death.py --serial emulator-5554
```

Result: PASS. Post-ack process death, pre-ack cleanup, in-flight upload recovery, source failure,
staging/reconciliation race, and metadata failure each returned `OK (1 test)`.

## Still not verified

Credential-gated authenticated role workflows, live notification recipient isolation, onboarding
schema/password cases, returned leave/evaluation transitions, and production upload success remain
open because no approved credential file was supplied to this run. Physical-device and Play gates
remain intentionally outside this source-gap sprint. No release APK/AAB was rebuilt or uploaded.
