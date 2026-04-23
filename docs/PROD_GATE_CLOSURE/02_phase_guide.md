# Phase Execution Guide - PGSIMS Production Gate

**Last Updated**: 2026-04-23  
**Purpose**: Step-by-step execution plan to convert NO-GO to GO  
**Scope**: All 11 blockers organized into logical execution phases

---

## Overview

This guide organizes the 11 blockers into **4 main phases** that can be executed in parallel where possible, with clear dependencies noted.

### Phase Structure
- **Phase 1**: Critical Dependency (must do first)
- **Phase 2**: Independent Work (can do in parallel with Phase 1)
- **Phase 3**: E2E Coverage (must do after Phase 1)
- **Phase 4**: Final Validation (must do last)

---

## Phase 1: Resolve E2E Dashboard Crisis (CRITICAL)

**Duration**: 2-10 hours  
**Effort**: Medium-High (diagnosis is the challenge)  
**Blocker**: #2 (E2E Dashboard Rendering)  
**Unblocks**: Blockers #3, #7, #8, #9, #10, #11

### Why This First?
6 other blockers depend on this being fixed. If dashboard E2E fails, you cannot verify any E2E coverage.

### Steps

#### Step 1a: Quick Diagnosis (15-30 min)
See `04_e2e_debugging.md` - Diagnostic Section

```bash
# 1. Check current status
cd frontend
npm run test:e2e:feature-layer:local 2>&1 | tee /tmp/e2e_result.txt

# 2. Identify which tests fail
grep "failed\|passed" /tmp/e2e_result.txt

# 3. Check error message
grep "Failed to load" /tmp/e2e_result.txt
```

#### Step 1b: Verify Services are Healthy (10 min)
```bash
# Check all services running
docker compose ps

# Verify backend API works
curl -s http://127.0.0.1:8014/api/residents/me/summary/ \
  -H "Authorization: Bearer test-token" | head -20

# Verify frontend is up
curl -s http://127.0.0.1:8082 | grep -q "html" && echo "Frontend OK"
```

#### Step 1c: Deep Diagnosis (30-60 min)
See `04_e2e_debugging.md` - Deep Diagnosis Section

```bash
# Add detailed logging
# 1. Modify E2E test to log auth state
# 2. Enable browser console capture
# 3. Run test with trace
npx playwright test e2e/feature-layer/auth-and-smoke.spec.ts --debug

# 4. Capture trace for inspection
# 5. Check output/ directory for test results
ls -la frontend/output/playwright/results/
```

#### Step 1d: Identify Root Cause
Use diagnostic results to determine which hypothesis is correct:
- **Hypothesis A**: Token not injected (modify session setup)
- **Hypothesis B**: API returns unexpected format (update type definitions)
- **Hypothesis C**: ALLOWED_HOSTS rejection (update settings)
- **Hypothesis D**: Session state cleared (refactor auth flow)
- **Hypothesis E**: Race condition (add wait conditions)

See `04_e2e_debugging.md` for detailed diagnosis procedures.

#### Step 1e: Implement Fix (1-6 hours depending on hypothesis)

**If Hypothesis A (Token Injection)**:
```typescript
// In frontend/e2e/feature-layer/helpers/session.ts
await page.goto(APP_BASE_URL);

// Add explicit wait for token
await page.evaluate(() => {
  return new Promise(resolve => {
    const checkToken = setInterval(() => {
      if (localStorage.getItem('access_token')) {
        clearInterval(checkToken);
        resolve(true);
      }
    }, 50);
  });
});

// Add longer delay before API calls
await page.waitForTimeout(200);
```

**If Hypothesis C (ALLOWED_HOSTS)**:
```python
# In backend/sims_project/settings.py
ALLOWED_HOSTS = [
    # ... existing hosts
    'testserver',  # Add for E2E tests
]
```

