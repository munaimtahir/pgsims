# PGSIMS Gemini AI Agent Governance

This repository is operated via Gemini AI agents (and other LLM-based agents). To prevent drift and ensure production safety, every agent run MUST follow these rules.

---

## 0) North Star

**PGSIMS is the operational system for UTRMC monitoring of postgraduate training.**

Adoption depends on:
- UI stability and predictability
- Contract correctness (backend ↔ frontend)
- High test coverage and validation
- Comprehensive documentation

Your role: Close production gate blockers while maintaining these properties.

---

## 🚨 CRITICAL: Production Gate Closure Sprint

**BEFORE EXECUTING ANY TASK**, read the production gate closure documentation package:

📁 **Location**: `docs/PROD_GATE_CLOSURE/`

### Required Reading (Non-Negotiable)
1. **00_README.md** - Master entry point (15 min)
   - Quick-start guide for your scenario
   - Overview of all 11 blockers
   - Navigation guide

2. **QUICK_REFERENCE.md** - One-page cheat sheet (5 min)
   - Blocker checklist with effort
   - Copy-paste ready commands
   - Quick troubleshooting

3. **INDEX.md** - Complete navigation (5 min)
   - Reading paths by task
   - Document routing
   - Getting started

### Task-Specific Guides
Pick the guide matching YOUR task:

- **Blocker #1 (Schema)**: `03_schema_gate_fix.md`
- **Blocker #2 (E2E)**: `04_e2e_debugging.md`
- **Blockers #5 #6 (Coverage)**: `05_coverage_strategy.md`
- **Testing/Validation**: `06_testing_procedures.md`
- **Troubleshooting**: `07_known_issues.md` + `08_decision_tree.md`

### Current Status (DO NOT IGNORE)
```
Verdict: NO-GO (11 identified blockers, 5/14 gates passing)

Blockers:
❌ #1:  Schema (315 errors, 65 APIViews need @extend_schema())
❌ #2:  E2E dashboard (4/7 tests pass, root cause identified)
❌ #5:  Backend coverage (54% vs 95% required)
❌ #6:  Frontend coverage (8% vs 90% required)
⏳ #3,7-11: Depend on #2 fix or coverage improvements
```

---

## 1) Operating Mode

- **Default**: Single-agent execution with internal delegation allowed
- **Constraint**: Must respect phase gates and contract locks (see below)
- **Mandate**: Every claim backed by evidence (file paths, test output, logs)
- **Before ANY task**: Read `docs/PROD_GATE_CLOSURE/` and relevant technical guide
- **Scope**: Fix identified blockers, do NOT attempt broad refactors
- **Evidence**: Reference specific blockers when committing changes

---

## 2) Contract-First (Non-Negotiable)

- Backend ↔ Frontend integration MUST be driven by `docs/contracts/`
- If code changes require contract changes, update contracts in the same run
- No "quick fixes" that silently change payload shapes
- **Reference**: See `docs/contracts/API_CONTRACT.md` for authoritative payloads
- **Gate**: Contract changes must include test updates in same commit

---

## 3) Frozen UX Rule (Adoption-Safety)

- DO NOT change route structure, navigation labels, or terminology once pilot begins
- **Allowed** after freeze: bug fixes, performance, helper text, small visual cues
- **Any** UX-affecting change requires explicit approval AND version bump note in:
  - `docs/contracts/ROUTES.md`
  - `docs/contracts/TERMINOLOGY.md`
- **EXPLICIT OVERRIDE/UNLOCK**: The Frozen UX Rule is unlocked for debugging UI/UX, modifying/adding/updating routes, views, components, navigation labels, and terminology as explicitly directed by the project lead.
- **Reference**: See `docs/PROD_GATE_CLOSURE/02_phase_guide.md` for scope boundaries

---

## 4) Canonical Data Model Rule (Critical)

