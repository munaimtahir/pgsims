# Backend Test Results

## Commands

```bash
docker compose -f docker/docker-compose.yml --env-file .env exec -T backend pytest sims -q
docker compose -f docker/docker-compose.yml --env-file .env exec -T backend python manage.py check
docker compose -f docker/docker-compose.yml --env-file .env exec -T backend python manage.py makemigrations --check --dry-run
```

## Results

| Command | Result | Count | Notes |
|---|---|---:|---|
| `pytest sims -q` | FAIL | 344 collected / 1 error | `ModuleNotFoundError: No module named 'pandas'` in `sims/tests/test_bulk_userbase_engine.py` |
| `manage.py check` | PASS | 0 issues | runtime Django config healthy |
| `makemigrations --check --dry-run` | PASS | no changes | migrations clean |

## Classification

- **Issue type:** environment/dependency
- **Priority:** P1 for the backend regression gate, because collection stops immediately