**If Hypothesis D (Session State)**:
```typescript
// In frontend/e2e/feature-layer/helpers/session.ts
// Switch to browser UI login instead of token injection
const loginButton = page.getByRole('button', { name: 'Login' });
await loginButton.click();
await page.fill('input[name="username"]', username);
await page.fill('input[name="password"]', password);
await page.click('button[type="submit"]');
await page.waitForNavigation();
```

#### Step 1f: Validate Fix (10-15 min)
```bash
# 1. Run E2E tests again
cd frontend
npm run test:e2e:feature-layer:local

# 2. Should see: "7 passed (X seconds)"
# 3. No failures

# 4. Run regression smoke
npx playwright test e2e/feature-layer/regression-smoke.spec.ts

# 5. Should see: "3 passed"
```

#### Step 1g: Commit Fix
```bash
git add frontend/
git commit -m "Fix E2E dashboard rendering - [brief description of fix]

- Identified root cause: [token/ALLOWED_HOSTS/session/etc]
- Applied fix: [what was changed]
- Result: 7/7 feature-layer tests passing, 3/3 regression smoke passing

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

### Success Criteria
```bash
# All must be true:
✓ npm run test:e2e:feature-layer:local → 7 passed
✓ npx playwright test e2e/feature-layer/regression-smoke.spec.ts → 3 passed
✓ Docker services running: docker compose ps → all healthy
✓ Seed data: ./scripts/e2e_seed.sh → success
```

### If This Fails
- See `08_decision_tree.md` for troubleshooting
- Check `07_known_issues.md` for similar issues
- Consider asking for help with detailed trace analysis

---

## Phase 2: Independent Parallel Work (While Phase 1 In Progress)

These can be done in parallel with Phase 1 since they don't depend on it.

### Phase 2A: Fix Schema Gate APIViews

**Duration**: 3-5 hours  
**Blocker**: #1  
**Reference**: `03_schema_gate_fix.md`

#### Quick Steps
```bash
# 1. Identify all APIViews needing decorators (30 min)
cd backend
python manage.py spectacular --file /tmp/schema.yaml --validate --fail-on-warn 2>&1 | \
  grep "unable to guess serializer" | tee /tmp/apiviews.txt
wc -l /tmp/apiviews.txt  # Should show ~65

# 2. For each APIView, add @extend_schema() decorator (3-4 hours)
# See 03_schema_gate_fix.md for examples

# 3. Validate (30 min)
python manage.py spectacular --file /tmp/schema.yaml --validate --fail-on-warn 2>&1 | \
  tail -5
# Check: Warnings should be ~31 or fewer, no "unable to guess serializer"
```

See `03_schema_gate_fix.md` for complete details.

### Phase 2B: Create Restart/Reseed Smoke Test

**Duration**: 1-1.5 hours  
**Blocker**: #4  
**Reference**: `01_blocker_analysis.md` (Blocker #4 section)

#### Quick Steps
```bash
# 1. Create test script (30 min)
cat > scripts/restart_reseed_smoke.sh << 'SCRIPT'
#!/bin/bash
set -e
echo "Starting restart/reseed smoke test..."
# ... (see blocker analysis for full script)
SCRIPT

# 2. Make executable
chmod +x scripts/restart_reseed_smoke.sh

# 3. Test it
./scripts/restart_reseed_smoke.sh

# 4. Integrate into main gate (30 min)
# ... (add to gate execution script)
```

### Phase 2C: Begin Backend Coverage Development

**Duration**: Ongoing (start now, continue in Phase 4)  
**Blocker**: #5  
**Reference**: `05_coverage_strategy.md`

#### Quick Steps
```bash
# 1. Analyze current coverage (30 min)
cd backend
pytest sims --cov=sims --cov-report=html --cov-report=term-missing
# Open htmlcov/index.html

# 2. Identify high-impact modules (30 min)
# Priority: permission classes, state machines, serializers

