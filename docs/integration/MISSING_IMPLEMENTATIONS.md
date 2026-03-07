# Missing Implementations

**Updated:** 2026-03-07 (Truthmap Remediation Phase)  
**Source:** Direct codebase scan; supersedes auto-generated version

---

## Summary

| Category | Count | Notes |
|----------|-------|-------|
| Backend only, no frontend page | 3 | Postings, templates, milestone-research-req |
| Frontend page confirmed existing | 2 | Thesis ✅, Workshops ✅ (previously reported as missing) |
| Contract added, no implementation | 0 | All Phase 7–8 endpoints are backend-ready |
| Raw API calls wrapped | 2 | MISMATCH-003a/b fixed |

---

## Section 1: Features Previously Reported Missing — Actually Exist

These were reported as missing in the initial document but were confirmed to exist on direct inspection:

| Feature | Backend | API Client | Page | Notes |
|---------|---------|-----------|------|-------|
| Thesis management | ✅ `sims/training/views.py` | ✅ `training.ts` `createThesis`, `submitThesis` | ✅ `/dashboard/resident/thesis/page.tsx` | Fully implemented |
| Workshop completions | ✅ `sims/training/views.py` | ✅ `training.ts` `listWorkshops`, `createWorkshopCompletion` | ✅ `/dashboard/resident/workshops/page.tsx` | Fully implemented |

---

## Section 2: Backend-Only Features (No Frontend Page, Low Priority)

These features have complete backend ViewSets but no frontend pages. They are deferred because they are not in the critical path for the pilot.

| Feature | Backend ViewSet | API Client | Page | Priority |
|---------|----------------|-----------|------|---------|
| Deputation Postings | ✅ `DeputationPostingViewSet` — `POST /api/postings/`, actions: approve/reject/complete | ✗ None | ✗ None | LOW — Defer to Phase 2 |
| Program Rotation Templates | ✅ `ProgramRotationTemplateViewSet` — `GET/POST /api/program-templates/` | ✗ None | ✗ None | LOW — Admin config only |
| Milestone Research Requirements | ✅ `MilestoneResearchRequirement` view | ✗ None | ✗ None | LOW — Part of program config |

---

## Section 3: Contract Additions Made in Remediation Phase

The following were documented in `docs/contracts/API_CONTRACT.md` as Phase 7–8 additions (all already exist in backend):

| Endpoint Group | Contract Section | Backend Status |
|---------------|-----------------|---------------|
| Rotation workflow actions (submit/hod-approve/utrmc-approve/activate/complete/return/reject) | Phase 7 | ✅ Implemented |
| Leave workflow actions (submit/approve/reject) | Phase 7 | ✅ Implemented |
| My Rotations, My Leaves | Phase 7 | ✅ Implemented |
| UTRMC Approval Inboxes | Phase 7 | ✅ Implemented |
| Auth profile endpoints (change-password, password-reset) | Phase 7 | ✅ Implemented |
| Resident summary dashboard | Phase 8 | ✅ Implemented |
| Supervisor summary dashboard | Phase 8 | ✅ Implemented |
| Resident progress (supervisor view) | Phase 8 | ✅ Implemented |
| Audit reports | Phase 8 | ✅ Implemented |

---

## Section 4: Known Gaps (Post-Pilot Roadmap)

| Feature | Description | Phase |
|---------|-------------|-------|
| Posting page | Frontend page for deputation posting management | Post-pilot |
| Program template page | Admin UI for rotation schedule templates | Post-pilot |
| Analytics export | CSV/PDF download of reports | Post-pilot |
