# Frontend Test Results

## Commands

```bash
cd frontend && npm test -- --watch=false
cd frontend && npm run lint
cd frontend && npm run typecheck
cd frontend && npm run build
```

## Results

| Command | Result | Notes |
|---|---|---|
| `npm test -- --watch=false` | FAIL | 1 failed, 80 passed, 81 total |
| `npm run lint` | PASS | no ESLint warnings or errors |
| `npm run typecheck` | FAIL | 7 TS errors in 5 test files |
| `npm run build` | PASS | production build succeeded |

## Failing unit test

- `app/dashboard/utrmc/hod/page.test.tsx`
- timeout waiting for the CTA flow test to complete

## Typecheck failures

- missing `afterEach` in several test files
- `jest.SpyInstance` not found in `lib/utils.test.ts`

## Classification

- **Unit failure:** test harness / timing
- **Typecheck failure:** test harness typing
- **Build/lint:** healthy
