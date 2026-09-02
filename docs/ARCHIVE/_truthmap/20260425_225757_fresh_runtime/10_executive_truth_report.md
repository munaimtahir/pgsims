# Stage 10: Executive Truth Report

## Executive Summary

The previous truthmap was contaminated by an invalid runtime baseline.

Fresh evidence now shows:

- the frontend container had been missing from the active PGSIMS compose stack
- after a no-cache rebuild, the current Next.js frontend is being served from a fresh image and fresh container
- most previous dashboard `404` claims were false positives caused by stale or absent frontend runtime

## What Is Now Confirmed Working

- resident dashboard, logbook, and schedule routes
- supervisor dashboard
- UTRMC overview, users, programs, and supervision routes
- resident logbook create/submit
- supervisor logbook review
- resident leave create/submit
- supervisor leave approve/reject
- bulk UI presence, template download, export download, dry-run validation

## What Is Still Actually Broken

- Data Quality frontend integration
- Supervision link save flow from the current UI
- top-level Program create/edit UI
- Workshops frontend discovery/active workflow

## Direct Answers

- Program create/edit present: No
- Training Program frontend present: Yes, partial
- Workshop frontend present: Deferred route exists, not active in nav
- Resident Logbook frontend present: Yes
- Supervisor Logbook Review frontend present: Yes
- Leave workflow frontend present: Yes
- Data Quality working: No, frontend proxy mismatch
- Bulk UI present: Yes

## Audit Correction

Do not use the old truthmap as the source of route truth.

Use this fresh-runtime audit plus the Docker-fix evidence folder for current route/module truth:

- `docs/_truthmap_docker_fix/20260425_223918/`
- `docs/_truthmap/20260425_225757_fresh_runtime/`
