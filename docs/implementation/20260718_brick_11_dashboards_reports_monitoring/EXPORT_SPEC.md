# Export Specifications - Brick 11: Dashboards, Reports, and Exports

## CSV Export Engine
All CSV reports are rendered using standard `csv.writer` logic streamed to `HttpResponse` content type `text/csv`.

## Filename Formats
- Resident Progress: `resident_progress_<username>.csv`
- Supervisor Workload: `supervisor_workload_<username>.csv`
- Evaluations: `evaluation_report.csv`
- Logbooks: `logbook_report.csv`
- Data Quality: `data_quality_report.csv`

## Columns Exported
- **Evaluations**: Resident, Supervisor, Template, Department, Program, Session, Status, Score, Max Score, Submitted At, Approved At, Pending Age (Days)
- **Logbooks**: Resident, Supervisor, Category, Type, Title, Entry Date, Status, Submitted At, Verified At, Pending Age (Days), Procedure Name, Procedure Code, Role Performed, Complexity, Outcome
- **Data Quality**: Discrepancy Category, Resident Name/Detail, Issue details/Notes
