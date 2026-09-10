# Navigation and Layout Audit

## Role-Based Routing Architecture
Defined primarily in `frontend/middleware.ts` using token decoding.

**Rules:**
- `RESIDENT`: Allowed in `/dashboard/pg` and `/dashboard/resident`
- `SUPERVISOR`: Allowed in `/dashboard/supervisor`
- `ADMIN`: Allowed everywhere, specifically `/users`, `/residents`, `/supervisors`, `/academics`, etc.
- `SUPPORT_STAFF`: Allowed in `/dashboard/utrmc`

## Audit Observations
1. **Divergent Paths**: The frontend components request API endpoints (e.g. `/api/academics/training-records/`) that do not exist in the backend (resulting in BROKEN status in the map). This will cause empty pages or immediate error toasts upon navigation for users holding these roles.
2. **Missing Components**: The backend contains legacy `dummy_urls` for HTML rendering (`/cases/`, `/logbook/`) which bypasses the React SPA entirely. If any frontend button links to these, the user will fall out of the SPA shell.
3. **Redirects**: Unauthenticated users are redirected to `/login`. Expired sessions correctly delete cookies and bounce.
4. **Layout Check**: NextJS `layout.tsx` files handle the standard shell. However, hitting a legacy backend Django route directly will lose the sidebar and layout context entirely.

## Verification Status
- Role verification: **STATICALLY VERIFIED** via middleware logic.
- Runtime routing consistency: **FAIL** (Many broken API endpoints guarantee failed data loading on page transitions).
