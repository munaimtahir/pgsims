# Real Import Clearance Checklist - Final Safety Checkpoint

## Phase 1: Pre-Import Safety Net (Must be COMPLETE)
- [x] Regular System Backup created and path recorded.
- [x] Backup file validated via `validate_system_backup`.
- [x] Backup archive stored safely on external media or secondary server.
- [x] Restore proof verified (Identity and Media preservation proven).
- [x] Super Admin-only restore protection confirmed.

## Phase 2: Data Readiness
- [ ] Official Resident Roster received and formatted.
- [ ] Official Supervisor Roster received and formatted.
- [ ] Hospital/Department/HospitalDepartment mapping verified against target sites.
- [ ] Import templates finalized and distributed.

## Phase 3: Import Execution (The "Golden Path")
- [ ] **Dry-Run Import**: Perform using official data with `Strict Mode` enabled.
- [ ] **Validation Review**: Review error reports; correct all source data anomalies.
- [ ] **Approval**: Obtain stakeholder approval on dry-run counts and site assignments.
- [ ] **Final Backup**: Create a fresh "Clean Baseline" backup immediately before real import.
- [ ] **Real Import**: Execute import with `Strict Mode` (Rollback on any error).

## Phase 4: Post-Import Verification
- [ ] Verify total Resident count matches roster.
- [ ] Verify total Supervisor count matches roster.
- [ ] Spot-check 3-5 placements for site accuracy.
- [ ] Verify login for 1 Sample Resident and 1 Sample Supervisor (using temporary passwords).
- [ ] Create Post-Import Regular System Backup.
- [ ] Create Full Server Recovery Backup.

**Status**: READY FOR PHASE 2. The technical safety net (Phase 1) is fully operational and verified.
