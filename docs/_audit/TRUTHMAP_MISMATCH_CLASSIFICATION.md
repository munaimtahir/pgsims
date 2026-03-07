# Truthmap Mismatch Classification

**Date:** 2026-03-07  
**Phase:** B — Classify Mismatches  
**Source:** `docs/integration/MISMATCH_REPORT.md` + direct code inspection

---

## Classification Key

| Class | Description |
|-------|-------------|
| 1 | Backend missing endpoint defined in contract |
| 2 | Backend response drift from contract |
| 3 | Backend request validation drift from contract |
| 4 | Frontend calling wrong endpoint |
| 5 | Frontend payload shape drift |
| 6 | Frontend expecting wrong response field |
| 7 | UI role visibility mismatch |
| 8 | Route guard mismatch |
| 9 | Missing client/service wrapper |
| 10 | Missing OpenAPI/contract definition for real endpoint |
| 11 | Error-handling inconsistency |
| 12 | Naming/status inconsistency |

---

## Classified Mismatches

### MISMATCH-001: Wrong supervision link URL  
**Class: 4 — Frontend calling wrong endpoint**  
**Status: ✅ FIXED**  

`departments.ts` called `/api/supervisor-resident-links/` (non-existent). Canonical URL is `/api/supervision-links/`. Fixed in commit `31854e7`.

---

### MISMATCH-002: Duplicate API module coverage  
**Class: 9 — Missing client/service wrapper (inverse: redundant wrapper)**  
**Status: ACCEPTED — No action needed**

`hospitals.ts` + `departments.ts` are legacy wrappers that predate `userbase.ts`. Both call the same endpoints. Governance docs declare `userbaseApi.*` as canonical for new development. Legacy modules remain for backward compatibility.

**Action:** None — already documented in `governance/FRONTEND_INTEGRATION_RULES.md`.

---

### MISMATCH-003a: Raw `apiClient.get` in research page (supervisor list)  
**Class: 9 — Missing client/service wrapper**  
**Status: NEEDS FIX**

**Location:** `frontend/app/dashboard/resident/research/page.tsx:54`  
```typescript
apiClient.get('/api/users/?role=supervisor')
```

**Resolution:** Add `getSupervisors()` function to `frontend/lib/api/users.ts` and update the research page to use it.

**Root cause:** No typed wrapper existed for filtered user listing at time of page development.

---

### MISMATCH-003b: Raw `apiClient.patch` in research page (file upload)  
**Class: 9 — Missing client/service wrapper**  
**Status: NEEDS FIX**

**Location:** `frontend/app/dashboard/resident/research/page.tsx:83`  
```typescript
apiClient.patch(`/api/my/research/`, fd, { headers: { 'Content-Type': 'multipart/form-data' } })
```

**Resolution:** Add `patchResearchFile(file: File)` to `trainingApi` in `frontend/lib/api/training.ts` and update the research page to use it.

**Root cause:** `trainingApi.patchResearch()` uses JSON, not FormData. A separate file-upload method is needed.

---

### MISMATCH-004: Contract says `/api/auth/me/`, frontend uses `/api/auth/profile/`  
**Class: 10 — Missing/incorrect contract definition + 12 — Naming inconsistency**  
**Status: NEEDS CONTRACT FIX**

**Detail:**  
- `docs/contracts/API_CONTRACT.md` documents: `GET /api/auth/me/` returns user payload
- Frontend `auth.ts` `getCurrentUser()` calls: `GET /api/auth/profile/`
- Both endpoints exist in backend:
  - `/api/auth/me/` → `AuthMeView` → uses `UserManagementSerializer` (richer: includes `home_department`, `home_hospital`, `supervisor`, `departments`)
  - `/api/auth/profile/` → `user_profile_view` → uses `UserSerializer` (simpler: no relationship fields)
- The two serializers return **different payloads**

**Resolution:**  
- Update `API_CONTRACT.md` to declare `/api/auth/profile/` as canonical for current-user read
- Document `/api/auth/me/` as returning the richer management payload (useful for admin user management)
- No code change required — current frontend usage of `/profile/` is correct

---

### MISMATCH-005: Implemented endpoints missing from contract  
**Class: 10 — Missing contract definition for real endpoint**  
**Status: PARTIALLY FIXED (Phase 6 was already in contract)**

**Re-analysis after reading API_CONTRACT.md in full:**

Already documented in contract (Phase 6 section):
- ✅ `/api/my/research/`, `/api/my/research/action/{action}/`
- ✅ `/api/my/thesis/`, `/api/my/thesis/submit/`
- ✅ `/api/my/workshops/`, `/api/my/eligibility/`, `/api/utrmc/eligibility/`
- ✅ `/api/system/settings/`

**Still missing from contract:**
- ✗ `GET /api/residents/me/summary/`
- ✗ `GET /api/supervisors/me/summary/`
- ✗ `GET /api/supervisors/residents/{id}/progress/`
- ✗ `GET/POST /api/audit/reports/`
- ✗ Rotation workflow actions (submit, hod-approve, utrmc-approve, activate, complete, returned, reject)
- ✗ Leave workflow actions (submit, approve, reject)
- ✗ Auth profile endpoints (register, logout, change-password, password-reset details)

**Resolution:** Add all missing entries to `docs/contracts/API_CONTRACT.md`.

---

### MISMATCH-006: Bulk specialised import endpoints  
**Class: 1 — (suspected), verified as false positive**  
**Status: ✅ RESOLVED — Not actually a mismatch**

All bulk import endpoints DO exist in `sims/bulk/urls.py`:
- `POST /api/bulk/import-trainees/` → `BulkTraineeImportView`
- `POST /api/bulk/import-supervisors/` → `BulkSupervisorImportView`
- `POST /api/bulk/import-residents/` → `BulkResidentImportView`
- `POST /api/bulk/import-departments/` → `BulkDepartmentImportView`

Frontend `bulk.ts` calls are all correct.

---

## Summary Table

| Mismatch | Class | Severity | Status | Action |
|----------|-------|----------|--------|--------|
| MISMATCH-001 | 4 | HIGH | ✅ FIXED | Done |
| MISMATCH-002 | 9 | LOW | ACCEPTED | None |
| MISMATCH-003a | 9 | LOW | NEEDS FIX | Add `getSupervisors()` wrapper |
| MISMATCH-003b | 9 | LOW | NEEDS FIX | Add `patchResearchFile()` to trainingApi |
| MISMATCH-004 | 10+12 | LOW | NEEDS CONTRACT FIX | Update API_CONTRACT.md |
| MISMATCH-005 | 10 | MEDIUM | PARTIAL | Add 4+ missing entries to API_CONTRACT.md |
| MISMATCH-006 | 1 (false) | LOW | ✅ RESOLVED | None |

**Total actionable:** 3 code fixes + 1 contract update  
**Pre-existing fixed:** 1  
**Accepted/deferred:** 2
