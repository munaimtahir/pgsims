# Restore Wizard Handoff (2026-06-02 UTC)

## Behavior
When “Download from Drive” succeeds:
- Frontend shows a success message: “Backup downloaded and prepared for restore. Open Restore Wizard to continue.”
- Frontend opens the existing Restore Wizard modal and passes `initialRestoreJobId` so the wizard begins at validation.

## Safety
- The UI does not auto-run restore.
- The existing 5-step wizard remains the only path to confirm and execute restore.

