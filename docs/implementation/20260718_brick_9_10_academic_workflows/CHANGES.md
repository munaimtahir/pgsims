# Changes - Brick 9-10 Combined Sprint: Academic Workflows

## Source Changes Overview
1. **Models**: Added `EvaluationSubmission`, `EvaluationResponse`, `LogbookEntry`, and `ProcedureRecord` to `backend/sims/academics/models.py`.
2. **Services**: Implemented core workflow service operations, summaries, workloads, and quality checkers in `backend/sims/academics/services.py`.
3. **Serializers**: Defined DRF serialization classes in `backend/sims/academics/serializers.py`.
4. **Views**: Configured DRF viewsets, API actions, and role permission checks in `backend/sims/academics/views.py`.
5. **URLs**: Wired ViewSets and API views to backend routers in `backend/sims/academics/workflow_urls.py`.
6. **Commands**: Created the pilot seed manager `seed_pilot_academic_workflows` in `backend/sims/academics/management/commands/seed_pilot_academic_workflows.py`.
7. **Frontend API**: Added TypeScript endpoints in `frontend/lib/api/academics.ts`.
8. **Frontend Pages**: Added pages for evaluations list, details, creation, review, logbook list, details, creation, verification, personal progress, supervisor workloads, and admin data quality.
