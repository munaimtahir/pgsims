# Stabilization Test Results

## Backend

### Canonical backend gate

Command:

```bash
cd backend && SECRET_KEY='audit-secret' DJANGO_SETTINGS_MODULE=sims_project.settings_test pytest sims -q
```

Outcome: **PASS**  
Summary: `188 passed, 156 warnings`

### Contract drift tests (new/updated)

Command:

```bash
cd backend && SECRET_KEY='audit-secret' DJANGO_SETTINGS_MODULE=sims_project.settings_test \
  pytest sims/training/test_phase6.py::ResearchProjectAPITests::test_supervisor_return_transitions_project_to_draft \
         sims/training/test_phase6.py::EligibilityAPITests::test_my_eligibility_items_use_reasons_field \
         sims/training/test_phase6.py::EligibilityAPITests::test_utrmc_eligibility_items_use_reasons_field -q
```

Outcome: **PASS**  
Summary: `3 passed`

What this validates:
- `supervisor-return` research action is accepted and transitions to draft.
- Eligibility API now returns canonical `reasons` field (not `reasons_json`) for both resident and UTRMC endpoints.

## Frontend

### Unit/integration gate

Command:

```bash
cd frontend && npm test -- --watch=false
```

Outcome: **PASS**  
Summary: `2 passed test suites, 4 passed tests`

Covered surfaces:
- `frontend/lib/api/training.test.ts`
  - normalizes `/api/my/eligibility/` envelope + `reasons_json` fallback
  - normalizes `/api/utrmc/eligibility/` results + `reasons_json` fallback
- `frontend/app/forgot-password/page.test.tsx`
  - submits email to backend API client
  - shows success/error messages based on API outcome

### Build gate

Command:

```bash
cd frontend && npm run build
```

Outcome: **PASS**

### E2E smoke gate

Command:

```bash
cd frontend && npm run test:e2e:smoke
```

Outcome: **PARTIAL / FUNCTIONAL FAILURES**

Execution summary:
- `7 passed`, `10 failed`
- No filesystem `EACCES` failures after output path fix.

Current failure class:
- Auth/login flow against configured smoke target and API fallback:
  - login redirects remained on `/login`
  - helper fallback attempted `http://localhost:8000/api/auth/login/` and failed `ECONNREFUSED`

Conclusion:
- Playwright is now runnable in this environment.
- Remaining failures are environment/data/auth-flow related, not ownership/permission related.
