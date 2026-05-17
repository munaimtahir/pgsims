# Backend API Truthmap

| API Route | View/ViewSet | App | Auth required | Role logic | Frontend consumer | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `/api/auth/login/` | `CustomTokenObtainPairView` | `sims.users` | No | Login throttle only | `frontend/lib/api/auth.ts`, E2E auth helpers | Working |
| `/api/auth/refresh/` | `TokenRefreshView` | `sims.users` | No | None | `frontend/lib/api/auth.ts` | Working |
| `/api/auth/logout/` | `logout_view` | `sims.users` | Yes | Any authenticated user | `frontend/lib/api/auth.ts` | Working |
| `/api/auth/register/` | `register_view` | `sims.users` | No | Public registration disabled by settings in this baseline | `frontend/lib/api/auth.ts`, `frontend/app/register/page.tsx` | Partial |
| `/api/auth/me/` | `AuthMeView` | `sims.users` | Yes | None | auth bootstrapping | Working |
| `/api/auth/profile/` | `user_profile_view` | `sims.users` | Yes | None | `frontend/lib/api/auth.ts` | Working |
| `/api/auth/profile/update/` | `update_profile_view` | `sims.users` | Yes | None | `frontend/lib/api/auth.ts` | Working |
| `/api/hospitals/` | `HospitalViewSet` | `sims.users` | Yes | Writes require `IsTechAdmin`; reads are auth-only | `frontend/lib/api/userbase.ts`, UTRMC hospitals/overview | Working |
| `/api/hospitals/{id}/departments/` | `HospitalViewSet.departments` | `sims.users` | Yes | Auth only | `frontend/lib/api/userbase.ts` | Working |
| `/api/departments/` | `DepartmentViewSet` | `sims.users` | Yes | Writes require `IsTechAdmin`; reads are auth-only | `frontend/lib/api/userbase.ts`, UTRMC departments/overview | Working |
| `/api/departments/{id}/roster/` | `DepartmentViewSet.roster` | `sims.users` | Yes | Auth plus roster-reader or membership check | UTRMC/PG roster pages | Working |
| `/api/hospital-departments/` | `HospitalDepartmentViewSet` | `sims.users` | Yes | Writes require manager/admin | `frontend/lib/api/userbase.ts`, UTRMC matrix | Working |
| `/api/users/` | `UserViewSet` | `sims.users` | Yes | Non-roster readers only see themselves; writes require manager/admin | `frontend/lib/api/userbase.ts`, UTRMC users | Working |
| `/api/residents/` | `ResidentProfileViewSet` | `sims.users` | Yes | Role/membership scoped | `frontend/lib/api/userbase.ts` | Working |
| `/api/staff/` | `StaffProfileViewSet` | `sims.users` | Yes | Role/membership scoped | backend-only / sparse frontend use | Working |
| `/api/department-memberships/` | `DepartmentMembershipViewSet` | `sims.users` | Yes | Manager/admin for writes | `frontend/lib/api/userbase.ts` | Working |
| `/api/hospital-assignments/` | `HospitalAssignmentViewSet` | `sims.users` | Yes | Manager/admin for writes | `frontend/lib/api/userbase.ts` | Working |
| `/api/supervision-links/` | `SupervisionLinkViewSet` | `sims.users` | Yes | Manager/admin for writes | `frontend/lib/api/userbase.ts`, UTRMC supervision | Working |
| `/api/hod-assignments/` | `HODAssignmentViewSet` | `sims.users` | Yes | Manager/admin for writes | `frontend/lib/api/userbase.ts`, UTRMC hod | Working |
| `/api/admin/data-quality/summary` | `DataQualitySummaryView` | `sims.users` | Yes | Admin/UTRMC-admin only | `frontend/lib/api/userbase.ts`, UTRMC overview/data-quality | Working |
| `/api/admin/data-quality/users` | `DataQualityUsersView` | `sims.users` | Yes | Admin/UTRMC-admin only | `frontend/lib/api/userbase.ts`, UTRMC data-quality | Working |
| `/api/admin/data-quality/recompute` | `DataQualityRecomputeView` | `sims.users` | Yes | Admin/UTRMC-admin only | `frontend/lib/api/userbase.ts`, UTRMC data-quality | Working |
| `/api/admin/data-quality/audit` | `DataCorrectionAuditView` | `sims.users` | Yes | Admin/UTRMC-admin only | `frontend/lib/api/userbase.ts`, UTRMC data-quality | Working |
| `/api/programs/` | `TrainingProgramViewSet` | `sims.training` | Yes | Admin/UTRMC-admin only for writes; list is role-scoped | `frontend/lib/api/training.ts`, Programs page | Working |
| `/api/programs/{id}/policy/` | `ProgramPolicyView` | `sims.training` | Yes | Admin/UTRMC-admin only | `frontend/lib/api/training.ts`, Programs page | Working |
| `/api/programs/{id}/milestones/` | `ProgramMilestoneViewSet` | `sims.training` | Yes | Admin/UTRMC-admin only | `frontend/lib/api/training.ts`, Programs page | Working |
| `/api/program-templates/` | `ProgramRotationTemplateViewSet` | `sims.training` | Yes | Admin/UTRMC-admin only | `frontend/lib/api/training.ts`, Programs page | Working |
| `/api/resident-training/` | `ResidentTrainingRecordViewSet` | `sims.training` | Yes | Scoped by role | UTRMC overview | Working |
| `/api/rotations/` | `RotationAssignmentViewSet` | `sims.training` | Yes | Scoped by role | resident/supervisor/UTRMC workflow pages | Working |
| `/api/leaves/` | `LeaveRequestViewSet` | `sims.training` | Yes | Scoped by role | resident/supervisor workflow pages | Working |
| `/api/postings/` | `DeputationPostingViewSet` | `sims.training` | Yes | Scoped by role | UTRMC postings | Working |
| `/api/workshops/` | `WorkshopViewSet` | `sims.training` | Yes | Scoped by role | resident workflows | Working |
| `/api/logbook/` | `LogbookEntryViewSet` | `sims.training` | Yes | Residents only for resident actions; supervisor reviews are separate actions | resident/supervisor pages | Working |
| `/api/logbook/review-queue/` | `LogbookReviewQueueView` | `sims.training` | Yes | Supervisor/admin scope | supervisor dashboard | Working |
| `/api/logbook/my-threshold/` | `LogbookMyThresholdView` | `sims.training` | Yes | Resident scope | resident progress page | Working |
| `/api/submissions/requirements/` | `SubmissionRequirementTemplateViewSet` | `sims.training` | Yes | Scoped by role | resident progress page | Working |
| `/api/submissions/synopsis/` | `SynopsisSubmissionView` | `sims.training` | Yes | Resident scope | deferred resident research workflow | Working |
| `/api/submissions/thesis/` | `ThesisSubmissionView` | `sims.training` | Yes | Resident scope | deferred resident thesis workflow | Working |
| `/api/submissions/certificates/` | `SubmissionCertificatesView` | `sims.training` | Yes | Scoped by role | UTRMC overview | Working |
| `/api/rotations/completions/` | `RotationCompletionsView` | `sims.training` | Yes | Scoped by role | UTRMC overview | Working |
| `/api/rotations/completions/{id}/verify/` | `RotationCompletionVerifyView` | `sims.training` | Yes | UTRMC/admin only | UTRMC overview | Working |
| `/api/residents/me/summary/` | `ResidentSummaryView` | `sims.training` | Yes | Resident access required; admin/UTRMC-admin fallback allowed | resident dashboard | Working |
| `/api/supervisors/me/summary/` | `SupervisorSummaryView` | `sims.training` | Yes | Supervisor/HOD or admin/UTRMC-admin | supervisor dashboard | Working |
| `/api/supervisors/residents/{resident_id}/progress/` | `SupervisorResidentProgressView` | `sims.training` | Yes | Supervisor/HOD or admin/UTRMC-admin | hidden supervisor progress page | Working |
| `/api/dashboard/resident/` | `ResidentOperationalDashboardView` | `sims.training` | Yes | Residents only | resident progress + resident dashboard logic | Working |
| `/api/dashboard/supervisor/` | `SupervisorOperationalDashboardView` | `sims.training` | Yes | Supervisor/HOD or admin/UTRMC-admin | supervisor dashboard | Working |
| `/api/dashboard/hod/` | `HODOperationalDashboardView` | `sims.training` | Yes | HOD only | backend-only; no frontend route exists | Working |
| `/api/dashboard/utrmc/` | `UTRMCOperationalDashboardView` | `sims.training` | Yes | UTRMC viewer only | UTRMC overview | Working |
| `/api/utrmc/approvals/rotations/` | `RotationApprovalInboxView` | `sims.training` | Yes | UTRMC/admin only | UTRMC overview | Working |
| `/api/utrmc/approvals/leaves/` | `LeaveApprovalInboxView` | `sims.training` | Yes | UTRMC/admin only | supervisor dashboard | Working |
| `/api/utrmc/eligibility/` | `UTRMCEligibilityView` | `sims.training` | Yes | UTRMC/admin only | UTRMC eligibility page | Working |
| `/api/supervisor/rotations/pending/` | `SupervisorPendingRotationsView` | `sims.training` | Yes | Supervisor/HOD or admin/UTRMC-admin | hidden supervisor workflow | Working |
| `/api/supervisor/research-approvals/` | `SupervisorResearchApprovalsView` | `sims.training` | Yes | Supervisor/HOD or admin/UTRMC-admin | supervisor research approvals page | Working |
| `/api/my/rotations/` | `MyRotationsView` | `sims.training` | Yes | Resident scope | resident schedule page | Working |
| `/api/my/leaves/` | `MyLeavesView` | `sims.training` | Yes | Resident scope | resident schedule page | Working |
| `/api/my/research/` | `ResidentResearchProjectView` | `sims.training` | Yes | Resident scope | deferred resident research page | Working |
| `/api/my/thesis/` | `ResidentThesisView` | `sims.training` | Yes | Resident scope | deferred resident thesis page | Working |
| `/api/my/workshops/` | `MyWorkshopCompletionsView` | `sims.training` | Yes | Resident scope | deferred resident workshop page | Working |
| `/api/my/eligibility/` | `MyEligibilityView` | `sims.training` | Yes | Resident scope | resident progress page | Working |
| `/api/system/settings/` | `SystemSettingsView` | `sims.training` | Yes | Scoped by role | UTRMC overview | Working |
| `/api/bulk/*` | bulk views | `sims.bulk` | Yes | Usually admin/UTRMC-admin | imported through overview/BulkSetupWorkspace | Working |
| `/api/notifications/*` | notification views | `sims.notifications` | Yes | Recipient-scoped | notification UI not currently surfaced in the main nav | Working |
| `/api/audit/activity/*` | audit viewsets | `sims.audit` | Yes | Admin/oversight scope | backend-only | Working |

## Backend Truthmap Notes

- Main URL config: [`backend/sims_project/urls.py`](/home/munaim/srv/apps/pgsims/backend/sims_project/urls.py)
- Training route family: [`backend/sims/training/urls.py`](/home/munaim/srv/apps/pgsims/backend/sims/training/urls.py)
- Org/userbase route family: [`backend/sims/users/userbase_urls.py`](/home/munaim/srv/apps/pgsims/backend/sims/users/userbase_urls.py)
- Auth route family: [`backend/sims/users/api_urls.py`](/home/munaim/srv/apps/pgsims/backend/sims/users/api_urls.py)
- The live admin token can access UTRMC and supervisor operational dashboards, but resident-specific endpoints reject it

