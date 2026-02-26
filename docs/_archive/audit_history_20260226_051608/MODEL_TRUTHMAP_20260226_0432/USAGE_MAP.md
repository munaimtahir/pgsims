# Model Usage Map

Based on RipGrep/GitGrep extraction of domain objects across the `backend/sims` and `frontend` layers.

### Backend Hotspots
- **Rotations Application (`backend/sims/rotations/`)**: The epicenter of the clinical workflow. 
  - Over 450 references discovered in `rotations/models.py`, `admin.py`, `views.py`, `forms.py`, `api_views.py`.
- **Logbook & Cases APIs (`backend/sims/logbook/`, `backend/sims/cases/`)**: Heavy dependency on `Rotation`. 
  - `sims.logbook.models.LogbookEntry` relies on `Rotation`, which automatically inherits the hospital/supervisor assignment. Any structural shift to `Rotation` guarantees downstream breakage in `Logbook` logic (Logbook forms actively filter rotations by PG supervisor).
- **Bulk Import (`backend/sims/bulk/services.py:25`)**: Heavily relies on mapping CSV structures directly to `rotations.Department` and `rotations.Hospital`.

### Frontend Hotspots
- **PG Dashboard Route (`frontend/app/dashboard/pg/rotations/page.tsx`)**: Directly renders lists of Rotation APIs from `backend`.
- **API Lib Maps (`frontend/lib/api/rotations.ts`, `frontend/lib/api/academics.ts`)**: The frontend maintains strict interface typing:
  - `RotationSummary` interface expects `department: string` and `hospital: string`.
  - Academic routes expect `department: number` IDs.
- **CSV Templates**: `frontend/public/templates/residents_template.csv` maps a plain `Department` string for ingest, directly driving the brittle bulk import behaviour.

### Impact of Consolidating Canonical Department
Any changes to merge `academics.Department` and `rotations.Department` will immediately impact:
1. `rotations.views.py` (Search filters)
2. `logbook.forms.py` (Cascading filters reliant on `Rotation.department`)
3. `bulk.services.py` (Ingestion mechanism for CSV templates)
