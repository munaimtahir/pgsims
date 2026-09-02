# Baseline Context

Date: 2026-05-16

## Repo State

- Branch: `codex/dead-code-cleanup`
- Current commit: `e21ec23`
- Latest commit message: `add current state report`
- Worktree: clean

## Current-State Report Comparison

The existing report at [`docs/_audit/20260516_CURRENT_STATE_STATUS.md`](/home/munaim/srv/apps/pgsims/docs/_audit/20260516_CURRENT_STATE_STATUS.md) says:

- Branch: `codex/dead-code-cleanup`
- Head: `fb5f25e`
- Worktree: clean
- Live frontend/backend were healthy
- Core admin routes were usable

Current repo inspection matched the branch and clean worktree, but the actual checked-out HEAD is different:

- Reported HEAD: `fb5f25e`
- Actual HEAD: `e21ec23`

That mismatch is the main state drift to note before the audit.

## Runtime Status

- Frontend responded on `http://127.0.0.1:8082`
- Backend responded on `http://127.0.0.1:8014`
- Admin login works with `admin / admin123`
- The live admin account is the only confirmed active account in the current baseline
- UTRMC operational routes return `200` under the admin token
- Resident dashboard API returns `403` for admin on `/api/dashboard/resident/`

## Verified Routes From Current-State Report

- `/dashboard/utrmc`
- `/dashboard/utrmc/hospitals`
- `/dashboard/utrmc/departments`
- `/dashboard/utrmc/users`
- `/dashboard/utrmc/matrix`
- `/dashboard/utrmc/hod`
- `/dashboard/utrmc/programs`
- `/dashboard/utrmc/eligibility-monitoring`

## Audit Evidence Collected

- Route manifest: [`docs/_ui_audit/20260516_ui_truthmap_visual_audit/screenshots/screenshot_manifest.json`](/home/munaim/srv/apps/pgsims/docs/_ui_audit/20260516_ui_truthmap_visual_audit/screenshots/screenshot_manifest.json)
- Screenshots were captured for UTRMC, supervisor, and resident routes under [`docs/_ui_audit/20260516_ui_truthmap_visual_audit/screenshots/`](/home/munaim/srv/apps/pgsims/docs/_ui_audit/20260516_ui_truthmap_visual_audit/screenshots/)
- Live screenshots confirm the UTRMC overview is import-heavy, the matrix is dense, and the resident landing page fails client-side

## Known Risks Before Audit

- Only the admin account is active in the live database snapshot.
- Resident and supervisor user accounts used by earlier E2E harnesses are not present in the current baseline.
- The resident landing dashboard crashes when it tries to render `summary.training_record.*` with a null training record.
- The resident schedule page errors out in the current baseline because resident-only APIs reject the admin token.
- The supervisor resident progress route is reachable, but it is not linked from the visible navigation.

## Summary

The system is live, but the current baseline is not a complete user-surface truth state:

- UTRMC/admin screens are reachable and mostly usable
- Supervisor screens load, but are sparse because there are no resident records
- Resident landing is broken in the current baseline
- Many workflow pages are intentionally deferred or hidden

