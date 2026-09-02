# Analytics Dimensions

## Canonical Dimensions
- `hospital_id` is retained everywhere (single-hospital mode and future multi-hospital).
- `department_id` remains optional where domain context is unavailable.

## Hospital Resolver
Source: `backend/sims/analytics/dimensions.py`

`get_current_hospital_id(...)` resolution order:
1. Explicit hospital argument
2. Actor `home_hospital_id`
3. Request user `home_hospital_id`
4. `ANALYTICS_DEFAULT_HOSPITAL_ID`
5. First active hospital (single-hospital fallback)

If unresolved and event catalog disallows missing hospital, validation fails.

## Department Resolution
`resolve_department_id(...)` resolution order:
1. Explicit department argument
2. Actor `home_department_id`

## Domain Consistency
Current workflow instrumentation (logbook verify/create/submit) uses the same tracker and therefore the same dimension resolver path.
