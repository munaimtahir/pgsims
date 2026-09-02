# Blocker Analysis - PGSIMS Production Gate

**Last Updated**: 2026-04-23  
**Analysis Type**: Comprehensive blocker mapping  
**Scope**: All 11 blockers preventing GO verdict

---

## Overview

This document maps each of the 11 blockers to:
- Exact file locations and error messages
- Root cause analysis
- Severity and impact
- Fix strategy and effort estimate
- Dependencies on other blockers
- Validation criteria

**Total Blockers**: 11  
**Total Effort to Close**: 20-40 hours (realistic: 24-36 hours)

---

## Blocker #1: Schema Gate - APIView Serializer Errors

### Summary
65 APIViews lack `@extend_schema()` decorators or explicit serializer definitions, causing schema generation to report "unable to guess serializer" errors. This prevents production-ready OpenAPI schema generation.

### Severity
🔴 **HIGH** - Blocks GO threshold: "strict schema gate passes"

### Current State
- **Errors**: 315 total (65 unique "unable to guess serializer")
- **Warnings**: 31 total
- **Location**: Multiple files across `sims.training.views`, `sims.users.api_views`, `sims.notifications.views`, `sims.bulk.views`

### Affected Views (Examples)
```
/app/sims/training/views.py:734 - RotationApprovalInboxView
/app/sims/training/views.py:761 - LeaveApprovalInboxView  
/app/sims/training/views.py:780 - MyRotationsView
/app/sims/bulk/views.py:291 - BulkDepartmentImportView
/app/sims/notifications/views.py:26 - NotificationListView
[... 60 more views]
```

### Root Cause
APIViews (not ViewSets) don't provide serializer information through standard DRF mechanisms. `drf-spectacular` cannot auto-detect serializer for APIViews and requires explicit `@extend_schema()` annotation.

### Impact
- Cannot generate production-ready OpenAPI schema
- Cannot validate schema against spec
- API consumers cannot auto-generate SDK from schema

### Fix Strategy

#### Option A: Add @extend_schema() Decorators (Recommended)
```python
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

class MyView(APIView):
    @extend_schema(
        request=MySerializer,
        responses=MyResponseSerializer,
    )
    def post(self, request):
        # implementation
        pass
```

#### Option B: Convert to GenericAPIView
```python
from rest_framework.generics import GenericAPIView

class MyView(GenericAPIView):
    serializer_class = MySerializer
    def post(self, request):
        pass
```

### Steps to Fix

**Phase A: Identify All Views (30 min)**
```bash
cd backend
python manage.py spectacular --file /tmp/schema.yaml --validate --fail-on-warn 2>&1 | \
  grep "unable to guess serializer" | tee /tmp/apiviews_to_fix.txt
```

**Phase B: Categorize by Priority (30 min)**
1. Views used by active E2E tests (CRITICAL)
2. Views used by active API contracts (HIGH)
3. Views used by UTRMC admin (HIGH)
4. Other views (MEDIUM)

**Phase C: Add Decorators (2-3 hours)**
For each view:
1. Create appropriate request/response serializers if needed
2. Add `@extend_schema()` decorator
3. Document response codes and error cases

**Phase D: Validate (30 min)**
```bash
python manage.py spectacular --file /tmp/schema.yaml --validate --fail-on-warn
```

### Effort Estimate
- **Quick path** (critical views only): 1-2 hours
- **Full path** (all 65 views): 3-5 hours

### Dependencies
- None (can be fixed independently)

### Validation Criteria
```bash
# Command to validate
cd backend && python manage.py spectacular --file /tmp/schema.yaml --validate --fail-on-warn 2>&1 | \
  grep -c "unable to guess serializer"

# Expected result: 0 (or only non-active views)
```

### Related Files
- `backend/sims/training/views.py` (34 errors)
- `backend/sims/bulk/views.py` (1 error)
- `backend/sims/notifications/views.py` (5 errors)
- `backend/sims/users/api_views.py` (1 error)
- `backend/sims_project/schema.py` (schema settings)

---

## Blocker #2: E2E Dashboard Rendering Fails

