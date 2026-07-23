# Report Specifications - Brick 11: Dashboards, Reports, and Exports

## Overview Reports
1. **Resident Progress Report**:
   - Identity: Full Name, Username, Email, Hospital name, Program name, Department name.
   - Spine status: Start Date, Expected End Date, Training Year, Record Status.
   - Supervision details: Primary supervisor email, co-supervisors.
   - Workflow numbers: Approved evaluations, pending reviews, verified logbooks count.
   - Milestone tracking: Verified logbook category counts vs category minimums.
   
2. **Supervisor Workload Report**:
   - Identity: Supervisor Name, Username, Email, Department, Hospital.
   - Workload KPIs: Supervised resident count, Pending evaluations, Pending logbooks, Overdue review queue items.
   - Assignments listing: Supervised resident list with name, username, program, training year.
   - Review queue details: Outstanding tasks with resident name, type, due date, notes.
   
3. **Evaluation Report**:
   - Columns: Resident, Supervisor, Template, Department, Program, Session, Status, Score, Max Score, Submitted At, Approved At, Pending Age.
   - Scoped: Resident sees self, Supervisor sees assigned, Admin sees all.
   
4. **Logbook Report**:
   - Columns: Resident, Supervisor, Category, Type, Title, Entry Date, Status, Submitted At, Verified At, Pending Age, Procedure Name, Complexity, Outcome.
   - Scoped: Resident sees self, Supervisor sees assigned, Admin sees all.
