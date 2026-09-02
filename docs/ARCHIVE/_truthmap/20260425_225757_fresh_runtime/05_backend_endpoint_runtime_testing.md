# Stage 5: Backend Endpoint Runtime Testing

Source evidence: `../_truthmap_docker_fix/20260425_223918/json/stage5_api_checks.json`

## End-to-End Mutation Checks

### Logbook

- Resident draft create: `201`
- Resident submit: `200`
- Supervisor queue before review: `1` pending item
- Supervisor review action: `200`

Verdict: backend workflow works with fresh runtime.

### Leave

- Resident draft create x2: `201`, `201`
- Resident submit x2: `200`, `200`
- Supervisor inbox before actions: `2`
- Supervisor approve: `200`
- Supervisor reject/return: `200`

Verdict: backend workflow works with fresh runtime.

### Programs / templates

- Programs list: `200`
- Program policy: `200`
- Program milestones: `200`
- Program-template create attempt with incomplete payload: `400`
- Error body required `department`

Verdict: backend supports program management; template creation is validated and requires a department.

### Workshops

- Workshop list: `200`
- My workshop completions: `200`
- Returned data count: `0` workshops, `0` completions in current seeded baseline

Verdict: backend endpoints exist, but current seed does not provide runtime workshop data to verify completion flow.

### Supervision links

- Initial create attempt with frontend-style keys failed: `400`
- Error body required:
  - `supervisor_user_id`
  - `resident_user_id`

Verdict: backend exists; payload contract differs from what the current page posts.

### Data Quality

Direct backend calls succeeded:

- `GET /api/admin/data-quality/summary` -> `200`
- `GET /api/admin/data-quality/users` -> `200`
- `GET /api/admin/data-quality/audit` -> `200`

Direct backend verdict: data-quality backend exists and responds.

### Bulk

- Template download endpoint: `200`
- Export CSV endpoint: `200`
- Dry-run endpoint with header-only CSV: `400`
- Returned validation message: `No data rows found in file.`

Verdict: bulk endpoints are active; the dry-run path validated and rejected an empty dataset as expected.
