# Management PowerPoint evidence pack: screenshots + AI-agent build guide

## Context

The user wants a PowerPoint that explains PGSIMS to management — medical doctors and other
non-technical stakeholders. It needs to be built by a (separate) AI agent later, so this task is
about producing the *inputs* for that: a curated set of real screenshots (Android app first, then
web app) across all 4 roles, taken against the live production system so the data shown is real
and credible, plus a self-contained written brief (features, module explanations, screenshot
index, and explicit instructions) that a downstream AI agent can use to actually build the .pptx
without needing to re-derive any of this context.

Confirmed with the user:
- Use **production**, not a local/demo stack. Single canonical backend behind three web domains
  (`pg.fmu.edu.pk`, `pgsims.alshifalab.pk`, `pgsims.pmc.edu.pk`) and API-only host
  `android.pgsims.alshifalab.pk` (what the Android release build talks to) — confirmed via
  `deploy/Caddyfile.pgsims`, `docs/_audit/20260606_PG_FMU_DOMAIN_ROUTING.md`,
  `docs/discovery/20260909_pgrsims_unified_platform_baseline/09_PRODUCTION_BASELINE.md`. All
  screenshots (web + Android) will reflect the same real institutional data.
- Login credentials to try on production: `admin`/`admin123`, `resident`/`resident123`,
  `supervisor`/`supervisor123` (already confirmed working against production per `SPRINT_STATE.md`),
  `staff`/`staff123`. Verify each with a direct API login call before trusting it in the browser/app.
- Real names/data in screenshots is explicitly OK — no blurring/anonymization needed.
- Android: emulator `pgsims` (AVD exists at `/home/munaim/.android/avd/pgsims.avd`, not currently
  booted) — must be booted fresh; app install state is unknown and must be checked, not assumed.

## Step 1 — Stand up the Android side first (per user's requested order)

1. Boot the `pgsims` AVD (`emulator -avd pgsims`), wait for `adb wait-for-device` +
   `adb shell getprop sys.boot_completed` to confirm ready.
2. Check `adb shell pm list packages | grep vexel` to see if `pk.vexel.pgrcompanion` is already
   installed, and if so what version (`adb shell dumpsys package pk.vexel.pgrcompanion`).
3. If not installed, or installed but wrong build: install the existing signed release AAB/APK
   if one is already built (`android/app-companion/build/outputs/...` per `SPRINT_STATE.md` mentions a
   built release AAB) — an AAB can't be installed directly via adb, so if only the `.aab` exists,
   build a matching release/debug **APK** via `./gradlew :app-companion:assembleRelease` (or
   `assembleDebug` pointed at prod — check `build.gradle.kts` for how `INSTITUTIONAL_API_BASE_URL`
   is set per build type; release already defaults to `https://android.pgsims.alshifalab.pk/`) and
   `adb install`. Prefer the already-built release artifact over rebuilding if it exists and matches
   current `main`.
4. Launch the app, log in as **supervisor** first (confirmed credentials), screenshot:
   - Login/sign-in screen (`SignInPane`)
   - Supervisor home/dashboard (`SupervisorHomeContent`)
   - Supervisor resident list (`SupervisorResidentsContent`)
   - Supervisor resident detail (`SupervisorResidentDetailScreen`)
   - Workflow queue screen(s) (`SupervisorWorkflowQueueScreen`) — for Logbook and at least one other
     workflow type (Leave/Rotation/Research), including the approve/reject/return dialog if it
     renders cleanly (per SPRINT_STATE this is mid-extension work — verify it looks presentable
     before including; skip a given workflow screenshot rather than showing a broken/placeholder UI)
5. Log in as **resident** (Android has no admin/support-staff screens — confirmed from code, skip
   those on Android), screenshot:
   - Resident training dashboard (`TrainingDashboard`/`CurrentTrainingCard`)
   - Logbook screen + entry dialog (`LogbookScreen`, `LogbookEntryDialog`)
   - Requirements screen (`RequirementsScreen`)
   - Rotation card/detail (`RotationCard`/`RotationDetail`)
6. Use `adb exec-out screencap -p > file.png` for each, saved directly into
   `presentation/screenshots/android/<role>_<screen-name>.png` with clear sequential naming.

## Step 2 — Web app screenshots (Playwright, since claude-in-chrome extension isn't connected)

1. `mcp__playwright__browser_navigate` to `https://pg.fmu.edu.pk`, resize viewport to 1440x900 for
   consistent, presentation-friendly framing.
