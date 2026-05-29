# AI Agent Entry Points

**For all AI agents (Claude, Gemini, or any LLM)** - Start here before ANY work session.

---

## 🎯 Quick Navigation (Pick Your Role)

### I'm an AI Agent Starting a New Session
1. **Read First**: `AGENTS.md` or `GEMINI.md` (sections 0-24) - 20 minutes
2. **Read Second**: `docs/ANTI_DRIFT_GUARDRAILS.md` - 15 minutes
3. **Read Third**: Relevant blocker guide from `docs/PROD_GATE_CLOSURE/`
4. **Do This**: Fill out session window template
5. **Now Start**: Fix your assigned blocker

**Total prep time**: 45-60 minutes | **Saves**: 10+ hours of false starts

### I'm Assigned a Specific Blocker
1. **Quick ref**: `docs/PROD_GATE_CLOSURE/QUICK_REFERENCE.md` (5 min)
2. **Analysis**: `docs/PROD_GATE_CLOSURE/01_blocker_analysis.md` (20 min)
3. **Guide**: Pick your blocker's technical guide:
   - Blocker #1 (Schema) → `03_schema_gate_fix.md`
   - Blocker #2 (E2E) → `04_e2e_debugging.md`
   - Blockers #5 #6 (Coverage) → `05_coverage_strategy.md`
4. **Guardrails**: `docs/ANTI_DRIFT_GUARDRAILS.md` sections: Session Window, Drift Detection
5. **Execute**: Follow guide step-by-step

### I'm Stuck on a Problem
1. **Decision Tree**: `docs/PROD_GATE_CLOSURE/08_decision_tree.md` (10-15 min)
2. **Known Issues**: `docs/PROD_GATE_CLOSURE/07_known_issues.md` (5-10 min)
3. **Specific Guide**: Relevant technical guide for your blocker
4. **Guardrails Check**: Did you skip any decision tree steps? (G5 violation)
5. **Ask for Help**: If >30 min stuck, document findings and ask

### I'm About to Commit Code
1. **Checklist**: Run `docs/ANTI_DRIFT_GUARDRAILS.md` drift detection checklist (5 min)
   - Scope check: One blocker?
   - Focus check: Followed decision tree?
   - Testing check: Full gate passed?
   - Contract check: Updated if needed?
   - Evidence check: Backed by proof?
   - Handoff check: Next person can continue?
2. **Validate**: Does this commit pass all 20 guardrails (G1-G20)?
3. **Message**: Include blocker reference + test output
4. **Result**: If ANY checklist item is NO → DO NOT COMMIT

### I'm Finishing a Session
1. **Gate**: Run full production gate from clean baseline
2. **Checkpoint**: Create checkpoint with session findings
3. **Next Steps**: Create `NEXT_STEPS.md` for next developer
4. **Status**: Update plan.md with blocker status (COMPLETE/PARTIAL/BLOCKED)
5. **Handoff**: Ready for next session/developer

---

## 📚 Complete File Reference

### Governance Files (Read First)
- **`AGENTS.md`** - Agent governance rules (sections 0-11: core rules, sections 12: guardrails)
- **`GEMINI.md`** - Gemini AI agent guidelines (sections 0-24, including section 24: guardrails)
- **`docs/ANTI_DRIFT_GUARDRAILS.md`** - Session focus enforcement (20 guardrails, drift detection, templates)

### Production Gate Documentation (Read Second)
- **`docs/PROD_GATE_CLOSURE/00_README.md`** - Master overview + quick-start scenarios
- **`docs/PROD_GATE_CLOSURE/01_blocker_analysis.md`** - All 11 blockers analyzed
- **`docs/PROD_GATE_CLOSURE/02_phase_guide.md`** - Phased execution plan
- **`docs/PROD_GATE_CLOSURE/03_schema_gate_fix.md`** - Blocker #1 technical guide
- **`docs/PROD_GATE_CLOSURE/04_e2e_debugging.md`** - Blocker #2 technical guide
- **`docs/PROD_GATE_CLOSURE/05_coverage_strategy.md`** - Blockers #5 #6 technical guide
- **`docs/PROD_GATE_CLOSURE/06_testing_procedures.md`** - How to run tests/gates
- **`docs/PROD_GATE_CLOSURE/07_known_issues.md`** - Common problems + solutions
- **`docs/PROD_GATE_CLOSURE/08_decision_tree.md`** - Troubleshooting diagnosis
- **`docs/PROD_GATE_CLOSURE/INDEX.md`** - Navigation guide
- **`docs/PROD_GATE_CLOSURE/QUICK_REFERENCE.md`** - One-page cheat sheet
- **`docs/PROD_GATE_CLOSURE/SESSION_3_FINDINGS.md`** - What was already fixed

