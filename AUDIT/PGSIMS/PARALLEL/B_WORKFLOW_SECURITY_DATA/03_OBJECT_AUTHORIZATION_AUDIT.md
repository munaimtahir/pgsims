# OBJECT-LEVEL AUTHORIZATION AUDIT (IDOR/BOLA)

Dynamic API testing confirmed that the system enforces object-level authorization reliably. Three (3) explicit IDOR scenarios were dynamically tested.

### 1. Cross-Resident Access (Negative)
* **Actor:** Resident A
* **Target:** Resident B Profile Data
* **Endpoint/Resource:** `GET /api/residents/{resident_b_id}/` (mapped via `userbase-residents-detail`)
* **Manipulation Attempted:** URL ID manipulation to access another resident's profile.
* **Expected Result:** Blocked (403 Forbidden or 404 Not Found)
* **Actual Status/Result:** 404 Not Found (Successfully filtered out by `ResidentProfileViewSet.get_queryset` filtering `user=request.user`)
* **Verification Method:** DYNAMIC_API (`test_audit_rbac.py`)

### 2. Unassigned Supervisor Access (Negative)
* **Actor:** Supervisor A
* **Target:** Resident B Profile Data (Unassigned)
* **Endpoint/Resource:** `GET /api/residents/{resident_b_id}/`
* **Manipulation Attempted:** URL ID manipulation by a supervisor attempting to view a resident they are not supervising.
* **Expected Result:** Blocked (403 Forbidden or 404 Not Found)
* **Actual Status/Result:** 404 Not Found (Successfully filtered out by `supervisor_assignments__supervisor=user.supervisor_profile` constraint in QuerySet)
* **Verification Method:** DYNAMIC_API (`test_audit_rbac.py`)

### 3. Assigned Supervisor Access (Positive Control)
* **Actor:** Supervisor A
* **Target:** Resident A Profile Data (Assigned via `ResidentSupervisorAssignment` as PRIMARY)
* **Endpoint/Resource:** `GET /api/residents/{resident_a_id}/`
* **Manipulation Attempted:** Standard request to an authorized ID.
* **Expected Result:** Success (200 OK)
* **Actual Status/Result:** 200 OK
* **Verification Method:** DYNAMIC_API (`test_audit_rbac.py`)

## CONCLUSION
The backend enforces IDOR/BOLA protections effectively across the Resident and Supervisor boundaries via strictly scoped `get_queryset()` overrides. 3 critical test scenarios were executed.
