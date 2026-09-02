# Failure-to-Fix Map
**Timestamp (UTC):** 20260422T221254Z

This map lists the exact 11 remaining blockers from the latest NO-GO gate, maps each to root causes and files, and defines the fix strategy.

## Blocker 1: Strict Schema Gate Failing (49 warnings + 315 errors)

**Status:** FAIL  
**Command:** `SECRET_KEY=test-secret python3 manage.py spectacular --file ../OUT/prod_gate_artifacts/20260422T211654Z/schema/openapi.yaml --validate --fail-on-warn`

**Exact Failure:**
- Endpoint wired at `/api/schema/` and smoke test passes
- But `--fail-on-warn` reveals 49 warnings and 315 schema generation errors
- Prevents strict OpenAPI validation gate from passing

**Root Causes (from prior analysis):**
1. Unannotated APIViews lacking `@extend_schema` decorators
2. Serializer method fields without schema hints (e.g., `SerializerMethodField`)
3. Duplicate schema component names (e.g., multiple `Department` definitions)
4. OperationId collisions between endpoints
5. Missing field type annotations in serializers

**Affected Files (priority order):**
- `backend/sims/training/serializers.py` (active logbook/leave/program serializers)
- `backend/sims/training/views.py` (active dashboards, eligibility, supervisor views)
- `backend/sims/users/userbase_views.py` (active UTRMC org graph)
- `backend/sims/users/userbase_serializers.py` (active UTRMC users)
- `backend/sims/common_permissions.py` (permission helper classes)
- `backend/sims/bulk/views.py` (active bulk import/export)

**Fix Strategy:**
1. Run schema generation with verbose output to classify each warning/error
2. For each active APIView lacking `@extend_schema`, add schema decorator with proper operationId, summary, description
3. For each `SerializerMethodField`, add `help_text` and OpenAPI schema hint via `_expand_field_serializer`
4. Deduplicate component names by ensuring serializers have unique names or renaming colliding models
5. Verify no --fail-on-warn errors remain for active scope; deferred/internal APIs may be silenced if not mounted

**Expected Outcome:**
- `spectacular --fail-on-warn` passes with 0 errors and ≤5 acceptable warnings
- OpenAPI schema clean and usable for client generation

---

## Blocker 2: Resident Dashboard E2E Rendering Fails

**Status:** FAIL  
**Test:** `frontend/e2e/feature-layer/auth-and-smoke.spec.ts:13-27`  
**Failure:** Page heading `/My Training Dashboard/i` not found; page shows "Failed to load dashboard. Please refresh."

**Exact Test Code:**
```typescript
await expect(page.getByRole('heading', { name: /My Training Dashboard/i })).toBeVisible();
```

**Root Cause Analysis (hypotheses to test):**
1. **Data contract mismatch:** Backend `/api/residents/me/summary/` response payload changed; frontend expects different shape
2. **Same-origin fetch path mismatch:** Frontend proxy `/api/residents/me/summary/` not routing correctly to backend `http://backend:8014/api/residents/me/summary/`
3. **SSR/hydration mismatch:** Page renders on server but hydration fails on client
4. **Role-specific empty state:** Seed user has role that returns 200 but empty/null summary data, triggering error boundary
5. **Selector drift:** Button/heading text changed in recent commits
6. **Auth token not sent:** E2E auth cookie/JWT not valid for the seed user

**Affected Files:**
- **Frontend:** `frontend/app/dashboard/resident/page.tsx` (render logic)
- **Frontend:** `frontend/lib/api/training.ts` (API wrapper for `/api/residents/me/summary/`)
- **Frontend:** `frontend/app/dashboard/layout.tsx` or client-side fetcher (auth/interceptor)
- **Backend:** `backend/sims/training/views.py::ResidentsummaryView` (if this class exists)
- **Backend:** `backend/sims_project/urls.py` (routing)

**Fix Strategy:**
1. **Inspect Playwright trace/network:** Look at exact network request to `/api/residents/me/summary/` and response
2. **Verify API response shape:** Check what backend returns; add backend test for expected payload
3. **Check frontend SSR:** Verify Next.js uses correct fetch credentials and headers for authenticated request
4. **Verify seed user:** Ensure seed user has correct role and training records so summary is not empty
5. **Add frontend test:** Render dashboard page with mocked API response; verify error handling
6. **Add backend test:** Test ResidentsummaryView with correct role and records

**Expected Outcome:**
- E2E logs in as resident, navigates to `/dashboard/resident`, sees "My Training Dashboard" heading
- Frontend test renders dashboard with mocked data
- Backend test returns valid summary payload

