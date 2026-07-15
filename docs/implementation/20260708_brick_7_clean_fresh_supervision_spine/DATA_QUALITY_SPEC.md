# Data Quality Spec

This document describes the supervision data-quality checks used by Brick 7.

## API

- `GET /api/supervision/data-quality/`

## Expected Output

The endpoint returns grouped anomaly counts and drill-down rows for:

- missing resident profile links
- missing supervisor profile links
- missing active primary supervisor assignments
- duplicate active assignments
- inactive or broken supervision records
- other consistency anomalies exposed by the supervision service layer

## Frontend

The canonical frontend surface is:

- `/dashboard/utrmc/data-quality`

That page renders the dashboard summary and expandable sections for issue categories.

## Behavior

1. Only admin users can access the backend endpoint.
2. The frontend shows aggregate counts and drill-down rows.
3. The data-quality page is read-only and refreshable.