2. Verify each of the 4 production logins via a plain `curl` POST to
   `https://pg.fmu.edu.pk/api/auth/login/` first (fast, avoids wasted browser navigation on a
   role whose credentials don't work) before driving the browser.
3. Per role, log in through the real `/login` UI (not by injecting tokens) and capture, using the
   route list already confirmed to exist under `frontend/app/`:

   **ADMIN**: `/dashboard/utrmc`, one institutional drill-down page (hospitals or departments),
   `/residents`, `/residents/[id]` (detail, pick one real resident), `/supervisors`,
   `/academics/review-queue`, `/admin/pending-supervisor-links`

   **SUPERVISOR**: `/dashboard/supervisor`, `/dashboard/supervisor/residents`,
   `/academics/logbook`, a logbook review/detail page mid-approval if it renders,
   `/academics/evaluations`, `/dashboard/supervisor/research-approvals`

   **RESIDENT**: `/dashboard/resident`, `/dashboard/resident/postings`,
   `/academics/logbook/new`, `/academics/my-progress`

   **SUPPORT_STAFF**: `/support-staff` list + one detail page only — do not attempt to demonstrate
   department scoping (backend doesn't enforce it); caption this honestly in the brief rather than
   silently showing it as if scoped.

4. Before shooting Logbook/Evaluations/Leave/Rotations pages, do one quick visual check that the
   page renders without errors (these were "seeded but not re-verified live" per the readiness
   report) — if broken, drop that specific shot rather than including a broken screen, and note the
   gap in the brief so the downstream agent doesn't silently paper over it in the deck.
5. Save into `presentation/screenshots/web/<role>/<sequence>_<page-name>.png`, full-page screenshots
   at 1440px width.

## Step 3 — Write the AI-agent build brief

Create `presentation/PRESENTATION_BRIEF.md` (the main guidance doc for whichever agent builds the
actual .pptx later) containing, in this order:

1. **One-paragraph plain-English pitch** of what PGSIMS is, for a doctor/administrator audience —
   no jargon, framed around problems it solves (tracking residents' training, approvals, rotations,
   audit trail) rather than technical architecture.
2. **Audience & tone guidance**: non-technical, medical-doctor management audience — avoid backend
   jargon (no "REST API", "Django", "RBAC"); talk in terms of roles (Admin/UTRMC office,
   Supervisor, Resident, Support Staff), workflows, and outcomes (accountability, faster approvals,
   single source of truth, mobile access for supervisors).
3. **Suggested slide structure** (title, problem/context, the 4 roles, module-by-module feature
   walkthrough web, then Android companion app, workflow example end-to-end e.g. logbook
   submit→approve, closing/roadmap) — a recommendation, not a rigid mandate, since the downstream
   agent should have room to adapt.
4. **Per-module feature briefs** — one short paragraph each, written for a non-technical reader, for:
   identity & roles, institutional/master data (hospitals/departments/programs), resident directory,
   supervisor-resident linkage, rotations, leave, logbook, evaluations/WBA, research/thesis tracking,
   review queue / approvals, audit trail, notifications, Android companion app. Each brief explicitly
   references which screenshot file(s) illustrate it (exact relative path).
5. **Full screenshot index** — a table: file path → role → what it shows → one-line caption suggestion.
6. **Known caveats to state honestly, not hide**: Support Staff department-scoping not yet enforced;
   any workflow screenshot that was skipped and why; "39 Supervision Warnings"-style data-quality
   numbers are real current data-breadth gaps, not defects — if such a number appears in a captured
   dashboard shot, call this out explicitly so the brief doesn't accidentally use it as a talking
   point against the product.
7. **Explicit AI-agent instructions**: build a .pptx (name/output location — ask user if unspecified,
   default to `presentation/PGSIMS_Management_Presentation.pptx`), use company-neutral professional
   styling, use the real screenshots (not recreate mockups), keep slide text minimal since screenshots
   carry the evidence, and don't invent features/data not evidenced by a screenshot or this brief.

## Files/paths involved

- New: `presentation/screenshots/android/*.png`, `presentation/screenshots/web/<role>/*.png`,
  `presentation/PRESENTATION_BRIEF.md`
- Read-only reference during the work: `deploy/Caddyfile.pgsims`, `SPRINT_STATE.md`,
  `docs/audits/FINAL_DEMONSTRATION_READINESS_REPORT.md`,
  `docs/implementation/20260910_urology_institutional_demo/DEMO_RUNBOOK.md`,
  `android/app-companion/build.gradle.kts`, `android/app-companion/src/main/java/pk/vexel/pgrcompanion/*.kt`,
  `frontend/app/**` (route confirmation only, no edits)
- No source code is modified by this task. No commits. This is a pure evidence-gathering +
  documentation task.

## Verification

- Each screenshot file opens and visually shows the intended screen with real data (spot-check a
  handful, not every file, by reading a few back as images).
- `presentation/PRESENTATION_BRIEF.md` cross-references every screenshot path that actually exists
  on disk (no dangling references).
- Report to the user: total screenshot count per platform/role, any role/workflow that had to be
  skipped and why (credential failure, broken page, unrenderable Android screen), and the final
  `presentation/` folder tree.