# 3. Start writing tests (3-4 hours)
# See 05_coverage_strategy.md for examples
```

### Phase 2D: Begin Frontend Coverage Development

**Duration**: Ongoing (start now, continue in Phase 4)  
**Blocker**: #6  
**Reference**: `05_coverage_strategy.md`

#### Quick Steps
```bash
# 1. Analyze current coverage (20 min)
cd frontend
npm run test:coverage

# 2. Identify critical gaps (30 min)
# Priority: Dashboard pages, logbook pages, auth flows

# 3. Start writing tests (3-4 hours)
# See 05_coverage_strategy.md for examples
```

### Parallelization Strategy

You can do **2A+2B in series** (3.5-6.5 hours) while someone else starts **2C+2D**.

**Recommended Team Split** (if 2 people):
- **Person A**: Phase 1 (E2E debugging)
- **Person B**: Phase 2A + 2B (Schema + Smoke)

OR (if 3+ people):
- **Person A**: Phase 1 (E2E)
- **Person B**: Phase 2A + 2C (Schema + Backend tests)
- **Person C**: Phase 2D (Frontend tests)

---

## Phase 3: E2E Coverage & Workflow Testing

**Duration**: 6-12 hours (depends on Phase 1 fix time)  
**Blockers**: #3, #7, #8, #9, #10, #11  
**Prerequisite**: Phase 1 must be complete  
**Reference**: `04_e2e_debugging.md` (E2E Testing section)

### Step 3a: Verify Phase 1 Success (10 min)
```bash
# MUST pass before starting Phase 3
cd frontend
npm run test:e2e:feature-layer:local 2>&1 | grep -E "passed|failed"
# Should show: "7 passed"
```

### Step 3b: Fix Logbook E2E Workflow (1-3 hours)
**Blocker #3**

Now that dashboard works, logbook E2E should work:
```bash
npx playwright test e2e/feature-layer/logbook.spec.ts -v
```

If still failing:
- Check that logbook page renders (now that dashboard works)
- Add missing assertions for logbook save workflow
- See `04_e2e_debugging.md` for debugging

### Step 3c: Add UTRMC Admin Coverage (2-4 hours)
**Blocker #7**

```bash
# Create E2E tests for admin workflows
# 1. Admin dashboard renders
# 2. Can approve rotations
# 3. Can manage staff roles
# 4. Can view org hierarchy
```

### Step 3d: Add Route Coverage Tests (2-3 hours)
**Blocker #8**

```bash
# Create E2E test for each active route
# 1. Test each route renders without errors
# 2. Verify proper permissions
# 3. Check for console errors
```

### Step 3e: Add Invalid Transition Tests (1-2 hours)
**Blocker #9**

```bash
# Test each invalid transition
# 1. Submit → Draft (error)
# 2. Approved → Pending (error)
# etc.
```

### Step 3f: Add Unauthorized Access Tests (1-2 hours)
**Blocker #10**

```bash
# Test unauthorized paths
# 1. Resident → Supervisor dashboard (redirected)
# 2. Supervisor → Admin dashboard (redirected)
# etc.
```

### Step 3g: Add Role Coverage Tests (2-3 hours)
**Blocker #11**

```bash
# Test each role
# 1. Create test for each role
# 2. Test allowed surfaces
# 3. Test denied surfaces
```

### Step 3h: Validate All E2E Tests Pass (15-30 min)
```bash
cd frontend
npm run test:e2e:feature-layer:local
npx playwright test e2e/feature-layer/regression-smoke.spec.ts

# Should see: "all tests passed"
```

---

## Phase 4: Coverage Gap Closure & Final Validation

**Duration**: 20-30 hours (can overlap with Phase 3)  
**Blockers**: #5, #6 (continued from Phase 2)  
**Reference**: `05_coverage_strategy.md`

### Step 4a: Complete Backend Coverage (if Phase 2C not done)

**Duration**: 9.5-15 hours total (possibly started in Phase 2)

```bash
cd backend

# 1. Analyze current coverage
pytest sims --cov=sims --cov-report=html --cov-report=term-missing

