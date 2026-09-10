# WORKFLOW MATRIX

The audit reviewed three major workflow engines: Logbook, Submissions (Synopsis/Thesis), and Onboarding.

| Workflow | Role | Required State | Action | Next State | Verified Enforcement |
|----------|------|----------------|--------|------------|----------------------|
| Synopsis Submit | Resident | DRAFT | Submit | UNDER_REVIEW/SUBMITTED | YES |
| Synopsis Review | Supervisor | SUBMITTED | Start Review | UNDER_REVIEW | YES |
| Synopsis Return | Supervisor | UNDER_REVIEW | Return | RETURNED | YES |
| Synopsis Verify | Supervisor | UNDER_REVIEW | Verify | CERTIFICATE_ISSUED | YES |
| Document Upload | Resident | Any | Upload | Active | YES |

The API views (e.g. `_SubmissionSubmitBaseView` and `_SubmissionReviewActionBaseView`) strongly couple state transitions to HTTP requests. A Resident cannot submit a document that is already Under Review.
