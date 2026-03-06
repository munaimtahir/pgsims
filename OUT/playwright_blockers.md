# PGSIMS Playwright — Blocker Report

Generated: 2026-03-06

This document lists known gaps that **could not be responsibly covered** in the
current E2E suite because the corresponding frontend features are not yet built.

---

## BLOCKER-001: Logbook Module — No Frontend UI

**Affected workflows:**
- Resident creates logbook entry
- Resident submits entry to supervisor
- Supervisor reviews, approves, returns entry
- Status transition display (draft → pending → approved/returned)

**Root cause:**
The logbook frontend exists only as legacy Django HTML views at `/logbook/pg/entries/`
(rendered by the Django backend, not the Next.js frontend). The Next.js frontend has
no logbook pages under `app/dashboard/`.

The `regression/logbook_submit_return_resubmit_approve.spec.ts` spec covers the API
contract test but cannot drive a real frontend workflow.

**Required fix:** Build logbook pages in `frontend/app/dashboard/resident/logbook/`
and `frontend/app/dashboard/supervisor/logbook/`.

---

## BLOCKER-002: Clinical Cases — No Frontend UI

**Affected workflows:**
- Resident creates clinical case
- Resident submits case for review
- Supervisor/admin reviews case

**Root cause:** Cases module exists only as legacy Django HTML views.
Frontend pages not present in `app/dashboard/`.

---

## BLOCKER-003: Certificates — No Frontend UI

**Affected workflows:**
- Certificate submission, bulk approval, compliance views

**Root cause:** Certificates module exists only as legacy Django HTML views.

---

## BLOCKER-004: Leave Requests — Not in Navigation

**Root cause:** Leave request pages not present in the Next.js frontend nav registry
(`lib/navRegistry.ts`). The backend API exists (`/api/my/leaves/`) but no frontend page.

---

## BLOCKER-005: Notifications — Not in Navigation

**Root cause:** While the backend notification API exists (`/api/notifications/`),
there is no dedicated notification page in the Next.js frontend nav.

---

## BLOCKER-006: Analytics Dashboard — Not in Frontend

**Root cause:** The legacy analytics app exists at `sims/_legacy/analytics/` but
no analytics pages exist in the Next.js `app/dashboard/` folder.

---

## BLOCKER-007: HOD Assignments Page Not Wired in Nav

**Root cause:** The page `/dashboard/utrmc/hod` exists but is not included
in the sidebar nav registry (`lib/navRegistry.ts`). It may load but cannot
be reliably found via nav-based test selectors.

**Mitigation:** Tests access it directly by URL — not a full blocker but nav
coverage is incomplete.

---

## Non-Blockers (Addressed)

| Issue | Resolution |
|-------|-----------|
| No `data-testid` on logout button | Added `data-testid="sidebar-logout-btn"` |
| No `data-testid` on form elements | Tests use semantic locators (`getByRole`, `getByLabel`, `getByText`) |
| Server lacks browser libs | Run tests via `mcr.microsoft.com/playwright:v1.56.1-jammy` Docker image |
| e2e_pg had no training record | `seed_e2e.py` already creates 3 rotations; research/thesis endpoints return 404 gracefully |
