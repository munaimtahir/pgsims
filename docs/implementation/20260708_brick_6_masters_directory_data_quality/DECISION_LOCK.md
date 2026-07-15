# DECISION_LOCK — PGMS Brick 6 Masters and Data Quality

This document locks down the architectural decisions made for **Brick 6: Masters, Directory Completion, Data Quality, and Pilot Readiness**.

---

## 1. Master Models Design
- **7 Master Categories**:
  - `Institution` (academics)
  - `Hospital` / Training Site (rotations)
  - `Department` (academics)
  - `TrainingProgram` (training)
  - `Specialty` (academics)
  - `Designation` (academics)
  - `AcademicSession` (academics)
- **Active Status Flag**:
  - `active = models.BooleanField(default=True)` is used consistently on the new models to align with the core schema.
  - `Hospital` continues to use `is_active` as previously established.
- **Unique Name/Code Constraints**:
  - Natural identifiers (`code`) and titles (`name`) are enforced as unique constraints.
  - Seeding uses a custom query resolution checking both `code` and `name` to prevent collisions.

---

## 2. Profile References & to_field="code"
- `ResidentProfile` and `SupervisorProfile` reference `AcademicSession`, `Specialty`, and `Designation` via a Foreign Key pointing to the target field `to_field="code"`.
- This ensures compatibility with legacy string-based assignments.
- A python `SafeForeignKeyDescriptor` wrapper intercepts string assignments and resolves them to model instances dynamically to achieve 100% backward compatibility with all old tests and demo datasets.

---

## 3. Onboarding & Dropdown Options
- `/api/identity/options/` is fully database-driven, loading active records from the 7 master tables.
- It returns key-value options where the `id` property equals the string `code` for code-referenced fields (designations, sessions, specialties) and integer `id` for primary-key-referenced fields (hospitals, departments, programs).
- Onboarding `/complete-profile` dynamically renders dropdown select inputs for fields configured with `input_type === 'select'` using option lists fetched from `/api/identity/options/`.
