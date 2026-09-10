# Failure Mode Audit

## Error Handling Review (Backend)
- A brief scan of `sims/users/userbase_views.py` shows multiple broad exception handlers (`except Exception:`, `except Exception as e:`).
- In some places, specific exceptions are caught (e.g., `ValidationError`, `Hospital.DoesNotExist`, `Department.DoesNotExist`), but broad exception swallowing is prevalent, which can lead to silent failures or raw HTTP 500s masked as generic 400 responses.
- The project implements custom rate limit classes (`LOGIN_RATE_LIMIT` environment variable mapping to Django Rest Framework throttles) to protect sensitive endpoints from brute force.

## Frontend Error Handling
- Playwright tests explicitly cover negative scenarios (e.g. `frontend/e2e/negative/validation.spec.ts`), testing application behavior during HTTP 400/403 states.
- Missing or malformed data is generally tested for resilience, but actual runtime E2E execution is recommended to verify error UI states continuously.

## Concurrency
- `userbase_engine.py` and `services.py` were reviewed structurally. There are custom actions like `create_supervisor_assignment` which need to rely on database constraints or transaction blocks to prevent duplicate writes during race conditions.
