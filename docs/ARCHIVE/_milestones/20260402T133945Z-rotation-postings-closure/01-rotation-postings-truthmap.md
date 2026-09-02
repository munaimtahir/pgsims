# Rotation and Postings Truth Map

| Workflow Step | Frontend Surface | Backend Support | State Model Support | Runtime Reachability | Pre-pass Classification | Action | Post-pass Classification |
|---|---|---|---|---|---|---|---|
| UTRMC creates rotation draft | `/dashboard/utrmc` | `POST /api/rotations/` | `RotationAssignment.STATUS_DRAFT` | Verified in browser | Active but Partial | Added create form on existing UTRMC overview route | Active |
| Resident sees assigned draft rotation | `/dashboard/resident/schedule` | `GET /api/my/rotations/` | `DRAFT` | Verified in browser | Broken | Switched schedule from summary-only shape to real rotation list | Active |
| Resident submits draft rotation | `/dashboard/resident/schedule` | `POST /api/rotations/{id}/submit/` | `DRAFT -> SUBMITTED` | Verified in browser | Active but Partial | Added submit action and real success refresh path | Active |
| Resident resubmits returned rotation | `/dashboard/resident/schedule` | `POST /api/rotations/{id}/submit/` | `RETURNED -> SUBMITTED` | Verified by API test | Broken | Backend now permits resubmission and clears return reason on submit | Active |
| Supervisor sees pending rotation | `/dashboard/supervisor` | `GET /api/supervisor/rotations/pending/` | `SUBMITTED` | Verified in browser | Broken | Added dashboard section and fixed supervisor scope logic | Active |
| Supervisor approves rotation | `/dashboard/supervisor` | `POST /api/rotations/{id}/hod-approve/` | `SUBMITTED -> APPROVED` | Verified in browser | Active but Partial | Added approve action on existing dashboard | Active |
| Supervisor returns rotation | `/dashboard/supervisor` | `POST /api/rotations/{id}/returned/` | `SUBMITTED/APPROVED -> RETURNED` | Verified by UI/API coverage | Active but Partial | Added return action and resident visibility of reason | Active |
| UTRMC sees approved rotations waiting activation | `/dashboard/utrmc` | `GET /api/rotations/` | `APPROVED` | Verified in browser | Placeholder | Added queue section on overview route | Active |
| UTRMC activates rotation | `/dashboard/utrmc` | `POST /api/rotations/{id}/activate/` | `APPROVED -> ACTIVE` | Verified in browser | Placeholder | Added activate action on overview route | Active |
| UTRMC completes rotation | `/dashboard/utrmc` | `POST /api/rotations/{id}/complete/` | `ACTIVE -> COMPLETED` | Verified in browser | Placeholder | Added complete action on overview route | Active |
| Resident creates posting request | `/dashboard/resident/postings` | `POST /api/postings/` | `DeputationPosting.STATUS_SUBMITTED` | Verified in browser | Broken | Added required `resident_training` payload wiring | Active |
| Resident sees posting lifecycle | `/dashboard/resident/postings` | `GET /api/postings/` | `SUBMITTED/APPROVED/REJECTED/COMPLETED` | Verified in browser | Active but Partial | Aligned UI to uppercase backend statuses | Active |
| UTRMC sees submitted postings | `/dashboard/utrmc/postings` | `GET /api/postings/` | `SUBMITTED` | Verified in browser | Active but Partial | Aligned status rendering and queue behavior | Active |
| UTRMC approves posting | `/dashboard/utrmc/postings` | `POST /api/postings/{id}/approve/` | `SUBMITTED -> APPROVED` | Verified in browser | Broken | Fixed status comparisons so real action renders | Active |
| UTRMC completes posting | `/dashboard/utrmc/postings` | `POST /api/postings/{id}/complete/` | `APPROVED -> COMPLETED` | Verified in browser | Broken | Fixed status comparisons so real action renders | Active |
| UTRMC user boundary on postings | `/dashboard/utrmc/postings` | list endpoint only | no write role | Verified in browser | Misleading | Added explicit read-only banner and hid actions | Active |

## Active-Surface Classification Summary

- Rotation workflow: **Active**
- Postings workflow: **Active**
- UTRMC user postings write path: **Deferred/Blocked by role**, explicitly preserved as read-only
- Legacy logbook/cases/analytics: **Deferred**, unchanged in this pass
