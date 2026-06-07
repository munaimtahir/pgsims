# PGSIMS Anti-Drift Guardrails for AI Agent Sessions

**Purpose**: Keep AI agents focused on specific session window and prevent scope creep during production gate closure sprint.

---

## 🎯 North Star

Every AI agent session is time-limited and scope-limited.

**Mission**: Fix one or more specific blockers from the production gate closure list.

**Not**: Broad refactoring, feature additions, architecture changes, or cleanup.

---

## Session Purpose Window

Every AI agent session MUST be initialized with:

```
SESSION WINDOW [Date/Time]
========================

PRIMARY PURPOSE
  Fix blocker #[N]: [Name]
  Success criteria from: docs/PROD_GATE_CLOSURE/01_blocker_analysis.md

IN-SCOPE (ALLOWED)
  - [ ] Changes to fix this blocker
  - [ ] Tests required for blocker
  - [ ] Documentation for blocker
  - [ ] Config changes required

OUT-OF-SCOPE (FORBIDDEN)
  - [ ] Refactoring unrelated code
  - [ ] New features beyond blocker
  - [ ] Architecture changes
  - [ ] Cleanup/dead code removal

SUCCESS CRITERIA
  - [ ] Specific test passes
  - [ ] Coverage metric improves
  - [ ] Gate validation passes
  - [ ] Blocker marked complete

FALLBACK PLAN
  If stuck after [time], then:
  1. Check docs/PROD_GATE_CLOSURE/08_decision_tree.md
  2. Document findings
  3. Ask for help; do not expand scope

GUARDRAILS ACTIVE
  ✅ G1-20 enforced
  ✅ Drift detection on
  ✅ Scope locked
  ✅ Focus validation every 30 min
```

---

## 20 Core Guardrails (G1-G20)

### A) SCOPE GUARDRAILS (Prevent Scope Creep)

#### Rule G1: No Refactoring Unless Required
- ❌ DO NOT refactor unrelated code to be "cleaner"
- ❌ DO NOT consolidate modules while fixing bugs
- ✅ DO refactor ONLY if required to fix blocker
- **Validation**: Commit message states "Required to fix blocker #X"
- **Evidence**: Refactoring change is in decision tree for this blocker

#### Rule G2: No New Features
- ❌ DO NOT add helper functions beyond blocker scope
- ❌ DO NOT enhance error handling not required
- ✅ DO add features ONLY if in blocker fix
- **Validation**: Feature is mentioned in blocker analysis
- **Evidence**: Feature referenced in 01_blocker_analysis.md section

#### Rule G3: No Architecture Changes
- ❌ DO NOT restructure directory layout
- ❌ DO NOT change dependency injection patterns
- ❌ DO NOT reorganize imports/modules
- ✅ DO structural changes ONLY if blocker requires
- **Validation**: Prior checkpoint shows no architecture drift
- **Evidence**: Change is minimal and targeted

#### Rule G4: No Configuration Tweaks
- ❌ DO NOT "optimize" settings.py
- ❌ DO NOT add environment variables "for convenience"
- ❌ DO NOT change build/test configurations
- ✅ DO config changes ONLY to fix blocker
- **Validation**: Config change referenced in technical guide
- **Evidence**: Change is necessary in decision tree

---

### B) FOCUS GUARDRAILS (Keep Eyes on Prize)

#### Rule G5: No Scope Expansion Mid-Task
- When stuck or hitting issues:
  1. ✅ Check `docs/PROD_GATE_CLOSURE/08_decision_tree.md`
  2. ✅ Review `docs/PROD_GATE_CLOSURE/07_known_issues.md`
  3. ✅ Follow diagnostic steps before scope expansion
  4. ❌ DO NOT pivot to adjacent problems
- **Validation**: Session log shows decision tree followed
- **Evidence**: Commit messages don't show abandoned approaches

#### Rule G6: No Adjacent Blockers Without Assignment
- ❌ DO NOT start fixing "related" blockers mid-session
- ❌ DO NOT "quickly fix" blocker #7 while assigned to #2
- ❌ DO NOT cherry-pick easy wins from other blockers
- ✅ DO one blocker at a time unless parallelized
- **Validation**: Commit targets single blocker
- **Evidence**: PR/session references single blocker in scope

#### Rule G7: No Cleanup Tasks
- ❌ DO NOT delete dead code "while we're here"
- ❌ DO NOT fix typos in unrelated files
- ❌ DO NOT remove commented code
- ✅ DO cleanup ONLY if in this blocker's scope
- **Validation**: Changes touch only files in blocker
- **Evidence**: All modified files are in decision tree

