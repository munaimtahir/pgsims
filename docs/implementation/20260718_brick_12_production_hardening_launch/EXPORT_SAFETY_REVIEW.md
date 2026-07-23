# Export Safety Review - Brick 12: Production Hardening, Backup/Restore, Security, and Launch Readiness

We conducted a review of the Excel/CSV data exports implemented in Brick 11 to ensure they meet data security guidelines:

## Findings & Compliance
1. **Scoping Restrictions**:
   - Residents can only download CSV files containing their own evaluations or clinical logbook entries.
   - Supervisors can only download logs corresponding to postgraduates linked to them via active `ResidentSupervisorAssignment` items.
   - Support staff cannot request raw export files by default.
2. **Access Control**: CSV view endpoints require Django authentication token validation headers; unauthenticated download requests are blocked with a `401 Unauthorized` response.
3. **Data Anonymization**: No unnecessary patient identification records (like full national ID numbers or names) are leaked in logbook exports. Columns are limited to: Resident, Supervisor, Category, Type, Title, Entry Date, Status, Procedure Name, Complexity, Outcome.
4. **Header Clarities**: Export headers map directly to the canonical model fields to prevent column misalignment.