### Project Governance
- **`README.md`** - Main project README (critical section at top)
- **`docs/README.md`** - Documentation index (critical section at top)
- **`HANDOFF_PROD_GATE_20260422.md`** - Production gate status summary

### Contracts (Authoritative)
- **`docs/contracts/API_CONTRACT.md`** - Backend API payloads
- **`docs/contracts/ROUTES.md`** - Frontend route structure (frozen)
- **`docs/contracts/TERMINOLOGY.md`** - User-facing terms (frozen)
- **`docs/contracts/RBAC_MATRIX.md`** - Role-based access control
- **`docs/contracts/DATA_MODEL.md`** - Canonical entity definitions

---

## 🚀 Session Setup Checklist

Before starting ANY work session:

```
Pre-Session Setup
================

READING (60 minutes)
- [ ] AGENTS.md or GEMINI.md (20 min)
- [ ] docs/ANTI_DRIFT_GUARDRAILS.md (15 min)
- [ ] docs/PROD_GATE_CLOSURE/00_README.md (10 min)
- [ ] Relevant blocker technical guide (15 min)

SESSION WINDOW SETUP (10 minutes)
- [ ] Copy session window template from ANTI_DRIFT_GUARDRAILS.md
- [ ] Fill out PRIMARY PURPOSE (what blocker am I fixing?)
- [ ] Fill out IN-SCOPE (what am I allowed to change?)
- [ ] Fill out OUT-OF-SCOPE (what am I forbidden from touching?)
- [ ] Fill out SUCCESS CRITERIA (how do I know it's done?)
- [ ] Confirm GUARDRAILS ACTIVE
- [ ] Save to session plan file

ENVIRONMENT CHECK (10 minutes)
- [ ] Backend environment set up
- [ ] Frontend environment set up
- [ ] Docker running (if needed)
- [ ] Can run tests: backend + frontend + E2E
- [ ] Can run full gate validation

READY TO START
- [ ] All 60+ minutes of reading done
- [ ] Session window template filled out
- [ ] Guardrails confirmed active
- [ ] Environment working
- [ ] Assigned blocker clearly understood
- [ ] Decision tree bookmarked for reference
- [ ] Known issues bookmarked for reference

NOW: Start with your blocker's technical guide
```

---

## 🎯 Guardrails at a Glance

### The 20 Core Guardrails (G1-G20)

| G# | Category | Rule | Validation |
|----|----------|------|-----------|
| G1 | Scope | No refactoring unless required for blocker | Commit message states "required for blocker #X" |
| G2 | Scope | No new features beyond scope | Feature in blocker analysis |
| G3 | Scope | No architecture changes | Prior checkpoint shows no drift |
| G4 | Scope | No config tweaks | Change in technical guide |
| G5 | Focus | No scope expansion when stuck | Decision tree followed |
| G6 | Focus | No adjacent blockers | Commit targets single blocker |
| G7 | Focus | No cleanup tasks | Changes in blocker scope only |
| G8 | Focus | No premature optimization | No performance claims without blocker ref |
| G9 | Testing | No test exclusions | `git log --grep="skip\|exclude"` empty |
| G10 | Testing | No trivial tests | Test checks state (not just 200 OK) |
| G11 | Testing | No coverage gaming | Coverage gain traced to functional areas |
| G12 | Testing | No silent mocking | Test includes both allow and deny paths |
| G13 | Contract | No payload changes without contract | All three files in same commit |
| G14 | Contract | No route changes without check | ROUTES.md has version bump |
| G15 | Contract | No migration without validation | Forward/reverse tested |
| G16 | Contract | No breaking changes without changelog | CHANGELOG.md has entry |
| G17 | Evidence | No claims without proof | Commit cites tests/outputs |
| G18 | Evidence | No estimates as facts | Final status exact (X pass, Y fail, Z gaps) |
| G19 | Evidence | No incomplete runbooks | Runbook shows real commands + output |
| G20 | Evidence | No handoff without guide | Checkpoint has NEXT_STEPS.md |

### Drift Detection Checklist (Before Every Commit)

```
STOP and answer all 6:

1. SCOPE: Does this fix exactly ONE blocker?
   - YES → Continue
   - NO → DO NOT COMMIT → Fix it

2. FOCUS: Did I follow decision tree? Skip any steps?
   - NO SKIPS → Continue
   - YES SKIPS → DO NOT COMMIT → Follow tree

3. TESTING: Did I run FULL gate? Coverage up/same?
   - YES/YES → Continue
   - NO or DOWN → DO NOT COMMIT → Run gate

4. CONTRACT: Updated contracts if payload changed?
   - YES or N/A → Continue
   - NO → DO NOT COMMIT → Update contracts

5. EVIDENCE: Can I cite test names/outputs?
   - YES → Continue
   - NO → DO NOT COMMIT → Add evidence

6. HANDOFF: Can next person pick up here?
   - YES → Continue
   - NO → DO NOT COMMIT → Document next steps

All YES? → COMMIT
Any NO? → DO NOT COMMIT
```

