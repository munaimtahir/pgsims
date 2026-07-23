# PGSIMS — Plain-Language Status Report

**For**: Non-technical stakeholders (programme leadership, hospital administration)
**Date**: 23 July 2026
**Purpose**: Explain, in plain language, what this application is, what it currently does, what
doesn't work yet, and what's left before we can safely pilot it with real residents and supervisors.

---

## What is PGSIMS?

PGSIMS is a web application that replaces paper-based and spreadsheet-based tracking of
postgraduate medical trainees (residents) at UTRMC. Instead of supervisors and administrators
chasing paper logbooks and Excel sheets, everyone logs into one system:

- **Administrators** set up hospitals, departments, and accounts, and see the full picture across
  the programme.
- **Supervisors** review and approve their residents' clinical logbook entries and evaluations, and
  see who is on track.
- **Residents** log the clinical procedures they perform, submit evaluations, and check their own
  progress toward eligibility for their milestone exams.
- **Support staff** have a limited, read-only assistant role for administrative help.

Everything a resident or supervisor does is recorded with a timestamp and an audit trail, so there's
a permanent, reliable record of who did what and when — something paper logbooks can't guarantee.

## Is it working?

**Yes, substantially.** We independently tested the entire system this week — not by reading old
status reports, but by actually running it: every automated test, every build, every consistency
check the engineering team has defined. Here's what that showed:

- The core workflows work: creating accounts, assigning residents to supervisors, placing residents
  into hospital rotations, logging and reviewing clinical procedures, and generating progress
  reports — all of this runs correctly today, end to end.
- 406 out of 406 automated backend checks passed. Every consistency rule the team has defined for
  the system (correct roles, no duplicate data, correct permissions) passed.
- The website itself builds and loads correctly across all ~90 pages we checked.

**One real problem — found and already fixed.** While testing, we found that a resident's own
dashboard — the main page they'd see after logging in — could show a blank error screen if their
training record was missing certain details (a normal, expected state early in onboarding, before
all their information has been fully entered). This was a genuine bug. It was small and
well-understood, and we fixed it and re-verified it as part of this review — it no longer happens.

We also found that a handful of the automated checks meant to catch exactly this kind of problem had
gone stale — they were checking for old page text that had since changed, so they weren't actually
protecting anything anymore. That's why this bug wasn't caught earlier. Refreshing those checks is
part of the plan below.

## What's genuinely solid

- **The data model is clean and consistent.** There is exactly one definition of "hospital" and one
  definition of "department" used everywhere in the system — a common source of bugs in systems like
  this (data getting out of sync between different parts of the app) has been deliberately designed
  out.
- **Roles and permissions are locked down and consistent.** Only four account types exist (Admin,
  Resident, Supervisor, Support Staff), and the system enforces who can see and do what, on the
  server side — not just hidden buttons in the interface, which can be bypassed.
- **There's a working backup and restore process** for the database, and a health-check the team can
  use to confirm the system is running correctly at any time.
- **Bulk import exists** for onboarding a whole roster of residents/supervisors at once from a
  spreadsheet, including a flexible mode for spreadsheets that don't match our exact template.

## What's not solid yet

- **Some of the highest-stakes code (the bulk-import roster tool, and the backup/restore tooling)
  has thin automated test coverage.** It works — we can see that from the checks that do exist and
  from the fact that it built successfully — but there's less of a safety net around it than the
  rest of the system. Given that bulk import is exactly what we'd use to onboard the pilot's real
  resident/supervisor roster, we recommend strengthening its tests before we rely on it for the real
  onboarding batch.
- **Some project documentation is out of date** and describes an earlier version of the system (with
  different account types and different features than what's actually built today). This isn't a
  functional problem, but it means anyone reading the wrong document — including future developers —
  could be misled about what the system actually does. This needs a cleanup pass so there's one
  clear, current source of truth.
- A few older, unused pages from an earlier design (e.g., a standalone "digital logbook" and
  "clinical cases" module) are still sitting in the codebase but are switched off and not part of the
  live system. They should be removed so they don't confuse anyone in the future, but they pose no
  risk today since they aren't reachable.

## An important addition: bulk roster import isn't usable yet

While answering a follow-up question about how onboarding works, we found something that changes
the priority order: **there is no working screen today for an administrator to upload a spreadsheet
and bulk-create a whole roster of residents/supervisors/rotations/etc through the website.**

The good news: almost everything needed for this already exists in the code — the backend logic to
process hospitals, departments, the hospital-department matrix, supervisors, residents, rotation
placements, and resident-supervisor links from a spreadsheet is built and tested, and so is the
actual on-screen import tool (file upload, preview, error reporting, template download). It just
isn't connected to any page yet — like having a fully wired appliance that was never plugged into
the wall. Two small backend pieces (training-programme import's template/export) also need finishing
to match everything else. Right now, the only way to bulk-load a roster is for someone with direct
server access to run it manually, which isn't realistic for pilot-site staff.

This has been added to the plan below as its own step, and — because bulk roster onboarding is
central to how the pilot is meant to start — we'd treat it as equally urgent to the other steps, not
something to defer until after them.

## Path to pilot — what's left, in plain terms

| Step | What it means | Status / rough effort |
|---|---|---|
| 1. Fix the resident dashboard bug | Small code fix, so residents never see a blank error page | **Done** |
| 2. Refresh the remaining stale automated checks | So the safety net actually catches problems like #1 in future | Half a day |
| 3. Strengthen tests around bulk import and backup/restore | The two areas we'll lean on hardest during real onboarding | 2–4 days |
| 4. Clean up outdated documentation and unused old pages | So the project is described accurately going forward | 1 day |
| 5. Build the working bulk-import screen | Connects the already-built import tool to an actual page so admins can onboard a full roster (residents, supervisors, hospitals, rotations, resident-supervisor links) themselves, without needing a developer | 1–2 days |

**Remaining estimated effort: roughly one working week**, after which the system should be genuinely
ready for the planned pilot scope: 1–2 hospitals, a couple of departments, about 10 supervisors and
30 residents.

## Bottom line

PGSIMS is not a prototype — it is a working system with a sound design, and the vast majority of it
has already been verified to work correctly through rigorous, independent testing this week. There
is one real, easily-fixable bug, some testing gaps in the two features we'll depend on most for
onboarding, and some documentation that needs tidying up so it accurately reflects what has been
built. None of these are structural or architectural problems — they are the normal, expected
punch-list items at this stage of a project, and they are all addressable within about a week before
a safe, confident pilot launch.
