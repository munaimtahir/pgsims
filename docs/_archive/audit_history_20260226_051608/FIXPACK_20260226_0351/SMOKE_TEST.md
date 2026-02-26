# Smoke Test - Phase-1 Logbook Verify Flow (FIXPACK_20260226_0351)

## Goal Proven
PG submits logbook -> Supervisor returns/approves with feedback -> PG sees feedback and status -> no server crash / notification write crash.

## Environment Used
- Repo: `/home/munaim/srv/apps/pgsims`
- Backend virtualenv created locally at `backend/.venv`
- Python: `3.12.3`
- Node: `v20.20.0`
- npm: `10.8.2`

## Commands Run
### Backend setup (local verification only)
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Targeted smoke test (API end-to-end)
```bash
cd backend
source .venv/bin/activate
python manage.py test sims.logbook.test_api.PGLogbookEntryAPITests.test_submit_return_feedback_visible_and_resubmit_approve_flow -v 2
```

### Backend checks
```bash
cd backend
source .venv/bin/activate
python manage.py check
python manage.py test sims.logbook.test_api -v 1
```

### Frontend build sanity
```bash
cd frontend
npm run build
```

## Results
### 1) Targeted smoke test
PASS
- `Ran 1 test ... OK`
- Covered flow:
  - PG creates entry
  - PG submits -> pending
  - notification row created with canonical `Notification` schema + metadata
  - supervisor returns with `feedback`
  - PG list API shows `status=returned` and both `feedback` + `supervisor_feedback`
  - PG edits returned entry and resubmits
  - supervisor approves using `supervisor_feedback`
  - PG edit blocked after approval

### 2) Backend system check
PASS
- `System check identified no issues (0 silenced).`

### 3) Logbook API test module regression check
PASS
- `Ran 18 tests ... OK`

### 4) Frontend build
PASS
- `npm run build` completed successfully (`next build`).

## Notes
- `stty: 'standard input': Inappropriate ioctl for device` appeared in CLI output during non-interactive shell runs; this is environment noise and did not affect test outcomes.
- Django emitted a warning about missing `backend/staticfiles/` during tests; it did not affect the smoke test result.
