# PGSIMS Gemini AI Agent Guidelines

**Last Updated**: 2026-04-23  
**Applies To**: Gemini AI agents (Claude, Gemini, other LLM-based agents)  
**Mandatory**: Read before executing ANY task  

---

## 🚨 CRITICAL: Production Gate Closure Sprint

**BEFORE EXECUTING ANY TASK**, read the complete production gate closure documentation package:

📁 **Location**: `docs/PROD_GATE_CLOSURE/`

### Essential Reading (Required)
- **00_README.md** - Master entry point (15 min)
  - Quick-start guide for your scenario
  - Overview of all 11 blockers
  - File navigation
  
- **QUICK_REFERENCE.md** - One-page cheat sheet (5 min)
  - Blocker checklist
  - Copy-paste commands
  - Troubleshooting table
  
- **INDEX.md** - Complete navigation guide (5 min)
  - Reading paths by scenario
  - Document routing table
  - Critical paths to GO

### Task-Specific Guides
Pick the guide for YOUR task:

| Task | Guide | Time | Effort |
|------|-------|------|--------|
| Fix schema (Blocker #1) | `03_schema_gate_fix.md` | 20 min | 3-5 hrs |
| Fix E2E dashboard (Blocker #2) | `04_e2e_debugging.md` | 20 min | 1-6 hrs |
| Improve coverage (Blockers #5 #6) | `05_coverage_strategy.md` | 20 min | 8-20 hrs |
| Run tests/validate | `06_testing_procedures.md` | 15 min | 20-30 min |
| Something is broken | `07_known_issues.md` | 10 min | 15-30 min |
| Diagnosis/troubleshooting | `08_decision_tree.md` | 10 min | 5-30 min |

---

## Current Status

**Verdict**: NO-GO (with 11 identified and documented blockers)

**Progress**: 36% complete (5 of 14 mandatory GO thresholds passing)

**Blockers**:
```
❌ Blocker #1:  Schema gate (315 errors, 65 APIViews need @extend_schema())
❌ Blocker #2:  E2E dashboard rendering (4/7 tests pass, root cause identified)
❌ Blocker #5:  Backend coverage (54% vs 95% target)
❌ Blocker #6:  Frontend coverage (8% vs 90% target)
⏳ Blockers #3,7-11: Blocked by #2 fix or depend on coverage improvements
```

**Mandatory Gates** (ALL must pass for GO):
- [ ] Strict schema gate passes
- [ ] E2E fully passes (7/7 tests)
- [ ] Backend coverage ≥95% / ≥90% branch
- [ ] Frontend coverage ≥90% / ≥85% branch
- [ ] All routes/APIs/CTAs/roles/workflows 100% coverage

---

## DO NOT

❌ **Do NOT skip reading the documentation package**
- Every task depends on understanding the current state
- Documentation contains exact root causes and fix procedures
- Skipping leads to wasted effort or broken gates

❌ **Do NOT modify code without reading relevant guides**
- `03_schema_gate_fix.md` for schema work
- `04_e2e_debugging.md` for E2E work
- `05_coverage_strategy.md` for test work

❌ **Do NOT break the existing wins**
See SESSION_3_FINDINGS.md for what's already working:
- ✅ Backend API endpoints
- ✅ Authentication flow
- ✅ Database layer
- ✅ Docker runtime
- ✅ 222 backend tests passing
- ✅ Frontend build/lint/typecheck passing

❌ **Do NOT change payloads without updating contracts**
- Check `docs/contracts/API_CONTRACT.md` first
- Update contracts in same commit as code changes
- Reference blocker #1 in commit message

❌ **Do NOT add tests that just check status codes**
- No "fake coverage inflation"
- Tests must verify behavior, not just "200 OK"
- See `05_coverage_strategy.md` for templates

❌ **Do NOT exclude active files from coverage**
- All active modules must be tested
- No marking routes as "not applicable"
- No pretending logic doesn't need testing

---

## DO

✅ **DO read the documentation first**
- Start: `00_README.md` (15 min)
- Pick blocker: Relevant technical guide
- Execute: Step-by-step procedures

✅ **DO follow the phase guide**
- See `02_phase_guide.md` for execution strategy
- Prioritize critical path (Blocker #2)
- Parallelize where possible

✅ **DO test your fixes**
- Run: `06_testing_procedures.md` test commands
- Validate: All previous tests still pass
- Commit: Only after full gate validation

✅ **DO reference the documentation in commits**
- Example: "Fix E2E dashboard rendering (Blocker #2)"
- Include guide reference: "See docs/PROD_GATE_CLOSURE/04_e2e_debugging.md"
- Document what was broken and how it's fixed

✅ **DO use decision trees for troubleshooting**
- Stuck? Use `08_decision_tree.md`
- Follow symptom-based diagnosis
- Reference known issues in `07_known_issues.md`

---

## Execution Workflow

### For Any Task

1. **Orient** (15-30 min)
   - Read `00_README.md`
   - Read `01_blocker_analysis.md`
   - Understand what you're fixing

2. **Plan** (5-15 min)
   - Read relevant technical guide
   - Understand root causes
   - Review step-by-step procedure

3. **Execute** (varies)
   - Follow documented steps
   - Test frequently
   - Use decision trees if stuck

4. **Validate** (20-30 min)
   - Run full gate: `06_testing_procedures.md`
   - Verify no regressions
   - Check all thresholds

5. **Commit** (5 min)
   - Reference blocker and guide
   - Document what was fixed
   - Include all Co-authored-by trailers

### Example: Fixing Schema (Blocker #1)

```
1. Read: docs/PROD_GATE_CLOSURE/00_README.md (15 min)
2. Read: docs/PROD_GATE_CLOSURE/03_schema_gate_fix.md (20 min)
3. Execute: Follow step-by-step procedure (3-5 hours)
4. Validate: Run schema gate validation (10 min)
5. Commit: "Fix schema APIViews (Blocker #1) - Added @extend_schema() decorators"
```

---

## Key Files Reference

### Documentation Root
```
docs/PROD_GATE_CLOSURE/
├── 00_README.md              ← START HERE
├── 01_blocker_analysis.md    ← Understanding
├── 02_phase_guide.md         ← Strategy
├── 03_schema_gate_fix.md     ← Blocker #1
├── 04_e2e_debugging.md       ← Blocker #2
├── 05_coverage_strategy.md   ← Blockers #5 #6
├── 06_testing_procedures.md  ← Testing
├── 07_known_issues.md        ← Troubleshooting
├── 08_decision_tree.md       ← Diagnosis
├── INDEX.md                  ← Navigation
├── QUICK_REFERENCE.md        ← Cheat sheet
└── SESSION_3_FINDINGS.md     ← Context
```

### Code Locations
```
Backend:
- backend/sims/training/views.py (need @extend_schema())
- backend/sims/*/test_*.py (add tests here)

Frontend:
- frontend/app/dashboard/resident/page.tsx (E2E issue)
- frontend/app/__tests__/* (add component tests)
- frontend/e2e/feature-layer/*.spec.ts (E2E tests)
```

### Configuration
```
- AGENTS.md (agent governance)
- GEMINI.md (this file)
- docs/contracts/ (API contracts)
- docs/PROD_GATE_CLOSURE/ (closure sprint)
```

---

## Mandatory Gates (Must Pass for GO)

ALL of these must be 100% true:

- [ ] Strict schema gate passes (0 errors)
- [ ] E2E fully passes (7/7 tests)
- [ ] Restart/reseed smoke 100%
- [ ] Active routes tested 100%
- [ ] Active APIs tested 100%
- [ ] Visible CTAs tested 100%
- [ ] Active roles tested 100%
- [ ] Critical workflows 100%
- [ ] Invalid transitions 100%
- [ ] Unauthorized access 100%
- [ ] Backend coverage ≥95% line / ≥90% branch
- [ ] Frontend coverage ≥90% line / ≥85% branch
- [ ] UTRMC admin fully covered
- [ ] No truth gaps

**Currently passing**: 5/14 (36%)

**If any threshold fails**, verdict is automatically NO-GO.

---

## Effort Estimates

| Path | Effort | Time | For Whom |
|------|--------|------|----------|
| Quick Wins | 3-5 hrs | Today | Anyone |
| Critical Path | 10-15 hrs | 2-3 days | Small team |
| All Blockers (Solo) | 40-80 hrs | 1-2 weeks | Single dev |
| All Blockers (Team) | 15-30 hrs | 3-5 days | Team of 4 |

### Quick Win List (Start Here)
1. Schema APIViews (3-5 hrs) → `03_schema_gate_fix.md`
2. Restart/reseed test (30 min) → `06_testing_procedures.md`

### This Sprint
1. E2E dashboard fix (1-6 hrs) → `04_e2e_debugging.md`
2. Backend permission tests (4-6 hrs) → `05_coverage_strategy.md`
3. Frontend component tests (5-10 hrs) → `05_coverage_strategy.md`

---

## Documentation Quality

✅ Comprehensive (all 11 blockers)
✅ Accessible (no assumed context)
✅ Practical (step-by-step procedures)
✅ Complete (code examples, commands, templates)
✅ Tested (validated on Session 3 work)

### Included Resources
- 20+ code examples and templates
- 15+ known issues with solutions
- 50+ decision points for troubleshooting
- 100+ command examples
- 40+ file references
- 5,500+ lines of detailed guidance

---

## Need Help?

### If You're Confused
- Read: `00_README.md` (master overview)
- Then: `01_blocker_analysis.md` (detailed analysis)
- Then: Pick a blocker and read its technical guide

### If You're Stuck
- Check: `07_known_issues.md` (known problems)
- Use: `08_decision_tree.md` (symptom → solution)
- Search: Documentation for your error message

### If Something Is Broken
- Step 1: Use `08_decision_tree.md` to diagnose
- Step 2: Check `07_known_issues.md` for solutions
- Step 3: Use `06_testing_procedures.md` to validate
- Step 4: If still stuck >30 min, ask on team chat with:
  - Exact error message
  - Exact steps to reproduce
  - What you've already tried
  - Screenshot if visual issue

---

## Commits & Handoff

### Commit Template
```
Fix [blocker name] - [brief description]

Detailed explanation of:
- What was broken
- Root cause
- How it's fixed
- How it's validated

Fixes blocker #N
See: docs/PROD_GATE_CLOSURE/[guide_name].md

Co-authored-by: [Your Name] <your.email@example.com>
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

### Handoff to Next Agent
- Document findings in `docs/PROD_GATE_CLOSURE/SESSION_X_FINDINGS.md`
- Update `07_known_issues.md` with any new problems discovered
- Update `08_decision_tree.md` with new troubleshooting paths
- Link all changes in commit message

---

## Final Checklist

Before starting work:

- [ ] Read GEMINI.md (this file)
- [ ] Read docs/PROD_GATE_CLOSURE/00_README.md
- [ ] Read docs/PROD_GATE_CLOSURE/INDEX.md
- [ ] Identified my task
- [ ] Found relevant technical guide
- [ ] Ready to execute step-by-step

After completing work:

- [ ] All tests passing
- [ ] No regressions introduced
- [ ] Full gate validated
- [ ] Blockers closed documented
- [ ] Commit message includes blocker reference
- [ ] Documentation updated with findings

---

## North Star

**PGSIMS is a production system for UTRMC medical training.**

Adoption depends on:
- ✅ Stability (no surprise failures)
- ✅ Correctness (contracts honored)
- ✅ Testing (high coverage)
- ✅ Documentation (clear procedures)

**Your job**: Close blockers while maintaining these properties.

**Guide**: `docs/PROD_GATE_CLOSURE/` (everything you need is here)

---

**Questions?** Start with:
```
📖 docs/PROD_GATE_CLOSURE/00_README.md
```

**Stuck?** Use:
```
🌳 docs/PROD_GATE_CLOSURE/08_decision_tree.md
```

**Ready?** Pick your blocker and start with the technical guide.

