# PGSIMS — Plain-Language Status Report

**For**: Non-technical stakeholders (programme leadership, hospital administration)
**Date**: 2 August 2026 (originally issued 23 July 2026; updated below to reflect two weeks of
follow-up work)
**Purpose**: Explain, in plain language, what this application is, what it currently does, what
doesn't work yet, and what's left before we can safely pilot it with real residents and supervisors.

**Headline since the last update: every step on the original punch list is done.** The team has
since built two more missing screens (rotation assignments, leave requests), found and fixed four
more real bugs through live testing, resolved three open data-design questions, and closed a real
security gap in how bulk-imported accounts get their first password. The one thing still ahead of
us is loading the real pilot roster and going live — see "Path to pilot" below.

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

**Yes, and more solidly than when we last reported.** Beyond the original independent test pass, the
team has since logged in with real admin/resident/supervisor accounts and clicked through every
major workflow end to end on the live pilot server, which surfaces bugs that automated checks alone
can miss. Here's what that showed:

- The core workflows work: creating accounts, assigning residents to supervisors, placing residents
  into hospital rotations, requesting and approving leave, logging and reviewing clinical procedures,
  and generating progress reports — all of this now runs correctly today, end to end, on the live
  server.
- The automated backend test suite has grown substantially (from 406 checks to over 800) and all of
  them pass. Every consistency rule the team has defined for the system (correct roles, no duplicate
  data, correct permissions) passed.
- The website itself builds and loads correctly across all pages we checked, and the frontend's own
  automated test suite — previously five tests behind on stale checks — is now fully clean.

**Five real problems found since 23 July — all fixed and re-verified live:**

1. The resident dashboard could show a blank error screen for residents with incomplete training
   records (reported previously; fixed).
2. Logging in for the first time could let a user skip a required setup step it was supposed to
   enforce — fixed, and re-tested until it genuinely couldn't be bypassed.
3. The "change your password" screen didn't always register that the password had actually been
   changed, which could trap a user in a loop — fixed.
4. A bulk supervisor-review action for logbook entries was completely broken (it referenced a field
   that no longer existed) — fixed.
5. Editing a training record crashed if the record had certain dates filled in — which, in practice,
   is almost always — fixed.

We also found that a handful of the automated checks meant to catch problems like these had gone
stale — checking for old page text that had since changed, so they weren't actually protecting
anything anymore. Those have all been refreshed and are back to catching real regressions.

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
- **Bulk import now has a real, working screen.** An administrator can upload a spreadsheet through
  the website itself (under "Masters") and bulk-create hospitals, departments, supervisors,
  residents, rotation placements, and resident-supervisor links — no developer or server access
  needed. This closes the gap flagged in our last update, where the tool existed in the code but
  wasn't reachable from any page.
- **A systematic, independent check confirmed every page and button leads somewhere real,** and
  nothing important was built behind the scenes with no way to reach it — the same kind of check that
  originally caught the bulk-import gap above, now done comprehensively rather than one-off.
- **Three data-design inconsistencies flagged in our last update have all been resolved.** Previously,
  a resident's specialty, their hospital/department affiliation, and their training record existed in
  more than one place in the system that could drift out of sync with each other. Each of these has
  now been unified onto a single, authoritative source, removing a class of bug before it could ever
  surface in real pilot data.
- **A real security gap was found and closed:** bulk-imported accounts with a system-generated
  temporary password were not being forced to change it on first login, unlike accounts created one
  at a time. Found and fixed while rehearsing the real pilot roster load — before any real credentials
  were handed out.

## What's not solid yet

- **Overall automated test coverage is 72%, short of the project's own 80-90% target.** The two
  highest-stakes areas (bulk import and backup/restore) specifically now have solid coverage and two
  real bugs were caught and fixed by the new tests. What's left uncovered is lower-risk: some
  one-off admin command-line tools, cloud backup providers not enabled in this deployment, and one
  remaining file in the user-management code. This is a judgment call on whether to invest further
  before pilot or accept it as-is (see "Path to pilot" below).
- A duplicate, unused second implementation of the logbook and admin dashboards (living alongside
  the real one the app actually uses) has been removed, reducing confusion for future developers.
  A separate, much older set of unused pages (a standalone "digital logbook" and "clinical cases"
  module from an earlier design) is still sitting in the codebase, switched off — it poses no risk
  since it isn't reachable, but removing it remains on the cleanup list.

## Path to pilot — what's left, in plain terms

| Step | What it means | Status / rough effort |
|---|---|---|
| 0. Verify every page and button against the real backend, both directions | Systematic check that nothing in the app is a dead end, and nothing built behind the scenes is unreachable | **Done** |
| 1. Fix the resident dashboard bug | Small code fix, so residents never see a blank error page | **Done** |
| 2. Refresh the remaining stale automated checks | So the safety net actually catches problems like #1 in future | **Done** |
| 3. Strengthen tests around bulk import and backup/restore | The two areas we lean on hardest during real onboarding | **Done** (coverage nearly doubled; two real bugs caught and fixed in the process) |
| 4. Clean up outdated documentation and unused old pages | So the project is described accurately going forward | **Done** (one older unused module still pending removal, no risk) |
| 5. Build the working bulk-import screen | Connects the already-built import tool to an actual page so admins can onboard a full roster (residents, supervisors, hospitals, rotations, resident-supervisor links) themselves, without needing a developer | **Done** |
| 6. Load the real pilot roster | Use the finished bulk-import screen to bring in the actual hospitals, departments, supervisors, and residents for the pilot | **In progress** — being rehearsed now; already caught and fixed the password-reset gap above |
| 7. Distribute real credentials and go live | Hand out logins to real supervisors/residents and start the pilot | **Not started** — deliberately held until step 6 is complete and signed off |

**What's left is no longer a code punch-list — it's an operational one:** finish loading and
verifying the real roster (step 6), then get the go-ahead to distribute credentials and start the
pilot (step 7). The one open judgment call is whether 72% automated test coverage (up from 62%,
against an 80-90% internal target) is acceptable to launch with, given that the remaining gap is
concentrated in low-risk, one-off admin tooling rather than resident/supervisor-facing features.

## Bottom line

PGSIMS is not a prototype — it is a working system with a sound design, and the entire original
punch-list from our 23 July review is now done: the missing bulk-import screen is built and live,
two more missing screens (rotation assignments and leave requests) have been built and
live-verified, five real bugs found through testing have been fixed, three data-design
inconsistencies have been resolved, and a real security gap in bulk-account password handling has
been closed — all before any real credentials were issued. What remains is not fixing the system; it
is the operational work of loading the real pilot roster and formally going live, plus one judgment
call on test-coverage depth. None of this is a structural or architectural problem — the system is
ready for a safe, confident pilot launch as soon as the roster load is complete and leadership signs
off on go-live.
