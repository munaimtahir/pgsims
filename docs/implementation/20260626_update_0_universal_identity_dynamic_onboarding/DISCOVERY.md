# Discovery Report — Update 0

## Overview
This document summarizes the discoveries made regarding the initial state of the PGMS / PGR SIMS repository prior to closing Update 0.

## Findings
1. **Active Root**: `/home/munaim/srv/apps/pgsims` is confirmed as the active project directory.
2. **Current State**:
   - The final four roles (`ADMIN`, `RESIDENT`, `SUPERVISOR`, `SUPPORT_STAFF`) are implemented and active in the User model.
   - Profile models (`AdminProfile`, `ResidentProfile`, `SupervisorProfile`, `SupportStaffProfile`) exist and sync with User.
   - The universal creation endpoint (`/api/users/`) creates users and linked profiles atomically.
   - The `/api/auth/me/` endpoint correctly returns the onboarding state.
   - Stale/HOD-specific dashboard endpoints and mixins were still present and needed cleanup.
   - Legacy tests was failing due to fixture collisions and outdated assertions.
