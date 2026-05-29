# Missing Implementations

**Updated:** 2026-04-06 (Contract Remediation Phase)  
**Source:** Direct codebase scan post-discovery audit

---

## Summary

| Category | Count | Notes |
|----------|-------|-------|
| Backend only, no frontend page | 2 | Program templates, milestone-research-req (admin config) |
| Frontend page confirmed existing | 4 | Thesis ✅, Workshops ✅, Postings ✅ (resident + UTRMC pages) |
| Contract added, no implementation | 0 | All Phase 7–8 endpoints are backend-ready |
| Raw API calls wrapped | 0 | All pages use proper API module functions |

---

## Section 1: Features Confirmed Existing (Previously Questioned)

All major resident-facing and UTRMC-facing features have been confirmed operational:

| Feature | Backend | API Client | Pages | Notes |
|---------|---------|-----------|------|-------|
| Thesis management | ✅ `sims/training/views.py` | ✅ `training.ts` `createThesis`, `submitThesis` | ✅ `/dashboard/resident/thesis/page.tsx` | Fully implemented |
| Workshop completions | ✅ `sims/training/views.py` | ✅ `training.ts` `listWorkshops`, `createWorkshopCompletion` | ✅ `/dashboard/resident/workshops/page.tsx` | Fully implemented |
| Deputation postings (resident) | ✅ `sims/training/views.py` | ✅ `training.ts` `createPosting` | ✅ `/dashboard/resident/postings/page.tsx` | Resident submission page operational |
| Deputation postings (UTRMC) | ✅ `sims/training/views.py` | ✅ `training.ts` | ✅ `/dashboard/utrmc/postings/page.tsx` | UTRMC approval page operational |
| Research project | ✅ `sims/training/views.py` | ✅ `training.ts`, `users.ts` | ✅ `/dashboard/resident/research/page.tsx` | Uses proper API modules (no raw apiClient) |

---

## Section 2: Intentionally Deferred Features (Admin Configuration Only)

These features have complete backend ViewSets but no dedicated frontend pages. They are intentionally deferred as they are admin-only configuration features, not in the critical operational path.

| Feature | Backend ViewSet | API Client | Page | Deferred Reason |
|---------|----------------|-----------|------|-----------------|
| Program Rotation Templates | ✅ `ProgramRotationTemplateViewSet` — `GET/POST /api/training/program-templates/` | ⚠️ Partial | ❌ None | Admin-only program configuration; embedded in program detail views; standalone page deferred post-pilot |
| Milestone Research Requirements | ✅ `MilestoneResearchRequirementViewSet` | ⚠️ Partial | ❌ None | Admin-only milestone configuration; embedded in milestone detail views; standalone page deferred post-pilot |

**Note**: Deputation postings are **no longer deferred** — both resident submission and UTRMC approval pages are operational.

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
| Program template dedicated UI | Standalone admin page for rotation schedule templates (currently embedded in program detail) | Post-pilot |
| Milestone research requirements UI | Standalone admin page for milestone research configuration (currently embedded) | Post-pilot |
| Analytics export | CSV/PDF download of advanced analytics reports | Post-pilot |
| Notification preferences UI | User-facing notification preferences management page | Post-pilot |
| Audit log viewer UI | Frontend audit activity log viewer (backend operational, RBAC access via `is_staff`) | Post-pilot |