#### Rule G8: No Premature Optimization
- ❌ DO NOT profile code to find micro-optimizations
- ❌ DO NOT rewrite algorithms to be "faster"
- ❌ DO NOT cache results "for performance"
- ✅ DO optimize ONLY if blocker requires
- **Validation**: No performance changes not in guide
- **Evidence**: Optimization is mentioned in blocker fix strategy

---

### C) TESTING GUARDRAILS (No Fake Wins)

#### Rule G9: No Test Exclusions
- ❌ DO NOT skip tests to get green
- ❌ DO NOT mark tests with `@skip` or `@pytest.mark.skip`
- ❌ DO NOT exclude files from coverage measurement
- ❌ DO NOT disable tests in CI/CD config
- ✅ DO fix the code, not the tests
- **Validation**: `git log --all --grep="skip\|exclude\|ignore.*test"` is empty
- **Evidence**: All tests in scope pass, none skipped

#### Rule G10: No Trivial Tests
- ❌ DO NOT add tests that only check status code
- ❌ DO NOT add mock-heavy tests that test nothing real
- ❌ DO NOT assert on HTTP headers only
- ✅ DO add tests that validate behavior + side effects
- **Validation**: Test file has assertions on state changes
- **Evidence**: Test checks data, permissions, workflow state (not just 200 OK)

#### Rule G11: No Coverage Gaming
- ❌ DO NOT add tests just to inflate coverage %
- ❌ DO NOT mock critical logic to avoid complexity
- ❌ DO NOT add whitespace-only lines to hide gaps
- ✅ DO raise coverage by testing real flows
- **Validation**: Coverage gain traced to specific functional areas
- **Evidence**: Test file name matches logic being tested

#### Rule G12: No Silent Mocking
- ❌ DO NOT mock permission checks to test happy path only
- ❌ DO NOT mock state machines to avoid complexity
- ❌ DO NOT stub out business logic
- ✅ DO test both allowed and denied paths
- ✅ DO test valid and invalid state transitions
- **Validation**: Test file includes both allow and deny tests
- **Evidence**: Test mentions @permission_required, assert_unauthorized, etc.

---

### D) CONTRACT GUARDRAILS (No Silent Changes)

#### Rule G13: No Payload Changes Without Contract Update
- ❌ DO NOT add field to API response without `API_CONTRACT.md` update
- ❌ DO NOT change field type without frontend test
- ❌ DO NOT rename fields in responses
- ✅ DO change payload AND contract AND tests together
- **Validation**: All three files in same commit
- **Evidence**: Commit touches API code, contract doc, and test file

#### Rule G14: No Route Changes Without Frozen Rule Check
- ❌ DO NOT change route structure (frozen per contract)
- ❌ DO NOT change nav labels
- ❌ DO NOT modify URL patterns
- ✅ DO change ONLY with explicit exception documented
- **Validation**: `ROUTES.md` has version bump if changed
- **Evidence**: CHANGELOG.md mentions exception + approval
- **EXPLICIT OVERRIDE/UNLOCK**: The Frozen UX Rule is unlocked for debugging UI/UX, modifying/adding/updating routes, views, components, navigation labels, and terminology as explicitly directed by the project lead.

#### Rule G15: No Migration Without Data Validation
- ❌ DO NOT add migration without forward + reverse testing
- ❌ DO NOT change model without default value
- ❌ DO NOT add NOT NULL constraint to existing data
- ✅ DO migration + reverse + data integrity check
- **Validation**: Migration tested locally; no null violations
- **Evidence**: Commit message shows migration tested forward/back

#### Rule G16: No Breaking Changes Without Changelog
- ❌ DO NOT merge breaking change without `CHANGELOG.md` entry
- ❌ DO NOT silently deprecate APIs
- ✅ DO update `CHANGELOG.md` with version, date, notes
- **Validation**: `CHANGELOG.md` has entry dated today
- **Evidence**: Breaking change has explicit section in changelog

---

### E) EVIDENCE GUARDRAILS (No Unjustified Claims)

#### Rule G17: No Claims Without Proof
- ❌ DO NOT say "tests pass" without running full suite
- ❌ DO NOT claim "no regressions" without before/after
- ❌ DO NOT assert without citing specific outputs
- ✅ DO cite specific test names, line numbers, artifacts
- **Validation**: Commit message includes grep output or test list
- **Evidence**: Commit shows actual pytest output lines

#### Rule G18: No Estimates Presented as Facts
- ❌ DO NOT say "production-ready" without all gates passing
- ❌ DO NOT claim "blocker fixed" if gates fail
- ❌ DO NOT hide failing tests with pass/skip
- ✅ DO report exact status: "X tests pass; Y thresholds met; Z gaps remain"
- **Validation**: Final summary lists status for each threshold
- **Evidence**: Verdict matches actual gate results

