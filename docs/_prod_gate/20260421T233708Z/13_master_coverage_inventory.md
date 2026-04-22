# Master Coverage Inventory

## A. Active Route / Page Inventory
| Route | Role(s) | Purpose | Visible nav | Primary CTA(s) | Dependent APIs | Status |
|---|---|---|---|---|---|---|
| `/login` | public | sign in | no | Sign in, forgot password | `/api/auth/login/` | tested |
| `/forgot-password` | public | password reset request | no | Send reset link | `/api/auth/password-reset/` | tested |
| `/register` | public | disabled registration notice | no | Back/sign-in link | none | tested |
| `/unauthorized` | public | access denied | no | none | none | tested |
| `/dashboard` | authenticated | role redirect | no | redirect | auth cookies/profile | tested |
| `/dashboard/resident` | resident/pg | resident dashboard | yes | schedule/logbook links | `/api/dashboard/resident/`, `/api/residents/me/summary/` | tested |
| `/dashboard/resident/schedule` | resident/pg | schedule and leave | yes | Save Draft, Submit for Review | `/api/my/rotations/`, `/api/my/leaves/`, `/api/leaves/`, `/api/leaves/{id}/submit/` | tested |
| `/dashboard/resident/progress` | resident/pg | logbook | yes | Save Draft, Submit Logbook | `/api/logbook/`, `/api/logbook/{id}/submit/`, `/api/logbook/my-threshold/` | tested |
| `/dashboard/supervisor` | supervisor | approval queues | yes | approve/return logbook, approve/reject leave | `/api/dashboard/supervisor/`, `/api/logbook/review-queue/`, `/api/utrmc/approvals/leaves/` | tested |
| `/dashboard/supervisor/residents/[id]/progress` | supervisor | resident detail progress | linked from data | Back | `/api/supervisors/residents/{id}/progress/` | not fully tested |
| `/dashboard/utrmc` | UTRMC admin/user | overview | yes | rotation/admin bulk/data quality actions | many UTRMC APIs | partially tested |
| `/dashboard/utrmc/hospitals` | UTRMC admin/user | hospitals | yes | Add Hospital | `/api/hospitals/` | partially tested |
| `/dashboard/utrmc/departments` | UTRMC admin/user | departments | yes | Add Department | `/api/departments/` | partially tested |
| `/dashboard/utrmc/departments/[id]/roster` | UTRMC admin/user | roster | linked | none | `/api/departments/{id}/roster/` | not fully tested |
| `/dashboard/utrmc/matrix` | UTRMC admin/user | hospital-department matrix | yes | toggle matrix cells | `/api/hospital-departments/` | partially tested |
| `/dashboard/utrmc/users` | UTRMC admin/user | users | yes | Add User | `/api/users/` | partially tested |
| `/dashboard/utrmc/supervision` | UTRMC admin/user | supervision links | yes | add/edit links | `/api/supervision-links/` | partially tested |
| `/dashboard/utrmc/hod` | UTRMC admin/user | HOD assignment | yes | assign HOD | `/api/hod-assignments/` | not fully tested |
| `/dashboard/utrmc/programs` | UTRMC admin/user | programs | yes | add/remove template, policy/milestones | `/api/programs/`, `/api/program-templates/` | partially tested |
| `/dashboard/utrmc/eligibility-monitoring` | UTRMC admin/user | eligibility | yes | filters | `/api/utrmc/eligibility/` | partially tested |
| `/dashboard/utrmc/data-quality` | UTRMC admin | data-quality repair | CTA | recompute/patch | `/api/admin/data-quality/*` | not fully tested |

## B. Active API Inventory
Active APIs were inventoried from frontend API calls and backend URLs. Coverage is partial: auth, dashboard, leave, logbook, UTRMC read-only, userbase, bulk dry-run, and role denials are tested; not every UTRMC detail endpoint and CTA mutation is fully tested.

## C. Workflow Inventory
| Workflow | Roles | Valid transitions | Invalid transitions | Status |
|---|---|---|---|---|
| Auth/login/logout/profile | all active | login -> dashboard | invalid credentials, unauthenticated route | tested |
| Resident leave | resident, supervisor | draft -> submitted -> approved | unauthenticated/wrong role | tested |
| Logbook | resident, supervisor | draft -> submitted -> returned -> resubmitted -> approved | unrelated supervisor blocked | tested |
| UTRMC read-only | UTRMC user | read pages only | mutation controls hidden/denied | tested |
| UTRMC admin CRUD cluster | UTRMC admin | create/edit/import actions | read-only denial | partially tested |

## D. Role-Permission Matrix
See `17_role_route_action_matrix.md`.

## E. CTA Inventory
See `20_cta_coverage_report.md`.

## F. Infra / Release Path Inventory
Install, build, migrate, seed, boot, restart, smoke after restart, artifact/report generation were exercised. Code coverage thresholds failed.

