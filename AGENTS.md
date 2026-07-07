# AGENTS.md — PGMS Clean-Room Agent Operating Rules

## Project

PGMS / PGR SIMS is a clean-room postgraduate management system.

All agents must treat this file as a binding instruction file before making code, migration, frontend, backend, documentation, or test changes.

---

## 1. Active Workspace Boundary

The active codebase is:

```text
/home/munaim/srv/apps/pgsims/
```

### Mandatory rule

Agents must work directly in this project (fixing and updating it rather than making a new `pgms/` subfolder). All references to `pgms/` in the guides or scripts logically refer to this active project directory `/home/munaim/srv/apps/pgsims/`.

There is no `pgms-workspace/` or `pgsims-legacy/` folder anymore.

---

## 2. Deleted / Forbidden Legacy PGMS Folders and Modules

The following old PGMS/PGSIMS-style modules are not part of the new clean-room foundation unless a future brick explicitly reintroduces them:

```text
legacy onboarding modules
legacy HOD modules
legacy placement modules
legacy rotation modules
legacy evaluation modules
legacy logbook modules
legacy backup/restore modules
legacy Google bridge modules
legacy AdminOps modules
legacy Google Drive connector modules
legacy hidden dashboard modules
legacy copied import modules
legacy old user/category modules
```

Do not recreate deleted folders just because old routes, imports, or references fail.

If a deleted folder is referenced by current code, fix the reference by aligning the code to the new PGMS architecture.

---

## 3. Current Sprint: Update 0 Identity Cleanup

The active architectural decision is:

```text
Update 0 = Universal Identity + Profile Synchronization + HOD Cleanup + Dynamic Onboarding
```

Do not proceed to Resident-Supervisor Mapping, rotations, evaluations, logbooks, backup, bridge integrations, or monitoring dashboards until Update 0 is complete and marked GO.

---

## 4. Final Role System

Only four roles are allowed:

```text
ADMIN
RESIDENT
SUPERVISOR
SUPPORT_STAFF
```

Remove or migrate away from:

```text
UTRMC_ADMIN
HOD
TEACHER
FACULTY
STUDENT
PGR
TRAINEE
CLERK
OFFICE_STAFF
DATA_ENTRY
SUPER_ADMIN
SYSTEM_ADMIN
```

Mapping rule:

```text
UTRMC_ADMIN / SUPER_ADMIN / SYSTEM_ADMIN -> ADMIN
TEACHER / FACULTY -> SUPERVISOR
STUDENT / PGR / TRAINEE -> RESIDENT
CLERK / OFFICE_STAFF / DATA_ENTRY -> SUPPORT_STAFF
HOD -> not a role; preserve only as designation text if needed
```

No backend choice, frontend dropdown, badge, filter, permission guard, test fixture, seed data, route, or documentation page should expose old roles.

---

## 5. HOD Is Not a Separate Identity

HOD must not exist as:

```text
role
user category
profile type
model
API endpoint
frontend route
sidebar item
directory
permission category
dashboard
import type
```

Allowed future representation only:

```text
SupervisorProfile.designation = "HOD"
```

or a future separate brick:

```text
DepartmentHeadAssignment
```

Do not build DepartmentHeadAssignment now.

---

## 6. Universal User Creation

The new locked rule is:

```text
/users/new is the universal identity creation center.
```

`/users/new` must allow creating users with only these four roles:

```text
ADMIN
RESIDENT
SUPERVISOR
SUPPORT_STAFF
```

When a role is selected, the backend must create:

```text
User + correct linked Profile + AuditLog
```

in the same database transaction.

Role-to-profile mapping:

```text
ADMIN -> AdminProfile
RESIDENT -> ResidentProfile
SUPERVISOR -> SupervisorProfile
SUPPORT_STAFF -> SupportStaffProfile
```

The old rule is deleted:

```text
/users/new is only for support staff/admin.
Residents must be created only from /residents/new.
Supervisors must be created only from /supervisors/new.
```

Do not reintroduce this old rule.

---

## 7. Required Profile Models

The new foundation requires:

```text
AdminProfile
ResidentProfile
SupervisorProfile
SupportStaffProfile
```

Every profile must have a one-to-one link to User.

Every User must have exactly one correct role-specific profile.

No orphan User.
No orphan Profile.
No wrong role/profile link.
No duplicate role profile for one User.
No multiple role profiles for one User.

---

## 8. Service-Layer Rule

Do not create profiles through uncontrolled hidden post-save signals.

Use explicit service-layer logic with transactions.

Expected service pattern:

