# MASTER RBAC MATRIX

## Verified Roles
1. Admin
2. Resident
3. Supervisor
4. Support Staff

## Key Conclusions
* `ResidentSupervisorAssignment` successfully acts as the canonical truth.
* Workflows enforce constraints correctly via Django/DRF permissions. Cross-supervisor object access dynamically throws `403 Forbidden`.
* Legacy `User.supervisor` field is unused in active workflow access paths.
