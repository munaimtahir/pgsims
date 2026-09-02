# Model Spec

This document describes the Brick 7 supervision model.

## Primary Model

`ResidentSupervisorAssignment`

### Fields

- `resident`
- `supervisor`
- `assignment_type`
- `start_date`
- `end_date`
- `status`
- `is_active`
- `notes`
- `reason_for_change`
- `created_by`
- `updated_by`
- `created_at`
- `updated_at`
- `extra_data`

### Assignment Types

- `PRIMARY`
- `CO_SUPERVISOR`

### Status Values

- `ACTIVE`
- `ENDED`
- `SUSPENDED`

## Constraints

1. One active primary supervisor per resident.
2. No duplicate active assignment for the same resident, supervisor, and assignment type.
3. Ended assignments require an end date.
4. Active assignments cannot have an end date.

## Audit

The model is paired with service-layer audit logging for create, end, and primary-change actions.
