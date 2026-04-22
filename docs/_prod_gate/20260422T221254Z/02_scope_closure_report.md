# Scope Closure Report

**Timestamp (UTC):** 20260422T221254Z

## Executive Summary

11 blockers remain from the latest NO-GO gate. This report organizes the closure work into 4 high-priority fix areas with exact file locations, change specifications, and test coverage requirements.

## Fix Priority and Impact Analysis

### Tier 1: Unblock Schema + E2E Runtime (Must Fix First)
- **Blocker #1: Strict schema gate failing** → PHASE 3
- **Blocker #2-4: E2E rendering/save failures** → PHASE 2A-C

These 4 blockers are prerequisites for all coverage and threshold work. Without them passing, higher coverage numbers are meaningless.

### Tier 2: Systematic Coverage Expansion (In Parallel with Tier 1)
- **Blockers #5-9: Route/API/CTA/Transition/Unauthorized coverage gaps** → PHASE 4
- **Blockers #10-11: Backend/Frontend code coverage below thresholds** → PHASES 5-6

## Structured Fix Plan

### PHASE 2A: Fix Resident Dashboard E2E (Status: PENDING)

**Failure Symptom:**
- E2E test `auth-and-smoke.spec.ts:18-24` fails on resident_user login
- Assertion: `page.getByRole('heading', { name: /My Training Dashboard/i })` not found
- Page shows error: "Failed to load dashboard. Please refresh."

**Root Cause (Hypothesis):**
Dashboard component calls `trainingApi.getResidentSummary()` which may:
1. Fail due to auth token not in request
2. Fail due to SSR hydration mismatch
3. Fail due to API response shape mismatch
4. Fail due to error in backend endpoint with specific E2E seed data

**Fixes Required:**

*Frontend: `frontend/app/dashboard/resident/page.tsx`*
- Add error logging before setError to console.error() actual error from API
- Add try/catch inside useEffect to catch promise rejections separately
- Add test: render with mocked API success, verify heading appears
- Add test: render with mocked API failure, verify error message appears

*Frontend: `frontend/lib/api/training.ts`*
- Add debug logging to getResidentSummary() for request/response
- Verify token is being sent in request headers

*Backend: `backend/sims/training/views.py::ResidentSummaryView`*
- Add test: verify endpoint returns 200 with valid structure for seed resident_user
- Add test: verify correct role filter (resident_user has role='pg')
- Add assertion tests for exact response shape

*E2E: `frontend/e2e/feature-layer/auth-and-smoke.spec.ts`*
- After login, wait for /api/residents/me/summary/ network request (not just heading)
- Capture network errors and log them in test report
- Add retry logic if dashboard is slow-loading

**Success Criteria:**
- E2E test passes consistently
- Frontend test mocking API success/failure passes
- Backend test confirms endpoint works with seed data
- No 5xx errors in backend logs

---

### PHASE 2B: Fix Logbook Draft Save E2E (Status: PENDING)

**Failure Symptom:**
- E2E test `logbook.spec.ts` clicks "Save Logbook Draft" button but assertion for saved confirmation not found
- Expected: `page.getByText(/Logbook draft saved/i)` to be visible

**Root Cause (Hypothesis):**
1. Endpoint `/api/logbook/{id}/save-draft/` doesn't exist or has wrong name
2. Request payload contract mismatch (frontend sends one shape, backend expects another)
3. Entry state machine prevents save (entry already approved/returned)
4. Frontend handler doesn't update UI on success or error

**Fixes Required:**

*Backend: `backend/sims/training/views.py::LogbookViewSet`*
- Verify `save_draft` action exists and is routed correctly
- Add schema annotation with `@extend_schema_field` for response
- Add test: POST /api/logbook/{id}/save-draft/ returns 200 with updated entry
- Add test: Invalid state (approved entry) returns 400 with error message

*Frontend: `frontend/components/logbook/` (exact component TBD)*
- Find save handler and add console.error on API failure
- Verify success response is handled and UI updated
- Add test: click save, mock success response, verify confirmation message

