# PROD Gate Blocker Recheck

| Old Blocker | Still Present? | Evidence | Current Severity | Recommended Action |
|---|---|---|---|---|
| #1 Schema | UNKNOWN | not re-run in this sprint | unknown | rerun schema validation |
| #2 E2E dashboard rendering | PARTIAL | smoke/active-surface now pass; legacy admin tests still fail | medium | rebaseline legacy admin tests or implement admin surface |
| #3 E2E logbook | NO | active-surface logbook workflow passed | low | none |
| #4 Restart/reseed smoke | YES, now working locally | restart + seed + smoke passed | low | add explicit restart smoke check if desired |
| #5 Backend coverage | UNKNOWN | coverage not re-run | unknown | rerun coverage gate |
| #6 Frontend coverage | UNKNOWN | coverage not re-run | unknown | rerun coverage gate |
| #7 Routes/APIs | PARTIAL | active routes pass; legacy admin route not implemented | medium | rebaseline legacy route expectations |
| #8 CTAs | PARTIAL | active CTAs pass; legacy admin CTA expectations fail | medium | rebaseline legacy admin tests |
| #9 Transitions | PARTIAL | active workflows pass; one research workflow is deferred | medium | rebaseline deferred workflow or implement it |
| #10 Unauthorized | YES, passing | negative suite passed | low | none |
| #11 UTRMC admin | PARTIAL | UTRMC admin pages pass; admin legacy route fails | medium | keep UTRMC baseline; retire legacy admin test |

