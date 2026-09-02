# Directory Cleanup Summary

This document details the cleanup and archiving process completed during the Final Application Standardization & Real-Data Readiness Sprint.

## Overview
All legacy, discovery, temporary, staging, mobile-proposal, and obsolete documentation files have been archived under `docs/ARCHIVE/` to ensure the repository has a single source of truth for all current features, workflows, deployment, and operation guides. 

## Archived Directories & Files

The following files and folders have been consolidated and moved to the [docs/ARCHIVE/](file:///home/munaim/srv/apps/pgsims/docs/ARCHIVE/) directory:

1. **Obsolete/Deprecated Analytics Specifications**:
   - `docs/ANALYTICS_UI_SPEC.md`
   - `docs/ANALYTICS_DIMENSIONS.md`
   - `docs/ANALYTICS_GOVERNANCE.md`
   - `docs/ANALYTICS_LIVE_FEED.md`
   - `docs/ANALYTICS_RUNBOOK.md`
   - `docs/ANALYTICS_PERFORMANCE.md`
   - `docs/ANALYTICS_OPENAPI.md`
   - `docs/ANALYTICS_MEGAPASS_REPORT.md`
   - `docs/ANALYTICS_BLUEPRINT.md`
   - `docs/copilot_session.md`

2. **Mobile Architecture Proposals**:
   - `docs/_mobile_android/` (Mobile MVP, Android App architecture proposals)

3. **Stale Developer Entrypoints & Staging Configs**:
   - `docs/MCP_PLAYWRIGHT_AGENT.md`
   - `docs/AI_AGENT_ENTRY_POINTS.md`
   - `docs/deploy/CADDY_ROUTINE.md`
   - `docs/testing/playwright-runbook.md`
   - `docs/testing/playwright-coverage-matrix.md`
   - `docs/testing/playwright-suite.md`

4. **Stale Handoffs & Older Remediation Reports**:
   - `docs/HANDOFF_PROD_GATE_20260422.md`
   - `docs/HANDOFF_PROD_GATE_20260422T221254Z.md`
   - `docs/REMEDIATION_SPRINT_SUMMARY.md`

5. **Legacy Integration Maps & Mismatch Reports**:
   - `docs/integration/` (various API catalogs, frontend/backend mismatch maps, manifest, and data shape documents)

6. **Staging / Temporary Screenshots & Verification Snapshots**:
   - `docs/_ui_audit/` (visual audit findings, recommended UI architecture, route truthmaps, screenshots)
   - `docs/_truthmap/` & `docs/_truthmap_docker_fix/` (older baseline snapshots)
   - `docs/_verification/` (verification matrices, deployment tests, audit execution notes)
   - `docs/_recovery/` (earlier codebase state snapshots)
   - `docs/_pilot_cleanup/`, `docs/_pilot_import/`, `docs/_pilot_launch/`, `docs/_cleanup/`, `docs/_milestones/`

7. **Stale Case Seeds & CSV Datasets**:
   - `docs/PGSIMS_Demo_CaseSeed_3Months.csv`
   - `docs/PGSIMS_Demo_CaseSeed_3Months.xlsx`

## Preserved Files
- Full project source code in `backend/` and `frontend/`
- Database migrations in `backend/sims/migrations/` (and other sub-apps)
- Frontend unit tests and E2E Playwright smoke tests
- Required JSON seed fixtures in `backend/sims/users/fixtures/` and custom management commands
- Deployment config files and Docker setup scripts

This cleanup establishes a clean baseline with no duplicate directories or confusing legacy documents.
