# Approval Workflow Inventory

| Workflow | Canonical model(s) | Submitter | Reviewer | States | UI route | API route | Classification |
|---|---|---|---|---|---|---|---|
| Academic logbook | `academics.LogbookEntry`, `LogbookReview`, `SupervisorReviewQueueItem` | Resident | Assigned supervisor/admin | Draft, Submitted, Verified, Returned, Rejected | `/academics/logbook`, `/academics/logbook/[id]/review` | `/api/academics/logbook-entries/` and `submit`, `verify`, `return_revision`, `reject` actions | Fully implemented |
| Evaluation/WBA | `academics.EvaluationSubmission`, `EvaluationResponse`, `SupervisorReviewQueueItem` | Resident/admin | Assigned supervisor/admin | Draft, Submitted, Under Review, Approved, Returned, Rejected | `/academics/evaluations`, `/academics/evaluations/[id]/review` | `/api/academics/evaluation-submissions/` actions | Fully implemented |
| Research project/synopsis | `training.ResidentResearchProject` | Resident | Assigned supervisor/admin, then university/admin | Draft, Submitted to Supervisor, Approved by Supervisor, Submitted to University, Accepted | `/academics/my-progress` and supervisor API | `/api/training/my/research/action/<action>/`, `/api/training/supervisor/research-approvals/` | Partially implemented UI; backend workflow implemented |
| Resident onboarding/profile review | `users.ResidentProfile` | Resident | Admin | Pending Review, Approved, Correction Required | Resident/admin profile screens | `/api/users/resident-profiles/<user_id>/approve-onboarding/` and correction action | Fully implemented |
| Resident document review | `users.ResidentDocument`, `ResidentDocumentRequirement` | Resident | Admin | Not Started, Uploaded, Pending Review, Verified, Reupload Required | Resident documents | `/api/users/resident-documents/<id>/upload/`, `review/` | Implemented, but no active document requirements exist in target DB |
| Rotation approval/completion | `training.RotationAssignment`, `RotationCompletion` | Admin/resident workflow | Admin/UTRMC (legacy HOD-compatible actions) | Draft, Submitted, Approved, Active, Completed, Returned, Rejected | `/academics/rotation-assignments` | `/api/training/rotations/` actions and completion verification | Fully implemented; not supervisor queue routed |
| Leave approval | `training.LeaveRequest` | Resident/admin | Admin/UTRMC | Draft, Submitted, Approved, Rejected | `/academics/leave-requests` | `/api/training/leaves/` actions | Fully implemented; not supervisor queue routed |
| Deputation/off-service approval | `training.DeputationPosting` | Admin workflow | Admin/UTRMC | Submitted, Approved, Rejected, Completed | No dedicated live supervisor screen | `/api/training/postings/` actions | Backend implemented |
| Workshop completion | `training.ResidentWorkshopCompletion` | Resident/admin import | None | Completion date/source | Resident academic baseline | `/api/training/my/workshops/` | Data-only; no approval workflow |
| Synopsis/thesis submission completeness | `training.ResidentSubmission`, `SubmissionDocument`, `SubmissionReview` | Resident | Supervisor/admin | Draft, Submitted, Under Review, Returned, Verified, Certificate Issued | No dedicated supervisor page currently exposed | `/api/training/submissions/synopsis/` and thesis equivalents | Backend implemented; not seeded where no submission requirements exist |

The seeder targets the active assigned MS Urology cohort and uses the actual academic
logbook/evaluation services so queue rows and audit events are generated normally. It also
creates marked research and leave examples where the existing resident training spine permits
them. It does not invent workshop approvals or identity-document evidence.
