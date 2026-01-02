# Stage 2 Feature Readiness Review

_Date: 2025-05-31_

This review validates the "Stage-2" feature set that the README and supporting docs label as
"Production-Ready for Pilot Deployment." It compares the published claims to the code that is
actually wired into the Django project configuration.

## Summary Verdict

The repository ships mature code for authentication, the core postgraduate workflow apps, and the
audit/logging utilities, but the Stage-2 bundle is **not deployment ready** yet. Several features
that the documentation promotes as complete are unreachable because their Django apps are not
installed, key dashboards still ship with placeholder logic, and the automated test suite fails
before tests can run.

## Claim vs. Reality Snapshot

| Feature family (README claim) | Documentation promise | What the code actually enables | Status |
| --- | --- | --- | --- |
| User management & security | Role-based accounts, archived users, validators | Custom `User` model enforces role rules and profile metadata | ✅ Ready【F:sims/users/models.py†L1-L200】 |
| Dashboards & analytics | "Customized dashboards" with analytics | Dashboards render but ship with placeholder `pass` blocks for recent submissions; analytics data is stubbed | ⚠️ Needs work【F:sims/users/views.py†L85-L172】 |
| Clinical cases, logbook, certificates, rotations | Full CRUD, review flows, exports | Views implement role-aware filtering and CSV export | ✅ Ready【F:sims/cases/views.py†L18-L112】【F:sims/rotations/views.py†L27-L120】【F:sims/rotations/views.py†L667-L719】 |
| Analytics & reporting | "Comprehensive statistics and data visualization" | `sims.analytics` and `sims.reports` apps exist but are not listed in `INSTALLED_APPS`, so none of their models, URLs, or templates load | ❌ Blocked【F:README.md†L32-L80】【F:sims_project/settings.py†L41-L66】 |
| Notifications & bulk ops | Email/in-app notifications, bulk tools | `sims.notifications` and `sims.bulk` also excluded from `INSTALLED_APPS`; corresponding tables and APIs never initialize | ❌ Blocked【F:README.md†L32-L46】【F:sims_project/settings.py†L41-L66】 |
| Global search & audit trail | Cross-module search with history and audit APIs | Search service and audit models are installed and callable | ✅ Ready【F:sims/search/views.py†L16-L47】【F:sims/audit/models.py†L1-L108】 |
| Automated quality gate | CI-ready test suite | `pytest` aborts during collection with 11 errors (missing app registrations, test fixtures requiring DB marks, missing `bs4`) | ❌ Blocked【94aacf†L1-L118】 |

## Deployment Implications

* **App registration gaps.** Until `sims.analytics`, `sims.bulk`, `sims.notifications`, and
  `sims.reports` are added to `INSTALLED_APPS`, every Stage-2 promise about analytics dashboards,
  notifications, bulk review, and report builders remains dormant.【F:sims_project/settings.py†L41-L66】
* **Dashboard polish.** The supervisor and PG dashboards need their analytics loops completed; as
  written they return empty arrays, so the "role dashboards with analytics" pledge is unmet.【F:sims/users/views.py†L85-L172】
* **Testing signal.** The failing test collection is an early warning sign that the extended feature
  set has not been verified. Fixing the missing apps and test fixtures is a prerequisite for a
  serious Stage-2 rollout.【94aacf†L1-L118】
* **Operational hardening.** The project still defaults to SQLite and DEBUG mode. Production-focused
  settings (Postgres, secure cookies, host headers) remain TODO items, matching the concerns raised
  in the earlier external review.【F:sims_project/settings.py†L102-L134】

## Recommended Next Steps

1. **Register the Stage-2 apps** in `INSTALLED_APPS`, apply migrations, and wire their URLs into
   `sims_project/urls.py` so analytics, reporting, notifications, and bulk tooling can actually run.
2. **Finish the dashboard data joins** (recent submissions, top metrics) so role homepages surface the
   analytics users expect.
3. **Stabilize the test suite** by fixing database fixtures, enabling `django_db` marks where
   required, and adding any third-party dependencies (`beautifulsoup4`) referenced by tests.【94aacf†L1-L118】
4. **Introduce production settings** (environment-driven secrets, Postgres, secure cookie flags) and
   verify the deployment scripts in `deployment/` reflect the new configuration.【F:sims_project/settings.py†L102-L134】

Once those gaps close, the Stage-2 features described in the docs will align with what the codebase
actually delivers, and the project will be ready for the "deploy + harden + extend" phase.
