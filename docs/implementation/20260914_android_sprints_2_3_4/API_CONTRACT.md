# Android Sprints 2–4 API Contract

## Notifications

- `GET /api/notifications/` is recipient-scoped and paginated. Android uses `results`.
- Each record may include `target`: `{ "kind": "leave|evaluation|logbook|rotation|research|resident_progress", "id": positive-integer? }`.
  An absent target is display-only. Android must never route from arbitrary `metadata`.
- `GET /api/notifications/unread-count/` returns `{ "unread": number }`.
- `POST /api/notifications/mark-read/` and `POST /api/notifications/mark-unread/` accept
  `{ "notification_ids": [positive-integer] }`. IDs belonging to another user are ignored.

## Idempotent offline recovery

- Android adds a UUID `client_request_id` to `POST /api/leaves/`. The value is unique in
  `LeaveRequest`; a retry by the owning resident returns the original record with HTTP 200.
- Android adds a UUID `client_request_id` to `POST /api/academics/logbook-entries/`. The owning
  resident's key is retained in `extra_data.mobile_client_request_id`; a retry returns the
  original record with HTTP 200.
- Invalid UUIDs return validation errors. The server remains authoritative for all ownership,
  workflow-state, and field validation.

## Reporting

Android uses already-existing, authenticated scoped endpoints: resident training, rotations,
logbook, evaluations, research, workshops, `residents/me/summary/`, and supervisor resident
progress. No mobile export or administrative report endpoint is introduced.
