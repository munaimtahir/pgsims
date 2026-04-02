# Rotation and Postings Closure Scorecard

| Dimension | Score | Justification |
|---|---:|---|
| Active-surface truth preservation | 9/10 | Closure stayed on existing routes and did not reactivate deferred legacy surfaces. |
| Rotation workflow completeness | 9/10 | Draft, submit, approve, activate, and complete are now verified end to end on the active surface. |
| Postings workflow completeness | 9/10 | Resident create plus UTRMC approve/complete is now verified end to end on the active surface. |
| Frontend stability after change | 8/10 | Lint, typecheck, unit tests, build, smoke, and workflow gate all passed after the changes. |
| Backend confidence after change | 9/10 | Full active backend suite plus targeted rotation tests and drift gates passed. |
| Contract/runtime alignment | 9/10 | Rotation/postings payloads, statuses, roles, and docs now materially align with runtime. |
| Runtime verification confidence | 9/10 | Current-tree Playwright workflow gate passed with the new rotation/postings scenarios. |
| Readiness for next milestone | 8/10 | Safe to proceed on the active surface, with deferred legacy modules still explicitly out of scope. |
