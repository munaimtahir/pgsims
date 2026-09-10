# Test Inventory

## Backend Tests
*   **Framework:** `pytest`, `pytest-django`.
*   **Location:** `backend/sims/` (e.g., `tests.py`, `test_*.py`).
*   **Configuration:** `backend/pytest.ini` and `backend/conftest.py`. Coverage configured for `sims` app, ignoring `sims/_legacy`, `sims/cases/tests.py`, `sims/certificates/tests.py`, `sims/logbook/tests.py`.
*   **Types of tests found via config:** Django tests (`django.test.TestCase` or `pytest-django`). Includes API tests since DRF is heavily used.

## Frontend Tests
*   **Framework:** `jest`, `@testing-library/react`. End-to-end via `playwright` (`@playwright/test`).
*   **Location:** `frontend/` (Jest for unit/component, Playwright for E2E).
*   **Scripts:** `npm run test` (Jest), `npm run test:e2e` (Playwright with multiple projects: smoke, workflow-gate, active-surface, etc.).

## Android Tests
*   **Framework/Source:** Discovered `android/` directory at root. Configured via gradle. Modules: `app-companion`, `core`.

## Environment Tooling
*   **Docker:** Used for production deployment via `docker/docker-compose.yml`. Provides `db` (Postgres 15), `redis`, `backend` (Django+Gunicorn), `worker` (Celery), `beat` (Celery beat), and `frontend` (Next.js standalone).
