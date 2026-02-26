# Backend Map (Truth Map)

## Framework & Tech Stack
- **Framework**: Django 4.2+
- **API**: Django REST Framework (DRF)
- **Auth**: `rest_framework_simplejwt` (JWT) & Session
- **Database**: PostgreSQL (Production) / SQLite (Dev)
- **Background Tasks**: Celery with Redis
- **Audit Logging**: `django-simple-history`

## Key API Endpoints
| Path | Method | View Handler | Role Enforcement |
|------|--------|--------------|------------------|
| `/api/auth/login/` | POST | `CustomTokenObtainPairView` | AllowAny |
| `/api/logbook/my/` | GET/POST | `PGLogbookEntryListCreateView` | `IsPGUser` |
| `/api/logbook/<id>/verify/` | PATCH | `VerifyLogbookEntryView` | `supervisor`/`admin` |
| `/api/attendance/` | - | `AttendanceRecord` views | `admin` |
| `/api/analytics/dashboard/` | GET | Analytics views | Auth Required |

## Auth & Role Enforcement
- **Auth**: `JWTAuthentication` configured in `settings.py`.
- **Role Enforcement**: Custom permission classes (e.g., `IsPGUser`) and explicit role checks in `APIView` methods:
  - **Evidence**: `backend/sims/logbook/api_views.py:46`
  ```python
  if getattr(user, "role", None) not in ["supervisor", "admin"]:
      raise PermissionDenied(...)
  ```

## Key Models (Rollout Relevant)
- **User**: `sims.users.models.User` (Custom model with `role`, `specialty`, `supervisor`).
- **LogbookEntry**: `sims.logbook.models.LogbookEntry` (Core of Phase 1).
- **Rotation**: `sims.rotations.models.Rotation` (Assignments).
- **Department**: Duplicate models in `academics` and `rotations` apps.
- **Notification**: `sims.notifications.models.Notification` (Recipient/Verb based).

## Known Unknowns
- Exact field sync between `LogbookEntry` and `LogbookTemplate`.
- Logic for mass migration of existing paper logbooks.

## Immediate Next Actions
1. Fix `AttributeError` in `VerifyLogbookEntryView` (`supervisor_comments` -> `supervisor_feedback`).
2. Update `Notification` creation logic to match the schema.
3. Investigate if `simple-history` is sufficient for "audit immutability" or if explicit status locking is required.
