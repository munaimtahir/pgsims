# Playwright Rerun Stability — `admin_analytics_live_feed.spec.ts`

## Command used for loop
```bash
cd /home/munaim/srv/apps/pgsims/frontend
for i in 1 2 3 4 5; do
  E2E_BASE_URL=http://127.0.0.1:3000 E2E_API_URL=http://127.0.0.1:8014 \
    npx playwright test admin_analytics_live_feed.spec.ts --workers=1
done
```

## Results

| Run | Result | Notes |
|---|---|---|
| 1 | PASS | setup + chromium spec passed |
| 2 | PASS | setup + chromium spec passed |
| 3 | PASS | setup + chromium spec passed |
| 4 | PASS | setup + chromium spec passed |
| 5 | PASS | setup + chromium spec passed |

## Determinism verdict
- **5/5 passes** for the target spec sequence.
