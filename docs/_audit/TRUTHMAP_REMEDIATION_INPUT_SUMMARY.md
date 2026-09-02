# Truthmap Remediation — Input Summary

**Date:** 2026-03-07  
**Phase:** A — Read Governance  
**Purpose:** Summarise all authoritative inputs before executing remediation

---

## 1. Contract Location

| Document | Path | Authority |
|----------|------|-----------|
| API Contract | `docs/contracts/API_CONTRACT.md` | Canonical source of truth |
| Data Model | `docs/contracts/DATA_MODEL.md` | Entity definitions |
| RBAC Matrix | `docs/contracts/RBAC_MATRIX.md` | Role permissions |
| Routes | `docs/contracts/ROUTES.md` | Frontend route structure |
| Terminology | `docs/contracts/TERMINOLOGY.md` | UI terminology |
| API Source of Truth | `governance/API_SOURCE_OF_TRUTH.md` | Governance declaration |
| Integration Truth Map | `docs/integration/BACKEND_FRONTEND_TRUTHMAP.md` | Feature integration map |
| Mismatch Report | `docs/integration/MISMATCH_REPORT.md` | Known divergences |
| Missing Implementations | `docs/integration/MISSING_IMPLEMENTATIONS.md` | Gaps in current scope |

---

## 2. Role Model (Verified)

| Role | Code | Permissions |
|------|------|------------|
| System Admin | `admin` | Full — requires `is_staff=True` |
| UTRMC Admin | `utrmc_admin` | Org config + approvals |
| UTRMC Staff | `utrmc_user` | Read-only oversight |
| Supervisor | `supervisor` | Assigned residents only |
| PG/Resident | `pg` / `resident` | Own records only |

Permission classes verified against test suite (103/103 tests pass):
- `IsTechAdmin` = `role=="admin" AND is_staff`
- `IsManager` = `role in ["admin", "utrmc_admin"]`
- `IsAdminUser` (DRF) = `is_staff` — only admin qualifies

---

## 3. Current Feature Map

### Fully Implemented (Backend + Frontend + Page)

| Feature | Backend | API Client | Page |
|---------|---------|-----------|------|
| Auth (login/register/logout/profile) | ✓ | `auth.ts` | `/login`, `/register` |
| Hospitals CRUD | ✓ | `hospitals.ts` + `userbase.ts` | `/utrmc/hospitals` |
| Departments CRUD | ✓ | `departments.ts` + `userbase.ts` | `/utrmc/departments` |
| Hospital-Dept matrix | ✓ | `departments.ts` + `userbase.ts` | `/utrmc/matrix` |
| Users management | ✓ | `users.ts` + `userbase.ts` | `/utrmc/users` |
| Supervision links | ✓ | `userbase.ts` | `/utrmc/supervision` |
| HOD assignments | ✓ | `departments.ts` + `userbase.ts` | `/utrmc/hod` |
| Training programs | ✓ | `training.ts` | `/utrmc/programs` |
| Research project | ✓ | `training.ts` | `/resident/research` |
| Thesis | ✓ | `training.ts` | `/resident/thesis` |
| Workshops | ✓ | `training.ts` | `/resident/workshops` |
| Eligibility monitoring | ✓ | `training.ts` | `/utrmc/eligibility-monitoring` |
| Notifications | ✓ | `notifications.ts` | Global component |
| Bulk import/export | ✓ | `bulk.ts` | (page assumed) |
| Audit logs | ✓ | `audit.ts` | (page assumed) |

### Partially Implemented

| Feature | Backend | API Client | Page |
|---------|---------|-----------|------|
| Deputation postings | ✓ ViewSet | ✗ None | ✗ None |
| Program rotation templates | ✓ ViewSet | ✗ None | ✗ None |
| Milestone research requirements | ✓ View | ✗ None | ✗ None |

---

## 4. Mismatch Categories

| ID | Description | Severity | Status |
|----|-------------|----------|--------|
| MISMATCH-001 | `departments.ts` used wrong URL `/supervisor-resident-links/` | HIGH | ✅ FIXED |
| MISMATCH-002 | Duplicate hospital/dept coverage in two modules | LOW | Acceptable |
| MISMATCH-003a | Research page: raw `apiClient.get('/api/users/?role=supervisor')` | LOW | Needs fix |
| MISMATCH-003b | Research page: raw `apiClient.patch('/api/my/research/', formData)` | LOW | Needs fix |
| MISMATCH-004 | Contract says `/api/auth/me/` but frontend uses `/api/auth/profile/` | LOW | Needs contract fix |
| MISMATCH-005 | 4 endpoints implemented but missing from API_CONTRACT.md | MEDIUM | Needs contract update |
| MISMATCH-006 | Bulk specialised import endpoints — existence unverified | LOW | ✅ VERIFIED (all exist) |

**Re: MISMATCH-005 — Revised finding:**  
After re-reading `docs/contracts/API_CONTRACT.md`, the Phase 6 section already documents research, thesis, workshops, eligibility, and system settings. The **actually missing** entries are:
- `GET /api/residents/me/summary/`
- `GET /api/supervisors/me/summary/`
- `GET /api/supervisors/residents/{id}/progress/`
- `GET /api/audit/reports/`
- Complete rotation/leave workflow (partial in contract)

---

## 5. Missing Implementation Categories

| Category | Count | Action |
|----------|-------|--------|
| Pages reported missing but actually exist | 2 (thesis, workshops found) | Update docs |
| Backend-only features (no frontend at all) | 3 (postings, templates, milestone-research-req) | Defer (low priority) |
| API client functions with unconfirmed pages | 4 | Confirmed via file scan |

---

## 6. Priority Order for Remediation

1. **P1 — Contract completeness**: Add 4 missing endpoints to `API_CONTRACT.md`
2. **P2 — Frontend drift**: Wrap raw `apiClient` calls in research page into API module functions  
3. **P3 — Auth standardisation**: Update contract to state `/api/auth/profile/` is canonical
4. **P4 — Documentation corrections**: Update MISSING_IMPLEMENTATIONS.md to reflect found pages
5. **P5 — Deferred features**: Postings, templates, milestone research req — no pages needed now
6. **P6 — Run tests and produce compliance report**
