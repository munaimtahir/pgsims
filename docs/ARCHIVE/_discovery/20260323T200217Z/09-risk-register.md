# Risk Register

| Title | Severity | Impact | Evidence | Why it matters | Recommended direction |
|---|---|---|---|---|---|
| Contract/runtime drift on logbook | Critical | Core workflow trust loss | `API_CONTRACT.md` references logbook API; frontend logbook pages absent; root URLs do not include legacy logbook API | Teams may plan on non-functional core flow | Reconcile contract, URL wiring, and frontend route availability immediately |
| Frontend lint gate failing | High | Release quality and maintainability | `npm run lint` errors across dashboard/api modules | Technical debt accumulates; CI confidence weak | Fix lint debt before feature expansion |
| Legacy + active module duality | High | False completeness and onboarding confusion | `_legacy/*` modules remain with models/tests/docs references | Easy to misread implemented vs active runtime surface | Publish active-surface map and enforce ownership boundaries |
| Documentation fragmentation | High | Planning errors | Missing files referenced in README, overlapping docs trees | Stakeholders can make wrong priority decisions | Consolidate and mark canonical docs per domain |
| Build process stability uncertainty | Medium | Deployment confidence gap | `next build` progressed but did not cleanly terminate in this run | Could hide environment/build regressions | Re-run build in controlled CI shell and capture definitive exit |
| Env/secret dependency fragility | Medium | Setup friction and failed verifications | Backend tests/check fail without `SECRET_KEY`; compose warnings for missing secrets | New environments fail fast without clear preflight | Add strict env preflight script + docs alignment |
| Profile endpoint duplication | Low | Contract ambiguity | `/api/auth/profile/` and `/api/auth/me/` both exist | Payload drift risk between clients | Deprecate one endpoint and document canonical response |