### Summary
E2E tests attempting to load resident dashboard fail with "Failed to load dashboard. Please refresh." error. This is the CRITICAL blocker affecting 3 tests directly and blocking 5 dependent blockers.

### Severity
🔴 **CRITICAL** - Blocks GO thresholds:
- "active-surface E2E fully passes"
- "critical workflows tested = 100%"
- "active routes tested = 100%"  
- "active APIs tested = 100%"
- "visible CTAs tested = 100%"

### Current State
- **Status**: 4 of 7 E2E feature-layer tests PASS
- **Failures**: 3 tests fail on dashboard rendering
- **Message**: "Failed to load dashboard. Please refresh."
- **Pattern**: Affects both resident and supervisor dashboards

### Failing Tests
1. `e2e/feature-layer/auth-and-smoke.spec.ts:18` - Core feature roles dashboard
2. `e2e/feature-layer/auth-and-smoke.spec.ts:27` - Key routes rendering
3. `e2e/feature-layer/logbook.spec.ts:9` - Logbook workflow (depends on dashboard)

### Regression Smoke Failures
1. `e2e/feature-layer/regression-smoke.spec.ts:6` - Resident core pages
2. `e2e/feature-layer/regression-smoke.spec.ts:25` - HOD pages

### Investigation Results

**What Works**: ✓
- Backend `/api/residents/me/summary/` returns HTTP 200
- Backend `/api/dashboard/resident/` returns HTTP 200
- Frontend service is running and responsive
- Frontend can reach backend through proxy
- Auth setup completes without errors
- Test data is seeded correctly

**What Fails**: ✗
- E2E test's dashboard page rendering
- Error boundary in `frontend/app/dashboard/resident/page.tsx` catches error
- Error message has no details (caught at high level)

### Root Cause Candidates

**Candidate A: Token Not Injected (Probability: 40%)**
- E2E auth setup uses `addInitScript()` to inject token into localStorage
- May have timing issue where API calls execute before token is injected
- Previous session added 100ms delay, but may not be enough

**Candidate B: API Returns Unexpected Format (Probability: 20%)**
- API may return different data structure than expected
- Causes deserialization error in frontend
- Not caught by previous error handling

**Candidate C: ALLOWED_HOSTS Rejection (Probability: 15%)**
- Backend may reject requests with wrong Host header
- Proxy forwards requests but may have Host header mismatch
- Error would be 400 Bad Request

**Candidate D: Session State Issue (Probability: 15%)**
- Playwright's browser context may not persist auth across page navigation
- Session cleared between login and dashboard load
- Token exists but session is invalid

**Candidate E: Race Condition (Probability: 10%)**
- API response arrives before component unmounts
- Memory leak or state update on unmounted component
- Subtle timing issue only reproducible in E2E environment

### Fix Strategy

See `04_e2e_debugging.md` for complete debugging procedures.

#### Quick Diagnosis (15-20 min)
1. Enable detailed logging in E2E test
2. Log token value and localStorage contents
3. Capture network trace from Playwright
4. Check backend logs for auth errors

#### Likely Fix (2-4 hours depending on diagnosis)
1. If token timing: Extend wait, verify token before API calls
2. If API format: Update frontend type definitions
3. If ALLOWED_HOSTS: Add test domains to settings
4. If session: Refactor E2E auth to use browser login flow
5. If race condition: Add explicit wait conditions

### Effort Estimate
- **Diagnosis**: 15-30 minutes
- **Quick fix** (if root cause obvious): 1-2 hours
- **Full investigation**: 2-4 hours
- **Redesign if needed** (browser login): 4-6 hours

### Dependencies
- **Blocks**: Blockers #3, #7, #8, #9, #10, #11
- **No dependencies** (can be debugged independently)

### Validation Criteria
```bash
# All E2E tests pass
cd frontend && npm run test:e2e:feature-layer:local

# Expected result: 7 passed (0 failed)
# Plus regression smoke: 3 passed (0 failed)
```

