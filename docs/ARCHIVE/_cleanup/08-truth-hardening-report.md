# Truth-Hardening Report

Date (UTC): 2026-04-21

## What Changed
- Added reproducible active-surface baseline seeding:
  - `seed_active_surface_baseline`
  - `scripts/e2e_seed.sh` now runs `seed_org_data`, `seed_active_surface_baseline`, and `seed_e2e`.
- Resident baseline is no longer dependent on manual hidden setup:
  - pilot PG/resident accounts receive an active baseline training record.
  - resident dashboard and summary paths have empty-state handling for missing training records.
- Leave create is contract-strict and usable on the baseline:
  - resident leave create requires `resident_training`.
  - schedule page sends the active training record id from the resident summary.
- Supervisor `/api/users/` truth is self-scoped read:
  - runtime remains self-only for non-managers.
  - RBAC/API contract wording and tests now match.
- Inactive surfaces were removed from active navigation and dashboard CTAs:
  - rotations phase-1
  - synopsis
  - thesis
  - resident postings
  - supervisor research approvals

## Classification
| Surface | Classification | Evidence |
|---|---|---|
| Auth/login/profile | WORKING PERFECTLY | `npm run test:e2e:active-surface:local` role smoke passed |
| Resident dashboard | WORKING PERFECTLY | backend `pytest sims -q`; active Playwright smoke passed |
| Leave create flow | WORKING PERFECTLY | backend baseline test creates draft leave; schedule UI sends `resident_training` |
| Supervisor dashboard | WORKING PERFECTLY | active Playwright smoke/logbook review passed |
| UTRMC dashboard/read-only boundary | WORKING PERFECTLY | active Playwright permission test passed |
| Supervisor `/api/users/` RBAC | WORKING PERFECTLY | backend userbase tests passed |
| Logbook active path | WORKING PERFECTLY | active Playwright logbook submit/return/resubmit/approve passed |
| Rotations phase-1 | NOT DONE / MISLEADING / HIDDEN | removed from active nav/gate |
| Synopsis workflow | NOT DONE / MISLEADING / HIDDEN | removed from active nav/gate |
| Thesis workflow | NOT DONE / MISLEADING / HIDDEN | removed from active nav/gate |

## Out Of Scope
- Completing rotations phase-1.
- Completing synopsis package submission/certification.
- Completing thesis package submission/certification.
- Promoting inactive-depth E2E failures into release truth.
