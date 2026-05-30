# Changed Files Summary: Flexible Column Mapping Import

The following files were changed or added to implement the Flexible Column Mapping Import feature (Commit `e2fb956670ce500947fce8eb51339c7095b8efbc`):

## Backend
- `backend/sims/bulk/models.py`: Added `MappingPreset` and `FlexibleImportAudit`.
- `backend/sims/bulk/serializers.py`: Added `MappingPresetSerializer` and entity serializers.
- `backend/sims/bulk/services.py`: Normalized header matching and registry for entities.
- `backend/sims/bulk/userbase_engine.py`: Refactored core import logic for better reuse.
- `backend/sims/bulk/views.py`: Implemented 6 new API views for flexible mapping flow.
- `backend/sims/bulk/urls.py`: Registered new endpoints.
- `backend/sims/bulk/tests.py`: Added comprehensive tests for flexible mapping.
- `backend/sims/bulk/migrations/0003_historicalmappingpreset_and_more.py`: Database migrations.

## Frontend
- `frontend/components/utrmc/FlexibleMappingImport.tsx`: New multi-step wizard component.
- `frontend/components/utrmc/FlexibleMappingImport.test.tsx`: Jest tests for the component.
- `frontend/components/utrmc/BulkSetupWorkspace.tsx`: Integrated the new component into the bulk setup page.

## E2E
- `frontend/e2e/workflow-gate/flexible-import.spec.ts`: Playwright E2E test for the full workflow.

## Documentation
- `docs/IMPORT_WORKFLOW.md`: Added section on Flexible Mapping.
- `docs/ONBOARDING_WORKFLOW.md`: Added section on Flexible Mapping.
