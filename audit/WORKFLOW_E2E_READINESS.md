# Workflow E2E Readiness Review

Date: 2026-03-14
Scope: next-phase workflow E2E promotion review on top of the existing smoke baseline

## Candidate Classification

| Candidate | Backend/state confirmed | Frontend/UI confirmed | Deterministic seeded precondition | Browser assertion quality | Decision | Notes |
|---|---|---|---|---|---|---|
| Research supervisor return workflow | Yes: `POST /api/my/research/action/supervisor-return/`, `GET /api/supervisor/research-approvals/` | Yes: supervisor approvals page and return form | Yes: `seed_e2e` provisions `e2e_pg` with submitted research | Strong | Promote now | Promote the pending-list rendering + return action path. |
| Resident eligibility display workflow | Yes: `GET /api/my/eligibility/`, resident summary endpoint | Yes: resident dashboard renders eligibility cards/reasons | Yes: `seed_e2e` provisions deterministic unmet reasons | Strong | Promote now | Browser gate asserts canonical reasons render. |
| Forgot-password request flow | Yes: `POST /api/auth/password-reset/` | Yes: `/forgot-password` form submits through real UI path | Yes | Strong | Promote now | Deterministic success message path works for seeded email. |
| Supervisor approvals list correctness | Yes: approvals serializer includes `resident_name` | Yes: pending card renders `Resident: ...` | Yes | Strong | Promote now | Scoped to pending approvals list correctness, not broader reviewed-history UI. |
| Stable userbase/org-management workflow | Yes, but mutation-heavy and cross-role | Yes, but broad admin/UTRMC/resident setup | Partially | Weak for a small gate | Keep unit/backend only for now | Existing spec creates many entities and is better kept outside the canonical workflow gate. |

## Readiness Notes

- The promoted workflow subset is intentionally small and deterministic.
- The supervisor approvals endpoint currently returns pending submissions only. Reviewed-history assertions were excluded from promotion because they are not part of the current backend contract.
- The optional userbase/org-management workflow is real, but it widens the gate into multi-entity regression coverage and increases cross-test coupling.

## Evidence Reviewed

- Contracts: `docs/contracts/API_CONTRACT.md`
- Seed/setup: `backend/sims/users/management/commands/seed_e2e.py`
- Browser specs: `frontend/e2e/workflow-gate/stabilized-workflows.spec.ts`
- UI surfaces:
  - `frontend/app/forgot-password/page.tsx`
  - `frontend/app/dashboard/supervisor/research-approvals/page.tsx`
  - `frontend/app/dashboard/resident/page.tsx`
- Backend views:
  - `backend/sims/users/api_views.py`
  - `backend/sims/training/views.py`
