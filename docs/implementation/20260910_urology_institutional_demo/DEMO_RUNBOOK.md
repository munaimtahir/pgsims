# Urology Supervisor Approval Demo Runbook

Seed with:

```bash
python manage.py seed_urology_workflow_demo --dry-run
python manage.py seed_urology_workflow_demo
```

Do not store passwords in this runbook. Use the selected supervisor account shown by the seeder
output and the normal password-management process.

## 1. Institutional context

Open the institutional/master-data screens and show Faisalabad Medical University → Allied
Hospital-I Faisalabad → Urology Department → MS Urology, then open the resident roster.

## 2. Supervisor logbook review

Log in as the selected primary demo supervisor. Open `Academics → Logbook`, filter submitted
entries, and open a pending procedure. Approve it and refresh the resident detail to show the
verified status. Procedures include urinary catheterization, diagnostic cystoscopy, ureteric
stent insertion, and suprapubic catheterization.

## 3. Revision workflow

Open the seeded TURP entry and choose `Return for revision`. Show the feedback:
“Please clarify your operative role and complete the procedure details before resubmission.”

## 4. Evaluation/WBA review

Open `Academics → Evaluations`, select a submitted periodic supervisor review, start review,
then approve it. A second seeded evaluation is returned with an action plan request.

## 5. Research review

Open the supervisor research approvals endpoint/screen if enabled for the deployment. Show the
pending endourology synopsis and the returned methodology example. The workflow uses the
resident’s assigned canonical supervisor.

## 6. Administration approvals

As an administrator, open leave/rotation approval screens to show the marked submitted,
approved, and rejected examples. Document review is not demonstrated unless active document
requirements exist, because the target database currently has none.

## Selected records

The seeder output identifies residents by stable username and reports created counts. The marker
`[DEMO-UROLOGY-20260910]` identifies seeded records for cleanup:

```bash
python manage.py seed_urology_workflow_demo --cleanup
```
