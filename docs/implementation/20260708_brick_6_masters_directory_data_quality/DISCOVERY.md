# Discovery Report — Brick 6

## Overview
This document records the initial state of the codebase for Brick 6 and outlines the plan for stabilizing the Master catalog, directory completion, data quality page, and pilot readiness data.

## Findings
1. **Active Root**: `/home/munaim/srv/apps/pgsims` is the active workspace.
2. **Current Models**:
   - `Hospital` is defined in `rotations/models.py` (with `is_active`).
   - `Department` is defined in `academics/models.py` (with `active`).
   - `TrainingProgram` is defined in `training/models.py` (with `active`).
   - `Institution`, `Specialty`, `Designation`, and `AcademicSession` models do not yet exist.
   - Profile models (`ResidentProfile`, `SupervisorProfile`) use CharFields for designation, academic session, and specialty.
3. **Identity options & Data quality**:
   - An `/api/identity/options/` endpoint exists under `userbase_views.py` but currently returns hardcoded arrays for designations and academic sessions.
   - Some basic data-quality views exist under `users/userbase_views.py` but need expansion.

## Plan
1. Define `Institution`, `Specialty`, `Designation`, and `AcademicSession` models in `academics/models.py`.
2. Add `institution` ForeignKey to `Hospital` model in `rotations/models.py`.
3. Update `ResidentProfile` and `SupervisorProfile` CharFields to use `ForeignKey` to the new models with `to_field="code"` to preserve compatibility.
4. Implement master views/serializers for all master categories and wire up routes.
5. Create frontend pages for `/masters/...` and link live API dropdown options.
6. Create data-quality views/pages and implement pilot seeding commands.
