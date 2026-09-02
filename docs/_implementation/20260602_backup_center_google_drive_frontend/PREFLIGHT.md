# Preflight (2026-06-02 UTC)

## Objective
Frontend-only sprint: fully expose the existing Google Drive backup workflow in the Backup Center UI for Super Admins, without changing routes or redesigning the accepted UI baseline.

## Current verified backend state
- Google Drive backend connector exists and is verified in the running environment.
- Connection health check: healthy (HTTP 200).
- Docker env passthrough for `GOOGLE_DRIVE_*` is working.

## Scope
- Frontend only (UI wiring, polish, tests, evidence).
- Backend changes only if a frontend-blocking API gap is discovered.

