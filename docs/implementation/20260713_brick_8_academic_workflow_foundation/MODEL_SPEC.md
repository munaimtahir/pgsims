# Brick 8 Model Spec

- `ResidentTrainingRecord`
  - One active record per resident enforced by conditional unique constraint.
  - Links resident profile, program, session, site, and department.
- `AcademicPeriod`
  - Registry for academic windows.
- `RotationTemplate`
  - Scaffold registry only.
- `EvaluationFormTemplate`
  - Registry only. No submissions in Brick 8.
- `LogbookCategory`
  - Registry only. No entries in Brick 8.
- `SupervisorReviewQueueItem`
  - Lightweight queue scaffold for future review workflows.
