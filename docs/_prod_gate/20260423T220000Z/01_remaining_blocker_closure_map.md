# Remaining Blocker Closure Map - 2026-04-23

## 1. Strict Schema Gate (Blocker #1)
- **Problem**: 315 errors, mainly "unable to guess serializer" for `APIView` subclasses.
- **Goal**: 0 errors, 0 warnings (strict gate).
- **Target Files**:
  - `backend/sims/users/api_views.py`
  - `backend/sims/users/userbase_views.py`
  - `backend/sims/bulk/views.py`
  - `backend/sims/training/views.py`
  - `backend/sims/notifications/views.py`

## 2. Active Scope Completeness
- **Goal**: 100% test coverage of active routes, APIs, and CTAs.
- **Status**: E2E active-surface is green (7/7), but more granular tests for all CTAs and role edge cases are needed.
- **Action**: Identify all active routes in `frontend/app/` and ensure they are exercised in E2E or unit tests.

## 3. Backend Coverage (Blocker #5)
- **Problem**: 54.38% line, 28.69% branch.
- **Goal**: 95% line, 90% branch.
- **Action**: Focus on `sims/training/`, `sims/users/`, and permission classes.

## 4. Frontend Coverage (Blocker #6)
- **Problem**: 8.71% line.
- **Goal**: 90% line.
- **Action**: Add Jest tests for components in `frontend/components/` and pages in `frontend/app/`.

## 5. UTRMC Admin Completeness
- **Goal**: Full coverage of the UTRMC admin cluster.
- **Action**: Targeted E2E tests for `/dashboard/utrmc/*`.
