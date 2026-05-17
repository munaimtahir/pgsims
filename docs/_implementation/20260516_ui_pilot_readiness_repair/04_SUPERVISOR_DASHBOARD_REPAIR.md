# Supervisor Dashboard Repair

## Problem

The supervisor dashboard was readable but too sparse and did not foreground pending work clearly enough.

## Fix

- Added a clearer top-level work summary.
- Prioritized:
  - My residents
  - Pending logbook reviews
  - Pending approvals
  - Recent submissions
  - Alerts / needs attention
- Added a calm empty state when no residents are assigned.

## Empty-State Text

- `No residents are assigned to you yet.`
- `Once UTRMC assigns residents, pending reviews and submissions will appear here.`

