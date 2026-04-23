# PGSIMS Agent Governance (AGENTS.md)

This repository is operated via CLI AI agents. To prevent drift, every agent run MUST follow these rules.

## 0) North Star
PGSIMS is the operational system for UTRMC monitoring of postgraduate training. Adoption depends on UI stability and contract correctness.

## 1) Operating Mode
- Default: single-agent execution with internal delegation allowed.
- You may group tasks and execute in any order, but MUST respect phase gates and contract locks below.
- Every claim must be backed by evidence (file paths, grep output, tests).

## 2) Contract-First (Non-Negotiable)
- Backend ↔ Frontend integration MUST be driven by docs under `docs/contracts/`.
- If code changes require contract changes, update contracts in the same run.
- No “quick fixes” that silently change payload shapes.

## 3) Frozen UX Rule (Adoption-Safety)
- Do NOT change route structure, navigation labels, or terminology once pilot begins.
- Allowed after freeze: bug fixes, performance, helper text, small visual cues.
- Any UX-affecting change requires explicit approval and a version bump note in:
  - `docs/contracts/ROUTES.md`
  - `docs/contracts/TERMINOLOGY.md`

## 4) Canonical Data Model Rule (Critical)
- There is exactly ONE canonical Department entity for the university.
- There is exactly ONE canonical Hospital entity for the university.
- A hospital hosts a subset of departments via a matrix table.
- Do NOT create or reintroduce a second Department model (e.g., “RotationDepartment”, “AcademicDepartment”).

## 5) Audit Integrity
- All state transitions must be auditable.
- Do not remove `django-simple-history`.
- Never silently mutate approved/verified records.

## 6) Notifications
- Notifications MUST use canonical schema: `recipient`, `verb`, `body`, `metadata`.
- Do not use legacy keys (`user`, `message`, `type`, `related_object_id`).
- Prefer a single NotificationService helper and add a drift test.

## 7) Phase Gates (Must Pass)
Each phase has mandatory gates in `docs/contracts/TRUTH_TESTS.md`.
A phase is not “done” until gates pass.

## 8) Definition of Done
A task is complete only when:
- Relevant tests pass
- Contracts updated (if applicable)
- No drift introduced (scan forbidden patterns)
- Work documented under `docs/_audit/`

## 9) Forbidden Patterns
- Duplicate Department models
- Breaking API payloads without updating contracts and frontend SDK
- Direct DB edits for state changes

## 10) MCP Agent Reproducibility Policy
- MCP server configs required for agent workflows MUST be committed (for example: `.mcp.json`, launcher scripts).
- MCP dependency manifests and lockfiles MUST be committed for reproducibility (for example: `package.json` + `package-lock.json` in tooling folders).
- Do NOT rely on floating versions (for example: `@latest`) in committed launcher scripts.
- Runtime artifacts/output folders from MCP tools MUST remain untracked.

## 11) Production Gate Closure Sprint (CRITICAL)

Before executing ANY task that affects the gate or coverage:

**MANDATORY**: Read `docs/PROD_GATE_CLOSURE/` documentation package
- Start with: `docs/PROD_GATE_CLOSURE/00_README.md`
- Quick reference: `docs/PROD_GATE_CLOSURE/QUICK_REFERENCE.md`
- Full index: `docs/PROD_GATE_CLOSURE/INDEX.md`

This package documents:
- All 11 remaining production gate blockers
- Root causes and fix strategies
- Step-by-step procedures for each blocker
- Testing and validation procedures
- Troubleshooting guides

**Current Status**: NO-GO with 11 identified blockers (see docs/PROD_GATE_CLOSURE/01_blocker_analysis.md)

**Mandatory Gates** (ALL must pass for GO):
- Strict schema gate
- E2E fully passes (7/7 tests)
- Backend coverage ≥95% / ≥90% branch
- Frontend coverage ≥90% / ≥85% branch
- Active routes/APIs/CTAs/roles/workflows 100%

