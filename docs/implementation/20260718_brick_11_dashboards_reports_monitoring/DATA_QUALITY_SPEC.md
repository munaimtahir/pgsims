# Data Quality Specifications - Brick 11: Dashboards, Reports, and Exports

Data quality warnings check compliance metrics across the training record and supervision assignment structures.

## Compliance Metrics Checked
1. **Missing Training Record**: Active ResidentProfiles without any linked `ResidentTrainingRecord` instances.
2. **Missing Primary Supervisor**: Active ResidentProfiles without a linked primary supervisor.
3. **No Evaluation submissions**: Active residents with training records that have logged zero evaluation submissions.
4. **No Logbooks submitted**: Active residents with training records that have logged zero procedure/logbook submissions.
5. **Supervisor Workload thresholds**: Warning flag if a supervisor has an excessive volume ($>5$) of pending queue reviews.
6. **Milestone progress gaps**: Warning if a resident is below the minimum category logbook counts.
