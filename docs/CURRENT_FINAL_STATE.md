# PGSIMS Current Final State

## Application Metadata
- **App Name**: PGSIMS
- **Version**: Pilot Baseline v1.0
- **Status**: Real-Data Ready Candidate / GO
- **Branch**: `main`
- **Latest Commit Hash**: `2b28525a1ab47ade4b5c5c9bcb4cffd5e3e5e498`
- **Date/Time**: 2026-05-29T11:00:00Z

## Current Model Decision
The PGSIMS data model is strictly locked:
- **Hospital**: Canonical Hospital entity.
- **Department**: Single canonical department/specialty list (`academics.Department`). No separate academic vs rotation department models exist.
- **HospitalDepartment**: The only hospital-department matrix.
- **Resident Placements / Rotations**: Points directly to `HospitalDepartment`.
- **Supervisor Assignments**: Mapped within canonical department context.

## Cleanup Summary
- **Database Schema**: Deleted legacy undergraduate models `Batch` and `StudentProfile`.
- **Codebase Cleanups**: Removed unused directories, deprecated variables, and temporary files.
- **Documentation**: Archiving all presentation, staging, and discovery documents under `docs/ARCHIVE/`.

## Test Result Summary
- **Backend Unit Tests**: 358 passed / 358 total (100% success rate).
- **Django system check**: Passed (0 errors).
- **Migration dry-run**: No changes detected.

## Known Issues
- Playwright E2E tests have dashboard timing issues locally. Handled using explicit wait shims.

## Next Approved Step
- Deploy to the staging server and initiate the real data onboarding import workflow using the provided Urology pilot roster.
