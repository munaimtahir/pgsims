# OUT/122_ROTATIONS_RBAC_MATRIX.md

## RBAC Matrix — Training & Rotations Module

| Action | admin | utrmc_admin | utrmc_user | supervisor/faculty | pg/resident |
|---|:---:|:---:|:---:|:---:|:---:|
| Programs CRUD | ✅ | ✅ | 🔴 | 🔴 | 🔴 |
| Templates CRUD | ✅ | ✅ | 🔴 | 🔴 | 🔴 |
| ResidentTrainingRecord CRUD | ✅ | ✅ | 🔴 | 🔴 (read own) | 🔴 (read own) |
| Create RotationAssignment | ✅ | ✅ | 🔴 | 🔴 | 🔴 |
| Submit rotation | ✅ | ✅ | 🔴 | 🔴 | ✅ (own only) |
| HOD Approve rotation | ✅ | ✅ | 🔴 | ✅ (dept-scoped) | 🔴 |
| UTRMC Approve rotation | ✅ | ✅ | 🔴 | 🔴 | 🔴 |
| Return/Reject rotation | ✅ | ✅ | 🔴 | ✅ (dept-scoped) | 🔴 |
| Activate/Complete rotation | ✅ | ✅ | 🔴 | 🔴 | 🔴 |
| View RotationApprovalInbox | ✅ | ✅ | 🔴 | ✅ (dept-scoped) | 🔴 |
| Create LeaveRequest | ✅ | ✅ | 🔴 | 🔴 | ✅ (own) |
| Submit leave | ✅ | ✅ | 🔴 | 🔴 | ✅ (own) |
| Approve/Reject leave | ✅ | ✅ | 🔴 | ✅ (supervisee-scoped) | 🔴 |
| Create DeputationPosting | ✅ | ✅ | 🔴 | 🔴 | ✅ (own) |
| Approve/Reject/Complete posting | ✅ | ✅ | 🔴 | ✅ (supervisee-scoped) | 🔴 |
| View My Rotations/Leaves | 🔴 | 🔴 | 🔴 | 🔴 | ✅ (own only) |
| Supervisor Pending Rotations | ✅ | ✅ | 🔴 | ✅ (dept-scoped) | 🔴 |

## Department Scoping Logic

Supervisors/HOD see only items in departments where they have:
- `HODAssignment.hod_user = user AND active=True`, OR
- `DepartmentMembership.user = user AND active=True`

Leave/posting scoping uses `SupervisorResidentLink.supervisor_user = user AND active=True`.
