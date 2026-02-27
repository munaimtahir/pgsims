# Analytics Live Feed

## Endpoint
`GET /api/analytics/events/live`

### Query Params
- `cursor` (`occurred_at|id`)
- `limit` (max 200)
- `start_date`, `end_date`
- `department_id`
- `hospital_id`
- `role`
- `event_type_prefix`
- `entity_type`

### Ordering
- Stable ordering: `occurred_at DESC, id DESC`

### Cursor Semantics
- Initial call (no cursor): returns latest window and `cursor` for newest row.
- Poll call (with cursor): returns only rows newer than cursor.

## Frontend Behavior
Admin analytics page live tab:
- Poll interval: 7 seconds
- Stores cursor from response
- Dedupe by `id`
- Caps list at 200 rows
- Additional filters: `event_type_prefix`, `entity_type` (with existing role/department filters)

## Drilldown Safety
Rows can include `drilldown_url` only for known entity types.
Frontend renders drilldown links only when URL is present.
