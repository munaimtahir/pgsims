# API-36 staging runtime verification

Date: 2026-09-08
Target: `pk.vexel.pgrcompanion.staging` built from this worktree with the isolated staging base URL
through the Android emulator loopback tunnel. Device: AdForge API 36, `emulator-5554`, x86_64.

| Gate | Result | Evidence |
| --- | --- | --- |
| Fresh install | PASS | App installed after local app data was cleared. |
| Resident login | PASS | Dedicated staging resident reached Home. |
| Home | PASS | Greeting, onboarding actions, training, supervisor, and document counts rendered from API data. |
| Profile | PASS | Backend-defined fields rendered; editable email saved successfully. |
| Training / supervisor | PASS | Staging programme, department, status, and supervisor rendered. |
| Documents | PASS | Approved, correction-required, and upload-required records rendered. |
| Upload | PASS | SAF-selected PDF uploaded; response refreshed the record to Under review. |
| Logout / re-login | PASS | Logout returned to login; the same staging resident could sign in again. |
| Kill / relaunch | PASS | Authenticated session restored after force-stop. |
| Uninstall isolation | PASS | Reinstall opened at login with no prior session. |
| Crash buffer | PASS | No application crash entries observed in the checked log buffer. |

The test used the purpose-built `seed_android_e2e_demo` staging fixture. Its credentials are
deliberately excluded from this document and were not created in, or tested against, production.

Known test boundary: an expired/revoked refresh token path is covered by unit tests and repository
logic, but was not forced against the staging service because doing so would require mutating the
fixture's active token state.
