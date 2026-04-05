# Data Correction Layer QA Checklist

## Access and permissions
- [ ] `utrmc_admin` can open `/dashboard/utrmc/data-quality`
- [ ] `admin` can open `/dashboard/utrmc/data-quality`
- [ ] `utrmc_user` cannot access admin data-quality APIs

## Dashboard integrity
- [ ] Summary counts load without error
- [ ] Filter buttons update resident table rows correctly
- [ ] Issue badges reflect `data_issues` values

## Inline correction
- [ ] Edit modal saves `email` update
- [ ] Edit modal saves `year` update (supports 1–5)
- [ ] Edit modal saves training date/level updates
- [ ] Flags recompute after save
- [ ] Resident completeness status updates accordingly

## Bulk correction command
- [ ] Dry-run prints changes and does not mutate DB
- [ ] Apply mode requires `--confirm`
- [ ] Apply updates records and produces update/skip/error totals
- [ ] Invalid email/year/date rows are rejected with clear errors

## Auditability
- [ ] UI edits create `DataCorrectionAudit` rows
- [ ] CSV apply creates `DataCorrectionAudit` rows with metadata
- [ ] `/api/admin/data-quality/audit` returns recent events

## Regression safety
- [ ] Existing userbase endpoints remain functional
- [ ] Existing pilot resident/supervisor roster loads unchanged
