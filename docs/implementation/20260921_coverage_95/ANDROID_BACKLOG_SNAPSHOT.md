# Three-account demonstration dataset

## Scope

Seed web/Android examples only for existing `admin`, `supervisor`, `resident`
profiles on the VPS. Preserve identities, credentials, training and primary link.
Owner explicitly authorized demo data on the deployed application. No staff,
new accounts, permission changes, resets, or unrelated deployment changes.
Android work resumes from `docs/_audit/20260921_ANDROID_SPRINT_HANDOFF.md`.

## Completed Work

- Confirmed three active demo logins and resident-to-supervisor primary link.
- Locked four examples each for logbook, evaluations, leave, rotations, documents.
- Implemented guarded seeder and import samples; 15 isolated tests pass, including
  replay, file/database rollback, access checks and real workflow actions.
- Drafted `DEMO_WALKTHROUGH.md`; prior Android scope is preserved in its handoff.

## Pending Work

1. Commit/push source, fetch into VPS, preview/apply/verify the marked dataset.
2. Complete `DEMO_WALKTHROUGH.md` with actual IDs, counts and web/Android limitations;
   preserve pending production records during verification.
