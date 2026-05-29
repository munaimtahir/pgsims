# Stage 8: Corrected Verified Gap Register

Only gaps that remain after the clean frontend rebuild and fresh-runtime verification are listed here.

## GAP-001: Data Quality Frontend Fails Through Proxy

- Type: `CONFIRMED_REAL_GAP`
- Severity: High
- User impact: UTRMC/admin data-quality page shell loads, but data never loads
- Evidence:
  - browser `404` on proxied data-quality requests
  - direct backend calls to the same logical endpoints return `200`
  - frontend proxy always appends trailing slash
- Root cause class: frontend-backend route/proxy mismatch

## GAP-002: Supervision Link Create Flow Is Broken

- Type: `CONFIRMED_REAL_GAP`
- Severity: High
- User impact: UTRMC/admin can open the modal but cannot save a supervision link from the current UI
- Evidence:
  - UI save attempt returns `Save failed`
  - backend validation requires `supervisor_user_id` and `resident_user_id`
  - current page posts `supervisor` and `resident`
- Root cause class: payload contract drift

## GAP-003: Program Create/Edit UI Is Absent

- Type: `CONFIRMED_REAL_GAP`
- Severity: Medium
- User impact: UTRMC/admin can browse existing programs and some sub-management tabs, but cannot visibly create or edit a top-level program from the current page
- Evidence:
  - programs route loads
  - no visible create button
  - no visible edit button
  - page is centered on existing-program detail tabs only

## GAP-004: Workshops Frontend Is Deferred / Not Discoverable

- Type: `CONFIRMED_REAL_GAP`
- Severity: Medium
- User impact: resident cannot discover or use a working workshops UI from the active dashboard nav
- Evidence:
  - workshops route file exists
  - workshops is not in resident nav
  - workshops page is a deferred notice
  - backend endpoints exist but current seed has no workshop runtime data

## Not A Fresh-Runtime Gap

These previous claims did not survive the clean rebuild:

- “All dashboards 404”
- “Programs page 404”
- “Supervision page 404”
- “Resident logbook page 404”
- “Supervisor logbook review UI missing”
- “Resident leave request UI missing”
- “Supervisor leave approval UI missing”
- “Bulk UI missing”
