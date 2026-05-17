# Baseline And Scope

## Branch And Commit

- Branch: `codex/dead-code-cleanup`
- Commit: `e21ec23`

## Scope

This sprint is limited to pilot-readiness UI repairs on the cleaned baseline.

In scope:

- Resident dashboard null safety
- Resident schedule null safety
- UTRMC overview simplification
- Dedicated onboarding/import landing route
- Supervisor dashboard readability and empty states
- Admin table accessibility polish
- Data quality calm fallback behavior

Out of scope:

- Broad feature redesign
- Route/nav terminology changes beyond the new onboarding landing route
- Backend contract changes
- Data model changes

## Baseline Confirmation

- The prior UI truthmap audit identified the resident dashboard crash, the schedule fallback gap, the import-heavy UTRMC overview, sparse supervisor dashboard treatment, and dense admin tables as the main pilot risks.
- The cleaned baseline still uses the current backend contracts and does not require payload changes for these UI repairs.

