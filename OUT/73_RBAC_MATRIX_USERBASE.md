# 73 — RBAC Matrix (Userbase)

| Endpoint / Action | admin | utrmc_admin | utrmc_user | supervisor | faculty | resident/pg |
|---|---|---|---|---|---|---|
| `GET /api/hospitals/` | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW |
| `POST/PATCH /api/hospitals/*` | ALLOW | DENY | DENY | DENY | DENY | DENY |
| `GET /api/departments/` | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW |
| `POST/PATCH /api/departments/*` | ALLOW | DENY | DENY | DENY | DENY | DENY |
| `GET /api/hospital-departments/` | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW |
| `POST/PATCH /api/hospital-departments/*` | ALLOW | ALLOW | DENY | DENY | DENY | DENY |
| `GET /api/users/` | ALLOW | ALLOW | DENY | DENY | DENY | self-only |
| `POST/PATCH /api/users/*` | ALLOW | ALLOW | DENY | DENY | DENY | DENY |
| `GET /api/residents/{user_id}/` | ALLOW | ALLOW | DENY | DENY | DENY | self-only |
| `GET /api/staff/{user_id}/` | ALLOW | ALLOW | DENY | self-only | self-only | DENY |
| `POST/PATCH/DELETE /api/department-memberships/*` | ALLOW | ALLOW | DENY | DENY | DENY | DENY |
| `POST/PATCH/DELETE /api/hospital-assignments/*` | ALLOW | ALLOW | DENY | DENY | DENY | DENY |
| `GET /api/supervision-links/` | ALLOW | ALLOW | DENY | DENY | DENY | DENY |
| `POST/PATCH /api/supervision-links/*` | ALLOW | ALLOW | DENY | DENY | DENY | DENY |
| `GET /api/hod-assignments/` | ALLOW | ALLOW | DENY | DENY | DENY | DENY |
| `POST/PATCH /api/hod-assignments/*` | ALLOW | ALLOW | DENY | DENY | DENY | DENY |
| `GET /api/departments/{id}/roster/` | ALLOW | ALLOW | ALLOW | own dept only | own dept only | own dept only |
| `GET /api/hospitals/{id}/departments/` | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW |

## Rationale
- Technical governance entities (Hospital/Department writes) remain locked to `admin`.
- UTRMC governance (`matrix`, userbase assignments/linking) is `utrmc_admin` with `admin` override.
- Non-manager clinical roles are profile-scoped and roster-scoped only.
