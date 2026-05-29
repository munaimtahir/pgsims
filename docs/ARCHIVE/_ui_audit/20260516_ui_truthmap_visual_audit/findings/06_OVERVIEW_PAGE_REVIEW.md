# Overview Page Review

## Current Layout Summary

The current UTRMC overview page is not just a summary dashboard. It mixes:

- Top-level operational counts
- Data-quality status
- Cross-department readiness
- Certificate verification queues
- A multi-step import and export workspace
- Rotation creation controls
- Draft, submitted, active, returned, and rejected rotation sections

The live screenshot shows the import workspace occupying most of the page:

- [`docs/_ui_audit/20260516_ui_truthmap_visual_audit/screenshots/utrmc_overview.png`](/home/munaim/srv/apps/pgsims/docs/_ui_audit/20260516_ui_truthmap_visual_audit/screenshots/utrmc_overview.png)

## Why It Confuses Users

- The primary screen reads like a control room for imports, not a simple operational dashboard
- Senior doctors and supervisors do not need to see hospital/departments upload steps before they see today’s work
- The page buries the meaningful summary under large import cards
- The wording is technical and assumes users understand setup sequencing

## What Should Stay On Overview

- Current role / welcome
- System status
- Today’s pending work
- Important alerts
- Resident / supervisor / UTRMC counts
- Brief data-health summary
- Latest imports as a small summary card only
- One clear quick action to open onboarding tools

## What Should Move Out

- Step-by-step import engine sections
- File upload controls
- Export controls
- Detailed column expectations
- Rotation draft creation form
- Long technical prerequisite notes

## Recommended New Layout

1. Top row with welcome, role, and system status
2. Three or four summary cards for today’s priorities
3. One alert panel for data issues
4. A concise “Import & onboarding tools” card with a single button
5. Role-aware task panels for UTRMC/admin, supervisor, and resident
6. Recent activity or latest changes at the bottom

## Recommendation

The overview page should become a simple operations dashboard, with onboarding/import moved to a dedicated workflow page. The current page is useful to admins, but it is too technical to be the first screen for non-technical users.