# 2. For each module with < 95% coverage:
#    - Write unit tests
#    - Write integration tests
#    - Test happy path + error paths

# 3. Target: >= 95% line, >= 90% branch
pytest sims --cov=sims --cov-report=term-missing -q
```

**Priority Modules** (if limited time):
1. Permission classes (affects all APIs)
2. Training state machines (critical workflow)
3. Logbook validation (critical workflow)
4. Serializer validation (data integrity)

### Step 4b: Complete Frontend Coverage (if Phase 2D not done)

**Duration**: 12-16 hours total (possibly started in Phase 2)

```bash
cd frontend

# 1. Analyze current coverage
npm run test:coverage

# 2. For each page/component with < 90% coverage:
#    - Write Jest unit tests
#    - Test render states (loading, error, empty, data)
#    - Test user interactions

# 3. Target: >= 90% line, >= 85% branch
npm run test:coverage
```

**Priority Components** (if limited time):
1. Dashboard pages (resident, supervisor, admin)
2. Logbook pages (entry, review)
3. Auth pages (login, redirect)
4. Navigation (role-based visibility)

### Step 4c: Run Full Gate from Clean Baseline (2-3 hours)

**Duration**: 2-3 hours  
**Purpose**: Final comprehensive validation

#### 4c-i: Clean Database & Services
```bash
# 1. Stop everything
docker compose down

# 2. Remove volumes (fresh DB)
docker compose down -v

# 3. Rebuild images
docker compose build --no-cache

# 4. Start fresh
docker compose up -d
sleep 10
```

#### 4c-ii: Run Full Gate Sequence
```bash
# 1. Database setup
docker compose exec -T backend python manage.py migrate

# 2. Seed data
./scripts/e2e_seed.sh

# 3. Backend tests + coverage
cd backend && SECRET_KEY=test-secret pytest sims -q --cov=sims --cov-report=term-missing
# Check: >= 95% line, >= 90% branch

# 4. Frontend linting
cd frontend && npm run lint

# 5. Frontend type checking
npm run typecheck

# 6. Frontend unit tests + coverage
npm test -- --watch=false
npm run test:coverage
# Check: >= 90% line, >= 85% branch

# 7. Frontend build
npm run build

# 8. Schema gate
cd backend && python manage.py spectacular --file /tmp/schema.yaml --validate --fail-on-warn
# Check: minimal errors/warnings, all critical views covered

# 9. Docker runtime bring-up
docker compose ps
# Check: all services healthy

# 10. E2E tests
cd frontend && npm run test:e2e:feature-layer:local
# Check: 7/7 passed

# 11. Regression smoke
npx playwright test e2e/feature-layer/regression-smoke.spec.ts
# Check: 3/3 passed

# 12. Restart/reseed smoke
./scripts/restart_reseed_smoke.sh
# Check: success
```

#### 4c-iii: Collect Results
```bash
# 1. Backend coverage report
cd backend && pytest sims --cov=sims --cov-report=term-missing | tail -20 > /tmp/backend_coverage.txt

# 2. Frontend coverage report
cd frontend && npm run test:coverage 2>&1 | tail -20 > /tmp/frontend_coverage.txt

# 3. Schema summary
cd backend && python manage.py spectacular --file /tmp/schema.yaml --validate --fail-on-warn 2>&1 | \
  tail -5 > /tmp/schema_summary.txt
