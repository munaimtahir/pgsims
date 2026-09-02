# Brick 8 Discovery

- Active root: `/home/munaim/srv/apps/pgsims`
- Update 0 status on entry: GO
- Brick 6 status on entry: GO
- Brick 7 status on entry: GO

## Findings

- `sims.academics` already existed and was the Brick 6 master-catalog app.
- Active `training` code still contains broader legacy workflow surface for rotations, logbook, thesis, and operations.
- `ResidentSupervisorAssignment` is the active supervision spine.
- `SupervisorResidentLink` is not active in frontend/backend integration paths used by Brick 8.
- No active HOD route/dashboard was required for Brick 8 implementation.

## Decision

- Extend `sims.academics` instead of creating a second academic app.
- Add a new `/api/academics/*` contract for Brick 8.
- Keep `/api/masters/*` stable for Brick 6.
- Do not revive old training/rotation/logbook workflows as part of the new academic foundation.