---

## Blocker 3: Logbook Draft Save E2E Workflow Fails

**Status:** FAIL  
**Test:** `frontend/e2e/feature-layer/logbook.spec.ts:*` (exact line TBD)  
**Failure:** Click "Save Logbook Draft" button does not produce "Logbook draft saved" confirmation

**Root Cause Analysis (hypotheses to test):**
1. **Endpoint mismatch:** Frontend calls `/api/logbook/{id}/save-draft/` but backend doesn't define this action
2. **Payload contract broken:** Frontend sends `{content: "..."}` but backend expects `{entry_data: {...}}`
3. **State machine bug:** Logbook entry in state where save is not allowed (e.g., already `approved`)
4. **Autosave timing:** Frontend autosave fires before user-click save, leaving entry in wrong state
5. **Selector flake:** "Save Logbook Draft" button text changed or selector no longer matches
6. **Missing seed prerequisites:** E2E seed doesn't create a logbook entry in `draft` state
7. **Optimistic UI mismatch:** Frontend updates UI before API responds, then API fails silently

**Affected Files:**
- **Frontend:** `frontend/app/dashboard/resident/progress/page.tsx` (page structure)
- **Frontend:** `frontend/components/logbook/LogbookForm.tsx` or `DraftSection.tsx` (form and save handler)
- **Frontend:** `frontend/lib/api/training.ts` (API wrapper for logbook save)
- **Backend:** `backend/sims/training/views.py::LogbookViewSet` (save-draft action)
- **Backend:** `backend/sims/training/serializers.py::LogbookEntrySerializer`
- **Backend:** `backend/sims_project/urls.py` (routing for logbook viewset)

**Fix Strategy:**
1. **Inspect test flow:** Verify seed creates logbook entry; check that it's in `draft` state
2. **Check Playwright trace:** Log network request to save endpoint and exact error response
3. **Verify API endpoint exists:** Check backend viewset has `save_draft` action with correct HTTP method
4. **Verify response shape:** Backend returns confirmation; frontend assertion checks for correct field
5. **Check form state:** Before save, verify entry not in `approved`/`returned` (non-draft state)
6. **Add backend integration test:** POST to logbook save endpoint; verify entry saved and status unchanged
7. **Add frontend test:** Render form, fill, click save, verify callback fired with success

**Expected Outcome:**
- E2E creates logbook entry, fills form, clicks save, sees "Logbook draft saved" message
- Backend integration test verifies save action works
- Frontend test verifies UI update fires

---

## Blocker 4: Restart/Reseed Critical Smoke Failing

**Status:** FAIL  
**Commands:**
```bash
docker compose --env-file .env -f docker/docker-compose.yml down -v
./scripts/e2e_up.sh
./scripts/e2e_seed.sh
```

**Root Cause Analysis:**
1. **Container health checks slow:** Services take >60s to become healthy, timing out smoke
2. **Seed race condition:** Seed script runs before Django/migrations fully settled
3. **Database state dirty:** Prior test data conflicts with new seed
4. **Migration failure:** A migration fails silently and seed uses stale schema

**Affected Files:**
- `scripts/e2e_up.sh` (start services)
- `scripts/e2e_seed.sh` (seed data)
- `docker/docker-compose.yml` (health checks, timeouts)
- `backend/sims_project/settings.py` (database config)

**Fix Strategy:**
1. **Increase health check timeout:** If services are healthy but slow, allow more time
2. **Add explicit wait loop:** Before seed, poll Django `/api/schema/` endpoint until 200 response
3. **Verify migrations:** Add `python manage.py migrate --check` before seed
4. **Clear seed state:** Ensure seed idempotently handles duplicate records (or delete before insert)
5. **Document smoke command:** Create stable, documented smoke sequence

**Expected Outcome:**
- Start docker stack, wait for health, run seed, verify no errors
- Smoke consistently succeeds in <120s

---

## Blocker 5: Active Routes Coverage Only 76% (need 100%)

**Status:** FAIL  
**Missing Routes (from closure_map.md):**
1. `/dashboard/supervisor/residents/[id]/progress` - Supervisor resident progress
2. `/dashboard/utrmc/departments/[id]/roster` - UTRMC department roster
3. `/dashboard/utrmc/data-quality` - UTRMC data quality
4. `/dashboard/utrmc/programs` - UTRMC programs
5. `/dashboard/utrmc/supervision` - UTRMC supervision links
6. `/dashboard/utrmc/matrix` - UTRMC hospital-department matrix
7. `/dashboard/utrmc/users` - UTRMC users
8. `/dashboard/utrmc/hospitals` - UTRMC hospitals
9. `/dashboard/utrmc/departments` - UTRMC departments
10. `/dashboard/utrmc/eligibility-monitoring` - UTRMC eligibility

