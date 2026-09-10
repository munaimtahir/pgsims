# 13 — Feature Dependency Graph

Derived from the verified model/workflow/contract findings in files 01-12, not assumed in advance.

## Core chain (verified, not the generic example from the sprint brief)

```
Identity (User + role profile, create_user_with_profile)
      ↓
Org graph (Department / Hospital / HospitalDepartment)
      ↓
ResidentTrainingRecord (training app — the ONE canonical record, post-consolidation, BE-1)
      ↓
   ┌──────────────┬───────────────┬──────────────────┐
   ↓              ↓               ↓                  ↓
RotationAssignment  LeaveRequest   Supervision        LogbookEntry (academics — the REAL one)
   ↓                                (assignment)         ↓
RotationCompletion                                   ProgramMilestone /
                                                      ResidentMilestoneEligibility
                                                         ↑ (SHOULD read academics.LogbookEntry,
                                                            ACTUALLY reads training.LogbookEntry — BE-2)
```

**BE-2 is a dependency-graph break, not just a data-quality note.** `ResidentMilestoneEligibility`
and threshold-based reporting are supposed to depend on real, verified logbook activity — but
their actual dependency edge points at the wrong node (`training.LogbookEntry`, fed only by bulk
import) instead of the node every real user interaction actually writes to
(`academics.LogbookEntry`). Any future feature built "on top of" milestone eligibility (e.g. an
automated milestone-completion notification, a resident progress report) inherits this break
silently. This is why BE-2 sits in Build Wave 0, not Wave 2 — it's foundational to the training
record spine, not a leaf-feature bug.

## Client dependency edges (web / Android against the same backend spine)

```
Backend domain model + RBAC + services (Lane A)
      │
      ├── Web client ── frontend/lib/api/*.ts ── frontend/app/* pages ── navRegistry.ts (nav entry)
      │                                                                       ↑
      │                                                        MISSING for Logbook/Evaluations/
      │                                                        reports/my-progress/monitoring/
      │                                                        workflow-overview (WEB-1) — the
      │                                                        page and API-client layers are both
      │                                                        present and correct; only the LAST
      │                                                        edge (nav wiring) is missing.
      │
      └── Android client ── InstitutionalRepository.kt (Retrofit) ── ResidentWorkflowScreens.kt
                                                                            │
                                                              COMPLETE for Auth/Home/Profile/
                                                              Training/Rotations/Supervision/Logbook.
                                                              Assessments/Research/Workshops stop at
                                                              a read-only summary — the UI layer for
                                                              full CRUD doesn't exist yet, but the
                                                              API edge is already live and stable
                                                              (IMPLEMENTED maturity, per
                                                              06_PLATFORM_API_CONTRACT_MATRIX.md) —
                                                              this is a client-side scope gap, not a
                                                              backend dependency gap.
```

## Contract-documentation dependency (a distinct graph from the code dependency graph)

```
docs/contracts/API_CONTRACT.md  (SUPPOSED to be the integration source of truth per CLAUDE.md)
      │
      ├── LogbookEntry section: STALE (P1-1) — wrong route, wrong fields, wrong action set
      ├── Roles section: STALE (P1-2) — describes a role model that no longer exists in code
      └── Everything else spot-checked (backup_center, bulk import/export, analytics): accurate

docs/contracts/INTEGRATION_TRUTH_MAP.md  (auto-regenerated every push by
      pgsims_drift_gates.yml's `integration-truth-map` CI job, from LIVE backend+frontend
      endpoint extraction)
      │
      └── Necessarily current for whatever it covers (self-verifying by construction) — this is
          why it's more trustworthy in practice than the hand-maintained API_CONTRACT.md, and
          explains HOW the drift in API_CONTRACT.md's logbook section was able to survive a full
          sprint of active logbook development without being caught by CI: CI checks the
          auto-generated truth map, not the hand-written contract doc, and nothing currently
          diffs the two against each other.
```

This is itself a build-order-relevant finding: **the mechanism that would have caught P1-1/P1-2
automatically already exists (`integration-truth-map` CI job) but isn't pointed at the file that
actually drifted.** A cheap Wave 1 fix (not previously identified in files 01-12, surfaced only by
synthesizing them together) is to either (a) have `API_CONTRACT.md` generated/checked against the
same truth-map extraction, or (b) deprecate `API_CONTRACT.md` in favor of
`INTEGRATION_TRUTH_MAP.md` as the CLAUDE.md-designated source of truth, since the truth map cannot
drift the way the hand-maintained doc did.

## Production dependency

```
main branch (backend + frontend + Android source)
      ↓
docker-compose.prod.yml stack (backend/frontend/db/redis/worker/beat) on vps-clone
      ↓
Caddy reverse proxy (pgsims.alshifalab.pk / pg.fmu.edu.pk / api.* / android.*)
```
Currently 1 commit behind main (docs-only, non-blocking). No migration-bearing commits pending.
The dangling `pgr.fmu.edu.pk` Caddy route is an orphaned edge — it depends on nothing in the
current stack and nothing depends on it; safe to remove independently of any other work.

## What this graph implies for sequencing (feeds directly into `15_BUILD_ORDER_AND_ROADMAP.md`)

1. **BE-2 (LogbookEntry split)** sits upstream of any milestone/eligibility/progress-reporting work
   — fix before extending that area.
2. **WEB-1 (nav wiring)** is a leaf-edge fix with no upstream dependency — it can be fixed
   immediately and in parallel with anything else; it is high-value (unlocks a fully-built,
   already-shipped feature) and near-zero-risk (adding nav entries doesn't touch business logic).
3. **Contract doc fixes (P1-1/P1-2)** have no code dependency at all — pure documentation, can run
   fully in parallel with everything, including Android/web feature work, with zero coordination
   cost.
4. **Android Assessments/Research/Workshops UI expansion** depends on a *product* decision (is this
   surface being reactivated for real use, per the "deferred/legacy" classification in
   `06_PLATFORM_API_CONTRACT_MATRIX.md`), not a technical blocker — the API edge is already stable.
5. **XC-1 (credential rotation)** has no code dependency on anything else in this graph — it's a
   pure operations action, deferred per user instruction but independent of all feature work above.
