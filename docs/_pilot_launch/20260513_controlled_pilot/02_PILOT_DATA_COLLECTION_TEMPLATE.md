# Pilot Data Collection Template

**Pilot Date**: TBD
**Data Owner**: TBD (UTRMC Lead)
**Created**: 2025-05-13

---

## Instructions

1. Gather resident data from HR/training records
2. Match each resident with their current supervisor
3. Verify all dates are accurate
4. Provide this data to IT for bulk import (dry-run first)
5. Reconcile any discrepancies with department heads
6. Review import preview report before committing

---

## Resident Data Roster

| Resident Name | Program | Year | Department | Home Hospital | Current Supervisor | Email | Phone | Training Start Date | Expected End Date | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TBD | General Surgery | PGY-1 | [Dept] | [Hospital] | TBD | TBD | TBD | TBD | TBD | active | |
| TBD | General Surgery | PGY-1 | [Dept] | [Hospital] | TBD | TBD | TBD | TBD | TBD | active | |
| TBD | General Surgery | PGY-2 | [Dept] | [Hospital] | TBD | TBD | TBD | TBD | TBD | active | |
| TBD | General Surgery | PGY-2 | [Dept] | [Hospital] | TBD | TBD | TBD | TBD | TBD | active | |
| TBD | General Surgery | PGY-3 | [Dept] | [Hospital] | TBD | TBD | TBD | TBD | TBD | active | |
| TBD | Internal Medicine | PGY-1 | [Dept] | [Hospital] | TBD | TBD | TBD | TBD | TBD | active | |
| TBD | Internal Medicine | PGY-1 | [Dept] | [Hospital] | TBD | TBD | TBD | TBD | TBD | active | |
| TBD | Internal Medicine | PGY-2 | [Dept] | [Hospital] | TBD | TBD | TBD | TBD | TBD | active | |
| TBD | Pediatrics | PGY-1 | [Dept] | [Hospital] | TBD | TBD | TBD | TBD | TBD | active | |
| TBD | Pediatrics | PGY-2 | [Dept] | [Hospital] | TBD | TBD | TBD | TBD | TBD | active | |

**Total Residents**: 10 (can vary 5–10)

---

## Program Distribution

| Program | Count | Department | Status |
|---------|-------|-----------|--------|
| General Surgery | 3 | [TBD] | target |
| Internal Medicine | 3 | [TBD] | target |
| Pediatrics | 2 | [TBD] | target |
| Other | 2 | [TBD] | optional |

---

## Data Validation Checklist

- [ ] All resident names verified with HR
- [ ] All programs match training records
- [ ] All years accurate as of pilot date
- [ ] All supervisors confirmed and active
- [ ] All email addresses in corporate domain
- [ ] All phone numbers in valid format
- [ ] No duplicate residents
- [ ] All start dates in past (pilot date or earlier)
- [ ] All end dates in future (pilot duration or longer)
- [ ] All status values are "active", "on-leave", or "completed"
- [ ] Department matches actual assignment
- [ ] Hospital matches home hospital in system

---

## Import Process (After Approval)

1. **Export this template to CSV**
   - Format: CSV with headers
   - Encoding: UTF-8
   - Save as: `pilot_resident_data_[DATE].csv`

2. **Dry-Run Import**
   - Use `/api/bulk/preview` endpoint
   - Upload CSV file
   - Review validation report
   - Note any warnings or errors

3. **Dry-Run Report Review**
   - [ ] Validation report shows 0 errors (warnings okay)
   - [ ] All residents recognized
   - [ ] All supervisors recognized
   - [ ] All departments valid
   - [ ] No data loss detected

4. **Commit Import** (After approval)
   - Use `/api/bulk/import` endpoint
   - Verify commit returned success
   - Run quick sanity check on dashboard
   - Confirm all residents visible to supervisors

5. **Post-Import Verification**
   - [ ] All residents created in system
   - [ ] All supervisors assigned correctly
   - [ ] All relationships visible on dashboards
   - [ ] No orphaned records
   - [ ] Audit log shows import transaction

---

## Data Reconciliation

If dry-run shows errors:
1. Document error message exactly
2. Identify affected rows
3. Contact data owner for correction
4. Update this template
5. Re-run dry-run
6. Repeat until 0 errors

---

**Template Version**: 1.0
**Last Updated**: 2025-05-13
