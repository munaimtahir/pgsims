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
