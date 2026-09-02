# Runtime Results Matrix

| Area / workflow | Role | Status | Steps executed | Expected | Actual | Infra/App | Fixed? | Evidence |
|---|---|---|---|---|---|---|---|---|
| Active-surface E2E | resident/supervisor/UTRMC | PASS | seeded active project | active smoke/logbook/permissions pass | `7 passed`; after restart `7 passed` | app | n/a | Playwright report |
| Auth smoke | resident/supervisor/UTRMC | PASS | login tests | redirects to correct dashboards | passed | app | n/a | Playwright report |
| Resident leave workflow | resident/supervisor | PASS | create draft, submit, approve | full live flow passes | passed after selector harness repair | infra/test | yes | workflow-gate |
| Logbook workflow | resident/supervisor | PASS | draft, submit, return, resubmit, approve | full lifecycle passes | passed | app | n/a | active-surface |
| UTRMC read-only boundary | UTRMC staff | PASS | UI mutation controls hidden | read-only user cannot mutate | passed | app | n/a | active-surface/rbac |
| Role route denial | all active roles | PASS | direct wrong-role route checks | redirected/blocked | passed | app | n/a | rbac/negative |
| UTRMC admin pages | UTRMC admin | PARTIAL | smoke/dashboard/navigation | visible pages render | most visible pages pass; not every CTA exercised | coverage gap | no | dashboard/navigation |
| Deferred routes hidden from nav | resident/supervisor | PASS | navigation checks | no research/thesis/workshop/research approvals nav | passed after test repair | infra/test | yes | navigation |
| Old workflow-gate inactive assertions | n/a | PASS after repair | removed inactive assertions from active gate | no deferred workflows in active gate | repaired | infra/test | yes | workflow-gate |

