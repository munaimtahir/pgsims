# Resident feature matrix

| Domain | Web | Backend/API | Android before | Sprint action |
| --- | --- | --- | --- | --- |
| Profile | Yes | `/api/auth/onboarding/` | Implemented | Preserved. |
| Training | Yes | `/api/resident-training/`, `/api/residents/me/summary/` | Summary | Programme/current-training card. |
| Rotations | Yes | `/api/my/rotations/` | Missing | List, current card, detail. |
| Supervision | Yes | `/api/supervision/assignments/` | Summary | Preserved in Training. |
| Logbook | Yes | `/api/academics/logbook-entries/` | Missing | List, detail, draft, edit, submit. |
| Assessments | Yes | `/api/academics/evaluation-submissions/` | Missing | Read-only requirement summary. |
| Research | Deferred web route | `/api/my/research/` | Missing | Read-only status summary. |
| Workshops | Deferred web route | `/api/my/workshops/` | Missing | Read-only completion summary. |
| Documents | Yes | `/api/resident-documents/` | Implemented | Moved under Requirements, preserved. |

Resident writes are limited to server-supported onboarding/document and academic-logbook actions.
Rotation assignment, assessment review, research approval, and workshop administration remain
server/staff controlled.
