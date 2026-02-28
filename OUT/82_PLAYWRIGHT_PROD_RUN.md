# 82 — Playwright Production Run

Base URL: `https://pgsims.alshifalab.pk`

## Userbase scenario command (no skip)
```bash
cd frontend && npx playwright test e2e/critical/userbase_foundation.spec.ts --project=chromium
```

## Userbase scenario output
```text

Running 2 tests using 1 worker

  ✓  1 [setup] › e2e/auth.setup.ts:9:6 › admin login and persist storage state (897ms)
  ✓  2 [chromium] › e2e/critical/userbase_foundation.spec.ts:4:5 › utrmc admin can build userbase graph and resident scope is enforced (16.0s)

  2 passed (18.3s)

To open last HTML report run:
[36m[39m
[36m  npx playwright show-report ../OUT/E2E_REMEDIATION/playwright-report[39m
[36m[39m
```

## Skip guard check
```text
No skip markers found in userbase_foundation.spec.ts
```

## Artifacts
- HTML report: `OUT/E2E_REMEDIATION/playwright-report`
- Traces/videos/screenshots: `frontend/test-results/`
