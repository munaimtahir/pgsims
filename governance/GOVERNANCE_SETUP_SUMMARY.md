# Governance Setup Summary

**Date:** 2026-03-07  
**Scope:** Full contract governance system establishment for PGSIMS

---

## 1. Governance System Established

The `governance/` directory has been created as the permanent architecture governance foundation.

### Files Created

| File | Purpose |
|------|---------|
| `governance/API_SOURCE_OF_TRUTH.md` | Declares docs/contracts/ as canonical source of truth |
| `governance/DEVELOPMENT_RULES.md` | Backend + frontend engineering rules |
| `governance/CONTRACT_CHANGE_POLICY.md` | Mandatory process for API changes |
| `governance/ROLE_PERMISSION_MODEL.md` | Complete RBAC table for all roles and endpoints |
| `governance/ERROR_HANDLING_CONTRACT.md` | Standard error shapes + frontend display logic |
| `governance/FRONTEND_INTEGRATION_RULES.md` | API layer architecture + known exceptions |
| `governance/BACKEND_API_RULES.md` | ViewSet/serializer/permission patterns |
| `governance/FEATURE_DEVELOPMENT_WORKFLOW.md` | 6-phase workflow for new features |
| `governance/GOVERNANCE_SETUP_SUMMARY.md` | This document |

---

## 2. Integration Documentation Created

The `docs/integration/` directory now contains a complete integration picture.

### Files Created

| File | Purpose |
|------|---------|
| `docs/integration/API_ENDPOINT_CATALOG.md` | All 120 backend endpoints with roles and source |
| `docs/integration/FEATURE_API_MAP.md` | Every frontend feature mapped to its API functions |
| `docs/integration/PAGE_ENDPOINT_MATRIX.md` | Every page × action × endpoint × role |
| `docs/integration/ROLE_ROUTE_MATRIX.md` | Which roles access which routes and actions |
| `docs/integration/FRONTEND_DATA_SHAPES.md` | All TypeScript interfaces for API data |
| `docs/integration/BACKEND_FRONTEND_TRUTHMAP.md` | Authoritative feature-level integration map |
| `docs/integration/MISMATCH_REPORT.md` | All discovered mismatches and their status |
| `docs/integration/MISSING_IMPLEMENTATIONS.md` | Features missing backend, frontend, or pages |

### Agent-Generated Reference Files (in `docs/integration/`)
- `API_CATALOG.md` — Detailed backend endpoint catalog from agent scan
- `BACKEND_STRUCTURE.md` — Backend directory structure and architecture
- `FRONTEND_API_MAP.md` — Frontend API call inventory from agent scan
- `FRONTEND_INDEX.md`, `FRONTEND_SUMMARY.txt` — Frontend architecture overview

---

## 3. Total Endpoints Discovered

| Category | Count |
|----------|-------|
| Auth endpoints | 10 |
| Org graph (hospitals, departments, links) | 28 |
| User management | 5 |
| Training programs + milestones | 10 |
| Resident training records | 4 |
| Rotations (CRUD + workflow) | 13 |
| Leaves (CRUD + workflow) | 8 |
| Deputation postings | 5 |
| Research / Thesis / Workshop / Eligibility | 15 |
| Summary + settings | 4 |
| Notifications | 5 |
| Audit | 5 |
| Bulk operations | 8 |
| **Total active endpoints** | **120** |

---

## 4. Total Frontend Integrations Discovered

| Module | API Functions | Endpoints Covered |
|--------|--------------|------------------|
| `auth.ts` | 9 | 9 |
| `userbase.ts` | 17 | 15 |
| `hospitals.ts` | 4 | 4 (overlap with userbase) |
| `departments.ts` | 8 | 8 (partial overlap) |
| `users.ts` | 1 | 1 |
| `training.ts` | 28 | 28 |
| `notifications.ts` | 6 | 5 |
| `audit.ts` | 3 | 3 |
| `bulk.ts` | 8 | 8 |
| **Total** | **84** | **~81 unique** |

---

## 5. Mismatches Found and Fixed