```python
create_user_with_profile(
    *,
    role,
    username=None,
    password=None,
    full_name,
    email=None,
    phone=None,
    profile_payload=None,
    actor=None,
    source="manual",
)
```

The service must:

```text
validate role
generate username if needed
set default temporary password if needed
create User
create linked Profile
set onboarding flags
calculate completion state
write AuditLog
return structured response
rollback all changes if any step fails
```

Use:

```python
transaction.atomic()
```

---

## 9. Default User Creation Rules

Default password:

```text
pgfmu123
```

New users default to:

```text
must_change_password = True
is_profile_complete = False
is_active = True
profile_status = INCOMPLETE
```

Username prefixes:

```text
ADMIN -> admin001, admin002...
RESIDENT -> pgr001, pgr002...
SUPERVISOR -> sup001, sup002...
SUPPORT_STAFF -> staff001, staff002...
```

The username generator must avoid duplicates and must be safe for future bulk import.

---

## 10. Dynamic Onboarding Rule

Onboarding is not only first login.

It is a permanent required-field completion system.

Whenever a new required field is added to any of these models:

```text
AdminProfile
ResidentProfile
SupervisorProfile
SupportStaffProfile
```

affected users must provide that missing data on their next login before accessing the main system.

The login state machine is:

```text
Login
-> if must_change_password=True, force /change-password
-> else if required profile fields are missing, force /complete-profile
-> else allow normal dashboard access
```

The backend must be the source of truth.

Frontend route guards must use backend state from:

```text
/api/auth/me/
```

---

## 11. Profile Completion Requirement Registry

Agents must implement and maintain a central backend profile-completion registry.

Each profile field must be classified as:

```text
required_for_onboarding = true
```

or:

```text
required_for_onboarding = false
```

When adding any field to AdminProfile, ResidentProfile, SupervisorProfile, or SupportStaffProfile, agents must document:

```text
is this field required for onboarding?
which role does it apply to?
should existing users complete it on next login?
what frontend input type is needed?
what label/help text appears on /complete-profile?
what backend validation is required?
does schema version need to increment?
what tests are required?
```

No required profile field may be added silently.

---

## 12. Profile Schema Versioning

Each profile model must support schema/version tracking or an equivalent robust mechanism.

Recommended fields:

```python
profile_schema_version = models.PositiveIntegerField(default=1)
completed_schema_version = models.PositiveIntegerField(default=0)
profile_completed_at = models.DateTimeField(null=True, blank=True)
```

When a new required field is added, increment the relevant role schema version.

Users with older completed schema versions must be rechecked at next login.

---

## 13. `/api/auth/me/` Must Return Onboarding State

`/api/auth/me/` must return:

```text
user id
username
role
must_change_password
is_profile_complete
profile_type
profile_id
profile_status
profile_schema_version
completed_schema_version
missing_required_fields
allowed_next_route
```

Route rule:

```text
must_change_password=True -> /change-password
missing required fields -> /complete-profile
complete -> dashboard
```

---

## 14. `/complete-profile` Must Be Dynamic

The `/complete-profile` page must render fields returned by backend.

It must not be hardcoded only for:

```text
full_name
phone
email
```

It must support role-specific required fields and future newly required fields.

---

## 15. Directory Page Rules

Keep these pages:

```text
/users
/users/new
/users/[id]
/residents
/residents/[id]
/supervisors
/supervisors/[id]
/support-staff
/support-staff/[id]
/admins
/admins/[id]
```

Purpose:

```text
/users = universal identity list and creation center
/residents = resident listing/detail/edit/completion/archive
/supervisors = supervisor listing/detail/edit/completion/archive
/support-staff = support staff listing/detail/edit
/admins = admin listing/detail/edit
```

Add Resident / Add Supervisor buttons may exist, but they must either open:

```text
/users/new?role=RESIDENT
/users/new?role=SUPERVISOR
```

or call the same shared identity service.

No duplicate creation logic.

---

## 16. Permissions

At this stage:

```text
ADMIN can create/manage all users and profiles.
SUPPORT_STAFF cannot create users unless a later permission assignment grants it.
RESIDENT can access own account/profile only.
SUPERVISOR can access own account/profile only until mapping workflows are built.
```

Permissions must be enforced in backend.

Frontend hiding alone is not sufficient.

---

## 17. Audit Requirements

Audit important identity and onboarding events.

Required action names include:

