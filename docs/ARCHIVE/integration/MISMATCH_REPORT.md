# Mismatch Report

**Generated:** 2026-03-07  
**Method:** Cross-referencing frontend `lib/api/*.ts` calls vs backend URL definitions vs existing contract docs

---

## Summary

| Category | Count |
|----------|-------|
| URL mismatches (frontend calls wrong path) | 1 |
| Duplicate API coverage (two modules call same endpoint) | 3 |
| Missing frontend coverage for backend endpoints | 8 |
| Contract gaps (implemented but not in API_CONTRACT.md) | 12 |
| Frontend bypasses API layer (direct apiClient in page) | 2 |

---

## MISMATCH-001: `/api/supervisor-resident-links/` vs `/api/supervision-links/`

**Severity:** ⚠️ HIGH — Will cause 404 in production  
**Status:** ✅ FIXED — 2026-03-07

**Fix Applied:**  
Updated `frontend/lib/api/departments.ts` lines 9–11 to use `/api/supervision-links/`.

**Problem:**  
`frontend/lib/api/departments.ts` calls:
- `getSupervisorResidentLinks()` → `GET /api/supervisor-resident-links/`
- `createSupervisorResidentLink()` → `POST /api/supervisor-resident-links/`
- `deleteSupervisorResidentLink()` → `DELETE /api/supervisor-resident-links/{id}/`

**Actual backend URL:**  
`/api/supervision-links/` (registered in `sims/users/userbase_urls.py`)

**Resolution:**  
Update `frontend/lib/api/departments.ts` to use `/api/supervision-links/` instead of `/api/supervisor-resident-links/`.

**Files to change:**
- `frontend/lib/api/departments.ts` — fix 3 URL strings
- `docs/integration/FEATURE_API_MAP.md` — already documents this mismatch

---

## MISMATCH-002: Duplicate Hospital/Department API Coverage

**Severity:** ℹ️ LOW — Functional but inconsistent  
**Status:** OPEN (low priority)

**Problem:**  
Two frontend modules cover the same endpoints:

| Endpoint | Covered By |
|----------|-----------|
| `GET /api/hospitals/` | `hospitals.ts` AND `userbase.ts` |
| `POST /api/hospitals/` | `hospitals.ts` AND `userbase.ts` |
| `GET /api/departments/` | `departments.ts` AND `userbase.ts` |
| `POST /api/departments/` | `departments.ts` AND `userbase.ts` |

**Root cause:**  
`hospitals.ts` and `departments.ts` are simpler early-phase wrappers. `userbase.ts` is the richer typed replacement added later.

**Resolution:**  
Pages should prefer `userbaseApi.*` functions. The legacy `hospitals.ts` and `departments.ts` exports can remain for backward compatibility but should not be used for new page development.

**Action:** Document canonical preference in `governance/FRONTEND_INTEGRATION_RULES.md` (already done).

---

## MISMATCH-003: Direct `apiClient` Calls in Page Component

**Severity:** ℹ️ LOW — Acceptable exceptions, documented  
**Status:** ACCEPTED (with documentation)

**Occurrences:**

1. `frontend/app/dashboard/resident/research/page.tsx:54`  
   `apiClient.get('/api/users/?role=supervisor')`  
   **Reason:** No dedicated supervisor-listing endpoint exists. Inline call is acceptable until a filtered users endpoint is added to `userbase.ts`.

2. `frontend/app/dashboard/resident/research/page.tsx:83`  
   `apiClient.patch('/api/my/research/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })`  
   **Reason:** File upload requires FormData which is not supported by the `trainingApi.updateMyResearch()` wrapper. Acceptable until `trainingApi` adds FormData support.

**Resolution:** Both are tracked. `trainingApi` should be extended to support file uploads in a future iteration.

---

## MISMATCH-004: `/api/auth/profile/` vs `/api/auth/me/`

**Severity:** ℹ️ LOW — Both endpoints exist and return user data  
**Status:** OPEN (needs standardisation)

**Problem:**  
The backend defines two endpoints that return current user data:
- `GET /api/auth/me/` → `AuthMeView` (class-based)
- `GET /api/auth/profile/` → `user_profile_view` (function-based)

Frontend `auth.ts` (`getCurrentUser()`) calls `/api/auth/profile/`.

**Resolution:**  
These should return identical payloads. Pick one as canonical and deprecate the other. Recommended: keep `/api/auth/profile/` as canonical (frontend already uses it), and document `/api/auth/me/` as legacy.

---

## MISMATCH-005: Backend Endpoints Not in `docs/contracts/API_CONTRACT.md`

**Severity:** ℹ️ MEDIUM — Contract docs are incomplete  
**Status:** OPEN

The following implemented endpoints are NOT documented in the existing `docs/contracts/API_CONTRACT.md`:

| Endpoint | Backend Implemented | Contract Documented |
|----------|--------------------|--------------------|
| `GET /api/my/research/` | ✓ | ✗ |
| `POST /api/my/research/action/{action}/` | ✓ | ✗ |
| `GET /api/my/thesis/` | ✓ | ✗ |
| `POST /api/my/thesis/submit/` | ✓ | ✗ |
| `GET/POST /api/my/workshops/` | ✓ | ✗ |
| `GET /api/my/eligibility/` | ✓ | ✗ |
| `GET /api/utrmc/eligibility/` | ✓ | ✗ |
| `GET /api/residents/me/summary/` | ✓ | ✗ |
| `GET /api/supervisors/me/summary/` | ✓ | ✗ |
| `GET /api/supervisors/residents/{id}/progress/` | ✓ | ✗ |
| `GET /api/system/settings/` | ✓ | ✗ |
| `GET/POST /api/audit/reports/` | ✓ | ✗ |

**Resolution:**  
Update `docs/contracts/API_CONTRACT.md` to include all Phase 6 and Phase 6B/6C endpoints.

---

## MISMATCH-006: `bulk.ts` Non-Standard Import Endpoints

**Severity:** ℹ️ LOW — May not all exist in backend  
**Status:** NEEDS VERIFICATION

`frontend/lib/api/bulk.ts` calls multiple specialised import endpoints:
- `/api/bulk/import-trainees/`
- `/api/bulk/import-supervisors/`
- `/api/bulk/import-residents/`
- `/api/bulk/import-departments/`

These need to be verified against `sims/bulk/urls.py` — the backend may only implement a single generic `/api/bulk/import/` endpoint with an entity type parameter.

**Resolution:**  
Verify backend bulk URL configuration and align frontend calls accordingly.

---

## Fixed Mismatches (Historical)

These mismatches were identified and resolved in previous test iterations:

| Mismatch | Fixed In | Resolution |
|----------|----------|-----------|
| Notification mark-read field `ids` vs `notification_ids` | Test iteration 4 | Backend uses `notification_ids` — tests corrected |
| Rotation return URL `/return/` vs `/returned/` | Test iteration 3 | Django names it `returned` — tests corrected |
| `is_read` setter on Notification (no setter, uses `read_at`) | Test iteration 5 | Remove `is_read=` from ORM creates |
| Audit URL `/api/audit/` vs `/api/audit/activity/` | Test iteration 3 | Corrected URL in tests |
| HOD approve sets `STATUS_APPROVED` not `STATUS_HOD_APPROVED` | Test iteration 4 | Both approve actions → `STATUS_APPROVED` |
| `degree_type` casing (`md` vs `MD`) | Test iteration 2 | Choices are uppercase |
| Notification unread count field `count` vs `unread` | Test iteration 5 | Field is `unread` |