| ID | Description | Severity | Status |
|----|-------------|----------|--------|
| MISMATCH-001 | `departments.ts` called `/api/supervisor-resident-links/` (wrong URL, should be `/api/supervision-links/`) | HIGH | ✅ FIXED |
| MISMATCH-002 | Duplicate hospital/dept coverage in two modules | LOW | Documented (acceptable) |
| MISMATCH-003 | Two direct `apiClient` calls in research page | LOW | Documented (acceptable exceptions) |
| MISMATCH-004 | `/api/auth/me/` vs `/api/auth/profile/` duplication | LOW | Open — needs standardisation |
| MISMATCH-005 | 12 Phase 6 endpoints not in API_CONTRACT.md | MEDIUM | Open — contract update needed |
| MISMATCH-006 | Bulk import specialised endpoints need backend verification | LOW | Open — needs verification |

---

## 6. Missing Items Documented

| Item | Location |
|------|---------|
| 6 backend endpoints with no frontend page | `MISSING_IMPLEMENTATIONS.md` §1 |
| 4 API client functions with uncertain page usage | `MISSING_IMPLEMENTATIONS.md` §2 |
| 3 partially implemented features (postings, program templates, milestone research req) | `MISSING_IMPLEMENTATIONS.md` §3 |
| 12 implemented endpoints not yet in API_CONTRACT.md | `MISSING_IMPLEMENTATIONS.md` §4 |
| 4 legacy apps intentionally excluded | `MISSING_IMPLEMENTATIONS.md` §5 |

---

## 7. Contract Governance Principles Established

1. **Contract-First** — `docs/contracts/` is the single source of truth
2. **No Undocumented Endpoints** — every backend endpoint must have a contract entry
3. **No Raw API Calls** — all frontend calls must go through `lib/api/*.ts`
4. **RBAC is Explicit** — every endpoint declares permission class matching RBAC matrix
5. **Canonical Entities** — one Department model, one Hospital model, forever
6. **Audit Trail** — `django-simple-history` must never be removed
7. **Notification Schema** — only `NotificationService` with canonical fields

---

## 8. Test Coverage

The role-based test suite confirms integration correctness:
- **103/103 tests passing** (`sims/tests/test_role_workflows.py`)
- Covers all 5 system roles × major API workflows
- Verifies RBAC boundaries, workflow state machines, field names
- Full audit report at `OUT/TEST_AUDIT_2026-03-07.md`

---

## Contract Governance Status

```
╔══════════════════════════════════════════════════════╗
║  CONTRACT GOVERNANCE STATUS: PARTIALLY COMPLIANT     ║
╠══════════════════════════════════════════════════════╣
║  ✅ Governance structure created                     ║
║  ✅ Development rules defined                        ║
║  ✅ API declared as source of truth                  ║
║  ✅ All endpoints catalogued (120 endpoints)         ║
║  ✅ Frontend calls mapped (84 functions)             ║
║  ✅ Truth map created                                ║
║  ✅ Critical mismatch fixed (MISMATCH-001)           ║
║  ✅ Missing items documented                         ║
║  ⚠️  12 Phase 6 endpoints not in API_CONTRACT.md    ║
║  ⚠️  3 missing frontend pages (thesis, workshops)   ║
║  ⚠️  Bulk endpoint URLs need backend verification   ║
╚══════════════════════════════════════════════════════╝

VERDICT: PARTIALLY COMPLIANT
Reason: Core governance is in place and integration is mapped.
The partial compliance is due to contract documentation gaps for
Phase 6 features (fully implemented but not yet in API_CONTRACT.md).
No breaking issues remain — MISMATCH-001 has been fixed.
```

---

## Next Steps (Recommended)

1. **Update `docs/contracts/API_CONTRACT.md`** to add all Phase 6 endpoints (research, thesis, workshops, eligibility, summaries)
2. **Verify bulk import endpoint names** match backend implementation  
3. **Create missing pages** for thesis and workshop management  
4. **Standardise** on `/api/auth/profile/` and deprecate `/api/auth/me/`  
5. **Extend `trainingApi`** to support FormData file uploads (eliminate the raw `apiClient` call in research page)
