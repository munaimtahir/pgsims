# 2026-06-19 User List Filtering Update

## Scope
Added permanent filtering controls to the UTRMC users page for role, department, account status, profile completeness, and search.

## Files Updated
- `backend/sims/users/userbase_serializers.py`
- `backend/sims/users/userbase_views.py`
- `backend/sims/users/test_userbase_api.py`
- `docs/contracts/API_CONTRACT.md`
- `frontend/app/dashboard/utrmc/users/page.tsx`
- `frontend/app/dashboard/utrmc/users/page.test.tsx`
- `frontend/lib/api/userbase.ts`
- `frontend/lib/api/userbase.test.ts`

## Behavior
- The users API now exposes `is_complete_profile` on roster rows.
- The users endpoint now accepts `is_complete_profile=true|false` alongside existing `role`, `department`, `active`, and `search` filters.
- The frontend users page now lets managers combine filters without leaving the page.

## Validation
Pending targeted backend and frontend test runs.