*E2E: `frontend/e2e/feature-layer/logbook.spec.ts`*
- Wait for /api/logbook/*/save-draft/ network response (not just UI)
- Log network response body on failure
- Capture page errors

**Success Criteria:**
- E2E test passes consistently
- Save endpoint test passes
- Frontend component test passes

---

### PHASE 2C: Fix Restart/Reseed Critical Smoke (Status: PENDING)

**Failure Symptom:**
- `docker compose down -v && ./scripts/e2e_up.sh && ./scripts/e2e_seed.sh` doesn't complete within timeout
- Services take >60s to become healthy
- Seed race: seed runs before Django fully ready

**Fixes Required:**

*`scripts/e2e_seed.sh`*
- Current: waits 60*2s = 120s with 2s sleep
- Change: add explicit health check endpoint polling instead of just `manage.py check`
- Poll `/api/schema/` until 200 response before running seed
- Add verbose output per seed step

*`docker/docker-compose.yml`*
- Verify health check timeout for all services is adequate
- Increase `interval` and `timeout` if services are borderline healthy

*Add test command:*
```bash
make smoke-test  # Should complete in <120s
```

**Success Criteria:**
- Restart/reseed completes in <120s with no errors
- All services healthy before seed runs

---

### PHASE 3: Fix Strict Schema Gate (Status: IN_PROGRESS)

See `01_schema_failure_analysis.md` for detailed breakdown.

**Priority 1 Fixes (Do These First):**

1. **Remove Duplicate Department Serializer**
   - Delete `sims/users/userbase_serializers.py::DepartmentSerializer` (lines ~43-50)
   - Update `sims/users/userbase_views.py::DepartmentViewSet` to import from `sims.academics.serializers`
   - Test: `pytest sims/users/test_userbase_api.py -xvs`

2. **Add @extend_schema to Critical Active Views**
   
   File: `backend/sims/training/views.py`
   - Line ~2656: `class ResidentOperationalDashboardView(APIView)`
     ```python
     @extend_schema(
         responses=ResidentOperationalDashboardSerializer,
         description="Resident command-center dashboard"
     )
     def get(self, request):
     ```
   - Line ~2780: `class SupervisorOperationalDashboardView(APIView)`
   - Line ~2860: `class HODOperationalDashboardView(APIView)`
   - Line ~2925: `class UTRMCOperationalDashboardView(APIView)`
   
   File: `backend/sims/users/userbase_views.py`
   - Line ~509: `class AuthMeView(APIView)`
   - Line ~521: `class DataQualitySummaryView(APIView)`
   - Line ~549: `class DataQualityUsersView(APIView)`
   - Line ~592: `class DataQualityRecomputeView(APIView)`
   - Line ~604: `class DataCorrectionAuditView(APIView)`

3. **Add @extend_schema_field to SerializerMethodFields**
   
   File: `backend/sims/training/serializers.py`
   - All 7 method fields need decorator (see 01_schema_failure_analysis.md)
   - Example:
     ```python
     @extend_schema_field(serializers.CharField())
     def get_resident_name(self, obj):
         return str(obj.resident_training.resident_user.full_name) if obj.resident_training else ''
     ```

4. **Fix Queryset Inspection Failures**
   
   File: `backend/sims/training/views.py::ProgramMilestoneViewSet`
   - Add `swagger_fake_view` check:
     ```python
     def get_queryset(self):
         if getattr(self, "swagger_fake_view", False):
             return self.queryset.none()
         return self.queryset.filter(program_id=self.kwargs['program_id'])
     ```

5. **Fix NotificationListView**
   
   File: `backend/sims/notifications/views.py`
   - Add `swagger_fake_view` check in get_queryset()

**Verification Command:**
```bash
cd backend && SECRET_KEY=test-secret python3 manage.py spectacular --file /tmp/schema_test.yaml 2>&1 | grep -i "error\|warning" | head -20
# Should show 0 errors and ≤5 acceptable warnings
```

---

### PHASE 4: Close Coverage Gaps (Routes/APIs/CTAs/Transitions/Unauthorized)

See `00_failure_to_fix_map.md` for complete lists.

**Work Items:**

1. **Active Routes (10 missing)** - Add Playwright tests
2. **Active APIs (10 missing)** - Add backend API tests  
3. **Visible CTAs (9 missing)** - Add Playwright/backend tests for mutations
4. **Invalid Transitions (6 missing)** - Add backend state machine tests
5. **Unauthorized Access (6 missing)** - Add role denial tests

**Strategy:** For each category, create a single test class that exercises all items:
- `backend/sims/test_active_scope_coverage.py` (new file)
- `frontend/e2e/feature-layer/active-scope-coverage.spec.ts` (or expand existing)

---

### PHASE 5: Raise Backend Coverage to >=95% / >=90%

**Affected Modules (from closure_map.md):**
- `sims/training/views.py` - 57.80% → target 95%
- `sims/common_permissions.py` - 26.48% → target 95%
- `sims/bulk/views.py` - 51.44% → target 95%
- Plus 6 others

**Strategy:**
- Create `backend/sims/test_coverage_expansion.py` with focused tests for:
  - Permission class allow/deny cases
  - State machine transitions (valid + invalid)
  - Viewset action branches
  - Serializer validation
  - Edge cases (empty data, missing fields, etc.)

**Command:**
```bash
cd backend && SECRET_KEY=test-secret pytest sims --cov=sims --cov-report=term-missing -v --tb=short 2>&1 | tail -50
```

---

### PHASE 6: Raise Frontend Coverage to >=90% / >=85%

**Affected Files (from closure_map.md):**
- All UTRMC dashboard pages (0% → 90%)
- All supervisor/resident dashboard pages (0% → 90%)
- API client wrappers (0-low% → 90%)
- Components (Sidebar, ImportExportPanel, etc.)

**Strategy:**
- Create Jest component tests for each dashboard page
- Test with mocked API responses (success/error/loading)
- Exercise visible CTAs and branches
- Test hooks and utilities independently

**Commands:**
```bash
cd frontend && npm test -- --watch=false --coverage 2>&1 | tail -30
```

---

### PHASE 7: Stabilize Harness Reproducibility

**Deliverable:** `03_harness_reproducibility.md`

Documents:
- Exact command sequence for full gate rerun
- Environment setup (Docker, env files, etc.)
- Health check timeouts and polling strategy
- Seed data consistency guarantees
- Coverage collection methodology
- Artifact generation and paths

---

### PHASE 8: Full Gate Rerun from Clean Baseline

**16-step sequence:**
1. dependency sanity (pip/npm)
2. migration check (`migrate --check`)
3. django/system check
4. backend tests + coverage
5. frontend lint
6. frontend typecheck
7. frontend unit tests + coverage
8. frontend build
9. strict schema gate
10. docker runtime bring-up
11. seed baseline
12. full active-surface E2E
13. role/CTA/API/negative/transition test suite
14. restart backend/frontend
15. rerun critical smoke
16. regenerate all artifacts

---

### PHASE 9: Produce Complete Evidence Pack

**Deliverables:**
- `00_failure_to_fix_map.md` (done: 20260422T221254Z)
- `01_schema_failure_analysis.md` (done: 20260422T221254Z)
- `02_scope_closure_report.md` (this file)
- `03_harness_reproducibility.md` (pending)
- `04_backend_coverage_report.md` (pending)
- `05_frontend_coverage_report.md` (pending)
- `06_role_route_action_matrix.md` (pending)
- `07_endpoint_coverage_report.md` (pending)
- `08_cta_coverage_report.md` (pending)
- `09_transition_coverage_report.md` (pending)
- `10_fixes_applied.md` (pending)
- `11_remaining_gaps.md` (pending)
- `12_final_verdict.md` (pending)

Plus regenerate OUT artifacts with new timestamp.

---

## Next Immediate Actions

1. Start PHASE 2A-C: Fix E2E runtime failures (highest impact)
2. Start PHASE 3 Priority 1: Remove duplicate Department serializer + add @extend_schema
3. Continue PHASE 4: Add systematic coverage tests
4. Execute PHASE 8: Full rerun
5. Produce evidence pack

## Timeline Estimate (tokens/effort)

- PHASE 2A-C: 2-3k tokens (diagnostics + fixes)
- PHASE 3: 3-4k tokens (schema annotations)
- PHASE 4: 5-7k tokens (test expansion)
- PHASE 5-6: 10-15k tokens (coverage expansion)
- PHASE 7-9: 3-5k tokens (documentation + final rerun)

**Total: ~25-35k tokens for complete closure**
