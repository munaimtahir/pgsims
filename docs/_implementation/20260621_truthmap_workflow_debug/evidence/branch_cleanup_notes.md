# Branch Cleanup Notes

The following files are kept in this branch because they are directly relevant to the core truth-map workflow fixes:

## 1. Resident Onboarding & Self-Service
- **Backend Files**:
  - `backend/sims/users/resident_onboarding_urls.py`
  - `backend/sims/users/resident_onboarding_views.py`
  - `backend/sims/users/resident_selfservice_urls.py`
  - `backend/sims/users/tasks.py`
  - `backend/sims/users/test_resident_onboarding.py`
- **Frontend Files**:
  - `frontend/app/dashboard/onboarding/`
  - `frontend/app/resident/`
  - `frontend/components/onboarding/`
  - `frontend/components/resident/`
  - `frontend/lib/api/onboarding.ts`
- **Reasoning**:
  - The resident onboarding flow is classified as `GREEN` in the active truth map (`FRONTEND_BACKEND_TRUTHMAP_20260621.md`). It represents the verified path for pilot users.
  - The targeted backend test suite explicitly contains `sims.users.test_resident_onboarding` which tests these views and workflows.

## 2. Shared Audit Documents
- **Documentation**:
  - `docs/_audit/20260619_resident_onboarding.md`
  - `docs/_audit/20260619_user_list_filtering.md`
  - `docs/_audit/20260620_onboarding_cleanup.md`
- **Reasoning**:
  - These document the state of onboarding and filtering changes implemented during this sprint to verify truth map completeness.

Other unrelated files (such as Urology PDFs, AdminOps bridge files, and MS Urology curriculum onboarding commands/migrations) have been removed from the working tree.
