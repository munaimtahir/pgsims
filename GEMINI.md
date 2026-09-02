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

Your role: Close the sprint blockers while maintaining these properties.

---

## 🚨 CRITICAL: Universal Identity, Profile Synchronization, HOD Cleanup, and Dynamic Onboarding

**BEFORE EXECUTING ANY TASK**, read the latest instruction files:
1. `AGENTS.md` - The master governance rules.
2. `docs/contracts/` - Authoritative API contracts (e.g., `docs/contracts/API_CONTRACT.md`).

---

## 1) Operating Mode

- **Default**: Single-agent execution with internal delegation allowed.
- **Constraint**: Must respect phase gates and contract locks.
- **Mandate**: Every claim backed by evidence (file paths, test output, logs).
- **Scope**: Fix identified blockers for Update 0 directly within the active codebase, do NOT attempt broad refactors of unrelated areas.

We are working directly in this project (fixing and updating it rather than making a new `pgms/` subfolder). All references to `pgms/` logically refer to the active project directory `/home/munaim/srv/apps/pgsims/`.

---

## 2) Contract-First (Non-Negotiable)

- Backend ↔ Frontend integration MUST be driven by `docs/contracts/`
- If code changes require contract changes, update contracts in the same run
- No "quick fixes" that silently change payload shapes
- **Gate**: Contract changes must include test updates in same commit

---

## 3) Frozen UX Rule (Adoption-Safety)

- DO NOT change route structure, navigation labels, or terminology unless explicitly unlocked or required for the sprint.
- For Update 0, the rule is unlocked specifically for:
  - Universal identity creation `/users/new`
  - Dynamic completion `/complete-profile`
  - Removal of HOD role references in all views, badges, labels, and dropdowns.

---

## 4) Canonical Data Model Rule (Critical)

- There is exactly ONE canonical Department entity for the university.
- There is exactly ONE canonical Hospital entity for the university.
- A hospital hosts a subset of departments via `HospitalDepartment` matrix table.
- **DO NOT** create or reintroduce a second Department model (e.g., "RotationDepartment", "AcademicDepartment").

---

## 5) Audit Integrity

- All state transitions must be auditable.
- Do NOT remove `django-simple-history`.
- Never silently mutate approved/verified records.
- **All models** with state changes must include history tracking.

---

## 6) Notifications

- Notifications MUST use canonical schema: `recipient`, `verb`, `body`, `metadata`.
- Do not use legacy keys (`user`, `message`, `type`, `related_object_id`).
- Prefer single `NotificationService` helper at `sims/notifications/services.py`.

---

## 7) Phase Gates (Must Pass)

Current mandatory gates for Update 0 (ALL must be true for GO):
- [ ] Strict schema gate (0 errors)
- [ ] Backend tests passing
- [ ] Frontend type-check & lint & build passing
- [ ] No orphan user/profile instances
- [ ] Repair command passes

---

## 8) Definition of Done

A task is complete only when:
- ✅ Relevant tests pass
- ✅ Contracts updated (if applicable)
- ✅ No drift introduced (scan forbidden patterns)
- ✅ Work documented under `docs/implementation/`
- ✅ Blocker reference included in commit message

---

## 9) Forbidden Patterns

1. **Duplicate Department models**
2. **Breaking API payloads without contract updates**
3. **Legacy Notification keys**
4. **Direct database edits for state changes**
5. **UX changes without exceptions**
6. **Fake coverage inflation**

---

## 15) Key Commands (Copy-Paste Ready)

### Backend Testing
```bash
cd backend && pytest sims -q
cd backend && pytest sims/users/ -v
```

### Frontend Testing
```bash
cd frontend && npm test -- --watch=false
cd frontend && npm run typecheck
```

### Schema Gate
```bash
cd backend && python manage.py spectacular --validate
```

---

## 18) Commit Template

```
Update 0 - [brief description of changes]

Detailed explanation of:
- What was changed
- How it is fixed
- How it is validated

Fixes Update 0 requirements
See: AGENTS.md

Validation:
- Tests passing
- Repair command output verified
```
