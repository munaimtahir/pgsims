# RBAC and Permissions Truth Map

## Identity and Auth Foundations
- **AUTH_USER_MODEL**: `users.User` (`backend/sims_project/settings.py:163`).
- **Role enum**: `admin`, `supervisor`, `pg`, `utrmc_user`, `utrmc_admin` (`backend/sims/users/models.py:9-15`).
- **Default DRF auth**: JWT + Session (`backend/sims_project/settings.py:287-290`).
- **Default DRF permission**: `IsAuthenticated` (`backend/sims_project/settings.py:291-294`).

## Role Semantics in Model Layer
`users.User` exposes role helpers used broadly in decorators/views:
- `is_admin()`, `is_supervisor()`, `is_pg()`, `is_utrmc_user()`, `is_utrmc_admin()` (`backend/sims/users/models.py:225-243`).
- Validation enforces role-specific constraints (PG requires supervisor/year/specialty, UTRMC users cannot have supervisors) (`backend/sims/users/models.py:176-207`).

## Shared DRF Permission Classes (`backend/sims/common_permissions.py`)
- `IsPGUser`: PG-only access (`36-46`).
- `IsUTRMCAdminUser`: UTRMC admin-only (`48-57`).
- `CanViewPendingLogbookQueue`: supervisor/admin/utrmc_user/utrmc_admin (`60-75`).
- `CanVerifyLogbookEntry`: supervisor/admin with object-scope check (supervisor must own PG assignment) (`78-103`).
- `CanApproveRotationOverride`: utrmc_admin-only (`106-115`).
- `ReadAnyWriteAdminOrUTRMCAdmin`, `ReadAnyWriteAdminOnly`, `ReadAnyWriteUTRMCAdmin`: read/write split by role (`118-166`).
- Denials are tracked via analytics (`auth.rbac.denied`) in `_track_rbac_denied` (`17-33`).

## View Decorators and Mixins (`backend/sims/users/decorators.py`)
- Function decorators: `admin_required`, `supervisor_required`, `pg_required`, `supervisor_or_admin_required`.
- Class mixins: `AdminRequiredMixin`, `SupervisorRequiredMixin`, `PGRequiredMixin`, `SupervisorOrAdminRequiredMixin`, `RoleBasedAccessMixin`.
- All denied checks raise `PermissionDenied` and emit analytics events.

## API-Level Enforcement Patterns (selected)
- **Logbook verify**: `CanVerifyLogbookEntry` + object-level assignment scope (`backend/sims/logbook/api_views.py:95-123`, `backend/sims/common_permissions.py:93-103`).
- **Cases review**: role and supervisor ownership checks inline (`backend/sims/cases/api_views.py:151-156`).
- **Rotations override approval**: `IsUTRMCAdminUser` + `CanApproveRotationOverride` (`backend/sims/rotations/api_views.py:131`).
- **Academics filtering**: queryset scoping by role in `StudentProfileViewSet.get_queryset()` (`backend/sims/academics/views.py:56-68`).

## Capability Matrix (truth from code)
| Capability | pg | supervisor | admin | utrmc_user | utrmc_admin |
|---|---:|---:|---:|---:|---:|
| Create/edit own logbook draft/returned | ✅ | ❌ | ❌ (API path is PG endpoint) | ❌ | ❌ |
| Verify logbook pending entries | ❌ | ✅ (assigned PG only) | ✅ | ❌ | ❌ |
| View pending logbook queue | ❌ | ✅ | ✅ | ✅ (read oversight) | ✅ |
| Create/submit own clinical cases | ✅ | ❌ | ❌ | ❌ | ❌ |
| Review submitted clinical cases | ❌ | ✅ (assigned PG only) | ✅ | ❌ | ✅ |
| Approve inter-hospital rotation override | ❌ | ❌ | ❌ | ❌ | ✅ |
| Write Department/Hospital master data via API | ❌ | ❌ | ✅ (or utrmc_admin for some rotation resources) | ❌ | ✅ (where `ReadAnyWriteAdminOrUTRMCAdmin`) |

## Groups/Custom Permission Codenames
- Logbook app seeds custom permission codenames (e.g., `can_approve_entries`, `can_export_entries`) in app startup (`backend/sims/logbook/apps.py:48-59`).
- Most operational API checks are role-driven rather than `has_perm`-driven.

## RBAC Gaps / Risks Observed
1. **Inconsistent style**: some endpoints rely on formal DRF permission classes, others use inline `if request.user.role ...` checks.
2. **UTRMC read-only role policy is endpoint-specific** (explicitly blocked in `CaseReviewActionView`, but not universally abstracted).
3. **Potential drift surface**: parallel RBAC logic exists in DRF permissions, Django decorators, admin classes, and template views.

