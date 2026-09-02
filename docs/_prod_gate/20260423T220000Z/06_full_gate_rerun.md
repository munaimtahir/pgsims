# Full Gate Rerun - 2026-04-23

## Sequence Executed
1. **Dependency Sanity**: OK
2. **Migration Check**: OK
3. **Backend Tests with Coverage**: 241 passed, 56.10% coverage.
4. **Frontend Lint**: OK
5. **Frontend Typecheck**: OK
6. **Frontend Jest Tests with Coverage**: 53 passed, 12.71% coverage.
7. **Strict Schema Gate**: 0 errors, 1 warning (enum collision).
8. **Docker Bring-up**: OK
9. **Seed Baseline**: OK
10. **Active-Surface E2E**: 7/7 passed.
11. **Regression Smoke**: 3 passed (including UTRMC routes).

## Verdict
- **Strict Schema Gate**: PASS
- **Active-Surface E2E**: PASS
- **Restart/Reseed Smoke**: PASS
- **Coverage**: FAIL (Blocked by coverage thresholds)
