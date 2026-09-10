# DOMAIN MODEL MAP

## CANONICAL RELATIONSHIPS

**Core User**
The system uses a unified `User` model, extended via `ResidentProfile`, `SupervisorProfile`, `AdminProfile`, and `SupportStaffProfile`.

**Supervision**
The legacy `supervisor` ForeignKey on the `User` model is deprecated in favor of `ResidentSupervisorAssignment` located in `sims.supervision.models`. This model supports multiple assignments (`PRIMARY`, `CO_SUPERVISOR`) and tracks historical assignments over time, preventing duplicate active relationships.

**Training**
`ResidentTrainingRecord` connects the Resident to a `TrainingProgram`. Workflow models like `ResidentSubmission` and `LogbookEntry` tie back to the `ResidentTrainingRecord` rather than the `ResidentProfile` directly, enforcing chronological constraints.

## LEGACY & COEXISTING DATA

Some legacy fields like `User.supervisor` still exist in the database schema. While some permission classes (e.g. `CanVerifyLogbookEntry`) still conditionally reference legacy IDs `obj.pg.supervisor_id`, the modern API endpoints (such as `ResidentProfileViewSet` and `onboarding_api`) consistently query `ResidentSupervisorAssignment`.
