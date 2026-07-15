# Known Limitations

- `SupervisorResidentLink` no longer exists in active code. Historical migration references remain by design.
- Several E2E suites still navigate through redirect-only legacy routes for compatibility checks.
- `frontend/lib/api/userbase.ts` remains a transitional helper pending a deeper split.
