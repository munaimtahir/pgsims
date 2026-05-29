# Executive Summary

## Overall System Verdict

The current system is believable on a narrow, truth-aligned active surface, not across the broader product claims still present in top-level docs.

- The active resident, supervisor, and UTRMC rotation/postings surface is real and runtime-verified.
- The recovered leave and research approval paths remain real and verified.
- Several other active pages exist and load correctly, but they have not yet crossed the same end-to-end verification bar.
- Multiple legacy capabilities are still present only as historical code or README language, not as active runtime truth.

## Confidence Level

Medium-high.

Confidence is high for the promoted active workflows that passed current-tree browser gates. Confidence is lower for secondary active pages that are only backed by route inspection, page inspection, backend presence, and lighter Playwright coverage.

## Category Counts

- `NOT DONE`: 6
- `DONE BUT NEEDS DEBUGGING`: 8
- `WORKING PERFECTLY`: 6

## Biggest Truths Learned

1. The app is no longer generally “broken”; it has a real, functioning active core.
2. “Working” is concentrated in a smaller verified surface than the README implies.
3. Rotation, postings, leave, resident dashboard eligibility, and supervisor research review are now the strongest parts of the system.
4. UTRMC program-administration pages are active and usable-looking, but most are still only lightly verified.
5. Deferred legacy surfaces remain deferred in runtime truth:
   - logbook
   - cases
   - legacy analytics
   - certificates/search/reporting ecosystems tied to `_legacy`
6. Top-level documentation still overclaims active scope:
   - certificate management
   - broad analytics/reporting
   - global search
   - broad CSV export

## Biggest Risks

1. Leadership could still read README/docs and assume wider functional readiness than runtime supports.
2. Admin/userbase/program pages look operational but lack the same end-to-end proof as the verified workflow-gate surfaces.
3. Build confidence is acceptable, but the frontend build path is still lenient:
   - `next build` ignores lint/type failures by config
   - `next start` is mismatched with `output: 'standalone'`
4. Test/runtime drift still exists in at least one regression suite:
   - `frontend/e2e/regression/utrmc_readonly_dashboard.spec.ts` expects UI/testids and logbook wording no longer present
5. Rapid re-login during automation hit a transient `429` on `/api/auth/login/`; the workflow run still passed, but auth throttling behavior should be treated as a hardening item rather than silently ignored.

## Recommended Next Milestone

P1: active-surface hardening on the non-deferred pages already exposed in navigation:

- UTRMC master-data and program-administration hardening
- thesis/workshops/progress/eligibility secondary workflow verification
- docs/runtime cleanup for remaining overclaims and stale route references

Do **not** move next into logbook, cases, legacy analytics, certificates, or search reactivation.