### Related Files
- `frontend/app/dashboard/resident/page.tsx` (error boundary here)
- `frontend/e2e/feature-layer/helpers/session.ts` (auth setup)
- `frontend/e2e/feature-layer/auth-and-smoke.spec.ts` (failing test)
- `frontend/lib/api/training.ts` (API client)
- `frontend/lib/api/client.ts` (axios config)
- `backend/sims/training/views.py` (ResidentSummaryView)

### Notes
- **Critical Priority**: This single blocker blocks 5+ dependent blockers
- **Must Fix First**: Cannot verify any E2E coverage until this works
- **May Indicate Real Bug**: E2E failures could reveal actual production issue

---

## Blocker #3: E2E Logbook Save Workflow Fails

### Summary
E2E test for logbook draft → save workflow fails. Depends on Blocker #2 (dashboard rendering).

### Severity
🔴 **HIGH** - Blocks GO threshold: "critical workflows tested = 100%"

### Current State
- **Status**: Test fails immediately at dashboard load
- **Root Cause**: Blocked by Blocker #2
- **Test**: `e2e/feature-layer/logbook.spec.ts:9`

### Expected Test Flow
1. Login as resident ✓ (works)
2. Navigate to dashboard ✗ (fails due to #2)
3. Create logbook entry (not reached)
4. Save as draft (not reached)
5. Submit (not reached)
6. Verify supervisor can return (not reached)

### Fix Strategy
1. **First**: Fix Blocker #2 (dashboard rendering)
2. **Then**: Verify test reaches logbook creation
3. **Then**: Add assertions for logbook save behavior
4. **Then**: Validate full workflow end-to-end

### Effort Estimate
- **Depends on Blocker #2 fix time**
- **Once #2 fixed**: 1-3 hours for workflow testing

### Dependencies
- **Depends on**: Blocker #2 (E2E dashboard rendering)

### Validation Criteria
```bash
cd frontend && npm run test:e2e:feature-layer:local
# Should see "logbook.spec.ts" all tests pass
```

---

## Blocker #4: Restart/Reseed Smoke Test Status Unknown

### Summary
No explicit test exists to verify that restarting services and reseeding data produces a clean, working system.

### Severity
🟡 **MEDIUM** - Blocks GO threshold: "restart/reseed critical smoke = 100%"

### Current State
- **Status**: Not explicitly tested
- **Assumption**: Works (based on prior sessions)
- **Risk**: Unknown if true

### Why This Matters
Production deployments require:
1. Stop backend/frontend/workers
2. Run migrations
3. Reseed data
4. Start services
5. Verify system is working

If this fails, production deployment will fail.

### Fix Strategy

#### Step 1: Document Current Procedure (15 min)
```bash
# Current procedure (undocumented)
docker compose down
docker compose build --no-cache
docker compose up -d
./scripts/e2e_seed.sh
# Verify services healthy: docker compose ps
```

#### Step 2: Create Test Script (30 min)
```bash
#!/bin/bash
set -e

echo "1. Stopping services..."
docker compose down

echo "2. Cleaning volumes (fresh DB)..."
docker compose down -v  # WARNING: Deletes data

echo "3. Building fresh images..."
docker compose build --no-cache

echo "4. Starting services..."
docker compose up -d
sleep 10

echo "5. Running migrations..."
docker compose exec -T backend python manage.py migrate

echo "6. Seeding data..."
./scripts/e2e_seed.sh

echo "7. Running health checks..."
curl -s http://localhost:8014/healthz/ | grep -q "ok"
curl -s http://localhost:8082/ | grep -q "html"

echo "✓ All checks passed - restart/reseed smoke OK"
```

#### Step 3: Integrate into Gate (15 min)
Add script to `scripts/` directory and call from main gate

### Effort Estimate
- **Create test**: 1 hour
- **Integrate into gate**: 0.5 hours
- **Total**: 1-1.5 hours

### Dependencies
- **No dependencies** (can be tested independently)

### Validation Criteria
```bash
# Should complete without errors
./scripts/restart_reseed_smoke.sh

# Expected result: "✓ All checks passed"
```

---

## Blocker #5: Backend Coverage Only 54% (Need 95%)

### Summary
Backend test coverage is 54.38% line, 28.69% branch. GO requires ≥95% line, ≥90% branch. Coverage gap is massive (40.62% line, 61.31% branch).

### Severity
🔴 **HIGH** - Blocks GO threshold: "backend line coverage >= 95%" and "backend branch coverage >= 90%"

### Current State
- **Line coverage**: 54.38%
- **Branch coverage**: 28.69%
- **Tests passing**: 222
- **Gap**: 40.62% line, 61.31% branch

### Coverage by Module (Estimate)
```
sims/users/                   ~80% (good)
sims/academics/               ~70% (fair)
sims/rotations/               ~60% (poor)
sims/training/                ~45% (very poor)
sims/logbook/                 ~40% (very poor)
sims/notifications/           ~50% (poor)
sims/audit/                   ~75% (fair)
sims/domain/ (validators)     ~30% (very poor)
sims/search/                  ~60% (poor)
```

### Root Cause
- Workflow state machines untested
- Permission classes/RBAC gates minimally tested
- Serializer validation branches untested
- Edge cases and error paths untested
- Dashboard/analytics endpoints untested
- Complex view logic (rotations, training) untested

### Fix Strategy

See `05_coverage_strategy.md` for detailed strategy.

#### Phase A: Identify Coverage Gaps (1-2 hours)
```bash
cd backend
pytest sims --cov=sims --cov-report=html --cov-report=term-missing
# Open htmlcov/index.html to visualize
```

#### Phase B: Prioritize High-Impact Modules (1 hour)
1. **Permission classes** (affects all APIs)
2. **Workflow state machines** (training/logbook/rotation)
3. **Serializer validation** (data integrity)
4. **Critical view actions** (used by E2E tests)
5. **Error paths** (resilience)

#### Phase C: Write Meaningful Tests (8-10 hours)
For each untested module:
```python
# Example: Test permission class
def test_permission_allows_own_entry(self):
    """User can edit their own logbook entry"""
    entry = LogbookEntry.objects.create(user=self.user, ...)
    request = factory.get('/')
    request.user = self.user
    perm = CanEditOwnEntry()
    assert perm.has_object_permission(request, view, entry)

def test_permission_denies_others_entry(self):
    """User cannot edit others' logbook entries"""
    entry = LogbookEntry.objects.create(user=other_user, ...)
    request = factory.get('/')
    request.user = self.user
    perm = CanEditOwnEntry()
    assert not perm.has_object_permission(request, view, entry)
```

#### Phase D: Validate Coverage (30 min)
```bash
pytest sims --cov=sims --cov-report=term-missing | tail -20
# Check all modules >= 95%
```

### Effort Estimate
- **Diagnosis**: 1-2 hours
- **Test development**: 8-12 hours
- **Validation**: 0.5-1 hour
- **Total**: 9.5-15 hours

### Dependencies
- **No dependencies** (can be developed independently)
- **Helpful**: Blocker #2 fix (to verify E2E coverage)

### Validation Criteria
```bash
cd backend
pytest sims --cov=sims --cov-report=term-missing -q
# Line coverage: >= 95%
# Branch coverage: >= 90%
# No excluded active files
```

### Related Files
- `backend/sims/*/tests.py` (test files)
- `backend/sims/*/test_*.py` (test files)
- `backend/sims_project/settings_test.py` (test settings)
- `pyproject.toml` (coverage config)

---

## Blocker #6: Frontend Coverage Only 8% (Need 90%)

### Summary
Frontend test coverage is 8.71% line, 7.56% branch. GO requires ≥90% line, ≥85% branch. Coverage gap is extreme (81.29% line, 77.44% branch).

### Severity
🔴 **HIGH** - Blocks GO thresholds: "frontend line coverage >= 90%" and "frontend branch coverage >= 85%"

### Current State
- **Line coverage**: 8.71%
- **Branch coverage**: 7.56%
- **Jest tests**: Minimal (focus was on E2E)
- **Gap**: 81.29% line, 77.44% branch

### Coverage Deficit Locations
```
frontend/app/dashboard/          0-5% (critical gap)
frontend/app/[dashboard page]/   0-10% (critical gap)
frontend/components/ui/          10-30% (poor)
frontend/lib/api/                30-50% (fair)
frontend/lib/auth/               60-80% (good)
frontend/lib/hooks/              20-40% (poor)
```

### Root Cause
- Focus was on E2E tests (which don't count toward coverage)
- Jest unit tests not systematically written
- No snapshot or component tests for pages
- No tests for hooks, utilities, API client variations

### Fix Strategy

See `05_coverage_strategy.md` for detailed strategy.

#### Phase A: Setup Coverage Measurement (30 min)
```bash
cd frontend
npm run test:coverage
# Open coverage/index.html
```

#### Phase B: Prioritize Tiers (1 hour)
- **Tier 1 (Critical)**: Dashboard pages, logbook pages, auth flows
- **Tier 2 (High)**: UTRMC admin pages, supervisor pages, role-based nav
- **Tier 3 (Medium)**: Shared components, hooks, utilities

#### Phase C: Write Component Tests (Tier 1, 6-8 hours)
```typescript
// Example: Test dashboard component
describe('ResidentDashboard', () => {
  it('should display training summary when data loads', async () => {
    const { getByText } = render(<ResidentDashboard />);
    await waitFor(() => {
      expect(getByText(/My Training Dashboard/i)).toBeInTheDocument();
    });
  });

  it('should show error when API fails', async () => {
    mockApiClient.getResidentSummary.mockRejectedValue(new Error('API Error'));
    const { getByText } = render(<ResidentDashboard />);
    await waitFor(() => {
      expect(getByText(/Failed to load/i)).toBeInTheDocument();
    });
  });

  it('should display eligibility cards for each program', async () => {
    const { getAllByTestId } = render(<ResidentDashboard />);
    await waitFor(() => {
      const cards = getAllByTestId('eligibility-card');
      expect(cards.length).toBeGreaterThan(0);
    });
  });
});
```

#### Phase D: Write Utility/Hook Tests (Tier 2, 3-4 hours)
```typescript
describe('useAuth hook', () => {
  it('should return user when authenticated', () => {
    const { result } = renderHook(() => useAuth());
    expect(result.current.user).toBeDefined();
  });

  it('should redirect to login when not authenticated', () => {
    // Mock auth context
    const { result } = renderHook(() => useAuth());
    expect(result.current.isAuthenticated).toBe(false);
  });
});
```

#### Phase E: Validate Coverage (30 min)
```bash
npm run test:coverage
# Check all modules >= 90% line, >= 85% branch
```

### Effort Estimate
- **Setup**: 0.5 hour
- **Tier 1 tests**: 6-8 hours
- **Tier 2 tests**: 3-4 hours
- **Tier 3 tests**: 2-3 hours (if needed)
- **Validation**: 0.5-1 hour
- **Total**: 12-16 hours (realistically 90% on Tier 1+2)

### Dependencies
- **No dependencies** (can be developed independently)
- **Helpful**: Blocker #2 fix (ensures E2E can verify coverage)

### Validation Criteria
```bash
cd frontend
npm run test:coverage
# Line coverage: >= 90%
# Branch coverage: >= 85%
```

### Related Files
- `frontend/__tests__/` (test directory)
- `frontend/jest.config.js` (jest config)
- `frontend/components/**/*.tsx` (component files to test)
- `frontend/app/**/page.tsx` (page files to test)

---

## Blocker #7: UTRMC Admin Cluster Coverage Incomplete

### Summary
UTRMC admin pages and APIs are only partially covered. E2E tests don't fully exercise admin workflows.

### Severity
🟡 **MEDIUM** - Blocks GO threshold: "UTRMC admin mounted cluster fully covered"

### Current State
- **Status**: E2E permission tests partially pass
- **Failing**: Admin-specific workflows
- **Root Cause**: Blocked by Blocker #2 (E2E dashboard rendering)

### Affected Surfaces
- `/dashboard/utrmc/` - UTRMC admin dashboard
- `/dashboard/utrmc/staff` - Staff management
- `/dashboard/utrmc/org-graph` - Organization graph
- `/api/utrmc/*` - UTRMC APIs
- `/api/admin/*` - Admin APIs

### Fix Strategy
1. **First**: Fix Blocker #2 (E2E rendering)
2. **Then**: Verify admin pages render
3. **Then**: Add E2E tests for admin workflows:
   - Approve rotations
   - Manage staff roles
   - View org hierarchy
4. **Then**: Add unit tests for admin view logic

### Effort Estimate
- **Depends on Blocker #2 fix time**: 1-4 hours
- **Once #2 fixed**: 2-4 hours for full coverage

### Dependencies
- **Depends on**: Blocker #2 (E2E rendering)

---

## Blocker #8: Active Routes Not 100% Tested

### Summary
Not all active (mounted, in-use) routes are tested. E2E doesn't systematically cover all routes.

### Severity
🟡 **MEDIUM** - Blocks GO threshold: "active routes tested = 100%"

### Current State
- **Status**: Some routes tested, some not
- **Root Cause**: Blocked by Blocker #2 + incomplete E2E suite

### Key Routes to Test
```
/dashboard/resident/
/dashboard/resident/schedule/
/dashboard/resident/progress/
/dashboard/supervisor/
/dashboard/supervisor/hod-view/
/dashboard/utrmc/
/dashboard/utrmc/staff/
/logbook/ (all logbook pages)
/training/ (all training pages)
/search/
```

### Fix Strategy
1. Fix Blocker #2
2. Create E2E test matrix for all active routes
3. Add one test per route (minimum)

### Effort Estimate
- **Once Blocker #2 fixed**: 2-3 hours

### Dependencies
- **Depends on**: Blocker #2

---

## Blocker #9: Invalid Transitions Not Fully Tested

### Summary
Not all invalid state transitions are tested. E2E doesn't cover negative paths.

### Severity
🟡 **MEDIUM** - Blocks GO threshold: "invalid transitions tested = 100% critical scope"

### Current State
- **Status**: Some transitions tested (unit tests pass)
- **Gap**: E2E coverage for invalid transitions

### Critical Transitions to Test
```
Draft → Draft (error)
Draft → Rejected (error - wrong role)
Pending → Draft (error - already submitted)
Pending → Approved (error - not supervisor)
Returned → Pending (valid)
Returned → Draft (valid)
```

### Fix Strategy
1. Fix Blocker #2
2. Add E2E test for each invalid transition
3. Verify proper error messages

### Effort Estimate
- **Once Blocker #2 fixed**: 1-2 hours

### Dependencies
- **Depends on**: Blocker #2

---

## Blocker #10: Unauthorized Access Tests Incomplete

### Summary
Not all unauthorized access paths are tested. Should verify that users get redirected/denied.

### Severity
🟡 **MEDIUM** - Blocks GO threshold: "unauthorized access tests = 100% active scope"

### Current State
- **Status**: Some permission tests pass
- **Gap**: Systematic unauthorized access testing

### Paths to Test
```
Anonymous user → any dashboard (redirect to login)
Resident → supervisor dashboard (denied)
Supervisor (limited scope) → other residents (denied)
UTRMC staff (read-only) → mutation controls (denied)
Non-HOD → HOD view (denied)
```

### Fix Strategy
1. Fix Blocker #2
2. Create E2E test for each unauthorized path
3. Verify proper error messages/redirects

### Effort Estimate
- **Once Blocker #2 fixed**: 1-2 hours

### Dependencies
- **Depends on**: Blocker #2

---

## Blocker #11: Active Roles Not Fully Tested

### Summary
Not all 5 active roles have complete test coverage. Missing coverage for some role combinations.

### Severity
🟡 **MEDIUM** - Blocks GO threshold: "active roles tested = 100%"

### Current State
- **Status**: Some roles tested
- **Gap**: Comprehensive role coverage

### Roles to Test
1. **PG (Postgraduate trainee)** - Resident portfolio
2. **Supervisor** - Supervise multiple PGs, approve workflows
3. **HOD (Head of Department)** - HOD view with department scope
4. **UTRMC Staff** - Read-only access to system
5. **UTRMC Admin** - Full admin access

### Coverage Matrix
```
Role         | Dashboard | Logbook | Rotation | Admin | Status
PG           | ✓ pass    | ✓ pass  | ? fail   | ✗ no  | PARTIAL
Supervisor   | ? fail    | ✓ pass  | ✓ pass   | ✗ no  | PARTIAL
HOD          | ? fail    | ✓ pass  | ✓ pass   | ✗ no  | PARTIAL
UTRMC Staff  | ✗ no      | ✗ no    | ✗ no     | ✓ pass| PARTIAL
UTRMC Admin  | ✗ no      | ✗ no    | ✗ no     | ✓ pass| PARTIAL
```

### Fix Strategy
1. Fix Blocker #2
2. Add E2E test for each role
3. Verify each role can access allowed surfaces
4. Verify each role is denied disallowed surfaces

### Effort Estimate
- **Once Blocker #2 fixed**: 2-3 hours

### Dependencies
- **Depends on**: Blocker #2

---

## Blocker Dependencies Graph

```
┌─────────────────────────────────────────────────────────────┐
│  BLOCKER #1: Schema Gate                                    │
│  (Can be fixed independently)                               │
│  Effort: 3-5 hrs                                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  BLOCKER #2: E2E Dashboard Rendering (CRITICAL)            │
│  (Must be fixed to unblock #3-11)                           │
│  Effort: 1-4 hrs (diagnosis) + 1-6 hrs (fix)               │
│  ⬇️                                                         │
│  UNBLOCKS: #3, #7, #8, #9, #10, #11                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  BLOCKER #3: E2E Logbook Save Workflow                      │
│  (Depends on #2)                                            │
│  Effort: 1-3 hrs (once #2 fixed)                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  BLOCKER #4: Restart/Reseed Smoke (INDEPENDENT)           │
│  (Can be fixed independently)                               │
│  Effort: 1-1.5 hrs                                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  BLOCKER #5: Backend Coverage (INDEPENDENT)                │
│  (Can be developed independently)                           │
│  Effort: 9.5-15 hrs                                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  BLOCKER #6: Frontend Coverage (INDEPENDENT)               │
│  (Can be developed independently)                           │
│  Effort: 12-16 hrs                                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  BLOCKERS #7-11: Various E2E Tests                          │
│  (All depend on #2)                                         │
│  Combined effort: 6-12 hrs (once #2 fixed)                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Summary Table

| # | Name | Severity | Block Count | Est. Time | Can Do In Parallel |
|---|------|----------|-------------|-----------|-------------------|
| 1 | Schema Gate APIViews | HIGH | 1 | 3-5 hrs | Yes (#2-6) |
| 2 | E2E Dashboard | CRITICAL | 6 | 1-4 hrs | No (blocks #3-11) |
| 3 | Logbook Save E2E | HIGH | 1 | 1-3 hrs | After #2 |
| 4 | Restart/Reseed Smoke | MEDIUM | 1 | 1-1.5 hrs | Yes (#1,5,6) |
| 5 | Backend Coverage | HIGH | 2 | 9.5-15 hrs | Yes (#1,4,6) |
| 6 | Frontend Coverage | HIGH | 2 | 12-16 hrs | Yes (#1,4,5) |
| 7-11 | E2E Coverage Gaps | MEDIUM | 5 combined | 6-12 hrs | After #2 |

---

## Total Effort Calculation

### Critical Path (Must Do)
- Blocker #2 (E2E): 2-10 hours (diagnosis + fix)
- Blocker #5 (Backend): 9.5-15 hours
- Blocker #6 (Frontend): 12-16 hours
- **Total**: 23.5-41 hours

### Optional (But Recommended)
- Blocker #1 (Schema): 3-5 hours
- Blocker #3 (Logbook): 1-3 hours (once #2 done)
- Blocker #4 (Smoke): 1-1.5 hours
- Blockers #7-11 (E2E): 6-12 hours (once #2 done)

### Realistic GO Path
**If doing well**: 20-30 hours  
**If debugging #2 is hard**: 30-40 hours  
**If all blockers**: 40-50 hours

---

## Next Steps

1. Read `02_phase_guide.md` to understand execution phases
2. Choose your starting blocker
3. Reference the specific fix guide for that blocker
4. Execute fixes following `06_testing_procedures.md`
5. Use `08_decision_tree.md` if you get stuck
