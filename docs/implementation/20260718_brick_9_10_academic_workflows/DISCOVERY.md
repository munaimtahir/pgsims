# Discovery - Brick 9-10 Combined Sprint: Academic Workflows

## Overview
This combined sprint designs and implements the full postgraduate training academic evidence workflow system.

## Domain Model
1. **EvaluationSubmission**: Links a resident, a template, a primary supervisor, and an academic period. It manages draft state, submission, evaluation review, and approval/rejection.
2. **EvaluationResponse**: Key-value responses matching the evaluation template schema.
3. **LogbookEntry**: Logs clinical case details including patient age/gender, resident reflections, case title, date, and status.
4. **ProcedureRecord**: Captures granular procedure-specific columns: procedure name, code, role performed, complexity, outcome, and complications.

## Supervision and Workload
* Resident training progress relies on `ResidentSupervisorAssignment` to map supervisors to residents.
* Supervisors access a workload view containing active review tasks.
* Admins monitor global data quality indicators (such as residents with records but no submitted evidence).
