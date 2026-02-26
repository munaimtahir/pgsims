# PGSIMS Model Truth Map Summary

## Overview
This audit reviews the current Django models governing Departments, Hospitals, Trainees (PGs), Rotations, Logbooks, and related compliance features in the PGSIMS application. The system's architecture contains a variety of domain entities representing academic and clinical structures.

## Key Entities
- **Trainee (PG)**: Represented primarily by `users.User` with `role="pg"`, alongside `academics.StudentProfile` for academic tracking.
- **Supervisor**: Represented by `users.User` with `role="supervisor"`.
- **Department**: Currently split into two distinct models: `academics.Department` (for academic structure) and `rotations.Department` (tied specifically to a `Hospital`).
- **Hospital**: Defined strictly under `rotations.Hospital`.
- **Rotation**: Links a Trainee (`pg`), a `Department` (`rotations.Department`), a `Hospital`, and a `Supervisor`.
- **Logbook**: Extensive system containing `LogbookEntry`, `Procedure`, `Diagnosis`, `Skill`, and `LogbookTemplate`.
- **Compliance & Audit**: Handled via `attendance.EligibilitySummary`, `audit.ActivityLog` and other status checks throughout rotation/case models.

## Crucial Duplicates
- **Department**: Duplicate models exist at `backend/sims/academics/models.py:16` (`academics.Department`) and `backend/sims/rotations/models.py:83` (`rotations.Department`). The `academics` variant focuses on batches and program coordinators, while the `rotations` variant represents a physically located unit tied directly to a `Hospital` (`hospital` FK).

## Biggest Risks
1. **Divergent Department Authority**: The existence of two Department models means academic routing and clinical (rotation) routing are disjointed, which conflicts with domain logic where a single canonical Department controls training across multiple Hospitals.
2. **Missing Home Affiliation**: Trainees (`users.User`/`academics.StudentProfile`) currently lack formal links to a "Home Hospital" or "Home Department". They are only linked to a `Batch` (which links to an `academics.Department`) and assigned a `Supervisor`.
3. **Rotation Schema Rigidity**: The `Rotation` model strictly assumes a direct mapping to local `rotations.Department` and `rotations.Hospital` without explicitly differentiating the PG's "host/home" location from their "visiting/to" location, nor does it log exceptions for external or inter-hospital rotations. 
