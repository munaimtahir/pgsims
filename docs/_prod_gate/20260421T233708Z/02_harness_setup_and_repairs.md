# Harness Setup And Repairs

## Repairs Applied
- Created isolated backend coverage venv:
  - `python3 -m venv ../OUT/prod_gate_artifacts/20260421T233708Z/backend-venv`
  - installed `backend/requirements.txt` and `backend/requirements-dev.txt`
- Repaired Playwright smoke selector ambiguity on UTRMC overview stat labels.
- Repaired navigation suite to assert current active nav:
  - supervisor: `Overview`, `My Residents`; no `Research Approvals`
  - resident: `My Dashboard`, `My Schedule`, `Logbook`; no research/thesis/workshops
- Repaired workflow gate to current active truth:
  - kept forgot-password, bulk dry-run, resident leave create/submit/approve
  - removed de-scoped research, rotation, and posting workflow assertions from the active workflow gate
  - updated leave card selectors to current UI classes

## Not Repaired In This Pass
- Coverage threshold gap. This requires substantial new tests across active backend/frontend modules, not a small harness fix.
- OpenAPI generation wiring. Existing contracts are handwritten and authoritative; generated schema tooling is not configured.

