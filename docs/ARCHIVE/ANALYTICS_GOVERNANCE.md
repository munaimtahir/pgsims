# Analytics Governance

## Event Catalog
Canonical source: `backend/sims/analytics/event_catalog.py`
- Event naming: `domain.object.action`
- Each event defines:
  - description
  - required metadata keys
  - allowed metadata keys
  - whether missing `hospital_id` is allowed
  - whether UI ingest is allowed

## Validation Enforcement
Validation is enforced in:
- `track_event(...)`
- `POST /api/analytics/events/`

Checks include:
- event type must exist in catalog (unless explicitly unlisted)
- required metadata keys present
- metadata keys allowlisted per event type
- metadata max size (`8KB`)
- non-system events require hospital dimension

## PII Guardrails
Blocked metadata key tokens include:
- `name`, `email`, `phone`, `mobile`, `mrno`, `address`, `cnic`, `dob`, `patient`, `password`, `token`

Behavior:
- blocked keys are rejected (400 at ingest, validation failure in helper)
- free-form keys outside allowlist are rejected

## Rejection Telemetry
Model: `AnalyticsValidationRejection`
- captures validation failures for auditability and trend analysis
- consumed by `GET /api/analytics/v1/quality/`
