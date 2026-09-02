# Remaining Risks and Accepted Limitations

| Risk | Severity | Blocks Pilot? | Mitigation |
| --- | --- | --- | --- |
| Legacy backend user-view/bulk test failures | Medium | No | Document as legacy coverage gap; keep pilot scope on active surfaces. |
| Frontend test-file typecheck errors | Low | No | Leave as test-only typing cleanup outside the pilot gate. |
| Research workflow | Medium | No | Keep excluded from pilot scope. |
| Analytics/live-feed | Medium | No | Keep excluded from pilot scope. |
| Legacy `/dashboard/admin` | Medium | No | Keep excluded from pilot scope. |
| Schema status | Low | No | Schema validation passed; keep the warning noted. |
| Coverage status | Medium | No | Coverage is 63.22%; treat as a known pilot limitation. |
| RBAC/workflow evidence | Low | No | Role boundaries and active workflows are confirmed for pilot paths. |
| Backup/restore drill depth | Low | No | Backup is created; restore is documented. |
| User onboarding/data quality | Medium | No | Require coordinator-led validation before pilot launch. |

## Accepted limitations

- Controlled pilot remains narrower than full production.
- Legacy coverage gaps remain outside the active pilot path.
- Test-only typecheck noise is tolerated until the test typing cleanup sprint.
