# Current State Status Report

Date: 2026-05-16

## Purpose

This document captures the current operational state of the PGSIMS codebase and live runtime after the demo-data cleanup and baseline initialization work.

## Executive Summary

- The repository is on branch `codex/dead-code-cleanup`.
- The latest commit is `fb5f25e` (`clean demo data baseline`).
- The worktree is clean and tracked against `origin/codex/dead-code-cleanup`.
- The live application is up and responding on both frontend and backend.
- The live database has been cleaned of the visible fake/demo/E2E surface and reinitialized with only minimal canonical master data.
- Admin access remains intact.
- Core dashboard pages are usable and were smoke-tested successfully.

## Codebase Status

### Repository

- Branch: `codex/dead-code-cleanup`
- HEAD: `fb5f25e`
- Remote tracking: `origin/codex/dead-code-cleanup`
- Worktree: clean

### Source Changes Present

- Added `reset_demo_data` management command for safe demo-data cleanup.
- Added `initialize_pgsims_baseline` management command for minimal canonical initialization.
- Added regression tests for cleanup and baseline initialization.
- Added a Playwright smoke test for the cleaned baseline routes.
- Standardized one stale internal backend string from `programme` to `program` in the active-surface seed command.

### What Was Not Changed

- No route structure changes.
- No visible terminology changes.
- No auth or RBAC redesign.
- No migration resets.
- No destructive database truncation.
- No removal of active workflow code.

## Runtime Status

### Live Services

- Frontend: healthy and responding.
- Backend: healthy and responding.
- Database: healthy.
- Redis: healthy.
- Worker and beat services are running.

### HTTP Checks

- Frontend root: `200 OK`
- Backend root: `200 OK`

### Observed Containers

- `pgsims_frontend` - healthy
- `pgsims_backend` - healthy
- `pgsims_db` - healthy
- `pgsims_redis` - healthy
- `pgsims_worker` - running
- `pgsims_beat` - running

## Data State

### Cleanup Result

The database cleanup removed the fake/demo surface that had been visible in admin and dashboard views.

### Preserved Canonical Data

- One admin/superuser account remains available.
- Canonical hospitals remain.
- Canonical departments remain.
- Canonical hospital-department matrix rows already present in the live database were preserved.

### Current Live Counts Observed

- Users total: `1`
- Superusers: `1`
- Fake users: `0`
- Hospitals total: `4`
- Fake hospitals: `0`
- Departments total: `20`
- Fake departments: `0`
- Matrix rows total: `50`
- Training programs: `0`
- Training records: `0`
- Rotations: `0`
- Leave records: `0`
- Eligibility rows: `0`
- Logbook rows: `0`
- Submission rows: `0`
- Notifications: `0`
- Bulk operations: `0`
- Membership rows: `0`
- HOD assignments: `0`

## Usability Status

### Verified Pages

The following UTRMC/admin routes were verified to load after cleanup:

- `/dashboard/utrmc`
- `/dashboard/utrmc/hospitals`
- `/dashboard/utrmc/departments`
- `/dashboard/utrmc/users`
- `/dashboard/utrmc/matrix`
- `/dashboard/utrmc/hod`
- `/dashboard/utrmc/programs`
- `/dashboard/utrmc/eligibility-monitoring`

### Auth Status

- Admin login remains functional.
- Preserved admin account: `admin`
- Preserved admin email: `admin@pgsims.local`

### Practical Result

The app is usable for manual administrative entry and review on the cleaned baseline. The visible fake/demo records are gone, and the core admin surfaces still render.

## Verification Status

### Backend

- Cleanup command tests: `4 passed`
- Existing seed regression tests: `2 passed`
- Active surface baseline tests: `2 passed`
- Django system check: no issues

### Frontend

- Frontend lint: clean
- Playwright smoke route test: `1 passed`

## Known Risks

- The full backend test suite was not rerun in this final reporting step.
- The canonical matrix was preserved rather than reconstructed, so the remaining `50` rows should still be spot-checked by an admin if the hospital-department mapping needs manual confirmation.
- Any stale terminology outside active backend source, especially in archived docs and historical evidence, was intentionally left in place.

## Final Assessment

GO

The codebase is in a stable, usable state, the runtime is healthy, and the cleaned baseline is working as intended.

