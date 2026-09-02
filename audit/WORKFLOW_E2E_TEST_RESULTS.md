# Workflow E2E Test Results

## Smoke gate

Command:

```bash
cd frontend && npm run test:e2e:smoke:local
```

Result: **PASS**

Summary:
- `17 passed`
- `0 failed`

## Workflow gate

Command:

```bash
cd frontend && npm run test:e2e:workflow:local
```

Result: **PASS**

Summary:
- `3 passed`
- `0 failed`

## Promoted workflow browser coverage

1. Forgot-password request submit path
   - UI form -> backend endpoint -> success message

2. Supervisor approvals + supervisor-return contract
   - pending research card visible
   - `resident_name` rendered
   - return action succeeds

3. Resident eligibility display
   - dashboard eligibility section visible
   - canonical reason strings rendered:
     - `Synopsis not yet approved by supervisor`
     - `Thesis not yet submitted`