### Drift Detection Alerts (Stop Immediately)

- ❌ 3+ commits to unrelated files → DRIFT ALERT
- ❌ Claim "fixed" but gate RED → DRIFT ALERT
- ❌ Starting new blocker mid-session → DRIFT ALERT
- ❌ Skipping decision tree → DRIFT ALERT
- ❌ Excluding tests → DRIFT ALERT

**Action**: Stop, read guardrails, refocus, ask for help.

---

## 📊 Current Status (As of Session 3)

| Metric | Status | Reference |
|--------|--------|-----------|
| Verdict | NO-GO | docs/PROD_GATE_CLOSURE/01_blocker_analysis.md |
| Blockers | 11 identified | docs/PROD_GATE_CLOSURE/01_blocker_analysis.md |
| Documentation | 150KB, 12 files | docs/PROD_GATE_CLOSURE/ |
| Backend tests | 222 passing | docs/PROD_GATE_CLOSURE/SESSION_3_FINDINGS.md |
| Frontend lint/type | Passing | docs/PROD_GATE_CLOSURE/SESSION_3_FINDINGS.md |
| E2E tests | 4/7 passing | docs/PROD_GATE_CLOSURE/SESSION_3_FINDINGS.md |
| Schema gate | 315 errors (65 APIViews) | docs/PROD_GATE_CLOSURE/03_schema_gate_fix.md |
| Backend coverage | 54% / 28% (need 95/90) | docs/PROD_GATE_CLOSURE/SESSION_3_FINDINGS.md |
| Frontend coverage | 8% / 7% (need 90/85) | docs/PROD_GATE_CLOSURE/SESSION_3_FINDINGS.md |

---

## ❓ FAQ

**Q: Where do I start if I'm new?**
A: Read in this order:
1. AGENTS.md or GEMINI.md (20 min)
2. docs/ANTI_DRIFT_GUARDRAILS.md (15 min)
3. docs/PROD_GATE_CLOSURE/00_README.md (10 min)
4. Your assigned blocker's technical guide

**Q: What if I get stuck?**
A: Use decision tree + known issues in PROD_GATE_CLOSURE/, follow the steps. If >30 min stuck, document and ask for help.

**Q: Can I fix multiple blockers in one session?**
A: No. One blocker per session. Guardrail G6.

**Q: Can I refactor unrelated code?**
A: Only if required to fix your assigned blocker. Guardrail G1.

**Q: Why all these guardrails?**
A: Previous sessions showed scope creep and incomplete validation. These prevent false starts and wasted time.

**Q: What's the difference between AGENTS.md and GEMINI.md?**
A: Same core governance. GEMINI.md is optimized for Gemini AI agent; AGENTS.md for any CLI agent.

**Q: How do I know my session was successful?**
A: All checks in drift detection checklist pass, blocker marked COMPLETE, full gate passes, checkpoint created.

---

## 🔗 Quick Links

| Need | Link | Time |
|------|------|------|
| Orientation | This file | 10 min |
| Governance | AGENTS.md or GEMINI.md | 20 min |
| Guardrails | docs/ANTI_DRIFT_GUARDRAILS.md | 15 min |
| Overview | docs/PROD_GATE_CLOSURE/00_README.md | 10 min |
| Blockers | docs/PROD_GATE_CLOSURE/01_blocker_analysis.md | 20 min |
| Stuck | docs/PROD_GATE_CLOSURE/08_decision_tree.md | 10 min |
| Fix guide | docs/PROD_GATE_CLOSURE/0X_[blocker].md | varies |
| Status | docs/PROD_GATE_CLOSURE/SESSION_3_FINDINGS.md | 5 min |
| Reference | docs/PROD_GATE_CLOSURE/QUICK_REFERENCE.md | 5 min |

---

## ✅ Pre-Session Validation

Before you consider yourself "ready to start," answer these:

- [ ] Have you read AGENTS.md / GEMINI.md sections 0-24? (Not just skimmed)
- [ ] Have you read docs/ANTI_DRIFT_GUARDRAILS.md thoroughly?
- [ ] Do you understand all 20 guardrails (G1-G20)?
- [ ] Can you explain your assigned blocker in one sentence?
- [ ] Do you know the success criteria for your blocker?
- [ ] Have you filled out the session window template?
- [ ] Can you navigate to decision_tree.md without help?
- [ ] Can you run the full production gate command from memory?
- [ ] Do you know what the drift detection checklist is?
- [ ] Are you ready to refer to guardrails if you get stuck?

If ANY answer is NO → Go back and re-read the relevant section.

**When ALL are YES → You're ready to start.**

---

**Remember**: Quality > Speed. Take 1 hour to prepare. Save 10 hours of rework.

**Start here**: Pick your section from "Quick Navigation" above.
