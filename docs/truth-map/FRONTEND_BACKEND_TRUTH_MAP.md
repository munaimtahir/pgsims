# Frontend-Backend Truth Map — PGMS Clean-Room Foundation

This document maintains the mapping between frontend user interface routes and the backend services/APIs.

---

## 1. Universal Identity & Profile Sync (Update 0)

| Frontend Page | Backend Endpoint | HTTP Method | Model(s) | Serializer |
| :--- | :--- | :--- | :--- | :--- |
| `/login` | `/api/auth/login/` | `POST` | `User` | `TokenObtainPairSerializer` |
| `/complete-profile` | `/api/auth/me/` <br> `/api/users/profile/` | `GET` <br> `PATCH` | `User` <br> `ResidentProfile`, `SupervisorProfile`, `AdminProfile`, `SupportStaffProfile` | `UserProfileSerializer` |
| `/users/new` | `/api/users/` | `POST` | `User` + Correct profile linked in atomic transaction | `UserCreateSerializer` |

---

## 2. Supervision Spine (Brick 7)

| Frontend Page | Backend Endpoint | HTTP Method | Model(s) | Serializer |
| :--- | :--- | :--- | :--- | :--- |
| `/supervision` | `/api/supervision/assignments/` <br> `/api/supervision/data-quality/` | `GET` | `ResidentSupervisorAssignment` | `ResidentSupervisorAssignmentSerializer` |
| `/supervision/assignments` | `/api/supervision/assignments/` | `GET` | `ResidentSupervisorAssignment` | `ResidentSupervisorAssignmentSerializer` |
| `/supervision/assignments/new` | `/api/supervision/options/` <br> `/api/supervision/assignments/` | `GET` <br> `POST` | `ResidentSupervisorAssignment` | `ResidentSupervisorAssignmentSerializer` |
| `/supervision/assignments/[id]` | `/api/supervision/assignments/{id}/` <br> `/api/supervision/assignments/{id}/end/` | `GET` <br> `POST` | `ResidentSupervisorAssignment` | `ResidentSupervisorAssignmentSerializer` |
| `/supervision/import` | `/api/supervision/import/` | `POST` | `ResidentSupervisorAssignment` | `ResidentSupervisorAssignmentSerializer` |
| `/supervision/data-quality` | `/api/supervision/data-quality/` | `GET` | `ResidentSupervisorAssignment` | `ResidentSupervisorAssignmentSerializer` |
| `/dashboard/utrmc/supervision` | redirect to `/supervision` | `GET` | `ResidentSupervisorAssignment` | `ResidentSupervisorAssignmentSerializer` |
| `/dashboard/utrmc/data-quality` | redirect to `/supervision/data-quality` | `GET` | `ResidentSupervisorAssignment` | `ResidentSupervisorAssignmentSerializer` |
| Resident Detail View | `/api/users/residents/{id}/` | `GET` | `ResidentProfile` | `ResidentProfileSerializer` |
| Supervisor Detail View | `/api/users/supervisors/{id}/` | `GET` | `SupervisorProfile` | `SupervisorProfileSerializer` |

---

## 3. Core Masters & Directory (Brick 6)

| Frontend Page | Backend Endpoint | HTTP Method | Model(s) | Serializer |
| :--- | :--- | :--- | :--- | :--- |
| `/masters` | `/api/hospitals/` <br> `/api/departments/` <br> `/api/hospital-departments/` | `GET`, `POST`, `PATCH`, `DELETE` | `Hospital`, `Department`, `HospitalDepartment` | `HospitalSerializer`, `DepartmentSerializer`, `HospitalDepartmentSerializer` |

---

## 4. Academic Workflow Foundation (Brick 8)

| Frontend Page | Backend Endpoint | HTTP Method | Model(s) | Serializer |
| :--- | :--- | :--- | :--- | :--- |
| `/academics` | `/api/academics/overview/` | `GET` | aggregate service | n/a |
| `/academics/training-records` | `/api/academics/training-records/` | `GET`, `POST` | `ResidentTrainingRecord` | `ResidentTrainingRecordSerializer` |
| `/academics/training-records/[id]` | `/api/academics/training-records/{id}/` <br> `/api/academics/training-records/{id}/close/` | `GET` <br> `POST` | `ResidentTrainingRecord` | `ResidentTrainingRecordSerializer` |
| `/academics/periods` | `/api/academics/periods/` | `GET`, `POST` | `AcademicPeriod` | `AcademicPeriodSerializer` |
| `/academics/rotation-templates` | `/api/academics/rotation-templates/` | `GET`, `POST` | `RotationTemplate` | `RotationTemplateSerializer` |
| `/academics/evaluation-templates` | `/api/academics/evaluation-templates/` | `GET`, `POST` | `EvaluationFormTemplate` | `EvaluationFormTemplateSerializer` |
| `/academics/logbook-categories` | `/api/academics/logbook-categories/` | `GET`, `POST` | `LogbookCategory` | `LogbookCategorySerializer` |
| `/academics/review-queue` | `/api/academics/review-queue/` | `GET`, `POST`, `PATCH` | `SupervisorReviewQueueItem` | `SupervisorReviewQueueItemSerializer` |
| `/academics/data-quality` | `/api/academics/data-quality/` | `GET` | academic data-quality aggregate | n/a |
| `/dashboard/resident` | `/api/academics/residents/me/summary/` | `GET` | `ResidentTrainingRecord` + supervision aggregate | n/a |
| `/dashboard/supervisor` | `/api/academics/supervisors/me/summary/` | `GET` | `ResidentTrainingRecord` + queue aggregate | n/a |
| `/residents/[id]` | `/api/residents/{id}/` <br> `/api/academics/residents/{id}/summary/` | `GET` | `ResidentProfile` + `ResidentTrainingRecord` | mixed |
| `/supervisors/[id]` | `/api/supervisors/{id}/` <br> `/api/academics/supervisors/{id}/summary/` | `GET` | `SupervisorProfile` + academic aggregate | mixed |

---

## 5. Brick 8.6 Cleanup Rule

- Canonical frontend full UIs must live only under `/users`, `/residents`, `/supervisors`, `/support-staff`, `/admins`, `/masters`, `/supervision`, `/academics`, and the three canonical dashboards.
- Old `/dashboard/pg*` and duplicate `/dashboard/utrmc/*` subpages are redirect-only compatibility routes.
- `SupervisorResidentLink` is a backend delete-candidate and must not be used by active frontend or dashboard code.
