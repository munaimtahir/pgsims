# Stage 1: Backend Route Inventory

Fresh-runtime scope focused on active routes exercised by the current frontend and required module checks.

## Runtime target

- Backend base URL: `http://127.0.0.1:8014`
- Backend container: `pgsims_backend`
- Health after runtime restoration: `200 OK` on `/healthz/`

## Inventory Sources

- Django URL resolver extraction during this run
- `frontend/lib/api/training.ts`
- `frontend/lib/api/userbase.ts`
- Direct runtime requests in `../_truthmap_docker_fix/20260425_223918/json/stage5_api_checks.json`

## Verified Active Endpoints

### Dashboard / summaries

- `GET /api/dashboard/resident/`
- `GET /api/dashboard/supervisor/`
- `GET /api/dashboard/utrmc/`
- `GET /api/residents/me/summary/`
- `GET /api/supervisors/me/summary/`

### Programs / training-program management

- `GET /api/programs/`
- `POST /api/programs/`
- `GET /api/programs/<program_id>/policy/`
- `PUT /api/programs/<program_id>/policy/`
- `GET /api/programs/<program_id>/milestones/`
- `POST /api/programs/<program_id>/milestones/`
- `GET /api/program-templates/`
- `POST /api/program-templates/`
- `PATCH /api/program-templates/<id>/`
- `DELETE /api/program-templates/<id>/`

### Logbook

- `GET /api/logbook/`
- `POST /api/logbook/`
- `PATCH /api/logbook/<id>/`
- `POST /api/logbook/<id>/submit/`
- `POST /api/logbook/<id>/review/`
- `GET /api/logbook/review-queue/`
- `GET /api/logbook/my-threshold/`

### Leave

- `GET /api/my/leaves/`
- `POST /api/leaves/`
- `POST /api/leaves/<id>/submit/`
- `GET /api/utrmc/approvals/leaves/`
- `POST /api/leaves/<id>/approve/`
- `POST /api/leaves/<id>/reject/`

### Workshops

- `GET /api/workshops/`
- `GET /api/my/workshops/`
- `POST /api/my/workshops/`
- `DELETE /api/my/workshops/<id>/`

### Userbase / supervision

- `GET /api/users/`
- `GET /api/supervision-links/`
- `POST /api/supervision-links/`
- `PATCH /api/supervision-links/<id>/`
- `GET /api/hod-assignments/`

### Data Quality

- `GET /api/admin/data-quality/summary`
- `GET /api/admin/data-quality/users`
- `GET /api/admin/data-quality/audit`
- `POST /api/admin/data-quality/recompute`

### Bulk

- `GET /api/bulk/templates/<resource>/`
- `GET /api/bulk/exports/<resource>/`
- `POST /api/bulk/import/<entity>/dry-run/`
- `POST /api/bulk/import/<entity>/apply/`

## Inventory Verdict

- Backend route coverage for the audited modules is present.
- The major remaining failures are not “missing backend across the board”.
- Fresh-runtime failures are narrower integration/UI contract problems.
