# Stabilization Contract Decisions

## 1) Research action contract

- **Canonical action:** `supervisor-return`
- **Endpoint:** `POST /api/my/research/action/supervisor-return/`
- **Payload:** `{ "project_id": int, "feedback": str }`
- **Behavior:** transitions project back to `DRAFT`, stores supervisor feedback.
- **Compatibility:** `return-to-draft` remains supported as a backward-compatible alias.

## 2) Eligibility contract (`/api/my/eligibility/`)

- **Canonical response envelope:**
  - `{ resident_training_record, program, current_month_index, eligibilities: MilestoneEligibility[] }`
- **Canonical eligibility item field:**
  - `reasons: string[]`
- **Decision rationale:**
  - Keep the existing envelope (already used by backend and tests),
  - standardize reasons to `reasons` (frontend-consumable) instead of leaking model field name `reasons_json`.

## 3) Supervisor approvals row contract

- **Canonical resident display field:** `resident_name`
- **Decision:** frontend uses serializer-provided `resident_name` for row rendering.

## 4) Forgot-password contract

- **Canonical frontend integration:** `authApi.passwordReset(email)`
- **Endpoint:** `POST /api/auth/password-reset/`
- **Behavior:** submit email to backend endpoint, show API success/error feedback in-page, no placeholder timers.
