# API Verification - Brick 9-10 Combined Sprint: Academic Workflows

## Endpoints Verified
1. **List / Retrieve / Create / Update Submissions**:
   * `GET /api/academics/evaluation-submissions/`
   * `POST /api/academics/evaluation-submissions/`
   * `GET /api/academics/evaluation-submissions/{id}/`
   * `PATCH /api/academics/evaluation-submissions/{id}/`
2. **Action Workflows**:
   * `/submit/`, `/start_review/`, `/approve/`, `/return_revision/`, `/reject/`, `/cancel/`
3. **Logbook Entries**:
   * `GET /api/academics/logbook-entries/`
   * `POST /api/academics/logbook-entries/`
   * `/verify/`, `/return_revision/`, `/reject/`, `/cancel/`
4. **Academics Progress & Dashboards**:
   * `GET /api/academics/my-progress/`
   * `GET /api/academics/residents/{id}/progress/`
   * `GET /api/academics/supervisor-workload/`
   * `GET /api/academics/admin-workflow-overview/`
   * `GET /api/academics/workflow-data-quality/`
5. **Seeding Utility**:
   * `POST /api/academics/seed-workflows/`
