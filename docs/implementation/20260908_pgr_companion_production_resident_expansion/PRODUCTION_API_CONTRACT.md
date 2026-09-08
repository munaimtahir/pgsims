# Production API contract

All routes require bearer authentication and are scoped by PGR SIMS RBAC.

| Android capability | Route | Method | Envelope / rule |
| --- | --- | --- | --- |
| Identity/onboarding | `/api/auth/me/`, `/api/auth/onboarding/` | GET/PATCH | Backend-defined profile fields. |
| Training | `/api/resident-training/` | GET | DRF page. |
| Current training | `/api/residents/me/summary/` | GET | Canonical current selection is `rotation.current`; no client date inference. |
| Rotations | `/api/my/rotations/` | GET | Own `RotationAssignment` records, paged; production exposes `department_name`/`hospital_name`. |
| Supervisor | `/api/supervision/assignments/` | GET | Own assignment records, paged. |
| Logbook list/category | `/api/academics/logbook-entries/`, `/api/academics/logbook-categories/` | GET | Active academic workflow, paged. |
| Logbook draft/edit | `/api/academics/logbook-entries/`, `/{id}/` | POST/PATCH | Server assigns resident/training ownership; only editable states. |
| Logbook submit | `/api/academics/logbook-entries/{id}/submit/` | POST | Own draft/returned entry only. |
| Assessments | `/api/academics/evaluation-submissions/` | GET | Own records only. |
| Research/workshops | `/api/my/research/`, `/api/my/workshops/` | GET | Resident-scoped responses. |
| Documents | `/api/resident-documents/` | GET/POST upload action | Existing owner-scoped workflow. |

Android does not calculate lifecycle transitions or current rotation; it displays server status and
the server-provided current rotation. Safe error messages mask raw HTTP/JSON responses.

Production probes on 2026-09-08 returned 200 for every listed route except `/api/my/research/`,
which returned 404 for the synthetic resident because that account has no research project. Android
treats that capability as unavailable/empty instead of failing the resident snapshot.
