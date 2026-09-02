# Decision Lock — Update 0

## Architecture Constraints Locked
1. **Four Final Roles Only**:
   - `ADMIN`
   - `RESIDENT`
   - `SUPERVISOR`
   - `SUPPORT_STAFF`
   - All legacy roles (`UTRMC_ADMIN`, `HOD`, `TEACHER`, `FACULTY`, `STUDENT`, `PGR`, `TRAINEE`, `CLERK`, `OFFICE_STAFF`, `DATA_ENTRY`, `SUPER_ADMIN`, `SYSTEM_ADMIN`) are completely rejected and forbidden from being exposed in any frontend views, API endpoints, or database choices.

2. **No HOD Identity Elements**:
   - HOD must not exist as a role, model, profile, API, frontend route, sidebar item, or dashboard.
   - HOD is allowed only as free-text designation metadata.

3. **Universal User Creation Center**:
   - `/users/new` is the single universal creation center.
   - Users and profiles must be created inside a transaction atomically.

4. **Dynamic Onboarding**:
   - Onboarding is driven dynamically by required fields defined in the registry.
   - `/api/auth/me/` returns the dynamic state and `allowed_next_route`.
