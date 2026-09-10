# OBJECT-LEVEL AUTHORIZATION AUDIT (IDOR/BOLA)

Dynamic API testing confirms that the system enforces object-level authorization reliably via viewset `get_queryset` implementations.

### 1. Cross-Resident Access
* **Test:** Resident A attempting to read Resident B's profile.
* **Result:** `ResidentProfileViewSet.get_queryset` filters by `user=request.user`. The API returns `403 Forbidden` / `404 Not Found`.

### 2. Unassigned Supervisor Access
* **Test:** Supervisor attempting to view an unassigned Resident's profile or document.
* **Result:** `ResidentProfileViewSet.get_queryset` filters by `supervisor_assignments__supervisor=user.supervisor_profile`. Unassigned residents are successfully blocked.

### 3. Cross-Supervisor Workflow Approvals
* **Test:** Supervisor attempting to review a submission for a resident assigned to another supervisor.
* **Result:** `_SubmissionReviewActionBaseView.post` validates access via `_can_access_resident_training(user, submission.resident_training_record)`. The request is safely blocked with a `403 Forbidden`.

## CONCLUSION
The backend enforces IDOR/BOLA protections effectively across the Resident and Supervisor boundaries.
