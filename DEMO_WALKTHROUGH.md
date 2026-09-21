# Three-account demonstration — web and Android

Populated and API-verified on the VPS on **2026-09-21**.

Dataset: `DEMO-THREE-ACCOUNTS-V1`. Use only the existing `admin`, `supervisor`,
and `resident` logins and their assigned profiles. Credentials are unchanged and
are not recorded here. The resident remains assigned to the same supervisor.

## Preparation and repeatability

Run in the backend environment:

```bash
python manage.py seed_three_account_demo --dry-run
python manage.py seed_three_account_demo --apply
python manage.py seed_three_account_demo --verify
```

Preview and verification do not write records. Apply adds missing marked examples
inside one database transaction. It does not reset existing examples, profiles,
passwords, declarations, training records, or assignments. It suppresses outbound
email/push in the command process; existing supported in-app events remain enabled.
Files created by a failed transaction are removed. There is no reset/cleanup mode.

Do not use the older cohort-wide demo seed or its cleanup command for this dataset.
The same records appear in web and Android: an action in either client consumes
that pending example in both. Use example 1 in web and example 2 in Android when
demonstrating the same review operation twice.

## Record inventory

Each record carries a stable marker ending in `:<feature>:<number>`. The `--verify`
output reports its actual ID and current state. Initial states are:

| Feature | Example 1 | Example 2 | Example 3 | Example 4 |
|---|---|---|---|---|
| Logbook | **34** — Submitted | **35** — Submitted | **36** — Returned for revision | **37** — Verified |
| Evaluation | **22** — Submitted | **23** — Submitted | **24** — Returned for revision | **25** — Approved |
| Leave | **22** — Submitted | **23** — Submitted | **24** — Draft | **25** — Approved |
| Rotation | **7** — Submitted | **8** — Submitted | **9** — Approved, ready to activate | **10** — Active, ready to complete |
| Document | **5** — Pending review | **6** — Pending review | **7** — Reupload required | **8** — Verified |

Numbers above are database IDs within each feature, not user/profile IDs.
The existing resident profile is **36**, supervisor profile **3**, training record
**11**, and primary assignment **4**. None was replaced or duplicated.
Other existing records are retained; distinguish these examples using the dataset
marker and the IDs, rather than assuming that every pending row belongs to this demo.

Rotation dates: #7 September 23–29; #8 September 30–October 6; #9 October 12–18;
#10 June 23–29, 2026 (a past active placement intentionally ready to complete).
Leave dates: #22 October 7–8; #23 October 19–20; #24 October 21–22;
#25 October 23–24, 2026. These avoid existing leave and each other.

## Presentation sequence

1. **Resident:** open the dashboard and show the existing profile, training and
   supervisor. Open the marked leave draft (example 3), then submit it.
2. **Supervisor, web:** open submitted logbook example 1 and verify it. Open
   submitted leave example 1 and approve it. Show the changed status as resident.
3. **Supervisor, Android:** use example 2 for the corresponding logbook/leave
   review. Return the logbook with a learning-point request; reject the leave with
   a clear demonstration reason.
4. **Resident, Android:** edit returned logbook example 3, add the requested
   reflection, and resubmit. Show feedback and pending status in web. Android also
   has a returned-evaluation editor; the web detail page exposes resubmission but
   does not provide an equivalent response editor.
5. **Supervisor:** review evaluation example 1 in web, enter score `4` out of `5`
   and feedback, then approve. Reserve example 2 for Android review.
6. **Admin:** activate rotation example 3 and complete example 4. Submitted
   rotation examples 1 and 2 remain available for supervisor approval/return/reject.
7. **Resident:** replace document example 3 with a clearly synthetic image. Show
   its pending-review status and compare with verified document example 4.
8. **Admin/supervisor/resident:** open role-appropriate reports and compare status
   counts. Demonstrate available CSV exports. Counts include pre-existing records.
9. **Admin:** demonstrate academic-session import validation using the files below.
   Preview first; apply the valid sample only as a deliberate presentation action.

## Screens and available actions

