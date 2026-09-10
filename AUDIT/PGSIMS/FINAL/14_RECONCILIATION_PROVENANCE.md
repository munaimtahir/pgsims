# RECONCILIATION PROVENANCE

## Common Baseline
- **Expected Baseline SHA:** 94d2a867a1b3683009d972adfb780ddc8e365754
- **Actual Verified Baseline SHA:** 94d2a867a1b3683009d972adfb780ddc8e365754

## Audit Session Sources

### Session A
- **Expected Branch:** audit/pgsims-a-truthmap-8158542665422048267
- **Actual Remote Branch:** origin/audit/pgsims-a-truthmap-8158542665422048267
- **Actual HEAD SHA:** b93816497ba88a8919184362d91c6e578f55acd4
- **Audit Only:** Yes
- **Discrepancies:** No discrepancies noted.

### Session B
- **Expected Branch:** audit/pgsims-b-workflow-security-4009719822637452867
- **Actual Remote Branch:** origin/audit/pgsims-b-workflow-security-400971982263745286
- **Actual HEAD SHA:** ce383e12dbd17d21149c7f4f6cda257b169286a2
- **Audit Only:** Yes
- **Discrepancies:** Branch suffix truncated in git remotes (ending in `286` rather than `2867`). `00_B_SESSION_SUMMARY.md` HEAD SHA was left as "REPLACE_ME". Actual Git Truth overrides.

### Session C
- **Expected Branch:** audit/pgsims-c-production-readiness
- **Actual Remote Branch:** origin/audit/pgsims-c-production-readiness-8787057082687975856
- **Actual HEAD SHA:** 3ebfeae18f515c6cfe633fd318ed1b2f27cea508
- **Audit Only:** Yes
- **Discrepancies:** Remote branch has a task suffix `8787057082687975856`. The closed SHA `e241e5...` or `7680e4...` mentioned in reports are superseded by the actual remote truth `3ebfeae`.
