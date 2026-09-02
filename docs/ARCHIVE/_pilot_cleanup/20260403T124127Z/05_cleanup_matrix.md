# Cleanup Matrix

## A. Keep As-Is

| Category | Reason |
| --- | --- |
| `django_migrations`, `django_content_type`, `auth_permission` | Structural platform metadata |
| Canonical departments `MED`, `SURG`, `PED`, `OBG`, `ORTH` | Required university structure |
| Canonical hospital `UTRMC` | Required single canonical hospital |
| `rotations_hospitaldepartment` rows linking canonical hospital to canonical departments | Required matrix structure |
| Admin user `admin` | Required recovery / access path |
| `notifications_notificationpreference` for remaining admin | Harmless user-level preference metadata |
| Celery beat schedule tables | Required scheduler structure |
| Static / media volumes and deployment env | Required runtime config |

## B. Delete / Purge

| Category | Reason |
| --- | --- |
| Demo/e2e/test users and their staff/resident profiles | Non-pilot runtime data |
| Demo/e2e/test department memberships, hospital assignments, HOD assignments | Dependent non-pilot runtime data |
| Demo/e2e/test supervisor-resident links | Dependent non-pilot runtime data |
| Demo/e2e/test training programs | Seeded runtime programs, not approved pilot data |
| Training records, rotation assignments, postings, leave, research, theses, workshop records linked to demo/test runtime entities | Dependent runtime test data |
| Demo notifications and demo notification preferences | Seed-generated runtime noise |
| Demo/test departments and hospitals | Violates canonical model if left in place |
| Demo-linked activity logs | Audit noise from non-pilot seeded records |

## C. Verify Manually Before Purge

| Category | Status |
| --- | --- |
| `admin` account | Preserved; still uses known default credentials and should be rotated before real go-live |
| Legacy template pages with mock JavaScript arrays | Not part of active Next.js pilot path; left in repo for later technical-debt cleanup |
| Finalized pilot workbook / final residents list / final supervisors list | Not found in workspace; import blocked |
| Live backend image contents | Not rebuilt in this run because of unrelated dirty worktree changes |

Decision:
- Purge proceeded only for clearly demo/e2e/test runtime data.
- Canonical structural/master data and the admin recovery path were preserved.