**Fix Strategy:**
- Add Playwright test for each route: render page and verify key UI elements present
- Add backend test for each route's primary API endpoint (shape, role denial)

**Expected Outcome:**
- All 10 routes have passing E2E tests
- Active routes coverage = 100%

---

## Blocker 6: Active APIs Coverage Only 80% (need 100%)

**Status:** FAIL  
**Missing API Tests (from closure_map.md):**
1. `GET /api/departments/{id}/roster/` - Response shape and role denial
2. `GET /api/hospitals/{id}/departments/` - Response shape and role denial
3. `POST/PATCH /api/hod-assignments/` - Create/update and read-only denial
4. `POST/PATCH /api/supervision-links/` - Create/update and read-only denial
5. `PATCH /api/hospital-departments/` - Matrix update and read-only denial
6. `POST/PATCH /api/programs/`, `/api/program-templates/`, etc. - Mutation and denial
7. `POST/PATCH /api/admin/data-quality/` - Recompute/patch and denial
8. `GET /api/supervisors/residents/{id}/progress/` - Allowed for assigned supervisor, denied for unrelated
9. `GET /api/users/` - UTRMC scope matrix for user retrieval

**Fix Strategy:**
- Add backend API test for each endpoint: happy path + role denial cases

**Expected Outcome:**
- All APIs have passing backend tests
- Active API coverage = 100%

---

## Blocker 7: Visible CTAs Coverage Only 51% (need 100%)

**Status:** FAIL  
**Missing CTA Tests (from closure_map.md):**
1. UTRMC overview: bulk import/export, data-quality CTA
2. UTRMC hospitals: Add Hospital CTA, validation, mutation, read-only denial
3. UTRMC departments: Add Department CTA, validation, mutation, read-only denial
4. UTRMC matrix: toggle matrix cell, read-only denial
5. UTRMC users: Add User CTA, validation, mutation, read-only denial
6. UTRMC supervision: add/edit link CTA, mutation, read-only denial
7. UTRMC HOD: assign HOD CTA, mutation, read-only denial
8. UTRMC programs: template/policy/milestone CTAs, mutation, read-only denial
9. UTRMC data quality: recompute/patch CTAs, denial for non-admin
10. Supervisor resident progress: Back/detail links navigation

**Fix Strategy:**
- Add Playwright test for each CTA: click, verify mutation (or deny for read-only role)
- Add backend test for each mutation endpoint

**Expected Outcome:**
- All visible CTAs have passing E2E tests (or explicit proof they are deferred/non-actionable)
- CTA coverage = 100%

---

## Blocker 8: Invalid Transitions Coverage Only 75% (need 100% critical)

**Status:** FAIL  
**Missing Transition Tests:**
1. Leave: approve/reject non-submitted leave (should fail)
2. Leave: resident creating leave for another's training record (should fail)
3. Logbook: submit approved/returned entry (should fail)
4. Logbook: supervisor review draft entry (should fail)
5. Logbook: unrelated supervisor review (should fail)
6. UTRMC admin: read-only user mutations to any write endpoint (should fail)

**Fix Strategy:**
- Add backend API test for each invalid transition: call with invalid state, verify error response

**Expected Outcome:**
- All invalid transitions have passing tests that verify denial
- Transition coverage = 100% critical

---

## Blocker 9: Unauthorized Access Coverage Only 90% (need 100%)

**Status:** FAIL  
**Missing Authorization Tests:**
1. UTRMC roster/org endpoints: resident/supervisor direct API denial
2. UTRMC admin mutations: UTRMC read-only user direct API denial
3. Supervisor progress: resident and unrelated supervisor denial
4. Data-quality endpoints: non-admin denial
5. Supervisor resident list: non-supervisor denial
6. Userbase object-level scope: supervisor/UTRMC user retrieval outside allowed scope

**Fix Strategy:**
- Add backend API test for each endpoint: call with wrong role, verify 403/403 or permission error

**Expected Outcome:**
- All unauthorized access denied correctly
- Unauthorized coverage = 100% active scope

---

## Blocker 10: Backend Coverage 54.38% Line / 28.69% Branch (need ≥95% / ≥90%)

