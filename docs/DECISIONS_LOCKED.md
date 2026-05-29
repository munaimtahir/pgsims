# PGSIMS Decisions Locked

This document records the architectural and design decisions locked for the PGSIMS Pilot rollout.

## 1. Single Department Master (2026-04-20)
- There is exactly one Department model (`academics.Department`) used university-wide.
- There are no separate "RotationDepartment" or "AcademicDepartment" models.
- All trainee assignments, supervision links, and placements reference this canonical model.

## 2. Matrix Validation (2026-04-20)
- Trainee placements are validated against `HospitalDepartment` matrix rows.
- A resident cannot be posted to a department in a hospital unless a valid `HospitalDepartment` record exists and is active.

## 3. UI Terminology Lock (2026-04-21)
- Terms displayed in the UI like **Submitted**, **Returned**, **Approved**, **Logbook**, **Home Hospital**, **Home Department** are locked.
- Replaced general "Student" with **Resident** or **Postgraduate (PG)** across all user-facing paths.

## 4. Deferral of Underdeveloped Modules (2026-04-21)
- Synopsis/thesis verification and certificates, and rotations phase-1 verification queues are marked as deferred workflows. They are excluded from active pilot navigation to ensure UI stability.
