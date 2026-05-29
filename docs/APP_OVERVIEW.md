# PGSIMS Application Overview

PGSIMS (Postgraduate Student Information Management System) is the official system for training tracking, rotation management, logbook validation, and program monitoring under the postgraduate medical education department of the university.

## Scope of the Pilot Rollout
The system is tailored for an initial pilot rollout comprising:
- **Hospitals**: 1-2 university-affiliated training hospitals.
- **Departments**: 2 pilot departments (e.g., Urology, Pathology).
- **Users**: ~10 supervisors/faculty members and ~30 residents.

## Core Features
1. **User base Management**: Custom role-based accounts (Super Admin, Admin, HOD, Supervisor, Resident, Data Entry, Read-only Viewer).
2. **Hospital-Department Matrix**: normalizes which clinical departments exist in which hospital sites.
3. **Training Program Registrations**: Tracks resident enrollment in degree programs (MS, MD, FCPS, Diploma) with effective start and expected end dates.
4. **Resident Rotation Assignments**: Manages clinical placements inside the Hospital-Department matrix with full state-machine workflows (Draft -> Submitted -> Returned/Approved).
5. **Leave Management**: Trainees submit leaves which must be approved by supervisors.
6. **Logbook Audit Trail**: Residents log clinical cases and procedures. Supervisors review and sign off or return entries with feedback.
7. **Readiness Dashboard**: Tracks resident milestone eligibility (Intermediate Membership iMM, Final Exam) based on compliance requirements (synopsis submission, thesis, logbook thresholds, workshop hours).

## Technical Architecture
- **Backend**: Django 4.2 REST Framework API with SimpleJWT authentication and PostgreSQL database. Celery task workers for background computing.
- **Frontend**: Next.js 14 Web Application utilizing Tailwind CSS and Axios-based client-side state management.
- **Deployment**: Dockerized services orchestrated via Docker Compose.
