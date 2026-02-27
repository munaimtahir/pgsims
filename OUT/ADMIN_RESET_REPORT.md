# ADMIN RESET REPORT

## Baseline Safety Snapshot (main branch)
- Repository: `/home/munaim/srv/apps/pgsims` (user target `/srv/apps/pgsims`)
- Branch at start: `main`
- Baseline HEAD: `05e67ec290df24234f04d36aa47c3013376f3314`
- Safety tag created: `before-admin-reset-20260228-0137`
- `OUT/` ensured: yes
- Note: worktree already had many unrelated pre-existing modifications before this task.

## Phase 1 Findings (What was overriding Django admin)
### Theme package/config scan
- Searched requirements/lock/config files for `jazzmin|grappelli|admin_interface|unfold|suit|material|adminlte`.
- Result: **no admin theme packages detected** in project dependency/config files.
- Searched settings for `JAZZMIN|GRAPPELLI|ADMIN_INTERFACE|UNFOLD|SUIT|ADMINLTE`.
- Result: **no theme settings blocks found**.

### Admin override sources found
- Template overrides found at: `backend/templates/admin/*` (multiple stock admin templates overridden, including `base_site.html`, `index.html`, `change_list.html`, login variants).
- URL override found in `backend/sims_project/urls.py`:
  - `path("admin/logout/", admin_logout_view, name="admin_logout")`
- Branding overrides found:
  - `backend/sims_project/urls.py` (`admin.site.site_header/site_title/index_title/site_url`)
  - `backend/sims/users/admin.py` (`admin.site.site_header/site_title/index_title`)
- Custom admin site class exists in `backend/sims/admin.py` (`SIMSAdminSite`) but is not wired to URLConf.

## Phase 2 Changes Applied (Reversible, no deletions)
### 1) URL reset to stock admin route behavior
- **File:** `backend/sims_project/urls.py`
  - Removed custom logout URL mapping from `urlpatterns` so `/admin/` is served by canonical Django admin URL set only.
  - Disabled admin branding override assignments at file end (left reversible comment marker).
  - Canonical route remains:
    - `path("admin/", admin.site.urls)`

### 2) Disabled admin branding override in users admin module
- **File:** `backend/sims/users/admin.py`
  - Disabled `admin.site.site_header/site_title/index_title` assignments (replaced with reversible marker comment).

### 3) Disabled admin template overrides by renaming (not deleting)
- Created: `_DISABLED/`
- Renamed:
  - `backend/templates/admin` -> `_DISABLED/admin_templates_disabled_20260228-013827`
- No `backend/static/admin` directory existed to move.

## Phase 3 Verification Commands + Evidence
All commands run from `backend/` using project venv python: `.venv/bin/python`.

1. `manage.py check`
   - Output: `System check identified no issues (0 silenced).`

2. `manage.py migrate --noinput`
   - Output included successful migration application:
     - `analytics.0001_initial ... OK`
     - `analytics.0002_analytics_hardening ... OK`

3. `manage.py test --failfast`
   - Output:
     - `Found 286 test(s).`
     - `Ran 286 tests in 14.323s`
     - `OK`

4. Runtime admin endpoint verification
   - Started server: `.venv/bin/python manage.py runserver 0.0.0.0:8000`
   - Probe: `curl -I http://127.0.0.1:8000/admin/`
   - Result:
     - `HTTP/1.1 302 Found`
     - `Location: /admin/login/?next=/admin/` ✅ expected stock admin auth redirect

5. Classic UI verification (non-themed)
   - Probe: `curl -s http://127.0.0.1:8000/admin/login/?next=/admin/ | head -n 25`
   - Evidence:
     - `<title>Log in | Django site admin</title>`
     - `href="/static/admin/css/base..."`
   - Confirms vanilla Django admin template/assets are active.

6. Admin registry evidence
   - Command:
     - `manage.py shell -c "from django.contrib.admin.sites import site; ..."`
   - Output:
     - `ADMIN_REGISTRY_COUNT= 36`
     - sample includes:
       - `academics.Department`
       - `rotations.Hospital`
       - `rotations.HospitalDepartment`
       - `rotations.Rotation`
       - `users.User`
       - `logbook.LogbookEntry`
       - `cases.ClinicalCase`
       - `certificates.Certificate`

7. Installed apps evidence
   - Core admin apps present:
     - `django.contrib.admin`
     - `django.contrib.auth`
     - `django.contrib.contenttypes`
     - `django.contrib.sessions`
     - `django.contrib.messages`
     - `django.contrib.staticfiles`
   - No admin theme apps present.

## Phase 4 Missing Models Diagnosis
Stock Django admin app-list behavior is restored.  
Any still-missing models are due to registration choices, not theming.

### Unregistered SIMS models (current state)
- `audit.ActivityLog`
- `audit.AuditReport`
- `audit.HistoricalAuditReport`
- `bulk.BulkOperation`
- `cases.HistoricalCaseCategory`
- `cases.HistoricalClinicalCase`
- `certificates.CertificateStatistics`
- `certificates.HistoricalCertificate`
- `certificates.HistoricalCertificateType`
- `logbook.HistoricalLogbookReview`
- `logbook.HistoricalProcedure`
- `logbook.HistoricalSkill`
- `notifications.Notification`
- `notifications.NotificationPreference`
- `reports.ReportTemplate`
- `reports.ScheduledReport`
- `rotations.HistoricalHospital`
- `rotations.HistoricalRotation`
- `search.SavedSearchSuggestion`
- `search.SearchQueryLog`
- `users.HistoricalUser`

### App-level admin registration signal
- `audit`: no `admin.py`
- `search`: no `admin.py`
- `bulk/admin.py`: present but empty (no registrations)
- `notifications/admin.py`: present but no registrations
- `reports/admin.py`: present but no registrations

## PASS/FAIL
## **PASS**
- `/admin/` is reachable and returns expected redirect to stock admin login.
- Vanilla Django admin templates/assets are restored (classic UI evidence captured).
- Admin registry is populated; default app-list behavior is back.
- Overrides were disabled reversibly (renamed to `_DISABLED/`, no deletions).

## Next Steps
1. If specific models must appear in admin, add explicit `ModelAdmin` registrations in each app’s `admin.py`.
2. Keep `_DISABLED/admin_templates_disabled_20260228-013827` until frontend/admin rebuild is complete; re-enable selectively if needed.
