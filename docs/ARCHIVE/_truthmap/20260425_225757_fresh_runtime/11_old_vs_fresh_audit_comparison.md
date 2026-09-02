# Stage 11: Old vs Fresh Audit Comparison

Old audit baseline: `docs/_truthmap/20260425_215047/`

Fresh audit baseline: `docs/_truthmap/20260425_225757_fresh_runtime/`

## Comparison Table

| Old finding | Fresh result | Classification |
|---|---|---|
| All dashboards `404` | Resident, supervisor, UTRMC, programs, supervision, users all load after clean rebuild | `FALSE_POSITIVE_DUE_TO_STALE_DOCKER` |
| Programs page `404` | Programs route loads `200` | `FALSE_POSITIVE_DUE_TO_STALE_DOCKER` |
| Supervision Links page `404` | Page loads `200`, but save flow fails | `PARTIALLY_TRUE` |
| Resident logbook page `404` | Route loads `200`; create/submit works | `FALSE_POSITIVE_DUE_TO_STALE_DOCKER` |
| Supervisor logbook review UI missing | UI exists on supervisor dashboard and review works | `FALSE_POSITIVE_DUE_TO_STALE_DOCKER` |
| Leave workflow missing | Resident and supervisor leave flows both work | `FALSE_POSITIVE_DUE_TO_STALE_DOCKER` |
| Bulk UI missing | Bulk UI exists on UTRMC overview; template/export/dry-run are wired | `FALSE_POSITIVE_DUE_TO_STALE_DOCKER` |
| Workshops not in nav | Still not in nav; route is deferred | `CONFIRMED_REAL_GAP` |
| Data Quality page `404` | Page shell loads, but frontend proxy calls fail | `PARTIALLY_TRUE` |
| “Create Program button likely exists” | Fresh loaded page shows no visible create button | `CONFIRMED_REAL_GAP` |
| “Edit Training Program likely exists” | Fresh loaded page shows no visible edit button | `CONFIRMED_REAL_GAP` |

## Corrected Interpretation

### False positives caused by stale Docker / missing frontend runtime

- blanket dashboard `404` claims
- logbook page `404`
- programs page `404`
- supervision page `404`
- bulk UI missing
- supervisor logbook review UI missing
- leave workflow UI missing

### Real gaps that remain

- Data Quality frontend proxy/path mismatch
- Supervision Links payload mismatch on save
- Program create/edit UI absent
- Workshops frontend deferred and not discoverable in nav

### Seed/data-limited areas

- Workshop completion workflow could not be fully exercised because the current seeded baseline returned zero workshops and zero completions
- Classification: `REQUIRES_SEEDED_DATA`
