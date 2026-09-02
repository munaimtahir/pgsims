# Supervisor-Resident Mapping Template

**Pilot Date**: TBD
**Created**: 2025-05-13

---

## Instructions

1. For each supervisor, list all residents they will supervise during pilot
2. Verify all mappings with department head
3. Ensure each resident has exactly 1 primary supervisor
4. Mark secondary supervisors where applicable
5. Provide this mapping before pilot data import

---

## Supervisor-Resident Mappings

| Supervisor | Supervisor Email | Resident | Program | Year | Role | Active From | Verified By | Notes |
|---|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | General Surgery | PGY-1 | primary | TBD | TBD | |
| TBD | TBD | TBD | General Surgery | PGY-1 | primary | TBD | TBD | |
| TBD | TBD | TBD | General Surgery | PGY-2 | primary | TBD | TBD | |
| TBD | TBD | TBD | General Surgery | PGY-2 | primary | TBD | TBD | |
| TBD | TBD | TBD | General Surgery | PGY-3 | primary | TBD | TBD | |
| TBD | TBD | TBD | Internal Medicine | PGY-1 | primary | TBD | TBD | |
| TBD | TBD | TBD | Internal Medicine | PGY-1 | primary | TBD | TBD | |
| TBD | TBD | TBD | Internal Medicine | PGY-2 | primary | TBD | TBD | |
| TBD | TBD | TBD | Pediatrics | PGY-1 | primary | TBD | TBD | |
| TBD | TBD | TBD | Pediatrics | PGY-2 | primary | TBD | TBD | |

---

## Supervisor Summary

| Supervisor | Count of Residents | Verified? | Contact Email | Notes |
|---|---|---|---|---|
| TBD | 3–4 | ❌ | TBD | Primary supervisor |
| TBD | 3–4 | ❌ | TBD | Secondary supervisor |
| TBD | 1–2 | ❌ | TBD | Tertiary supervisor |

---

## Verification Checklist

- [ ] All supervisors are active and available during pilot
- [ ] Each resident has exactly 1 primary supervisor
- [ ] No resident is unassigned
- [ ] No supervisor exceeds workload capacity (suggest 3–4 residents max)
- [ ] All relationships verified with department head
- [ ] All active dates are on or before pilot start date
- [ ] No supervisor-resident conflicts of interest
- [ ] Supervisor contact information current

---

## During Pilot Adjustments

If supervisor-resident mappings need to change:
1. Document reason for change
2. Get approval from UTRMC lead
3. Update this mapping file
4. Run update via `/api/supervisors/[id]/residents` endpoint
5. Verify change visible on both dashboards
6. Log change in issue tracker

---

## Handoff to System

Once verified:
1. Export this table to CSV format
2. Use with 02_PILOT_DATA_COLLECTION_TEMPLATE.md
3. Include both in bulk import dry-run
4. Verify all relationships created correctly
5. Confirm supervisors can see their residents on dashboard

---

**Template Version**: 1.0
**Last Updated**: 2025-05-13
