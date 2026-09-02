# API Source of Truth

## Canonical Reference

The API contract documents located in `docs/contracts/` are the **single, authoritative source of truth** for all backend–frontend integration in PGSIMS.

The following files form the canonical contract:

| File | Authority |
|------|-----------|
| `docs/contracts/API_CONTRACT.md` | All API endpoint shapes, payloads, and status codes |
| `docs/contracts/DATA_MODEL.md` | Canonical entity definitions and relationships |
| `docs/contracts/RBAC_MATRIX.md` | Role-based access permissions per endpoint |
| `docs/contracts/ROUTES.md` | Frontend route structure |
| `docs/contracts/TERMINOLOGY.md` | User-facing terminology |
| `docs/integration/API_ENDPOINT_CATALOG.md` | Full backend endpoint inventory |
| `docs/integration/BACKEND_FRONTEND_TRUTHMAP.md` | Verified integration map |

---

## What Must Align to the Contract

Every layer of the application must conform to the contract:

### Backend
- Route paths must match the contract exactly
- Request validation must enforce the contract schema
- Response payloads must match the schema precisely (no extra or missing fields)
- Authentication/authorization must follow the documented RBAC rules
- HTTP status codes must match contract-defined values
- Error response shapes must follow `ERROR_HANDLING_CONTRACT.md`

### Frontend
- All API calls must use defined client functions (`frontend/lib/api/*.ts`)
- No raw `fetch()` or `axios` calls may be made directly from page components
- Request payloads must match the contract schema
- Response parsing must align with the documented response shape
- UI actions must correspond to a documented contract endpoint

---

## Enforcement Principles

1. **No endpoint may exist outside the contract.** If a backend endpoint is created, its contract definition must exist first.
2. **No frontend call may reference an undocumented endpoint.** If a new endpoint is consumed, the contract must be updated simultaneously.
3. **Payload changes are breaking changes.** Any field addition, removal, or rename requires a contract update + frontend SDK update.
4. **Role permission changes are breaking changes.** RBAC changes require a contract update before deployment.

---

## Canonical Data Model Invariants

These rules are non-negotiable and cannot be changed without a major version bump:

- There is **exactly one** canonical `Department` entity: `sims.academics.Department`
- There is **exactly one** canonical `Hospital` entity: `sims.rotations.Hospital` (mapped via `sims.users`)
- Hospitals host departments through the `HospitalDepartment` matrix table — never through a separate model
- No duplicate Department models (e.g., `RotationDepartment`) may be introduced

---

## Version History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-03-07 | System | Initial governance baseline |