```text
USER_CREATED
PROFILE_CREATED
IDENTITY_CREATED
USER_UPDATED
PROFILE_UPDATED
IDENTITY_REPAIRED
ROLE_MIGRATED
HOD_REMOVED_OR_MIGRATED
PASSWORD_RESET
PASSWORD_CHANGED
PROFILE_COMPLETION_REQUIRED
PROFILE_COMPLETION_STARTED
PROFILE_COMPLETED
PROFILE_SCHEMA_VERSION_UPDATED
PROFILE_REQUIRED_FIELD_ADDED
PROFILE_NEXT_LOGIN_REQUIRED
```

---

## 18. Identity Repair Command

Create or maintain:

```text
python manage.py repair_identity_profiles
```

It must:

```text
scan all users
detect missing profiles
create missing profiles if safe
detect wrong profile type
detect duplicate profiles
detect multiple profile types for one user
recalculate profile completion state
update completed schema version where appropriate
report final no-orphan status
```

---

## 19. Migration Strategy

If test database/migrations are disposable:

```text
clean up models
remove obsolete HOD model
remove obsolete role choices
create AdminProfile and SupportStaffProfile
regenerate clean migrations
reset test database
run migrate from zero
```

If migrations cannot be reset:

```text
create safe forward migrations
migrate old role values
drop HOD safely
create missing profile tables
backfill linked profiles
validate no orphan users/profiles
```

Document the strategy used.

---

## 20. Required Tests

Agents must add/update tests for:

```text
four roles only
old roles rejected
HOD rejected/removed
/api/users/ creates User + correct Profile for all four roles
transaction rollback on profile/user failure
username generation
default password pgfmu123
must_change_password=True
profile_status=INCOMPLETE
/api/auth/me onboarding state
dynamic missing required fields
next-login completion after required field addition
/complete-profile dynamic field rendering
no orphan users/profiles
repair_identity_profiles command
audit logs
backend permissions
frontend guards
```

---

## 21. Documentation Requirements

For Update 0, create:

```text
docs/implementation/20260626_update_0_universal_identity_dynamic_onboarding/
```

Required files:

```text
DISCOVERY.md
DECISION_LOCK.md
CHANGES.md
MIGRATION_NOTES.md
API_VERIFICATION.md
FRONTEND_VERIFICATION.md
TEST_RESULTS.md
IDENTITY_REPAIR_REPORT.md
ONBOARDING_COMPLETION_RULES.md
PROFILE_REQUIREMENT_REGISTRY.md
KNOWN_LIMITATIONS.md
FINAL_VERDICT.md
```

Update the truth map:

```text
docs/truth-map/FRONTEND_BACKEND_TRUTH_MAP.md
```

---

## 22. Gate Script

Create or update:

```text
scripts/check_update_0_identity_cleanup.sh
```

It should check:

```text
HOD references removed
old roles removed or limited to migration notes/tests
only four roles in backend choices
only four roles in frontend dropdowns
AdminProfile exists
ResidentProfile exists
SupervisorProfile exists
SupportStaffProfile exists
/api/users/ documented as universal identity creation
/users/new role-aware
/complete-profile dynamic
profile completion registry exists
repair_identity_profiles command exists
required docs exist
```

---

## 23. Verification Commands

Backend:

```bash
cd backend
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py check
python manage.py test
python manage.py repair_identity_profiles
```

Frontend:

```bash
cd frontend
npm run typecheck || npx tsc --noEmit
npm run lint
npm run build
```

Project:

```bash
bash scripts/check_update_0_identity_cleanup.sh
docker compose -f compose.yml config
```

Also rerun existing brick gates if present:

```bash
bash scripts/check_brick1.sh
bash scripts/check_brick2.sh
bash scripts/check_brick3.sh
bash scripts/check_brick4.sh
bash scripts/check_brick5.sh
```

---

## 24. Explicit Non-Scope

Do not implement:

```text
Resident-Supervisor Mapping
DepartmentHeadAssignment
HOD dashboard
rotations
evaluations
logbooks
academic monitoring
backup/restore
Google bridge
AdminOps bridge
Google Drive connector
bulk import UI unless already partially present
external integrations
```

---

## 25. Final Report Required

At the end of the sprint, report:

```text
summary of changes
final role list
deleted HOD files/models/routes
deleted/ignored legacy folders
migration strategy
profile models created/updated
identity service functions
API changes
frontend changes
dynamic onboarding implementation
profile completion registry
schema versioning behavior
identity repair command output
tests run
gate script results
docs updated
known limitations
confirmation pgsims-legacy unchanged
final verdict GO / CONDITIONAL GO / BLOCKED
commit hash
```

Do not proceed to the next brick until Update 0 is GO.
