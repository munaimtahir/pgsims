# Missing Implementations

**Generated:** 2026-03-07  
**Source:** Cross-reference of `API_ENDPOINT_CATALOG.md`, `FEATURE_API_MAP.md`, and frontend page structure

---

## Summary

| Category | Count |
|----------|-------|
| Backend implemented, no frontend page | 6 |
| Frontend API client ready, page not confirmed | 4 |
| Contract defined, not implemented | 0 |
| Partially implemented (backend only) | 3 |

---

## Section 1: Backend Endpoints Without a Known Frontend Page

These endpoints are implemented in the backend and have frontend API client functions, but no explicit page was found consuming them in `frontend/app/`.

| Feature | Endpoint | Backend | Frontend API fn | Page |
|---------|----------|---------|----------------|------|
| Thesis management | `GET/POST /api/my/thesis/` | ✓ | `trainingApi.getMyThesis()` | ✗ Not found |
| Thesis submit | `POST /api/my/thesis/submit/` | ✓ | `trainingApi.submitThesis()` | ✗ Not found |
| Workshop listing | `GET /api/workshops/` | ✓ | `trainingApi.listWorkshops()` | ✗ Not found |
| Workshop completions | `GET/POST /api/my/workshops/` | ✓ | `trainingApi.getMyWorkshops()` | ✗ Not found |
| Audit reports | `GET/POST /api/audit/reports/` | ✓ | `auditApi.listReports()` | ✗ Not found |
| Deputation postings | `GET/POST /api/postings/` | ✓ | None | ✗ Not found |

**Recommendation:** Either create the missing pages, or confirm these are admin-only features with no frontend UI yet and mark as intentionally deferred.

---

## Section 2: Frontend API Client Functions Without Confirmed Pages

These API client functions exist in `lib/api/` but could not be confirmed as used by a specific page (may be used indirectly via summary endpoints or not yet wired up).

| Function | Module | Endpoint | Likely Page |
|----------|--------|----------|------------|
| `trainingApi.getMyEligibility()` | `training.ts` | `GET /api/my/eligibility/` | `/dashboard/pg/eligibility` (assumed) |
| `trainingApi.getMilestoneEligibility()` | `training.ts` | `GET /api/utrmc/eligibility/` | `/dashboard/utrmc/eligibility` (assumed) |
| `bulkApi.*` (all bulk functions) | `bulk.ts` | `/api/bulk/*` | `/dashboard/utrmc/bulk` (assumed) |
| `auditApi.*` (all audit functions) | `audit.ts` | `/api/audit/*` | `/dashboard/admin/audit` (assumed) |

---

## Section 3: Partially Implemented Features

### 3.1 Postings (Deputation)

| Layer | Status |
|-------|--------|
| Contract defined | ✗ |
| Backend ViewSet (`DeputationPostingViewSet`) | ✓ |
| Frontend API client | ✗ |
| Frontend page | ✗ |

**Notes:** The `DeputationPostingViewSet` exists in `sims/training/views.py` and is registered at `/api/postings/`. No frontend client functions or pages have been identified for this feature.

### 3.2 Program Rotation Templates

| Layer | Status |
|-------|--------|
| Contract defined | ✗ |
| Backend ViewSet (`ProgramRotationTemplateViewSet`) | ✓ |
| Frontend API client | ✗ |
| Frontend page | ✗ |

**Notes:** Registered at `/api/program-templates/`. No frontend coverage found. May be an admin configuration feature not yet surfaced in the UI.

### 3.3 Milestone Research Requirements Detail

| Layer | Status |
|-------|--------|
| Contract defined | ✗ |
| Backend View (`MilestoneResearchRequirementView`) | ✓ |
| Frontend API client | ✗ (milestones listed but requirements detail not fetched) |
| Frontend page | ✗ |

**Notes:** `GET /api/milestones/{id}/requirements/research/` exists but no frontend client function calls it.

---

## Section 4: Contract Documentation Gaps

These endpoints are fully implemented (backend + frontend) but are NOT yet documented in `docs/contracts/API_CONTRACT.md`. They should be added.

| Feature | Endpoints | Priority |
|---------|----------|---------|
| Research project workflow | `/api/my/research/`, `/api/my/research/action/{action}/` | HIGH |
| Thesis workflow | `/api/my/thesis/`, `/api/my/thesis/submit/` | HIGH |
| Workshop tracking | `/api/workshops/`, `/api/my/workshops/` | MEDIUM |
| Milestone eligibility | `/api/my/eligibility/`, `/api/utrmc/eligibility/` | HIGH |
| Resident summary | `/api/residents/me/summary/` | MEDIUM |
| Supervisor summary | `/api/supervisors/me/summary/` | MEDIUM |
| Supervisor progress | `/api/supervisors/residents/{id}/progress/` | MEDIUM |
| System settings | `/api/system/settings/` | LOW |
| Audit reports | `/api/audit/reports/` | LOW |
| Postings | `/api/postings/` | LOW |
| Program templates | `/api/program-templates/` | LOW |
| Milestone research req | `/api/milestones/{id}/requirements/research/` | LOW |

---

## Section 5: Legacy/Inactive Backend Apps

The following apps exist in `sims/_legacy/` and are **NOT** active in the main URL routing. They are intentionally excluded from this governance system:

| App | Status | Notes |
|-----|--------|-------|
| `sims.cases` | Legacy | Not routed in `sims_project/urls.py` |
| `sims.logbook` | Legacy | Not routed |
| `sims.certificates` | Legacy | Not routed |
| `sims.analytics` | Legacy | Not routed |

These can be safely ignored unless there is a plan to reactivate them, in which case a contract must be defined first.

---

## Action Items

| Priority | Action | Owner |
|----------|--------|-------|
| HIGH | Fix MISMATCH-001: `/api/supervisor-resident-links/` URL in `departments.ts` | Frontend |
| HIGH | Add Phase 6 endpoints to `docs/contracts/API_CONTRACT.md` | Docs |
| MEDIUM | Create missing pages for thesis, workshops, audit reports | Frontend |
| MEDIUM | Add frontend client for postings (`DeputationPostingViewSet`) | Frontend |
| LOW | Verify bulk import endpoint names match backend | Backend + Frontend |
| LOW | Resolve `/api/auth/me/` vs `/api/auth/profile/` duplication | Backend |