**Status:** FAIL  
**Priority Modules (from closure_map.md):**
1. `sims/training/views.py` - 57.80% line / 41.53% branch (active dashboards, leave, logbook, eligibility)
2. `sims/training/serializers.py` - 90.54% line / low branches (active serializers)
3. `sims/users/userbase_views.py` - 68.63% line / 51.19% branch (active UTRMC org)
4. `sims/users/userbase_serializers.py` - 72.58% line / 14.29% branch (active UTRMC users)
5. `sims/common_permissions.py` - 26.48% line / 4.84% branch (permission gates)
6. `sims/bulk/views.py` - 51.44% line / 37.50% branch (active bulk import)
7. `sims/bulk/userbase_engine.py` - 56.11% line / 39.66% branch (active userbase import)
8. `sims/users/models.py` - 69.77% line / 30.77% branch (user/role/org models)
9. `sims/training/eligibility.py` - 62.50% line / 53.85% branch (eligibility logic)
10. `sims/users/data_quality.py` - 83.33% line / partial branches (data quality)

**Fix Strategy:**
- Add permission/RBAC tests: each permission class tested with allow/deny cases
- Add workflow tests: each state transition tested with valid/invalid paths
- Add viewset action tests: each action (create/update/delete) tested with branches
- Add serializer validation: each complex serializer method field tested
- Add edge cases: role scoping, object-level access, audit trail

**Expected Outcome:**
- Backend line coverage ≥95%
- Backend branch coverage ≥90%

---

## Blocker 11: Frontend Coverage 8.71% Line / 7.56% Branch (need ≥90% / ≥85%)

**Status:** FAIL  
**Priority Files (from closure_map.md):**
1. `frontend/app/dashboard/utrmc/page.tsx` - 0% (render, CTA branches)
2. `frontend/app/dashboard/utrmc/data-quality/page.tsx` - 0% (loading/error/success/action)
3. `frontend/app/dashboard/utrmc/programs/page.tsx` - 0% (render, template/policy controls)
4. `frontend/app/dashboard/supervisor/page.tsx` - 0% (render queues, approve/reject/return)
5. `frontend/app/dashboard/resident/schedule/page.tsx` - 0% (leave form, validation, submit)
6. `frontend/app/dashboard/resident/progress/page.tsx` - 0% (logbook, draft/submit/error)
7. `frontend/app/dashboard/utrmc/{hospitals,departments,matrix,users,supervision,hod,eligibility-monitoring}/page.tsx` - 0%
8. `frontend/lib/api/{client,training,userbase,bulk,auth}.ts` - low/0% (API wrappers)
9. `frontend/components/layout/Sidebar.tsx` - 0% (role nav visibility)
10. `frontend/components/ui/ImportExportPanel.tsx` - 0% (dry-run/apply/error)

**Fix Strategy:**
- Add unit/component tests for each mounted page: render with mocked API, verify branches
- Add hook tests for API wrappers: success/error/loading branches
- Add integration tests for workflows: E2E-adjacent tests in Jest
- Prefer behavior tests over snapshots

**Expected Outcome:**
- Frontend line coverage ≥90%
- Frontend branch coverage ≥85%

---

## Summary of 11 Blockers and Closure Strategy

| # | Blocker | Current | Required | Fix Phase |
|---|---------|---------|----------|-----------|
| 1 | Strict schema gate | FAIL (315 errors) | PASS | Phase 3 |
| 2 | Resident dashboard E2E | FAIL | PASS | Phase 2A |
| 3 | Logbook draft save E2E | FAIL | PASS | Phase 2B |
| 4 | Restart/reseed smoke | FAIL | PASS | Phase 2C |
| 5 | Active routes coverage | 76% | 100% | Phase 4 |
| 6 | Active API coverage | 80% | 100% | Phase 4 |
| 7 | Visible CTA coverage | 51% | 100% | Phase 4 |
| 8 | Invalid transition coverage | 75% | 100% | Phase 4 |
| 9 | Unauthorized access coverage | 90% | 100% | Phase 4 |
| 10 | Backend code coverage | 54.38% / 28.69% | ≥95% / ≥90% | Phase 5 |
| 11 | Frontend code coverage | 8.71% / 7.56% | ≥90% / ≥85% | Phase 6 |

**Execution Order:**
1. Phase 1: Complete this map (DONE)
2. Phase 2A-C: Fix runtime E2E (blocks Phase 5-6)
3. Phase 3: Fix schema gate
4. Phase 4: Close coverage gaps (parallelize with Phase 5-6 if possible)
5. Phase 5: Raise backend coverage meaningfully
6. Phase 6: Raise frontend coverage meaningfully
7. Phase 7: Stabilize reproducibility
8. Phase 8: Full gate rerun
9. Phase 9: Regenerate evidence pack and issue verdict