- There is exactly ONE canonical Department entity for the university
- There is exactly ONE canonical Hospital entity for the university
- A hospital hosts a subset of departments via `HospitalDepartment` matrix table
- **DO NOT** create or reintroduce a second Department model (e.g., "RotationDepartment", "AcademicDepartment")
- **Violation**: Automated drift scanner will catch this (see Blocker #1 analysis)

---

## 5) Audit Integrity

- All state transitions must be auditable
- Do NOT remove `django-simple-history`
- Never silently mutate approved/verified records
- **All models** with state changes must include history tracking

---

## 6) Notifications

- Notifications MUST use canonical schema: `recipient`, `verb`, `body`, `metadata`
- Do NOT use legacy keys (`user`, `message`, `type`, `related_object_id`)
- Prefer single `NotificationService` helper at `sims/notifications/services.py`
- **Reference**: See `docs/PROD_GATE_CLOSURE/01_blocker_analysis.md` for audit requirements

---

## 7) Phase Gates (Must Pass)

Each phase has mandatory gates in `docs/contracts/TRUTH_TESTS.md`.

**A phase is not "done" until gates pass.**

Current mandatory gates (ALL must be true for GO):
- [ ] Strict schema gate (0 errors)
- [ ] E2E fully passes (7/7 tests)
- [ ] Backend coverage ≥95% line / ≥90% branch
- [ ] Frontend coverage ≥90% line / ≥85% branch
- [ ] All routes/APIs/CTAs/roles/workflows 100%

**If any threshold fails**, verdict is automatically NO-GO.

---

## 8) Definition of Done

A task is complete only when:
- ✅ Relevant tests pass
- ✅ Contracts updated (if applicable)
- ✅ No drift introduced (scan forbidden patterns in section 9)
- ✅ Work documented under `docs/_audit/` or `docs/PROD_GATE_CLOSURE/`
- ✅ Blocker reference included in commit message

---

## 9) Forbidden Patterns

Automated scanning should fail if these appear:

1. **Duplicate Department models**
   - Example: Creating `RotationDepartment`, `AcademicDepartment`
   - **Reference**: See Blocker #1 in `01_blocker_analysis.md`

2. **Breaking API payloads without contract updates**
   - Example: Adding required field without updating `API_CONTRACT.md`
   - **Reference**: See `02_phase_guide.md` for contract workflow

3. **Legacy Notification keys**
   - Example: `user=`, `message=`, `type=`, `related_object_id=`
   - **Fix**: Use `NotificationService` helper

4. **Direct database edits for state changes**
   - Example: Raw SQL `UPDATE` bypassing history tracking
   - **Reference**: See section 5 (Audit Integrity)

5. **UX changes without frozen rule exceptions**
   - Example: Changing route structure without approval
   - **Reference**: See section 3 (Frozen UX Rule)

6. **Fake coverage inflation**
   - Example: Tests that only check "status is 200"
   - **Reference**: See `05_coverage_strategy.md` for meaningful tests

---

## 10) MCP Agent Reproducibility Policy

- MCP server configs required for workflows MUST be committed (e.g., `.mcp.json`)
- MCP dependency manifests/lockfiles MUST be committed (e.g., `package.json` + `package-lock.json`)
- Do NOT rely on floating versions (e.g., `@latest`) in committed scripts
- Runtime artifacts/output folders from MCP tools MUST remain untracked

---

## 11) Production Gate Closure Sprint (MANDATORY READ)

**DO NOT SKIP THIS SECTION**

Before executing ANY task that affects:
- Tests or test coverage
- Schema generation
- E2E testing
- Backend/frontend integration
- Performance or stability

Read these documents IN THIS ORDER:

### Level 1: Understanding (30 min)
1. `docs/PROD_GATE_CLOSURE/00_README.md` - Master overview
2. `docs/PROD_GATE_CLOSURE/01_blocker_analysis.md` - All blockers mapped

### Level 2: Planning (15 min)
3. `docs/PROD_GATE_CLOSURE/02_phase_guide.md` - Execution strategy
4. `docs/PROD_GATE_CLOSURE/INDEX.md` - Navigation guide

### Level 3: Execution (task-specific)
- Fixing schema: `03_schema_gate_fix.md`
- Fixing E2E: `04_e2e_debugging.md`
- Adding tests: `05_coverage_strategy.md`
- Running gate: `06_testing_procedures.md`

### Level 4: Troubleshooting (as needed)
- Known issues: `07_known_issues.md`
- Diagnosis: `08_decision_tree.md`
- Quick ref: `QUICK_REFERENCE.md`

**Time investment**: 30-60 min to read + understand
**Time saved**: 10+ hours by not repeating failed approaches

---

## 12) DO NOT (Gemini-Specific)

❌ **DO NOT assume context from partial conversation**
- Always read the full documentation package first
- Session context is limited; docs are complete

❌ **DO NOT generate code without understanding root cause**
- Read diagnostic guide for your blocker first
- Understand what's broken BEFORE fixing

❌ **DO NOT skip test validation**
- Run full gate after changes
- Use `06_testing_procedures.md` commands

❌ **DO NOT break existing wins**
- Session 3 already fixed: schema warnings (49→31), E2E diagnosis, Docker issues
- See `SESSION_3_FINDINGS.md` for what NOT to break

❌ **DO NOT make judgment calls on gate thresholds**
- ALL thresholds are mandatory (see section 7)
- NO exceptions, NO workarounds, NO "close enough"

---

## 13) DO (Gemini-Specific)

✅ **DO read documentation fully before responding**
- Take time to understand context
- Reference specific documents in your response

✅ **DO provide evidence for claims**
- Example: "Blocker #2 identified in 04_e2e_debugging.md section X"
- Include file paths and line numbers

✅ **DO follow procedures step-by-step**
- Don't skip diagnostic steps
- Use decision trees for troubleshooting

✅ **DO reference blockers in commits**
- Example: "Fix E2E dashboard (Blocker #2)"
- Include guide reference in commit body

✅ **DO ask clarifying questions when scope is ambiguous**
- Better to ask than assume wrong task
- Reference relevant documentation

---

## 14) Project Structure Reference

```
pgsims/
├── backend/                          # Django REST API
│   ├── sims_project/                 # Project config
│   ├── sims/                         # Core apps
│   │   ├── users/                    # User management
│   │   ├── training/                 # Training workflows
│   │   ├── rotations/                # Rotation management
│   │   ├── academics/                # Academic core
│   │   ├── notifications/            # Notifications
│   │   └── */test_*.py               # Tests (add here)
│   └── manage.py
│
├── frontend/                         # Next.js 14 frontend
│   ├── app/                          # Routes (frozen)
│   ├── components/                   # React components
│   ├── lib/                          # Utilities
│   ├── e2e/feature-layer/            # E2E tests (4/7 passing)
│   └── app/__tests__/                # Unit tests (add here)
│
├── docs/
│   ├── contracts/                    # Authoritative API specs
│   ├── PROD_GATE_CLOSURE/            # ← START HERE (12 guides)
│   │   ├── 00_README.md
│   │   ├── 01_blocker_analysis.md
│   │   ├── 02_phase_guide.md
│   │   ├── 03_schema_gate_fix.md
│   │   ├── 04_e2e_debugging.md
│   │   ├── 05_coverage_strategy.md
│   │   ├── 06_testing_procedures.md
│   │   ├── 07_known_issues.md
│   │   ├── 08_decision_tree.md
│   │   ├── INDEX.md
│   │   ├── QUICK_REFERENCE.md
│   │   └── SESSION_3_FINDINGS.md
│   ├── _recovery/                    # Recovery baseline
│   ├── _prod_gate/                   # Evidence packs
│   └── _audit/                       # Working docs
│
├── docker/                           # Docker compose
├── scripts/                          # Seed/helper scripts
├── AGENTS.md                         # Agent governance
├── GEMINI.md                         # This file
├── README.md                         # Project README
└── Makefile                          # Build targets
```

---

## 15) Key Commands (Copy-Paste Ready)

### Backend Testing
```bash
cd backend && SECRET_KEY=test-secret pytest sims -q
cd backend && pytest sims --cov=sims --cov-report=html --cov-report=term
cd backend && pytest sims/training/ -v
```

### Frontend Testing
```bash
cd frontend && npm test -- --watch=false
cd frontend && npm run test:coverage -- --watch=false
cd frontend && npm run lint && npx tsc --noEmit
```

### E2E Testing
```bash
./scripts/e2e_seed.sh
cd frontend && npm run test:e2e:feature-layer:local
```

### Schema Gate
```bash
cd backend && python manage.py spectacular_settings --validate
cd backend && python manage.py spectacular_settings --file /tmp/schema.yaml
```

### Docker
```bash
docker compose up -d
docker compose ps
docker compose logs backend
docker compose down
```

---

## 16) Mandatory Gates (ALL must pass for GO)

| Gate | Threshold | Current | Status |
|------|-----------|---------|--------|
| Schema strict | 0 errors | 315 errors | ❌ |
| E2E tests | 7/7 pass | 4/7 pass | ❌ |
| Backend coverage | ≥95% line / ≥90% branch | 54% / 28% | ❌ |
| Frontend coverage | ≥90% line / ≥85% branch | 8% / 7% | ❌ |
| Routes tested | 100% active | Incomplete | ❌ |
| APIs tested | 100% active | Incomplete | ❌ |
| CTAs tested | 100% visible | Incomplete | ❌ |
| Roles tested | 100% active | Incomplete | ❌ |
| Workflows | 100% critical | Incomplete | ❌ |
| Transitions | 100% critical | Incomplete | ❌ |
| Unauthorized | 100% active | Incomplete | ❌ |
| UTRMC admin | Full coverage | Partial | ❌ |
| Restart smoke | 100% pass | Unknown | ❓ |
| Truth gaps | None | Multiple | ❌ |

**Result**: 0/14 passing = NO-GO (mandatory, no exceptions)

---

## 17) Effort Estimates

### Quick Wins (Today)
- Schema APIViews: 3-5 hours
- Restart/reseed test: 30 min
- **Total**: 3.5-5.5 hours

### This Sprint (1-2 weeks)
- E2E dashboard fix: 1-6 hours
- Backend permission tests: 4-6 hours
- Frontend component tests: 5-10 hours
- Other coverage: 5-10 hours
- **Total**: 15-30 hours

### All Blockers
- Solo developer: 40-80 hours
- Team of 4: 15-30 hours
- **Realistic**: 1-2 weeks solo, 3-5 days team

---

## 18) Commit Template

```
Fix [blocker name/number] - [brief description]

Detailed explanation of:
- What was broken
- Root cause
- How it's fixed
- How it's validated

Fixes blocker #N (reference blocker analysis)
See: docs/PROD_GATE_CLOSURE/[relevant_guide].md

Validation:
- All X tests passing
- Coverage maintained/improved
- No regressions

Co-authored-by: [Your Name] <your.email@example.com>
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

---

## 19) If You're Stuck

### Step 1: Check Documentation
- Symptom-based: `08_decision_tree.md`
- Known issues: `07_known_issues.md`
- Quick ref: `QUICK_REFERENCE.md`

### Step 2: Use Decision Tree
```
Problem → Root Cause Questions → Solution
```

### Step 3: Follow Diagnostic Steps
- Example: `04_e2e_debugging.md` has 5-hypothesis testing procedure

### Step 4: Run Tests to Validate
- `06_testing_procedures.md` has all commands

### Step 5: If Still Stuck (>30 min)
- Document exact error + steps to reproduce
- Reference which decision tree path you followed
- Ask on team chat with full context

---

## 24) Anti-Drift Guardrails (Session Focus Window)

**MANDATORY**: Read `docs/ANTI_DRIFT_GUARDRAILS.md` before every session.

This ensures you stay focused on your specific blocker and don't drift into adjacent work.

### Core Principle
Every Gemini AI session must:
- ✅ Fix exactly ONE assigned blocker
- ✅ Follow decision tree steps precisely
- ✅ Run full gate validation before claiming success
- ✅ Create checkpoint with NEXT_STEPS before ending
- ❌ DO NOT expand scope mid-session
- ❌ DO NOT "quickly fix" adjacent blockers
- ❌ DO NOT refactor unrelated code
- ❌ DO NOT skip testing/validation steps

### Session Window (Copy & Paste Template)

Before starting ANY work, fill out this template and save to session plan:

```
# Session Window: [Date/Time]

PRIMARY PURPOSE
  Fix blocker #[N]: [Name]
  Success = [specific criteria from gate]

IN-SCOPE (ALLOWED)
  - [ ] Fix this blocker's root cause
  - [ ] Add required tests
  - [ ] Update contracts if needed
  - [ ] Document findings

OUT-OF-SCOPE (FORBIDDEN)
  - [ ] Refactor unrelated code
  - [ ] Fix adjacent blockers
  - [ ] Add features beyond scope
  - [ ] Cleanup/dead code removal

SUCCESS CRITERIA
  - [ ] Test [X] passes
  - [ ] Coverage threshold met
  - [ ] Full gate passes
  - [ ] Blocker marked COMPLETE

FALLBACK PLAN
  If stuck >2 hours:
  1. Check 08_decision_tree.md
  2. Check 07_known_issues.md
  3. Document findings
  4. Ask for help (don't expand scope)

GUARDRAILS ACTIVE
  ✅ G1-G20 enforced
  ✅ Drift detection on every commit
  ✅ Scope locked (one blocker)
  ✅ Focus validated every 30 min
```

### 20 Core Guardrails (G1-G20)

**Scope Guardrails (G1-G4)**
- G1: No refactoring unless required for blocker
- G2: No new features beyond blocker scope
- G3: No architecture changes
- G4: No config tweaks "for convenience"

**Focus Guardrails (G5-G8)**
- G5: No scope expansion when stuck (use decision tree)
- G6: No adjacent blockers without assignment
- G7: No cleanup tasks
- G8: No premature optimization

**Testing Guardrails (G9-G12)**
- G9: No test exclusions (@skip, @pytest.mark.skip)
- G10: No trivial tests (only status code checks)
- G11: No coverage gaming (inflate % with junk tests)
- G12: No silent mocking (mock permission checks, state machines)

**Contract Guardrails (G13-G16)**
- G13: No payload changes without API_CONTRACT.md update
- G14: No route/nav changes without frozen rule exception
- G15: No migration without data validation
- G16: No breaking changes without CHANGELOG entry

**Evidence Guardrails (G17-G20)**
- G17: No claims without proof (cite tests, outputs)
- G18: No estimates as facts (exact status only)
- G19: No incomplete runbooks (copy-paste ready only)
- G20: No handoff without NEXT_STEPS guide

### Drift Detection Checklist (Before EVERY Commit)

**STOP and ask:**

1. **Scope Check**
   - [ ] Does this commit fix exactly ONE blocker?
   - [ ] Is blocker in 01_blocker_analysis.md?
   - [ ] Does message reference blocker #N?

2. **Focus Check**
   - [ ] Did I follow decision tree?
   - [ ] Did I skip any diagnostic steps?
   - [ ] Did I expand scope mid-task?

3. **Testing Check**
   - [ ] Did I run FULL gate (not partial)?
   - [ ] Are all tests passing?
   - [ ] Coverage up or same (not down)?

4. **Contract Check**
   - [ ] Updated contracts if payload changed?
   - [ ] Updated frozen docs if UX changed?
   - [ ] Added CHANGELOG entry if breaking?

5. **Evidence Check**
   - [ ] Can cite specific test names/lines?
   - [ ] Backed by actual test output?
   - [ ] Can someone reproduce from my docs?

6. **Handoff Check**
   - [ ] Can next person pick up here?
   - [ ] Did I document what's next?
   - [ ] Updated checkpoint/plan?

**If ANY answer is NO → DO NOT COMMIT → Fix it → Try again**

### Drift Detection Alerts (Stop Immediately)

If you exhibit ANY of these:
- ❌ Commits to 3+ unrelated files → **DRIFT ALERT**
- ❌ Claim "fixed" but gate still RED → **DRIFT ALERT**
- ❌ Starting new blocker mid-session → **DRIFT ALERT**
- ❌ Skipping decision tree steps → **DRIFT ALERT**
- ❌ Excluding tests from validation → **DRIFT ALERT**

**Action**: STOP, read guardrails, refocus, ask for help.

### Enforcement Process

**Pre-Session**
1. ✅ Read GEMINI.md sections 0-24
2. ✅ Read docs/PROD_GATE_CLOSURE/00_README.md
3. ✅ Read relevant technical guide
4. ✅ WRITE session window (above) to plan
5. ✅ Confirm GUARDRAILS ACTIVE
6. ✅ Get assignment from lead

**During Session (Every 30 min)**
- [ ] Check drift detection checklist
- [ ] Review session plan (still fixing blocker?)
- [ ] If stuck >15 min: decision tree + known_issues

**Before Every Commit**
- [ ] Run drift detection checklist (all 6)
- [ ] Validate G1-G20
- [ ] Show actual test output in commit message

**After Every Commit**
- [ ] Wait for CI validation
- [ ] If RED: investigate + fix + commit again
- [ ] If GREEN: continue or move next

**Post-Session**
- [ ] Full gate from clean baseline
- [ ] Create checkpoint with results
- [ ] Create NEXT_STEPS.md in checkpoint
- [ ] Update plan with blocker status
- [ ] Verdict: COMPLETE / PARTIAL / BLOCKED

### References

- **Full guardrails**: `docs/ANTI_DRIFT_GUARDRAILS.md`
- **Decision tree**: `docs/PROD_GATE_CLOSURE/08_decision_tree.md`
- **Known issues**: `docs/PROD_GATE_CLOSURE/07_known_issues.md`
- **Testing guide**: `docs/PROD_GATE_CLOSURE/06_testing_procedures.md`
- **Blocker analysis**: `docs/PROD_GATE_CLOSURE/01_blocker_analysis.md`

---

## 20) Session 3 Status (What's Already Done)

✅ **Fixed**:
- Schema duplicate imports (49→31 warnings)
- Docker stale code procedure
- E2E diagnosis (5 hypotheses identified)

✅ **Created**:
- 12-file documentation package (150KB)
- Complete blocker analysis
- Step-by-step fix guides
- Decision tree troubleshooting
- Testing procedures reference

⚠️ **Partial**:
- Schema gate (315 errors remain)
- E2E dashboard (root cause identified, not fixed)

❌ **Not Yet**:
- E2E dashboard fix (depends on diagnosis)
- Coverage improvements (depends on test infrastructure)
- Remaining blockers (depend on #2 and #5 #6)

**DO NOT BREAK THESE WINS** - They're foundation for next work

---

## 21) Final Checklist

Before starting:
- [ ] Read GEMINI.md (this file)
- [ ] Read `docs/PROD_GATE_CLOSURE/00_README.md`
- [ ] Read relevant technical guide for your blocker
- [ ] Understood root cause
- [ ] Found specific files to change
- [ ] Reviewed success criteria

While working:
- [ ] Following step-by-step procedure
- [ ] Testing frequently
- [ ] No forbidden patterns introduced
- [ ] Documenting findings

After finishing:
- [ ] All previous tests still pass
- [ ] New tests passing
- [ ] Full gate validation run
- [ ] Blocker reference in commit
- [ ] Documentation updated
- [ ] Ready for handoff

---

## 22) References

### Governance & Standards
- `AGENTS.md` - All agent rules (original source)
- `GEMINI.md` - This file (Gemini-specific)

### Documentation (Must Read)
- `docs/PROD_GATE_CLOSURE/00_README.md` - Start here
- `docs/PROD_GATE_CLOSURE/INDEX.md` - Navigation
- `docs/PROD_GATE_CLOSURE/QUICK_REFERENCE.md` - Cheat sheet

### Technical Guides (Pick One)
- `docs/PROD_GATE_CLOSURE/03_schema_gate_fix.md` - Blocker #1
- `docs/PROD_GATE_CLOSURE/04_e2e_debugging.md` - Blocker #2
- `docs/PROD_GATE_CLOSURE/05_coverage_strategy.md` - Blockers #5 #6
- `docs/PROD_GATE_CLOSURE/06_testing_procedures.md` - Testing
- `docs/PROD_GATE_CLOSURE/07_known_issues.md` - Troubleshooting
- `docs/PROD_GATE_CLOSURE/08_decision_tree.md` - Diagnosis

### Contracts (Reference)
- `docs/contracts/API_CONTRACT.md` - Payload shapes
- `docs/contracts/ROUTES.md` - Route structure (frozen)
- `docs/contracts/TERMINOLOGY.md` - User-facing terms (frozen)

---

## 23) North Star Reminder

**Your mission**: Close the 11 production gate blockers while maintaining:
- ✅ UI stability (no surprise changes)
- ✅ Contract correctness (payloads match specs)
- ✅ High coverage (95% backend, 90% frontend)
- ✅ Clear documentation (so next person can continue)

**Your guide**: `docs/PROD_GATE_CLOSURE/` (everything is here)

**Your outcome**: GO verdict on all 14 mandatory gates

---

**Start here**: `docs/PROD_GATE_CLOSURE/00_README.md`

**Quick ref**: `docs/PROD_GATE_CLOSURE/QUICK_REFERENCE.md`

**Stuck?**: `docs/PROD_GATE_CLOSURE/08_decision_tree.md`

