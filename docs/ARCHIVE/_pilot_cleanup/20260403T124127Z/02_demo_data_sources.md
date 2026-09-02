# Demo Data Sources

Confirmed demo / seed / bootstrap sources in repo:

| Source | Evidence | Status |
| --- | --- | --- |
| Demo seed command | `backend/sims/users/management/commands/seed_demo_data.py` | Present in repo, not run automatically by active compose |
| E2E seed command | `backend/sims/users/management/commands/seed_e2e.py` | Present in repo, not run automatically by active compose |
| Demo case importer | `backend/sims/users/management/commands/import_demo_cases.py` | Present in repo |
| Sandbox preload script | `scripts/sandbox/preload_demo_data.py` | Present in repo |
| Sandbox demo notifications | `scripts/sandbox/create_demo_notifications.py` | Present in repo |
| E2E shell seeding | `scripts/e2e_seed.sh` | Present in repo |
| Auto-create admin on boot | `docker/docker-compose.yml` previously called `python manage.py create_superadmin` in backend startup | Removed from compose during this run |

Legacy mock UI content found:
- `backend/templates/users/user_reports.html`
- `backend/templates/cases/case_statistics.html`

Assessment of legacy mock UI content:
- These are legacy Django templates with hardcoded mock JavaScript arrays.
- They are not the active Next.js UTRMC dashboard path used in the current pilot deployment.
- They should still be treated as technical debt for later cleanup, but they were not the active runtime source of the live demo data that was visible in the deployed app.

Active runtime recreation mechanism found:
- The only confirmed startup recreation mechanism in the live deployment path was backend startup running `create_superadmin`.
- No automatic `seed_demo_data` or `seed_e2e` invocation was found in the active compose startup command.

Workspace pilot-file discovery result at initial discovery time:
- Search across `/home/munaim/srv`, `/home/munaim/Downloads`, `/home/munaim/Desktop`, and `/home/munaim/Documents` only surfaced:
  - `PGSIMS_Demo_CaseSeed_3Months.csv`
  - `PGSIMS_Demo_CaseSeed_3Months.xlsx`
  - unrelated non-PGSIMS spreadsheet `VEXEL_CATALOG_MASTER_FINAL.xlsx`
- No finalized pilot workbook, final residents list, or final supervisors list were found at that stage.

Pilot source package created during this run:
- `pilot_data/first_pilot_run/final_supervisors_list.csv`
- `pilot_data/first_pilot_run/final_residents_list.csv`
- `pilot_data/first_pilot_run/final_supervision_links.csv`
- `pilot_data/first_pilot_run/final_training_programs.csv`
- `pilot_data/first_pilot_run/final_resident_training_records.csv`
- `pilot_data/first_pilot_run/final_pilot_workbook.xlsx`

Current interpretation:
- The import-asset blocker is partially resolved because concrete source files now exist.
- The operational blocker remains because those files contain no real pilot rows yet.
