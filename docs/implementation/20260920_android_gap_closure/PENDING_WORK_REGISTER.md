# Android pending-work register and gap-closure scope

## Source audit

The active Android backlog was reconciled from `android.md`, `SPRINT_STATE.md`, `pendingwork.md`,
the 2026-09-15 parity acceptance/reconciliation reports, Android source, and Android tests.
Older release documents are evidence of previous source states and are not additional current work.

## Status rules

- **Implemented** means source and automated coverage exist.
- **Runtime pending** means source exists but authenticated emulator/device evidence is incomplete.
- **Next sprint** means the capability is not required to close the current parity candidate.
- **Release gate** means external/device/release work after source gap closure.
- **Deferred** means explicitly excluded and must not be revived by this sprint.

## Current gap-closure checklist

| Area | Current state | Required closure evidence |
|---|---|---|
| Pagination | Implemented in repository for current paged endpoints | Unit test plus authenticated multi-page fixture |
| Returned evaluation | UI/repository present; runtime transition not certified | Returned record edit, response preservation, resubmit, same ID |
| Leave editing | UI/repository present for editable states; runtime not certified | Draft/returned PATCH, immutable request ID, resubmit rules |
| Supervisor review | Actions and scoring present; assigned-resident runtime not certified | Start review, score, approve, return/reject reason, refresh |
| Notifications | UI/repository present; full isolation/paging runtime not certified | Four-role recipient isolation, read/unread/preferences, targets |
| Onboarding/session | Backend route handling and unit contracts present | Password-first, schema bump, expiry, refresh failure, restart |
| Offline recovery | Queue/retry/purge coverage present; remaining metadata/lifecycle findings | Duplicate workers, account switch, abrupt death, retry/discard |
| Admin directories/setup/reports | Current read/create/report surfaces present in source | Authenticated role filtering, details, setup, CSV and error states |

## Next-sprint implementation checklist

1. Dedicated role directory/detail management using existing canonical user/profile APIs.
2. Resident progress/report detail and canonical multi-page totals.
3. Generic supervisor review queue/workload/status parity.
4. Admin document requirements, pending supervisor links and supervision mutations.
5. Academic master authoring for training, periods, rotation/evaluation templates and categories.
6. Administrative workflow actions for leaves, logbooks and evaluations.
7. Report detail/filter/export surfaces where backend contracts are available.
8. Standard/flexible import, mapping presets and dry-run/apply behavior.
9. Cross-screen pagination/error/empty/filter regression coverage.

## Release-gate checklist

1. Physical-device install, upgrade, process death, network loss, picker and accessibility checks.
2. Final source freeze, then rebuild the already-approved version `1.1.9` / code `9`.
3. Verify package, signatures, certificate SHA-256 and artifact hashes.
4. Upload only the verified AAB to Play Console and record the console result.

## Explicit exclusions

FCM activation, Google Drive/cloud backup, Android backup/restore UI, production deployment/Caddy,
workflow seed/demo execution, and web-deferred research/thesis/postings/workshops remain excluded.
