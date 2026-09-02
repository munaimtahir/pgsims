# Legacy Delete Candidates

| Backend Model Name | App / File Path | Database Table Name | Current Status | Why It Is Legacy | Canonical Replacement | Active References Found | Deletion Risk | Can Delete Now? | Recommended Deletion Sprint | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| `SupervisorResidentLink` | `backend/sims/users/models.py` | `users_supervisorresidentlink` | DELETED | Legacy supervisor-resident link model from pre-Brick 7 design | `sims.supervision.models.ResidentSupervisorAssignment` | Historical migrations only, plus deletion migration `backend/sims/users/migrations/0009_delete_supervisorresidentlink.py` | Low | DONE | Brick 8.6 | Removed from active backend/frontend code and dropped by migration. |
