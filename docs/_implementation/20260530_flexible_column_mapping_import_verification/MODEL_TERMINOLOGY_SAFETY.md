# Data Model & Terminology Safety: Flexible Column Mapping Import

- **Date**: 2026-05-30
- **Auditor**: Gemini CLI
- **Verdict**: PASS

## 1. Specialty vs. Department
The flexible import implementation for `residents` includes a `specialty` field. 

### Findings:
- `specialty` maps directly to the `User.specialty` field, which is a choice-based field (`SPECIALTY_CHOICES`).
- It is used as a **resident/program descriptor** and does NOT affect or substitute for placement logic.
- Placement logic continues to use `HospitalDepartment` via the separate `rotation-assignments` import or the `User.home_department` affiliation.
- There is no separate "Specialty" model that competes with the canonical `Department` model.

### Terminology Check:
- UI labels use "Specialty" for the resident's field of study and "Department Code" for their administrative affiliation.
- No legacy terms like "Academic Department" or "Rotation Department" have been revived in this implementation.

## 2. HospitalDepartment Placement
The flexible import for placements (`rotation-assignments`) correctly maps to `hospital_code` and `department_code`.

### Findings:
- The transformation layer produces a standard payload that the existing `BulkService` uses to lookup `HospitalDepartment` records.
- No direct database writes bypass the `HospitalDepartment` matrix verification.

## 3. Mandatory Model Compliance
- **Hospital**: Exactly one canonical model. (Verified)
- **Department**: Exactly one canonical model. (Verified)
- **HospitalDepartment**: Matrix table correctly used for placement. (Verified)
- **History Tracking**: The models `MappingPreset` and `FlexibleImportAudit` are correctly integrated and the `FlexibleImportAudit` records the user performing the action.
