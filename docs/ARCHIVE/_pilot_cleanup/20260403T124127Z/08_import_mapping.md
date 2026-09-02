# Import Mapping

Prepared reusable import path:
- `backend/sims/users/management/commands/import_pilot_bundle.py`

Supporting import surfaces discovered in code:
- `backend/sims/bulk/services.py`
- `backend/sims/bulk/userbase_engine.py`

Import strategy designed:
1. Import training programs if present in the workbook.
2. Import supervisors.
3. Import residents.
4. Import supervisor-resident links.
5. Import resident training records.

Discovered target entities:
- `faculty-supervisors`
- `residents`
- `supervision-links`
- `training-programs`
- `resident-training-records`

Supervisor mapping:

| Source concept | Target entity | Target field | Rule |
| --- | --- | --- | --- |
| Supervisor name | `faculty-supervisors` | `full_name` | Required |
| Supervisor email | `faculty-supervisors` | `email` | Use source if present; otherwise generate placeholder |
| Phone | `faculty-supervisors` | `phone_number` | Pass through if present |
| Designation | `faculty-supervisors` | `designation` | Pass through if present |
| Registration number | `faculty-supervisors` | `registration_number` | Pass through if present |
| Department | `faculty-supervisors` | `department_code` | Normalize to canonical department code |
| Hospital | `faculty-supervisors` | `hospital_code` | Default to active canonical hospital if missing |
| Specialty | `faculty-supervisors` | `specialty` | Derive from department if absent |

Resident mapping:

| Source concept | Target entity | Target field | Rule |
| --- | --- | --- | --- |
| Resident name | `residents` | `full_name` | Required |
| Resident email | `residents` | `email` | Use source if present; otherwise generate placeholder |
| Phone | `residents` | `phone_number` | Pass through if present |
| Training year | `residents` | `year` | Normalize integer-like values |
| PGR / registration id | `residents` | `pgr_id` | Pass through if present |
| Training start | `residents` | `training_start` | Parse to valid date |
| Training end | `residents` | `training_end` | Parse to valid date |
| Training level | `residents` | `training_level` | Pass through if present |
| Department | `residents` | `department_code` | Normalize to canonical department code |
| Hospital | `residents` | `hospital_code` | Default to active canonical hospital if missing |
| Specialty | `residents` | `specialty` | Derive from department if absent |
| Supervisor email / name | internal staging | `_supervisor_email` / `_supervisor_name` | Used later to create links |
| Track / program | staging | `program_track` | Used to synthesize program or training-record rows when supported |

Relationship mapping:

| Source concept | Target entity | Target field | Rule |
| --- | --- | --- | --- |
| Supervisor + resident pairing | `supervision-links` | supervisor / resident / department | Resolve by email first, then by normalized name |

Program / training mapping:

| Source concept | Target entity | Target field | Rule |
| --- | --- | --- | --- |
| Program code / name / duration | `training-programs` | program fields | Import only if workbook provides stable values |
| Resident enrollment | `resident-training-records` | resident, program, start, expected end, level | Import after users and programs exist |

Placeholder handling policy:
- Missing emails: generate deterministic placeholder emails under `pilot-placeholder.local`.
- Missing hospital: default to the single active canonical hospital `UTRMC`.
- Department labels: map to canonical department codes already present in DB.
- Thesis / synopsis / IMM placeholders: do not force them into unsupported strict enums; warn unless a verified compatible field is available.

File discovery policy in the command:
- Search roots:
  - `/home/munaim/srv/apps/pgsims`
  - `/home/munaim/srv`
- Exclusions:
  - demo/template files
  - `PGSIMS_Demo_CaseSeed*`
  - filenames containing `template` or `demo`

Current status:
- Mapping logic is prepared.
- Real source workbook/lists were not found, so no actual source-column-to-row validation against final pilot files was possible in this run.

