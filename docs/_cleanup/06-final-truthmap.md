# Final Truthmap (Post-Cleanup Baseline)

Date (UTC): 2026-04-21

| Active feature/surface | Classification | Evidence |
|---|---|---|
| Auth login + profile (`/api/auth/login`, `/api/auth/profile`) | **WORKING PERFECTLY** | API smoke checks returned 200 for all verification roles |
| Backend core contract/workflow test suite | **WORKING PERFECTLY** | `pytest sims -q` → 209 passed |
| Frontend unit/lint/type/build gates | **WORKING PERFECTLY** | Jest + lint + tsc + next build all passed |
| Supervisor dashboard surface | **WORKING PERFECTLY** | API smoke `/api/dashboard/supervisor/` 200; feature-layer supervisor smoke passed |
| UTRMC dashboard surface (read) | **WORKING PERFECTLY** | `/api/dashboard/utrmc/` 200 for `utrmc_user`/`utrmc_admin` |
| UTRMC read-only mutation blocking | **WORKING PERFECTLY** | `utrmc_user` POST mutation attempts return 403 |
| Resident dashboard operational counters | **WORKING BUT NEEDS DEBUGGING** | `/api/dashboard/resident/` returns 404 on clean baseline resident; E2E dashboard scenario failed |
| Resident onboarding completeness dependency | **WORKING BUT NEEDS DEBUGGING** | clean baseline resident requires additional training-record wiring for full workflows |
| Leave workflow (resident create/submit path) | **WORKING BUT NEEDS DEBUGGING** | create returns 400 requiring `resident_training`; list endpoints available |
| Supervisor user listing scope behavior | **WORKING BUT NEEDS DEBUGGING** | `/api/users/` for supervisor returns self-only 200; RBAC contract wording mismatch |
| Logbook permission-boundary flow | **WORKING BUT NEEDS DEBUGGING** | dedicated logbook workflow test passes, but feature-layer permission path timed out at submit control |
| Rotations phase-1 workflow | **NOT DONE / MISLEADING / HIDDEN** | feature-layer rotations scenario failed; resident create path contract/runtime mismatch (`403`) |
| Synopsis submission workflow | **NOT DONE / MISLEADING / HIDDEN** | feature-layer synopsis scenario failed (required card/actions missing) |
| Thesis submission workflow | **NOT DONE / MISLEADING / HIDDEN** | feature-layer thesis scenario failed (required card/actions missing) |
| Presentation/discovery artifact surfaces | **NOT DONE / MISLEADING / HIDDEN** | stale non-authoritative packs removed from active repository surface |