#### Rule G19: No Incomplete Runbooks
- ❌ DO NOT document "run command X" without showing output
- ❌ DO NOT leave "TODO: fix later" in code
- ❌ DO NOT have unvalidated procedures
- ✅ DO provide complete reproduction steps + actual output
- **Validation**: Runbook in docs shows real commands + real output
- **Evidence**: Runbook is copy-paste ready, not pseudocode

#### Rule G20: No Handoff Without Runbook
- ❌ DO NOT leave session without "how to continue" guide
- ❌ DO NOT end without blocker status update
- ✅ DO create checkpoint with clear next steps
- **Validation**: Checkpoint directory has `NEXT_STEPS.md`
- **Evidence**: Next developer can read checkpoint and continue

---

## Drift Detection Checklist

**Before EVERY commit, validate:**

### 1. Scope Check
```
- [ ] Does this commit fix exactly ONE blocker?
- [ ] Is this blocker in 01_blocker_analysis.md?
- [ ] Does commit message reference blocker #N?
- [ ] Are all changes for this blocker only?
```

### 2. Focus Check
```
- [ ] Did I follow decision tree steps?
- [ ] Did I skip any diagnostic steps? (If yes: DO NOT COMMIT)
- [ ] Did I expand scope mid-task? (If yes: DO NOT COMMIT)
- [ ] Is this only fixing the assigned blocker?
```

### 3. Testing Check
```
- [ ] Did I run FULL gate, not partial?
- [ ] Are all relevant tests passing?
- [ ] Did coverage go up or stay same (not down)?
- [ ] Did I exclude any tests? (If yes: DO NOT COMMIT)
```

### 4. Contract Check
```
- [ ] Did I update contracts if payload changed?
- [ ] Did I update frozen docs if UX changed?
- [ ] Did I add CHANGELOG entry if breaking?
- [ ] Are all contract changes in this commit?
```

### 5. Evidence Check
```
- [ ] Can I cite specific test names/line numbers?
- [ ] Is claim backed by actual test output?
- [ ] Can someone reproduce my work from my docs?
- [ ] Does commit message show proof?
```

### 6. Handoff Check
```
- [ ] Can next person pick up from here?
- [ ] Did I document what's next?
- [ ] Did I update checkpoint/plan?
- [ ] Is blocker status clear (COMPLETE / PARTIAL / BLOCKED)?
```

**If ANY answer is NO → DO NOT COMMIT → Fix it → Try again**

---

## Guardrail Enforcement Process

### Pre-Session (Before Starting)
1. ✅ Read `AGENTS.md` or `GEMINI.md` (sections 0-23)
2. ✅ Read `docs/PROD_GATE_CLOSURE/00_README.md`
3. ✅ Read relevant technical guide for your blocker
4. ✅ WRITE out session window to session plan (copy template above)
5. ✅ Confirm "GUARDRAILS ACTIVE" in plan
6. ✅ Get assignment from project lead