| Login | Web route | Android surface | Actions |
|---|---|---|---|
| resident | `/dashboard/resident` | Home / Training | Existing affiliation, supervisor, summary |
| resident | `/academics/logbook` | Logbook | View, submit; edit returned entries in Android |
| supervisor | `/academics/logbook/<id>/review` | Logbook review queue | Verify, return, reject |
| resident | `/academics/evaluations/<id>` | Evaluations | View, submit; edit returned responses in Android |
| supervisor | `/academics/evaluations/<id>/review` | Evaluation review queue | Start review, score, approve, return, reject |
| resident | `/academics/leave-requests/<id>` | Leave requests | Submit draft, view decision |
| supervisor / admin | `/academics/leave-requests/<id>` | Leave review queue | Approve or reject submitted requests |
| supervisor / admin | `/academics/rotation-assignments/<id>` | Rotation review | Review submitted placements |
| admin | `/academics/rotation-assignments/<id>` | Use web for lifecycle steps not exposed by the installed Android build | Activate / complete |
| resident | `/dashboard/resident/documents` | Documents | Upload/replace, view feedback |
| admin | `/supervision/assignments` | Supervision workspace | Show existing assignment; do not end it during this demo |
| admin | `/masters` | Standard import workspace | Academic-session CSV validation/import |
| all three | Role-appropriate `/academics/reports/*` | Available reports/progress screens | Inspect/export supported data |

Opening the **web evaluation review page starts review automatically**. Do not open
it during read-only pre-presentation checks if you want to preserve `SUBMITTED`.

The installed Android version may lag current source. Screen mappings describe
current source; a physical-device UI rehearsal is separate from backend verification.

## Import samples

- [Four valid academic sessions](demo_data/three_account_demo/academic_sessions_valid.csv)
- [Two deliberately invalid rows](demo_data/three_account_demo/academic_sessions_invalid.csv)

Choose **Academic sessions**, not users or training records. Valid sample codes
are `DEMO3-S1` through `DEMO3-S4`; they do not change the resident's session or
institutional affiliation. Invalid rows omit the required code or name. The samples
have been tested through the actual academic-session import service. These CSVs
are not automatically imported by the seeder.

## Explicit limitations

- Exactly one existing resident/supervisor pair is retained. There are no fake
  pending assignments and no additional users or duplicate training records.
- Document review is an existing admin-only API action, but no usable web/Android
  review control was found. Show the seeded feedback and resident upload workflow;
  do not promise a document-review screen.
- Optional synthetic attachments do not create global requirements or change
  onboarding completeness. Existing onboarding requirements still apply.
- Web notification inbox, FCM push, deferred research/thesis/workshop workflows,
  staff actions, and live backup/restore are not part of this dataset.
- Dataset presence does not certify all web/Android UI paths. Isolated handler tests
  and deployed read checks are reported separately from UI acceptance.

## Verification and deployment

- Seeder source commit: `822fab8`; fetched into the VPS checkout via Git.
- Installed only the new command module in the running backend container. No
  application restart, migrations, settings changes, or unrelated service changes.
  Future image builds include the command from the committed source.
- First apply: **20 created, 0 missing**. Second apply: **0 created, 20 retained**.
- **15 isolated tests passed**, including real approval/revision handlers, unchanged
  identities, repeatability, failed-transaction file cleanup, and import previews.
- **120/120 authenticated HTTPS record reads passed**: 20 records × 3 roles ×
  web (`pg.fmu.edu.pk`) and Android (`android.pgsims.alshifalab.pk`) API hosts.
- Actual Android resident list feeds contain all four rotations, leaves, and
  documents. Supervisor feeds contain both pending leaves, rotations, logbooks,
  and evaluations. All seeded workflow states remained unchanged by verification.
- User count remains **70**. All three demonstration accounts have complete
  registry profiles and no forced password change. The supervisor's academic
  pending queue now totals **9**, including **4 newly seeded** academic reviews.
- Django system check and migration-drift check pass; identity gate passes;
  production HTTPS health reports database OK.
- No fresh browser click-through or installed-device rehearsal was performed.
  API verification used short-lived in-memory access tokens without changing
  passwords; it does not certify credential entry or the installed Android version.

Detailed evidence: [implementation audit](docs/_audit/20260921_THREE_ACCOUNT_DEMO.md).
