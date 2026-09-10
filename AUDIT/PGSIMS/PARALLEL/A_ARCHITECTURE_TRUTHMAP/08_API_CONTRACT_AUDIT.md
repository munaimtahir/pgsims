# API Contract Audit

This document compares actual frontend API expectations with backend behavior.

| Frontend Call | Backend Endpoint | Findings | Status |
|---|---|---|---|
| `/api/auth/login/` | `/api/auth/login/` | Schema generally matches for basic auth. | VERIFIED |
| `/api/users/` | `/api/users/` | Paginator metadata (count, next, previous) expected by frontend list views matches backend DRF `PageNumberPagination`. | VERIFIED |
| `/api/academics/evaluation-templates/` | `Unknown` | Frontend expects an endpoint that does not exist in backend URL configurations. | FRONTEND_DEFECT |
| `/api/academics/training-records/` | `Unknown` | Training records exist under `sims.training` app (`/api/training/records/`), but frontend is querying `/api/academics/...`. | FRONTEND_DEFECT |
| `/api/rotations/` | `/rotations/` | Frontend calls `/api/rotations/` but backend serves them under `/rotations/` or `/api/training/rotations/`. | FRONTEND_DEFECT |

*Note: Without a fully synchronized running backend and frontend environment producing network traces, this represents a static analysis of route divergence.*
