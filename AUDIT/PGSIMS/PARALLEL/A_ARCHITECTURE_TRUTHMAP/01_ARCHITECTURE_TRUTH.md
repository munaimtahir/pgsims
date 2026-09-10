# Architecture Truth

## Backend
- **Framework:** Django 4.2.30 / Django REST Framework
- **Modules/Apps:** `users`, `academics`, `rotations`, `training`, `supervision`, `backup_center`, `notifications`, `bulk`, `audit`
- **Database:** PostgreSQL (via `psycopg2-binary`)
- **Cache/Broker:** Redis (via `django-redis` and `celery`)
- **Authentication:** JWT (`rest_framework_simplejwt`)

## Frontend
- **Framework:** React / Next.js (App Router)
- **Role System:** Role-based access control managed heavily in `middleware.ts` for route protection (`ADMIN`, `RESIDENT`, `SUPERVISOR`, `SUPPORT_STAFF`).
- **Data Fetching:** Custom `axios` client with API base URLs.

## Mobile Client
- **Status:** Android source code exists (`android/` directory using Gradle build system). Retrofit is used for API communication. It has partial coverage of the API.

## Truth Mapping Notes
We observed API drift between React frontend and backend implementation. Specifically, several NextJS pages request API structures that do not exist (resulting in BROKEN paths), suggesting either frontend legacy code or missing backend views.