```

### Step 4d: Generate Final Evidence Pack (1-2 hours)

Create documentation summarizing:
- All blockers fixed/not fixed
- Test results for each threshold
- Coverage reports
- Schema validation results
- E2E test results
- Final verdict (GO or NO-GO)

See `SESSION_3_FINDINGS.md` for format reference.

---

## Decision Points During Execution

### Decision 1: After Phase 1 (E2E Fix)
**Question**: "Can we deploy with current coverage levels?"  
**Answer**: NO. Schema gate and coverage must also pass.

### Decision 2: After Phase 2B (Smoke Test)
**Question**: "Should we continue with coverage work?"  
**Answer**: YES. Must complete Phases 3 & 4 to reach GO.

### Decision 3: Mid Phase 4 (After Backend Coverage)
**Question**: "Frontend tests taking too long. Can we skip?"  
**Answer**: NO. Frontend coverage is a mandatory GO threshold.

### Decision 4: Before Final Gate Run
**Question**: "Should we try partial gate run?"  
**Answer**: NO. Must run full gate from clean baseline per requirements.

---

## Timeline Examples

### Example 1: Well-Resourced Team (3+ people, 2-3 days)

**Day 1**:
- Person A: Phase 1 (E2E debug) → 4-6 hrs (with hypothesis testing)
- Person B: Phase 2A (Schema) + Phase 2B (Smoke) → 5-6 hrs in parallel
- Person C: Phase 2C (Backend tests start) → 4-6 hrs in parallel

**Day 2**:
- Person A: Phase 3 (E2E workflows) → 6-8 hrs (now dashboard works)
- Person B: Phase 2A completion + Phase 4A (Backend coverage) → 8-10 hrs
- Person C: Phase 4B (Frontend coverage) → 8-10 hrs

**Day 3**:
- All: Phase 4C (Full gate run) + Phase 4D (Evidence) → 4-6 hrs
- **Result**: GO (assuming all thresholds met)

### Example 2: Lean Team (1 person, 1 week)

**Monday-Tuesday**: Phase 1 (E2E debug) → 4-10 hrs (depending on hypothesis complexity)  
**Wednesday**: Phase 2A (Schema) + Phase 2B (Smoke) → 5-6 hrs  
**Thursday**: Phase 2C/2D (Coverage analysis) → 4 hrs  
**Friday A**: Phase 3 (E2E workflows) → 6-8 hrs  
**Friday B**: Phase 4C (Full gate) → 2-3 hrs  

**Mon-Wed of Week 2**: Phase 4 (Coverage closure) → 20-30 hrs  
**Result**: GO (but stretched timeline)

### Example 3: Blocked Team (Can't fix Phase 1)

If Phase 1 (E2E) cannot be fixed:
- Phases 2A, 2B, 2C, 2D can still be done → 15-22 hrs work
- But **cannot reach GO** because E2E threshold blocks
- Recommend: Stop and escalate Phase 1 to specialists

---

## Progress Tracking

Use this table to track your progress:

```
Phase | Blocker | Status | Start | End | Notes
------|---------|--------|-------|-----|-------
1     | #2      | ⬜     | -     | -   | E2E dashboard
1     | #2      | ⬜     | -     | -   | E2E regression
2A    | #1      | ⬜     | -     | -   | Schema APIViews
2B    | #4      | ⬜     | -     | -   | Restart/smoke
2C    | #5      | ⬜     | -     | -   | Backend coverage
2D    | #6      | ⬜     | -     | -   | Frontend coverage
3     | #3      | ⬜     | -     | -   | Logbook E2E
3     | #7      | ⬜     | -     | -   | UTRMC admin
3     | #8      | ⬜     | -     | -   | Routes
3     | #9      | ⬜     | -     | -   | Transitions
3     | #10     | ⬜     | -     | -   | Unauthorized
3     | #11     | ⬜     | -     | -   | Roles
4     | all     | ⬜     | -     | -   | Full gate run
```

---

## Next Steps

1. **Choose Your Team Size**: 1, 2, or 3+ people?
2. **Pick Your Timeline**: 2 days, 1 week, or longer?
3. **Assign Phases**: Who does what?
4. **Start Phase 1**: Reference `04_e2e_debugging.md`
5. **Track Progress**: Update progress table above

---

## If You Get Stuck

- See `08_decision_tree.md` for symptom-based troubleshooting
- See `07_known_issues.md` for common problems
- See `10_database_debugging.md` if database is suspect
- Re-read relevant blocker section in `01_blocker_analysis.md`
