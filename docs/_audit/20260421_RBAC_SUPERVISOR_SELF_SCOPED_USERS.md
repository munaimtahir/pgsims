# 2026-04-21 RBAC reconciliation: supervisor self-scoped `/api/users/`

- Verified current `UserViewSet` behavior already scopes non-manager users to their own user row on `GET /api/users/` and allows `GET /api/users/{id}/` only for self or manager roles.
- Updated `docs/contracts/RBAC_MATRIX.md` and `docs/contracts/API_CONTRACT.md` to state that supervisors, faculty, residents/PGs, and `utrmc_user` have self-only read access instead of blanket denial wording.
- Added regression coverage in `backend/sims/users/test_userbase_api.py` for supervisor list-self and retrieve-self / retrieve-other behavior.
- No route or payload shape changes were introduced.
