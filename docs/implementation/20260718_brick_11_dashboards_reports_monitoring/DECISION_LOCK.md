# Decision Lock - Brick 11: Dashboards, Reports, and Exports

## Architectural Decisions Locked
1. **Reporting Layer isolation**: All summary and reporting query calculations are placed inside a dedicated module (`reporting.py`) rather than generic view methods.
2. **Scoping rules**:
   - Residents are strictly locked to their own progress records.
   - Supervisors can only query workload details and Assigned Resident report cards corresponding to active assignments.
   - Admins maintain full visibility.
3. **Export Formats**: Standard RFC 4180 CSV exports are generated dynamically at `/api/academics/reports/.../export.csv` with filename mappings.
4. **No Legacy Models**: No active reference or queries target legacy HOD, post placement or SupervisorResidentLink objects.
