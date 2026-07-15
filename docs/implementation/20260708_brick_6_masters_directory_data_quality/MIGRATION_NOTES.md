# MIGRATION NOTES — PGMS Brick 6 Masters and Data Quality

This document outlines the database migration strategy and implementation details.

---

## 1. Schema Upgrades
- Added new database tables for:
  - `academics_institution`
  - `academics_specialty`
  - `academics_designation`
  - `academics_academicsession`
- Added column `institution_id` (ForeignKey pointing to `academics_institution`) to the table `rotations_hospital`.
- Converted columns `academic_session_ref`, `specialty_ref` in `users_residentprofile` and `designation_ref`, `specialty_ref` in `users_supervisorprofile` from `VARCHAR` fields to database ForeignKey relationships pointing to their respective master tables targeting their unique `code` columns.

---

## 2. Backward Compatibility
- String-based legacy data assignments are supported out-of-the-box.
- A custom python descriptor `SafeForeignKeyDescriptor` intercepts string assignments, calls `get_or_create` on the target model class, and assigns the resulting model instance.
- A custom `__eq__` method on the master models evaluates to `True` when compared against a matching string code (e.g. `specialty_ref == "GI_SURG"`), preserving all unit test assertions and data queries.
