# Truth Tests (Must Always Pass)

## Phase 1 Gate — Logbook Verify Flow
- `sims.logbook.test_api.PGLogbookEntryAPITests.test_submit_return_feedback_visible_and_resubmit_approve_flow`

## Migration Gate — Department/Hospital/Rotation (must pass pre/post cutover)
1) Create Hospital, Department, HospitalDepartment
2) Create PG with home_hospital + home_department
3) Create Rotation with (hospital, department)
4) If hospital != home_hospital AND destination department exists in home_hospital:
   - requires override_reason + `utrmc_admin` approval
5) Frontend build must pass

## Drift Gate (static)
Fail if any forbidden patterns appear:
- legacy Notification create keys (`user=`, `message=`, `type=`, `related_object_id=`)
- reintroduction of duplicate Department models

## Analytics Gate
- `sims.analytics.tests.AnalyticsV1ApiTests`
- Must include coverage for:
  - event catalog validation + PII rejection
  - rollup command idempotency
  - live cursor endpoint behavior
  - quality endpoint response shape
