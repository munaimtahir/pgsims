# Brick 8.6 Discovery

- Active root: `/home/munaim/srv/apps/pgsims`
- Branch: `main`
- Starting commit: `2a045748c63a4726075ccca783b0400a97673704`
- Starting worktree: dirty from prior Brick 8 / 8.5 work; Brick 8.6 applied in-place.

## Findings

- Duplicate frontend admin routes still existed under `/dashboard/utrmc/*`.
- Legacy resident and supervisor workflow routes were already redirect-only, but stale tests and helper imports remained.
- `frontend/lib/api/departments.ts`, `frontend/lib/api/hospitals.ts`, and `frontend/lib/api/training.ts` were no longer needed by canonical UI.
- `SupervisorResidentLink` no longer drove active frontend or dashboard behavior, but still existed as a legacy backend model with admin/command/test references.
