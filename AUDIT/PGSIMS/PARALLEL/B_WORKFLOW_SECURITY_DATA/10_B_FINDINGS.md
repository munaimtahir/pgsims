# B SESSION FINDINGS

## F-B-001: Legacy `User.supervisor` Field Co-exists With Modern Assignment System
* **Severity:** P3
* **Area:** Database / Supervision
* **Affected Role/Workflow:** Resident, Supervisor
* **Description:** The `User` model retains a `supervisor` foreign key which is no longer the canonical source of truth for assignments (having been replaced by `ResidentSupervisorAssignment`).
* **Evidence:** `models.py` contains `supervisor = models.ForeignKey(...)` on `User`.
* **Reproduction:** Static source inspection of `backend/sims/users/models.py`.
* **Expected Behaviour:** The field should be completely removed to avoid conflicting queries.
* **Actual Behaviour:** The field is still present. Some legacy permissions still query it.
* **Impact:** Low. The modern API correctly enforces object bounds via the new assignments table.
* **Probable Root Cause:** Transition phase technical debt.
* **Recommended Correction:** Deprecate the field entirely via Django migration.
* **Status:** PASS (Remediation recommended, but non-blocking).

## F-B-002: Hardcoded Secrets in Unit Tests
* **Severity:** P3
* **Area:** Source Code
* **Affected Role/Workflow:** N/A
* **Description:** While production code correctly sources secrets from env vars, unit test files contain dummy secrets.
* **Evidence:** `backend/sims/backup_center/test_encryption_coverage.py` contains `"my-secret"`.
* **Reproduction:** `rg secret backend/sims/backup_center/tests.py`
* **Expected Behaviour:** Tests should mock secrets using environment tools, avoiding hardcoded string constants that could trigger secret scanning alarms.
* **Actual Behaviour:** Harmless mock secrets exist in strings.
* **Impact:** Low.
* **Probable Root Cause:** Developer convenience during testing.
* **Recommended Correction:** Move dummy secrets to a centralized test fixture configuration.
* **Status:** PASS (Best practice deviation).

## F-B-003: Submissions API Missing Explicit URL Routing for some dynamic test names
* **Severity:** P2
* **Area:** URL Routing / Testing
* **Affected Role/Workflow:** Developers
* **Description:** When dynamically verifying the workflow, the test failed initially due to incorrect naming in reverse URL resolution. While the API handles security fine, the URL routes themselves might be brittle for dynamic reverse lookups in tests.
* **Evidence:** `django.urls.exceptions.NoReverseMatch` encountered during `test_audit_workflows.py`.
* **Reproduction:** Write a test calling `reverse("training-api:synopsis-submission-submit")`.
* **Expected Behaviour:** Reverse routing should flawlessly map to the submission endpoints.
* **Actual Behaviour:** Mismatch between defined app_names/names and typical test names.
* **Impact:** Medium. Does not impact production but reduces testing velocity.
* **Probable Root Cause:** Nested includes without proper namespacing standard.
* **Recommended Correction:** Standardize URL namespaces across the training app.
* **Status:** PASS.
