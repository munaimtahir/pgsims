# Anti-Drift Guardrails - Quick Start Guide

**For AI Agents Starting a New Session**

---

## 🚀 60-Second Orientation

You are about to work on **PGSIMS production gate closure sprint**.

**Your mission**: Fix ONE assigned blocker while maintaining focus and quality.

**To prevent drift**, follow these 4 steps:

---

## Step 1: Read the Governance (20 min)

Read **IN THIS ORDER**:

1. `AGENTS.md` or `GEMINI.md` → Sections 0-24 (20 min)
   - Why: Understand PGSIMS governance and guardrails
   - Focus: Sections 11-12 on production gate + guardrails

---

## Step 2: Read the Guardrails (15 min)

Read **`docs/ANTI_DRIFT_GUARDRAILS.md`** (15 min)

Key sections:
- **Session Purpose Window** (template)
- **20 Core Guardrails** (G1-G20)
- **Drift Detection Checklist** (pre-commit validation)
- **Automatic Drift Alerts** (what stops you)

---

## Step 3: Read Your Task (10 min)

Read **`docs/PROD_GATE_CLOSURE/00_README.md`** (10 min)

Then read **your assigned blocker's technical guide**:
- Blocker #1? → `03_schema_gate_fix.md`
- Blocker #2? → `04_e2e_debugging.md`
- Blockers #5-6? → `05_coverage_strategy.md`
- Other? → `01_blocker_analysis.md` (find yours)

---

## Step 4: Set Up Your Session (10 min)

Before writing ANY code:

1. **Copy** the session window template from `docs/ANTI_DRIFT_GUARDRAILS.md`
2. **Fill out**:
   - PRIMARY PURPOSE: What blocker am I fixing?
   - IN-SCOPE: What am I allowed to change?
   - OUT-OF-SCOPE: What am I forbidden from touching?
   - SUCCESS CRITERIA: How do I know it's done?
3. **Confirm**: GUARDRAILS ACTIVE ✅
4. **Save** to your session plan file

**Total prep time**: ~60 minutes (saves 10+ hours of rework)

---

## 🎯 The 5 Rules (Shortened)

### Rule 1: One Blocker Per Session
❌ Do NOT start fixing another blocker mid-session
✅ Finish YOUR assigned blocker first

### Rule 2: Full Validation Always
❌ Do NOT run partial gates to claim "it works"
✅ Always run full gate before committing

### Rule 3: Drift Detection Before Commit
❌ Do NOT commit without passing all 6 checks
✅ Run drift detection checklist EVERY TIME

### Rule 4: Update Contracts If Needed
❌ Do NOT change APIs without updating API_CONTRACT.md
✅ Change payload AND contract AND tests together

### Rule 5: Document for Handoff
❌ Do NOT leave without NEXT_STEPS.md
✅ Create checkpoint so next person continues

---

## ⚠️ Drift Detection Checklist (Before Every Commit)

**STOP and answer all 6 questions:**

```
1. SCOPE:     Does this fix exactly ONE blocker?
2. FOCUS:     Did I follow decision tree? Skip any steps?
3. TESTING:   Run FULL gate? Coverage up or same (not down)?
4. CONTRACT:  Updated contracts if payload changed?
5. EVIDENCE:  Can I cite specific test names/outputs?
6. HANDOFF:   Can next person pick up from here?
```

**If ANY answer is NO → DO NOT COMMIT**

Go back, fix the issue, try again.

---

## 🚨 Drift Alerts (Stop Immediately)

These are automatic RED FLAGS:

- ❌ You committed to 3+ unrelated files
- ❌ You claim "fixed" but gate is RED
- ❌ You started another blocker mid-session
- ❌ You skipped decision tree steps
- ❌ You excluded tests from validation

**If ANY of these happen → STOP immediately**
1. Read guardrails again
2. Refocus on YOUR blocker
3. Ask for help

---

## 📋 Before You Start Each Day

1. Fill out session window (start of day)
2. Confirm guardrails ACTIVE
3. Review last checkpoint (if continuing)
4. Check decision tree bookmark
5. Check known issues bookmark

---

## 🔄 During Your Session

Every 30 minutes:
- [ ] Check drift detection checklist
- [ ] Review session plan (still on track?)
- [ ] If stuck >15 min: Use decision tree

Before EVERY commit:
- [ ] Run drift detection checklist (all 6)
- [ ] Validate G1-G20 guardrails
- [ ] Show actual test output in commit

After session:
- [ ] Run full gate from clean baseline
- [ ] Create checkpoint with results
- [ ] Create NEXT_STEPS.md
- [ ] Update blocker status
- [ ] Ready for handoff

---

## 📖 Quick File Reference

| What I Need | File | Time |
|-------------|------|------|
| Entry point | docs/AI_AGENT_ENTRY_POINTS.md | 10 min |
| Guardrails | docs/ANTI_DRIFT_GUARDRAILS.md | 15 min |
| Overview | docs/PROD_GATE_CLOSURE/00_README.md | 10 min |
| Stuck? | docs/PROD_GATE_CLOSURE/08_decision_tree.md | 10 min |
| Cheat sheet | docs/PROD_GATE_CLOSURE/QUICK_REFERENCE.md | 5 min |
| Status | docs/PROD_GATE_CLOSURE/SESSION_3_FINDINGS.md | 5 min |

---

## ✅ Success Looks Like

A successful session:
- ✅ All 6 drift checks passed before commit
- ✅ Full gate passing
- ✅ Blocker marked COMPLETE
- ✅ Checkpoint created with NEXT_STEPS
- ✅ Handed off to next session
- ✅ No rework needed

---

## ❌ Failure Looks Like

- ❌ Drift alerts triggered
- ❌ Gate still failing
- ❌ Blocker only partially fixed
- ❌ No checkpoint/next steps
- ❌ Code needs rework

---

## 🤔 Common Questions

**Q: What if I get stuck?**
A: Read `docs/PROD_GATE_CLOSURE/08_decision_tree.md`

**Q: Can I fix multiple blockers?**
A: No. One blocker per session (Rule 1).

**Q: Can I refactor unrelated code?**
A: Only if required to fix YOUR blocker.

**Q: Why so many guardrails?**
A: Previous sessions showed scope creep. These prevent it.

**Q: How long should this take?**
A: Prep (60 min) + Work (2-10 hours) + Validation (30 min)

---

## 🎬 Ready to Start?

1. ✅ Read governance files (20 min)
2. ✅ Read guardrails (15 min)
3. ✅ Read your blocker guide (10 min)
4. ✅ Fill session window (10 min)
5. ✅ Confirm guardrails ACTIVE
6. ✅ **NOW**: Follow your blocker's technical guide

---

**Total prep time: 55-60 minutes**

**This prep saves 10+ hours of rework**

**Quality > Speed. Read the docs. Follow the guardrails. Do good work.**

---

**NEXT**: Read `AGENTS.md` or `GEMINI.md` sections 0-24 (start now!)
