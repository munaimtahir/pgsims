# Training and rotation audit

The canonical training record is `training.ResidentTrainingRecord`. Rotation history is exposed by
the resident-scoped `/api/my/rotations/` endpoint over `training.RotationAssignment`. The
authoritative current posting is supplied separately by `/api/residents/me/summary/` at
`rotation.current`; Android never derives it from dates. The production serializer supplies
`department_name`, `hospital_name`, period and status. Supervisor data remains authoritative in
`supervision.ResidentSupervisorAssignment` via `/api/supervision/assignments/`.

The Android Training tab consumes these three existing APIs for programme, current rotation,
chronological history/detail and supervisor information. It permits no resident-side alteration of
training, posting or supervisor assignment.
