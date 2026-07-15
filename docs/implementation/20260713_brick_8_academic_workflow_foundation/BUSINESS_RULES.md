# Brick 8 Business Rules

- A resident may have only one active academic `ResidentTrainingRecord`.
- Training record defaults may prefill from `ResidentProfile`.
- Resident academic summary combines training record + supervision + queue state.
- Supervisor academic summary is scoped by active `ResidentSupervisorAssignment`.
- Admin manages global academic registries.
- Resident and supervisor are read-only on global setup registries.
