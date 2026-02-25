# TRUTHMAP Executive Summary
**Date:** 2026-02-26
**Project:** PGSIMS (UTRMC Rollout)
**Status:** ⚠️ PARTIAL READINESS

## Overview
The PGSIMS codebase is structurally sound, using a modern **Next.js (App Router)** frontend and a **Django/DRF** backend. Most core entities (Users, Logbooks, Rotations) are implemented with comprehensive models. However, critical "last-mile" mismatches in API contracts and field naming will block the Phase 1 supervisor verification workflow.

## Top Blockers
1. **API Field Mismatch (Critical)**: The `LogbookEntry` model uses `supervisor_feedback`, but the verification API view attempts to write to `supervisor_comments`, which will cause a server crash on approval.
2. **Notification Model Drift**: The `LogbookEntry` save signal attempts to create notifications using fields like `user` and `message`, which do not exist in the `Notification` model (which uses `recipient` and `body`).
3. **Duplicate Department Models**: There are two distinct `Department` models (`sims.academics.Department` and `sims.rotations.Department`) which may cause confusion during data migration and rollout.
4. **Missing UTRMC Role**: The system lacks an explicit `utrmc` role; oversight currently relies on the broad `admin` role.

## Phase Readiness Summary
- **Phase 1 (Pilot)**: ⚠️ **PARTIAL** - Blocked by API crashes in supervisor verification.
- **Phase 2 (Compliance)**: ⚠️ **PARTIAL** - Basic analytics exist, but escalation logic is missing.
- **Phase 3 (Eligibility)**: ✅ **PASS** - Attendance-based eligibility calculation is implemented.
- **Phase 4 (Research)**: ⚠️ **PARTIAL** - Research templates exist but lack specialized milestone tracking.

## Known Unknowns
- Exact UTRMC dashboard requirements (currently maps to standard Admin analytics).
- Immutability enforcement details (Audit logs exist via `simple-history`, but explicit "lock" logic for approved entries is soft-coded in views rather than database-level).

## Immediate Next Actions
1. Fix `LogbookEntry` field mismatch (`supervisor_feedback` vs `supervisor_comments`).
2. Sync `Notification` creation calls with the actual model schema.
3. Consolidate or cross-link `Department` models to ensure data integrity.
4. Add `utrmc` role to `User` model for granular oversight auditing.
5. Verify `LogbookEntry` immutability via database-level constraints or more robust view guards.
6. Update `PGLogbookEntrySerializer` to include feedback fields.
7. Perform an E2E test of the "Submit -> Verify" flow to confirm notification delivery.
