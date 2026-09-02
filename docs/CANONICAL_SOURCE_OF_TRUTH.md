# Canonical Source Of Truth

- Roles: `ADMIN`, `RESIDENT`, `SUPERVISOR`, `SUPPORT_STAFF`
- Identity creation: `/users/new` -> `create_user_with_profile(...)`
- Supervision model: `ResidentSupervisorAssignment`
- Academic foundation models:
  - `ResidentTrainingRecord`
  - `AcademicPeriod`
  - `RotationTemplate`
  - `EvaluationFormTemplate`
  - `LogbookCategory`
  - `SupervisorReviewQueueItem`
- Canonical frontend route families:
  - `/users`, `/residents`, `/supervisors`, `/support-staff`, `/admins`, `/masters`
  - `/supervision/*`
  - `/academics/*`
  - `/dashboard/utrmc`, `/dashboard/resident`, `/dashboard/supervisor`
  - `/complete-profile`, `/change-password`
