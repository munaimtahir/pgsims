# Test Results

## Backend

### Cleanup command tests

```bash
cd backend
SECRET_KEY=test-secret pytest sims/users/test_demo_data_reset.py -q
```

Result:

- `4 passed`

### Existing seed command regression coverage

```bash
cd backend
SECRET_KEY=test-secret pytest sims/users/test_seed_demo_data.py -q
```

Result:

- `2 passed`

### Active surface baseline coverage

```bash
cd backend
SECRET_KEY=test-secret pytest sims/training/test_feature_layer_ops.py::ActiveSurfaceBaselineTests -q
```

Result:

- `2 passed`

### Django system check

```bash
cd backend
SECRET_KEY=test-secret python3 manage.py check
```

Result:

- `System check identified no issues (0 silenced).`

## Frontend

### Route smoke

```bash
cd frontend
E2E_BASE_URL=http://127.0.0.1:8082 E2E_API_URL=http://127.0.0.1:8014 npx playwright test e2e/smoke/cleanup_baseline_routes.spec.ts --project=smoke
```

Result:

- `1 passed`

### Frontend lint

```bash
cd frontend
npm run lint
```

Result:

- `✔ No ESLint warnings or errors`
