# MASTER FRONTEND/BACKEND TRUTH MAP

## Overview
Reconciliation of Session A confirms that the API contract between the frontend and backend is fundamentally sound. The frontend paths successfully map to the appropriate backend routers.

## Route Mappings
* `/api/academics/training-records/` maps to `sims.academics.workflow_urls`
* `/api/rotations/` maps to `sims.training.urls` under the `api/` path
* `/api/auth/` and `/api/users/` function as expected.

## Discrepancies
* Session A's reported API contract drifts for `/api/academics/` and `/api/rotations/` were false positives caused by static analysis limitations. Resolving paths dynamically validates the contract.
* Dead routes mapping to dummy HTML templates still exist but do not affect active API integrations.
