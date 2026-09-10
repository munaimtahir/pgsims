# DATABASE INTEGRITY AUDIT

Database schemas employ strong constraints:

* **Foreign Keys**: Almost all relationships use strict `ON_DELETE=PROTECT` or `CASCADE`. `ResidentSupervisorAssignment` uses `PROTECT`, preventing accidental deletion of a Resident or Supervisor who has active workflow linkages.
* **Unique Constraints**: Used generously. `ResidentSupervisorAssignment` uses `UniqueConstraint` on active assignment status. `ProgramMilestone` uses `unique_together` on `program` and `code`.
* **Mass Assignment Protection**: Profile updates via serializers (`SelfProfileUpdateSerializer`) explicitly whitelist fields (`first_name`, `last_name`, etc.) and ban role/is_active manipulation.
