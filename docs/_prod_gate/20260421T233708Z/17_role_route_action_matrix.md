# Role Route Action Matrix

| Role | Accessible routes tested | Inaccessible routes tested | Allowed actions tested | Denied actions tested | Status |
|---|---|---|---|---|---|
| resident/pg | dashboard, schedule, logbook | supervisor, UTRMC | leave draft/submit, logbook draft/submit/resubmit | unrelated supervisor review denied indirectly; UTRMC denied | PASS for critical scope |
| supervisor | dashboard, residents nav | resident, UTRMC | leave approve, logbook return/approve | unrelated resident logbook review denied | PASS for critical scope |
| utrmc_admin | UTRMC overview/admin pages | resident/supervisor | bulk dry-run; admin page visibility | n/a | PARTIAL |
| utrmc_user | UTRMC read-only pages | supervisor routes, mutation controls | read-only overview | mutation controls hidden | PASS for critical read-only boundary |
| unauthenticated | login/register/forgot | dashboards | login/password reset | dashboard redirect to login | PASS |

