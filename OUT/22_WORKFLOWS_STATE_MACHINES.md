# Workflows and State Machines

## 1) LogbookEntry Workflow (`logbook.LogbookEntry`)

**State set**: `draft`, `pending`, `approved`, `rejected`, `returned`, `archived` (`backend/sims/logbook/models.py:409-416`).

### Transition table
| From | To | Trigger | Enforced in | Who can trigger |
|---|---|---|---|---|
| `new` | `draft` | Create entry | `PGLogbookEntryListCreateView.post` (`backend/sims/logbook/api_views.py:278-305`) | PG (`IsPGUser`) |
| `draft` / `returned` | `pending` | Submit entry | `PGLogbookEntrySubmitView.post` (`backend/sims/logbook/api_views.py:339-402`) + `_handle_status_change` (`backend/sims/logbook/models.py:673-718`) | PG owner |
| `pending` | `approved` | Verify action=`approved` | `VerifyLogbookEntryView.patch` (`backend/sims/logbook/api_views.py:95-249`) | Supervisor of assigned PG or admin (`CanVerifyLogbookEntry`) |
| `pending` | `returned` | Verify action=`returned` | same as above | Supervisor/admin |
| `pending` | `rejected` | Verify action=`rejected` | same as above | Supervisor/admin |
| any non-`draft` | `draft` | Explicit status set then save | `_handle_status_change` resets audit fields (`backend/sims/logbook/models.py:707-713`) | Internal/model logic |

### Side effects
- On submit: `submitted_to_supervisor_at` set, supervisor assignment/notification logic in `_handle_status_change` (`backend/sims/logbook/models.py:677-683`, `720-735`).
- On supervisor action: `supervisor_action_at`, `verified_by`, `verified_at` set/cleared (`backend/sims/logbook/api_views.py:154-171`).
- Analytics/audit events emitted (`safe_track_event`, `log_action`) in verify/submit/create flows (`backend/sims/logbook/api_views.py:173-229`, `379-399`, `282-303`).
- Edit gate: only `draft`/`returned` (`can_be_edited`, `backend/sims/logbook/models.py:754-755`; checked in API `backend/sims/logbook/api_views.py:322-334`).

---

## 2) ClinicalCase Workflow (`cases.ClinicalCase` + `cases.CaseReview`)

**State set**: `draft`, `submitted`, `approved`, `needs_revision`, `rejected`, `archived` (`backend/sims/cases/models.py:73-80`).

### Transition table
| From | To | Trigger | Enforced in | Who can trigger |
|---|---|---|---|---|
| `new` | `draft` | Create case | `PGCaseListCreateView.post` (`backend/sims/cases/api_views.py:48-69`) | PG |
| `draft` / `needs_revision` | `submitted` | Submit case | `PGCaseSubmitView.post` (`backend/sims/cases/api_views.py:113-128`) | PG owner |
| `submitted` | `approved` / `needs_revision` / `rejected` | Review action | `CaseReviewActionView.post` + `CaseReview.save` (`backend/sims/cases/api_views.py:144-175`, `backend/sims/cases/models.py:579-592`) | Supervisor (assigned PG), admin, UTRMC admin |
| `draft` | soft-delete (`is_active=False`) | Delete | `PGCaseDetailView.delete` (`backend/sims/cases/api_views.py:100-110`) | PG owner |

### Side effects
- `CaseReview.save()` synchronizes case status and review metadata (`reviewed_by`, `reviewed_at`, score propagation) (`backend/sims/cases/models.py:584-591`).
- Edit gate: only `draft`/`needs_revision` (`backend/sims/cases/api_views.py:93-98`, `backend/sims/cases/models.py:372-374`).
- Review scope enforcement for supervisors to assigned PGs (`backend/sims/cases/api_views.py:153-156`).

---

## 3) Rotation Workflow (`rotations.Rotation`)

**State set**: `planned`, `ongoing`, `completed`, `cancelled`, `pending` (`backend/sims/rotations/models.py:131-137`).

### Transition table
| From | To | Trigger | Enforced in | Who can trigger |
|---|---|---|---|---|
| `planned` | `ongoing` | Date window reaches start | `Rotation.save` (`backend/sims/rotations/models.py:359-367`) | Automatic model logic |
| `ongoing` | `completed` | Date passes end | `Rotation.save` (`backend/sims/rotations/models.py:366-367`) | Automatic model logic |
| inter-hospital requiring override | approved override metadata | UTRMC override approval endpoint | `UTRMCRotationOverrideApproveView.patch` + `approve_rotation_override` (`backend/sims/rotations/api_views.py:124-170`, `backend/sims/rotations/services.py:70-83`) | `utrmc_admin` only |

### Override policy controls
- Policy decision: `evaluate_rotation_override_policy` checks home hospital/department + hospital-department matrix (`backend/sims/rotations/services.py:15-43`).
- Validation: `validate_rotation_override_requirements` demands `override_reason` and `utrmc_admin` approval when required (`backend/sims/rotations/services.py:46-67`), invoked by `Rotation.clean` (`backend/sims/rotations/models.py:343-355`).

---

## 4) Certificate Workflow (`certificates.Certificate` + `certificates.CertificateReview`)

**Certificate states**: `pending`, `approved`, `rejected`, `expired`, `under_review` (`backend/sims/certificates/models.py:128-134`).

**Review states**: `pending`, `approved`, `rejected`, `needs_clarification` (`backend/sims/certificates/models.py:422-427`).

### Transition table
| From | To | Trigger | Enforced in | Who can trigger |
|---|---|---|---|---|
| `approved` | `expired` | Certificate passes expiry date | `Certificate.save` (`backend/sims/certificates/models.py:299-307`) | Automatic model logic |
| `pending` / `under_review` | `approved` | Review status `approved` | `CertificateReview.save` (`backend/sims/certificates/models.py:500-510`) | Reviewer (supervisor/admin; PG blocked in validation) |
| `pending` / `under_review` | `rejected` | Review status `rejected` | `CertificateReview.save` (`backend/sims/certificates/models.py:510-512`) | Reviewer |
| `pending` | `under_review` | Review status `needs_clarification` | `CertificateReview.save` (`backend/sims/certificates/models.py:513-515`) | Reviewer |

### Side effects
- `verified_by`/`verified_at` set on approval (`backend/sims/certificates/models.py:505-509`).
- Reviewer constraints enforced in `CertificateReview.clean` (supervisor scope + PG cannot review) (`backend/sims/certificates/models.py:481-499`).

---

## 5) StudentProfile Workflow (`academics.StudentProfile`)

**State field**: `status` + timestamp `status_updated_at` (`backend/sims/academics/models.py:166-174`).

### Transition table
| From | To | Trigger | Enforced in | Who can trigger |
|---|---|---|---|---|
| any valid status | any valid status in `STATUS_CHOICES` | `POST /academics/studentprofile/<id>/update_status/` | `StudentProfileViewSet.update_status` (`backend/sims/academics/views.py:70-81`) + `StudentProfile.update_status` (`backend/sims/academics/models.py:237-240`) | Authenticated users with object access by queryset scope |

---

## Workflow Observations
- Strongest API-level state machine exists in **logbook** and **cases** modules.
- **Rotations** combines model lifecycle state with separate override-approval policy state.
- **Certificates** state transitions are model-driven through `CertificateReview.save()`; API coverage in `certificates/api_views.py` is currently read-only for PG listing/download.
