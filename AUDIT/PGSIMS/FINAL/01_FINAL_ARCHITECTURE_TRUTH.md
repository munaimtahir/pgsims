# FINAL ARCHITECTURE TRUTH MAP

## Routing Findings Reconciliation

### F-A-001: `/api/academics/` Contract Drift
* **Session A Claim:** Frontend queries `/api/academics/training-records/` but backend defines `sims.training` URLs.
* **Session D Verification:** FRESH REPRODUCTION reveals that `sims_project.urls.py` correctly mounts `sims.academics.workflow_urls` at `/api/academics/`. Furthermore, `resolve('/api/academics/training-records/')` correctly maps to `ResidentTrainingRecordViewSet` internally in the `sims.academics` module.
* **Conclusion:** This was a FALSE POSITIVE in Session A static analysis. The frontend paths match actual backend behavior.

### F-A-002: Dead Code (Dummy Routes)
* **Session A Claim:** Obsolete dummy routes in backend mapping to HTML templates (`cases`, `logbook`, `certificates`).
* **Session D Verification:** Verified in `sims_project.urls.py`. `cases_dummy_urls.py` etc are still mounted.
* **Conclusion:** CONFIRMED as P3 Technical Debt.

### F-A-003: Orphan Routes
* **Conclusion:** CONFIRMED as P3 Technical Debt. No action required for production readiness.

### F-A-004: Middleware / API Rotations Mismatch
* **Session A Claim:** `/api/rotations/` in frontend vs backend.
* **Session D Verification:** Frontend calls `/api/rotations/`. `sims_project.urls.py` delegates `/api/` to `sims.training.urls`, which mounts `RotationAssignmentViewSet` under the route `rotations/` inside `api/`. Therefore, `/api/rotations/` resolves correctly to `sims.training.views.RotationAssignmentViewSet`. The top-level `/rotations/` path points to `sims.rotations.urls` (legacy dummy redirect).
* **Conclusion:** The API surface `/api/rotations/` perfectly aligns. Session A's claim of a Frontend Defect is FALSE POSITIVE.
