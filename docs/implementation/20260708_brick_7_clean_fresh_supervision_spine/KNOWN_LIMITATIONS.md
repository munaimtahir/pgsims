# KNOWN LIMITATIONS — PGMS Brick 7 Clean Fresh Pilot Supervision Spine

This document lists design assumptions, constraints, and limitations for **Brick 7**.

---

## 1. Design Assumptions & Scope Bounds

- **Department & Hospital Match Rules**:
  - The matching rules enforce that residents and supervisors must share the exact same `hospital` and `department_ref` on their profiles.
  - While this is correct for Faisalabad Medical University's pilot departments, it does not support multi-department cross-appointments (which is out of scope for this pilot sprint).
- **Primary Supervisor Limit**:
  - A resident can only have exactly *one* active primary supervisor mapping at a time. The database model restricts this via a conditional unique index.
- **Historical Retention**:
  - Modifying or ending an assignment does not physically delete the database row; instead, it updates the `status` to `ENDED` and `is_active` to `False` to maintain audit integrity and simple-history records.

---

## 2. Technical Limitations

- **Bulk Import Formats**:
  - The CSV mapping importer expects strict matches on username, registration number, or email. Missing profiles will be flagged as dry-run failures.
- **Legacy Compatibility**:
  - The old `SupervisorResidentLink` is still referenced by legacy userbase, bulk, and training compatibility paths, plus `/api/supervision-links/` helpers in the frontend API layer. It is not part of the new `backend/sims/supervision` spine or the compiled `/dashboard/utrmc/supervision` page.
