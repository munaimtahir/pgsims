# PGSIMS Production Gate Closure Sprint - Complete Documentation

**Status**: NO-GO → Targeted Closure Sprint  
**Session**: 3 (Session 2 Investigation + Session 3 Initial Fixes + Comprehensive Docs)  
**Last Updated**: 2026-04-23  
**Target**: GO Verdict  

---

## What Is This?

This folder contains **complete, self-contained documentation** for closing the 11 remaining blockers that prevent PGSIMS from achieving production-ready GO status.

If you're reading this, you need to **fix production gate failures** to release the system. This documentation is designed so that **any developer**, regardless of experience with PGSIMS, can understand the problems and execute the fixes independently.

---

## Quick Start (Pick Your Scenario)

### Scenario A: I've Never Seen This Project

**Start Here** (20 minutes):
1. Read this file (you're doing it!)
2. Read `01_blocker_analysis.md` - Understand what's broken
3. Read `02_phase_guide.md` - Understand how to fix it
4. Pick a blocker from "Quick Win List" below

Then proceed to technical guides.

**Total Time**: 3-5 hours to understand everything

---

### Scenario B: I Need to Fix [Specific Blocker]

**Jump To**:
- Blocker #1 (Schema): `03_schema_gate_fix.md`
- Blocker #2 (E2E Dashboard): `04_e2e_debugging.md`
- Blocker #5 #6 (Coverage): `05_coverage_strategy.md`
- Any blocker: `06_testing_procedures.md` (how to run tests)

**Total Time**: 1-6 hours depending on blocker complexity

---

### Scenario C: I'm Stuck on a Problem

**Use**:
- `07_known_issues.md` - Known problems + solutions
- `08_decision_tree.md` - Symptom → root cause → fix
- `06_testing_procedures.md` - How to run tests and debug

**Total Time**: 15-60 minutes depending on problem

---

## The 11 Blockers (Summary)

| # | Blocker | Status | Effort | Priority |
|---|---------|--------|--------|----------|
| 1 | Schema gate 315 errors | ⚠️  Partial (18 fixed) | 3-5 hrs | HIGH |
| 2 | E2E dashboard fail (4/7 tests) | ❌ Unsolved | 1-6 hrs | CRITICAL |
| 3 | E2E logbook save fail | ❌ Blocked by #2 | 2-4 hrs | HIGH |
| 4 | Restart/reseed smoke | ❓ Unknown | 1-2 hrs | MEDIUM |
| 5 | Backend coverage 54% | ❌ Gap: 41 pts | 8-15 hrs | CRITICAL |
| 6 | Frontend coverage 8% | ❌ Gap: 82 pts | 15-20 hrs | CRITICAL |
| 7 | UTRMC admin partial coverage | ❌ Incomplete | 3-5 hrs | MEDIUM |
| 8 | Routes/APIs incomplete | ❌ Incomplete | 2-4 hrs | MEDIUM |
| 9 | CTAs incomplete | ❌ Incomplete | 1-3 hrs | LOW |
| 10 | Transitions incomplete | ❌ Incomplete | 1-3 hrs | LOW |
| 11 | Unauthorized paths incomplete | ❌ Incomplete | 1-2 hrs | LOW |

**Total Effort**: 40-80 hours (~1-2 weeks solo, or 3-5 days with team)

---

## Quick Win List (Smallest Effort First)

**Today** (5-7 hours):
1. ✅ Fix Docker stale code issue (DONE - Session 3)
2. ⚠️  Fix schema gate APIViews (3-5 hours) - `03_schema_gate_fix.md`
3. ⏳ Test restart/reseed smoke (30 mins) - `06_testing_procedures.md`

**This Sprint** (15-20 hours):
1. Fix E2E dashboard rendering (1-6 hours) - `04_e2e_debugging.md`
2. Fix logbook E2E workflow (2-4 hours) - `04_e2e_debugging.md`
3. Add backend permission tests (4-6 hours) - `05_coverage_strategy.md`
4. Add frontend component tests (5-10 hours) - `05_coverage_strategy.md`

**Remaining** (coverage, routes, CTAs, admin): Depends on #2 E2E fix

---

## File Navigation

### For Everyone
- **`00_README.md`** (this file) - Start here, overview
- **`01_blocker_analysis.md`** - What's broken and why

### For Execution
- **`02_phase_guide.md`** - How to fix everything (phased plan)
- **`03_schema_gate_fix.md`** - How to fix schema (Blocker #1)
- **`04_e2e_debugging.md`** - How to fix E2E (Blocker #2)
- **`05_coverage_strategy.md`** - How to improve coverage (Blockers #5 #6)
- **`06_testing_procedures.md`** - How to run tests and validate

### For Troubleshooting
- **`07_known_issues.md`** - Known problems + solutions
- **`08_decision_tree.md`** - Symptom-based troubleshooting

---

## Key Findings from Investigation

### What Works (Don't Break These)
- ✅ Backend API endpoints (tested with curl)
- ✅ Authentication flow (token generation works)
- ✅ Database layer (test data persists)
- ✅ Docker runtime (all services healthy)
- ✅ Schema endpoint (wired at /api/schema/)
- ✅ 222 backend tests passing
- ✅ Frontend build/lint/typecheck passing

### What's Broken (Must Fix These)
- ❌ E2E tests fail on dashboard rendering (root cause: unknown)
- ❌ Schema generation has 315 errors (root cause: 65 APIViews lack @extend_schema())
- ❌ Backend coverage is 54% (root cause: permission logic untested)
- ❌ Frontend coverage is 8% (root cause: components not tested)

### Critical Insight
The **E2E dashboard rendering failure** is blocking everything. Until this is fixed, you cannot verify:
- E2E functionality (3 tests)
- Critical workflows (2 blockers)
- Transition testing (2 blockers)
- UTRMC admin coverage (4 blockers)

**Recommendation**: Fix E2E dashboard first, then everything else becomes testable.

---

## Mandatory GO Thresholds

ALL of these MUST be true for GO verdict:

- ✅ strict schema gate passes (currently 315 errors)
- ❌ active-surface E2E fully passes (currently 4/7 pass)
- ❓ restart/reseed critical smoke = 100% (unknown status)
- ❌ active routes tested = 100% (currently incomplete)
- ❌ active APIs tested = 100% (currently incomplete)
- ❌ visible CTAs tested = 100% (currently incomplete)
- ❌ active roles tested = 100% (currently incomplete)
- ❌ critical workflows tested = 100% (blocked by E2E #2)
- ❌ invalid transitions tested = 100% (blocked by E2E #2)
- ❌ unauthorized access tests = 100% (blocked by E2E #2)
- ❌ backend line coverage >= 95% (currently 54%)
- ❌ backend branch coverage >= 90% (currently 28%)
- ❌ frontend line coverage >= 90% (currently 8%)
- ❌ frontend branch coverage >= 85% (currently 7%)
- ❌ UTRMC admin mounted cluster fully covered (currently incomplete)

**Result**: 10 thresholds failing = NO-GO (mandatory)

**To reach GO**: Must close ALL 11 blockers AND pass ALL 14 thresholds

---

## How to Use This Documentation

### Step 1: Understand the Problem
Read `01_blocker_analysis.md` to understand:
- What each blocker is
- Why it exists
- What it blocks
- Estimated effort to fix

**Time**: 15-20 minutes

### Step 2: Plan Your Execution
Read `02_phase_guide.md` to understand:
- How to break work into phases
- What can be parallelized
- Dependencies between blockers
- Timeline estimates

**Time**: 10-15 minutes

### Step 3: Pick a Blocker
Choose from Quick Win List or your assignment.

**Start With**: 
- `03_schema_gate_fix.md` if fixing schema (Blocker #1)
- `04_e2e_debugging.md` if fixing E2E (Blocker #2)
- `05_coverage_strategy.md` if adding tests (Blockers #5 #6)

### Step 4: Execute Fix
Follow the step-by-step guide:
1. Understand the problem
2. Diagnostic/investigation steps
3. Implement fix
4. Validate with tests
5. Commit with message

**Time**: Varies by blocker (1-20 hours)

### Step 5: Verify
Use `06_testing_procedures.md` to run full gate:
- Backend tests + coverage
- Frontend tests + lint + type-check + build
- Schema gate
- E2E tests
- Restart/reseed smoke

**Time**: 20-30 minutes

### Step 6: If Stuck
Check `07_known_issues.md` and `08_decision_tree.md`:
- Symptom matching
- Solution lookup
- Debugging procedures

**Time**: 15-60 minutes

---

## Session 3 Results

### What Was Fixed
- ✅ Department serializer duplicates (schema warnings: 49 → 31)
- ✅ Docker rebuild procedure (eliminated stale Python bytecode issue)
- ✅ E2E test diagnostics (identified 5 root cause hypotheses)
- ✅ Comprehensive documentation (this folder)

### What Still Needs Fixing
- ❌ E2E dashboard rendering (root cause still unknown)
- ❌ 65 APIViews without @extend_schema() decorators
- ❌ Backend coverage gap (41 percentage points)
- ❌ Frontend coverage gap (82 percentage points)
- ❌ 10 other blockers (routed/CTAs/transitions/unauthorized/admin)

### Recommendations for Next Team
1. **Priority #1**: Fix E2E dashboard rendering (Blocker #2)
   - Use Playwright Inspector for network trace debugging
   - Try token injection timing fix first
   - If no progress in 2 hours, try browser UI login refactor

2. **Priority #2**: Add @extend_schema() decorators (Blocker #1)
   - Low risk, mechanical work
   - Can be parallelized across team
   - 3-5 hours to completion

3. **Priority #3**: Add permission tests (Blocker #5)
   - High ROI (covers many code paths)
   - Template provided in `05_coverage_strategy.md`
   - 4-6 hours for meaningful progress

4. **Work in Parallel**:
   - Team A: Fix E2E dashboard
   - Team B: Add schema decorators
   - Team C: Write permission tests
   - Team D: Write component tests

---

## Getting Help

### If You're Confused
- Check `02_phase_guide.md` for big picture
- Check `01_blocker_analysis.md` for details on specific blocker

### If Something Is Broken
- Check `07_known_issues.md` for known problems
- Check `08_decision_tree.md` for troubleshooting

### If You Need Details
- Check specific guide: `03_schema_gate_fix.md`, `04_e2e_debugging.md`, etc.
- Check `06_testing_procedures.md` for how to run tests

### If You're Stuck for >30 minutes
- Take screenshot of error
- Copy full error message
- Document exactly what you were trying to do
- Check if this is in `07_known_issues.md`
- Ask on team chat with context

---

## Reference Data

### Project Structure
```
pgsims/
├── backend/              # Django app
├── frontend/             # Next.js app
├── docker/               # Docker compose config
├── docs/
│   └── PROD_GATE_CLOSURE/  # This folder ← START HERE
│       ├── 00_README.md
│       ├── 01_blocker_analysis.md
│       ├── 02_phase_guide.md
│       ├── 03_schema_gate_fix.md
│       ├── 04_e2e_debugging.md
│       ├── 05_coverage_strategy.md
│       ├── 06_testing_procedures.md
│       ├── 07_known_issues.md
│       └── 08_decision_tree.md
└── scripts/              # Seed/helper scripts
```

### Key Commands

```bash
# Start everything
docker compose up -d

# Run backend tests
cd backend && pytest sims -q

# Run backend with coverage
cd backend && pytest sims --cov=sims --cov-report=term

# Run frontend tests
cd frontend && npm test -- --watch=false

# Run E2E tests
./scripts/e2e_seed.sh && cd frontend && npm run test:e2e:feature-layer:local

# Full gate
make clean && make build && make test-backend-coverage && \
  make test-frontend && make schema-gate && make e2e-smoke
```

### Key Contacts
- Backend lead: [Name]
- Frontend lead: [Name]
- E2E specialist: [Name]
- Documentation: This folder (04_e2e_debugging.md, etc.)

---

## Next Steps

1. **Read** `01_blocker_analysis.md` (15 mins)
2. **Read** `02_phase_guide.md` (15 mins)
3. **Pick a blocker** (decide)
4. **Execute** using relevant technical guide (varies)
5. **Test** using `06_testing_procedures.md` (20 mins)
6. **Validate** gate passes
7. **Commit** and move to next blocker

---

## Final Notes

- **This is NOT a fresh audit**: We know exactly what's broken
- **This IS a targeted sprint**: Fixes are surgical, not broad refactors
- **All resources are here**: No hunting for info, it's in this folder
- **You can do this**: Every step is documented
- **Together is faster**: Parallelization recommendations in Phase Guide

---

**Ready?** → Start with `01_blocker_analysis.md`