### During Session (Every 30 minutes)
- [ ] Check drift detection checklist (Section above)
- [ ] Review session plan (haven't drifted from PURPOSE?)
- [ ] Ask: "Am I still fixing blocker #N?"
- [ ] If NO: Stop, refocus, read decision tree
- [ ] If stuck >15 min: Check known_issues.md + decision_tree.md

### Before Every Commit
- [ ] Run drift detection checklist (all 6 sections)
- [ ] Validate against G1-G20
- [ ] Show actual test output in commit message
- [ ] Reference blocker number in commit

### After Every Commit
- [ ] Wait for CI to validate
- [ ] If RED: Investigate, fix, commit again
- [ ] If GREEN: Continue or move to next blocker

### Post-Session (At End)
- [ ] Run full gate from clean baseline
- [ ] Create checkpoint with results
- [ ] Create `NEXT_STEPS.md` in checkpoint
- [ ] Update plan.md with blocker status
- [ ] Explicit verdict: COMPLETE / PARTIAL / BLOCKED

---

## Drift Detection Alerts (Automatic Red Flags)

If agent exhibits ANY of these:
- ❌ Commits to 3+ files unrelated to assigned blocker → **DRIFT ALERT**
- ❌ Claim "fixed" but gate still shows RED → **DRIFT ALERT**
- ❌ Starts working on new blocker mid-session → **DRIFT ALERT**
- ❌ Skips decision tree diagnostic steps → **DRIFT ALERT**
- ❌ Excludes tests or files from validation → **DRIFT ALERT**
- ❌ Changes route/nav/terminology without frozen rule exception → **DRIFT ALERT**
- ❌ Adds configuration "for convenience" not in guide → **DRIFT ALERT**
- ❌ Claims coverage fixed but percentage same/lower → **DRIFT ALERT**

**Action**: Stop immediately, read guardrails section above, refocus, ask for help.

---

## Code Reviewer Anti-Drift Checklist

When reviewing PRs from AI agent sessions, check:

```
SCOPE & FOCUS
- [ ] Commit message references single blocker number
- [ ] All changes related to that blocker
- [ ] No refactoring of unrelated code
- [ ] No new features beyond blocker scope
- [ ] No adjacent blockers touched

TESTING
- [ ] Tests actually test behavior (not just status)
- [ ] No @skip or exclusions on tests
- [ ] No coverage gaming or trivial tests
- [ ] Coverage maintained or improved
- [ ] Full gate shown to pass in PR

CONTRACTS
- [ ] API contracts updated if payload changed
- [ ] Frozen routes/terms not changed (or exception noted)
- [ ] CHANGELOG updated if breaking
- [ ] No silent breaking changes

EVIDENCE
- [ ] Commit shows actual test output
- [ ] Claims backed by proof (not estimates)
- [ ] Runbook is complete, not pseudocode
- [ ] Checkpoint created with NEXT_STEPS.md

HANDOFF
- [ ] Next developer can pick up from checkpoint
- [ ] Blocker status is clear (COMPLETE/PARTIAL/BLOCKED)
- [ ] No "TODO: fix later" left in code
```

**If ANY fail → Request changes → Do not merge until all pass**

---

## Session Window Template (Copy & Paste)

```markdown
# Session Window: [Date/Time]

## Primary Purpose
Fix blocker #[N]: [Name]
Reference: docs/PROD_GATE_CLOSURE/01_blocker_analysis.md#blocker-[N]
Success criteria: [From blocker analysis]

## In-Scope (Allowed)
- [ ] [File/change #1]
- [ ] [File/change #2]
- [ ] [Test addition]
- [ ] [Documentation update]

## Out-of-Scope (Forbidden)
- [ ] Refactoring unrelated code
- [ ] Adding features beyond blocker
- [ ] Changing route structure
- [ ] Changing nav labels/terminology
- [ ] Other blockers/cleanup

## Success Criteria
- [ ] Test: [Specific test name/number]
- [ ] Coverage: [Target %]
- [ ] Gate: [Which gate passes]
- [ ] Blocker: [Marked COMPLETE]

## Fallback Plan
If stuck after 2 hours:
1. Check docs/PROD_GATE_CLOSURE/08_decision_tree.md
2. Check docs/PROD_GATE_CLOSURE/07_known_issues.md
3. Document findings
4. Ask lead for guidance; do NOT expand scope

## Guardrails
- ✅ G1-G20 enforced
- ✅ Drift detection on
- ✅ Scope locked
- ✅ Focus validated every 30 min

## Notes
[Session notes, decisions, blockers encountered]
```

---

## References

- **Blocker Analysis**: `docs/PROD_GATE_CLOSURE/01_blocker_analysis.md`
- **Decision Tree**: `docs/PROD_GATE_CLOSURE/08_decision_tree.md`
- **Known Issues**: `docs/PROD_GATE_CLOSURE/07_known_issues.md`
- **Testing Guide**: `docs/PROD_GATE_CLOSURE/06_testing_procedures.md`
- **Agent Governance**: `AGENTS.md` section 1-11
- **Gemini Rules**: `GEMINI.md` sections 0-23
- **Contracts**: `docs/contracts/API_CONTRACT.md`, `ROUTES.md`, `TERMINOLOGY.md`

---

## Quick Reference: When You're Stuck

1. **Feeling lost?** → Read `docs/PROD_GATE_CLOSURE/00_README.md` (15 min)
2. **Don't know what to fix?** → Read `01_blocker_analysis.md` (20 min)
3. **How do I fix it?** → Read relevant technical guide (1-5 hours)
4. **Test failing mysteriously?** → Check `08_decision_tree.md` + `07_known_issues.md`
5. **Want to expand scope?** → STOP, read G5-G6, follow decision tree instead
6. **Ready to commit?** → Run drift detection checklist (section above)
7. **Done with blocker?** → Create checkpoint, update plan, mark COMPLETE

---

## Success = All Guardrails Active + Blocker Fixed

✅ Session is successful when:
- All G1-G20 followed
- Drift detection checklist passed (all 6 sections)
- Blocker marked COMPLETE in plan
- Full gate passing
- Checkpoint created with NEXT_STEPS
- Handed off to next session/developer

❌ Session fails if:
- Any guardrail violated (even one)
- Drift detection finds red flag
- Gate still failing
- Blocker partially fixed (incomplete)
- No checkpoint/next steps documented

**When in doubt: Refer to guardrails, not your judgment.**

