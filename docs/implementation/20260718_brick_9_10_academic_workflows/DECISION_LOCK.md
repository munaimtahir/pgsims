# Decision Lock - Brick 9-10 Combined Sprint: Academic Workflows

## Decided Architectural Lock-ins
1. **Academic Spine Core**: All academic workflow evidence requires an active `ResidentTrainingRecord` instance.
2. **Supervision Verification**: Resident submissions default to their active `ResidentSupervisorAssignment` supervisor.
3. **Audit Log Coverage**: All submission, review, approval, verification, return, and rejection events generate corresponding `ActivityLog` records.
4. **Idempotent Pilot Data**: Seeding pilot workflows is idempotent and avoids duplicating core lookup data.
