# STATE MACHINE TRANSITION AUDIT

## TRANSITION RULES

Dynamic testing confirmed that state transitions cannot be arbitrarily bypassed.

### Scenario 1: Submitting a Synopsis outside of DRAFT state
* **Test:** Sent a POST to `/api/submissions/synopsis/submit/` while the submission was artificially set to `UNDER_REVIEW` in the database.
* **Result:** Blocked by API: `"Cannot submit from status UNDER_REVIEW."`

### Scenario 2: Starting review on a DRAFT submission
* **Test:** Supervisor sends a POST to `/api/submissions/synopsis/<id>/review/` with action `start-review` when the submission is in `DRAFT`.
* **Result:** Blocked by API: `"Cannot start review from status DRAFT."`

State enforcement is robust and strictly tied to business rules.