**Do NOT**:
- Skip reading the documentation package
- Break the existing wins (see docs/PROD_GATE_CLOSURE/SESSION_3_FINDINGS.md)
- Modify tests without updating coverage targets
- Change payloads without updating contracts

**Reference**: See `docs/PROD_GATE_CLOSURE/` for complete context before starting work.

## 12) Anti-Drift Guardrails (MANDATORY)

Every agent session must stay focused on its specific window and prevent scope creep.

**MANDATORY**: Read `docs/ANTI_DRIFT_GUARDRAILS.md` BEFORE every session

### Core Principle: One Blocker Per Session
- ✅ DO fix exactly one assigned blocker per session
- ❌ DO NOT expand scope mid-session
- ❌ DO NOT "quickly fix" adjacent blockers
- ❌ DO NOT refactor unrelated code

### 20 Core Guardrails (G1-G20)

**G1-G4: Scope Guardrails**
- G1: No refactoring unless required (for blocker)
- G2: No new features beyond blocker scope
- G3: No architecture changes
- G4: No configuration tweaks

**G5-G8: Focus Guardrails**
- G5: No scope expansion mid-task
- G6: No adjacent blockers without assignment
- G7: No cleanup tasks
- G8: No premature optimization

**G9-G12: Testing Guardrails**
- G9: No test exclusions
- G10: No trivial tests (only status codes)
- G11: No coverage gaming
- G12: No silent mocking of critical logic

**G13-G16: Contract Guardrails**
- G13: No payload changes without contract update
- G14: No route/nav changes without frozen rule check
- G15: No migration without data validation
- G16: No breaking changes without changelog

**G17-G20: Evidence Guardrails**
- G17: No claims without proof (cite tests, outputs)
- G18: No estimates presented as facts
- G19: No incomplete runbooks
- G20: No handoff without next-steps guide

### Session Window Template
Every session MUST start with:
```
PRIMARY PURPOSE: Fix blocker #[N]
IN-SCOPE: [List of allowed changes]
OUT-OF-SCOPE: [List of forbidden work]
SUCCESS CRITERIA: [How we know it's done]
FALLBACK PLAN: [If stuck >2 hours]
GUARDRAILS ACTIVE: G1-20 enforced
```

### Drift Detection Checklist (Before Every Commit)
1. **Scope**: Does commit fix exactly ONE blocker?
2. **Focus**: Did I follow decision tree and skip no steps?
3. **Testing**: Did I run FULL gate (not partial)?
4. **Contract**: Did I update contracts if payload changed?
5. **Evidence**: Can I cite specific test names/outputs?
6. **Handoff**: Can next person pick up from here?

**If ANY answer is NO → DO NOT COMMIT**

### Drift Detection Alerts (Stop Immediately)
❌ Commits to 3+ unrelated files → DRIFT ALERT
❌ Claim "fixed" but gate still RED → DRIFT ALERT
❌ Starting new blocker mid-session → DRIFT ALERT
❌ Skipping decision tree steps → DRIFT ALERT
❌ Excluding tests from validation → DRIFT ALERT

**Action**: Stop, read guardrails, refocus, ask for help.

### Code Reviewer Anti-Drift Checklist
- [ ] Commit references single blocker
- [ ] All changes related to that blocker
- [ ] No refactoring of unrelated code
- [ ] Tests test behavior (not just status)
- [ ] Coverage maintained/improved
- [ ] Contracts updated if payload changed
- [ ] Full gate shown to pass
- [ ] Checkpoint with NEXT_STEPS created

**If ANY fail → Request changes; do not merge**

### References
- Full guardrails: `docs/ANTI_DRIFT_GUARDRAILS.md`
- Blocker analysis: `docs/PROD_GATE_CLOSURE/01_blocker_analysis.md`
- Decision tree: `docs/PROD_GATE_CLOSURE/08_decision_tree.md`
- Known issues: `docs/PROD_GATE_CLOSURE/07_known_issues.md`
