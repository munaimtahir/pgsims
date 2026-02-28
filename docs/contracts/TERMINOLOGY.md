# Terminology Lock (UI Dictionary)

These are user-facing terms. Do not change once pilot begins.

- **Submitted**: entry sent to supervisor for review (backend status may be `pending`)
- **Returned**: supervisor requests edits
- **Rejected**: supervisor declines entry (must include feedback/reason)
- **Approved**: supervisor verifies entry
- **Feedback**: supervisor message shown to PG
- **Home Hospital**: trainee’s primary hospital until graduation
- **Home Department**: trainee’s primary department until graduation
- **Rotation**: time-bounded posting in a (Hospital, Department) pair
- **Resident**: postgraduate trainee role (legacy `pg` remains accepted)
- **Faculty**: senior academic role that may supervise residents and hold HOD assignment
- **HOD**: active head-of-department assignment tracked with effective dates

Notes:
- UI displays **Submitted** even if backend enum is `pending`.
- UI reads `feedback` from API (alias of `supervisor_feedback`).
