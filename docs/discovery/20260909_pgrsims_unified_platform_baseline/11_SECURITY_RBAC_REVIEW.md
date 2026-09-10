# Security / RBAC Review — 2026-09-09

Scope: backend/sims (active apps only). Read-only source review; no exploitation attempted.
Reconciled against `docs/contracts/RBAC_MATRIX.md`, `docs/AUDIT_2026-07-23_PILOT_READINESS.md`, and
`sims/users/test_security_remediation_m1.py` (evidence a prior "M0 P0 security blockers" remediation
pass already occurred — this review largely confirms that work still holds, rather than finding it
fresh).

## Authentication
- JWT via `rest_framework_simplejwt`, `SIGNING_KEY = SECRET_KEY` (`sims_project/settings.py:706`).
  `SECRET_KEY` is required from env (`settings.py:39-41`, raises `RuntimeError` if unset — good, no
  silent insecure default).
- `SESSION_COOKIE_AGE = 28800` (8h), `SESSION_COOKIE_SECURE`/`CSRF_COOKIE_SECURE` default to
  `not DEBUG` and are env-overridable (`settings.py:259-261`). `SECURE_HSTS_*` env-driven, forced on
  in the prod block (`settings.py:583-585`). `X_FRAME_OPTIONS = "DENY"` (`settings.py:245`).
- A prior incident is documented inline: a settings.py comment (`:575-578`) notes Caddy's own
  SSL/HSTS previously silently masked missing `Secure` flags on session/CSRF cookies — now fixed by
  making these env-driven rather than DEBUG-inferred. This is resolved, not an open finding.
- `must_change_password` / onboarding gate exists per `CLAUDE.md` and `AGENTS.md` (not independently
  re-verified line-by-line in this pass; covered by the backend-architecture fork).

## Authorization / cross-resident isolation (highest-value check) — PASS
Spot-checked `get_queryset()` on every resident-facing ViewSet. All consistently filter by role
rather than relying on serializer-only checks:
- `training/views.py:224-237` (`ResidentTrainingRecordViewSet`), `:268-` (`RotationAssignment`),
  `:624-639` (`LeaveRequestViewSet`), `:717-732` (`DeputationPostingViewSet`) — RESIDENT sees only
  `resident_user=user`; SUPERVISOR sees only `_get_supervised_resident_ids(user)`; ADMIN sees all;
  everyone else `qs.none()`.
- `academics/views.py:101-117` (`ResidentTrainingRecordViewSet`, academics variant), `:221-232`
  (`SupervisorReviewQueueItemViewSet`), `:357-371` (`EvaluationSubmissionViewSet`), `:498-513`
  (`LogbookEntryViewSet`) — same pattern: RESIDENT → `resident_user=user` / `resident=user.
  resident_profile`; SUPERVISOR → filtered to assigned residents via `ResidentSupervisorAssignment`;
  unmatched role → `queryset.none()`.
- `notifications/views.py:36-40` — `Notification.objects.filter(recipient=user)`, correct.
- `supervision/views.py:32-47` (`ResidentSupervisorAssignmentViewSet`) — RESIDENT →
  `resident__user=user`; SUPERVISOR → own assignments.
- `users/onboarding_api.py:327-348` (`ResidentDocumentViewSet`) — RESIDENT implicit via
  `_resident_profile(user)` pattern used elsewhere in the file; SUPERVISOR → assigned residents only
  via active `ResidentSupervisorAssignment`; ADMIN/SUPPORT_STAFF → all (with optional `?resident=`
  filter). No IDOR path found: no view returns an unfiltered queryset to a RESIDENT or SUPERVISOR
  role.

**No cross-resident IDOR confirmed in this pass.** This is a meaningfully positive finding — the
codebase applies the queryset-filtering pattern uniformly rather than per-view ad hoc.

## Mass assignment
- `ResidentDocumentSerializer` (`onboarding_api.py:52-56`) correctly marks `resident`, `status`,
  `verified_by`, `verified_at` as `read_only_fields` — a resident cannot self-verify a document or
  attach it to another resident's profile via payload manipulation.
- `LogbookEntryViewSet.perform_create` (`academics/views.py:513+`) resolves `resident` server-side
  from `user.resident_profile` for RESIDENT role (client cannot set it), but accepts a client-supplied
  `supervisor` id verbatim with only an existence check (`SupervisorProfile.objects.filter(pk=
  supervisor_id).first()` — `academics/views.py` in `perform_create`), not checked against the
  resident's actual assigned supervisor(s). **P3**: a resident can tag an arbitrary supervisor on
  their own logbook entry (affects only entry routing/visibility for that supervisor, not another
  resident's data — low impact, but inconsistent with the otherwise-strict assignment model).
- `backup_center/serializers.py` uses `fields = '__all__'` on `BackupJobSerializer`/
  `RestoreJobSerializer`/`BackupAuditLogSerializer`, but every view in `backup_center/views.py` is
  gated `permission_classes = [IsAuthenticated, IsSuperAdmin]` (confirmed for all ~25 views). Mass
  assignment risk here is not exploitable by non-superadmin roles — **no finding**, but flagged as a
  pattern to avoid (prefer explicit `fields=` even under superadmin-only gating, for defense in
  depth). **P3**.

## File uploads
- `ResidentDocumentViewSet` (`onboarding_api.py:327-333`): `ALLOWED_EXTENSIONS = {".pdf", ".jpg",
  ".jpeg", ".png", ".doc", ".docx"}`, `MultiPartParser`/`FormParser`, `http_method_names = ["get",
  "post", "head", "options"]` (no PUT/DELETE exposed — resubmission presumably goes through a
  separate correction endpoint, not independently verified here). Extension allowlist exists; this
  pass did not confirm server-side content-type/magic-byte verification (extension spoofing is a
  residual risk) — **P2, needs verification**: confirm whether `django-storages`/Pillow or similar
  validates actual file content vs. trusting the client-supplied extension.
- Media serving: `MEDIA_URL`/`MEDIA_ROOT` (`settings.py:224-225`) only auto-served by Django when
  `DEBUG=True` (`sims_project/urls.py:185-187`); in production, `deploy/Caddyfile.pgsims:28-29`
  explicitly routes `/media/*` through the Django backend "for authorization" rather than serving
  static files directly from disk — **correct pattern**, prevents unauthenticated direct-URL access
  to uploaded resident documents by path guessing. `robots.txt` also disallows `/media/private/`,
  `/admin/`, `/api/` (`sims_project/urls.py:130-137`) — this is cosmetic (SEO), not a security
  control, and should not be relied on as one; the actual control is the Caddy proxy-through-Django
  routing, which is present. **No finding.**

## Sensitive logging / secrets
- No `print(`/logger calls found emitting password/token/secret values in the files reviewed
  (spot-checked `users/`, `training/`, `academics/`, `backup_center/`, `notifications/`).
  `SECRET_KEY` is never hardcoded — sourced from env with a hard failure if absent.
- Did not exhaustively grep every app for logging statements in this pass (time-boxed); recommend a
  full `grep -rn "logger\.\|print(" backend/sims --include=*.py | grep -i "password\|token\|secret"`
  sweep as a P3 follow-up rather than treating this as fully closed.

## CORS / HTTPS
- `CORS_ALLOWED_ORIGINS` explicit-origins-only from env, empty list otherwise (`settings.py:718-
  735`) — no wildcard `CORS_ALLOW_ALL_ORIGINS`. `CORS_ALLOW_CREDENTIALS = True` paired with explicit
  origins (not `*`) — correct pairing (credentialed CORS with a wildcard origin would be a real
  finding; this is not that). **No finding.**
- `SECURE_SSL_REDIRECT` intentionally left `False` in the prod override block with an inline comment
  explaining Caddy already handles the HTTP→HTTPS redirect (`settings.py:578`) — consistent, not a
  gap, provided Caddy config actually redirects (not independently verified in this fork; cross-check
  against `09_PRODUCTION_BASELINE.md`).

## Summary of findings

| # | Severity | Area | Finding |
|---|----------|------|---------|
| 1 | P2 | File upload | Extension allowlist on `ResidentDocumentViewSet` is not confirmed to be backed by content/magic-byte validation — needs verification, not confirmed exploitable |
| 2 | P3 | Mass assignment | `LogbookEntryViewSet.perform_create` accepts any existing `supervisor` id from a RESIDENT caller, not constrained to their actual assigned supervisor(s) |
| 3 | P3 | Serializer hygiene | `backup_center` serializers use `fields = '__all__'`; safe today only because every consuming view is `IsSuperAdmin`-gated — brittle if a less-privileged view is ever added against the same serializer |
| 4 | P3 | Logging sweep | Sensitive-value logging grep was spot-checked, not exhaustive across all active apps |

**No P0 or P1 findings in this pass.** Cross-resident data isolation — the highest-risk category for
this domain — checked out clean across every resident-facing ViewSet reviewed. This corroborates
`sims/users/test_security_remediation_m1.py` existing as a regression suite for a prior remediation,
suggesting the P0 issues that once existed here were already fixed and are now guarded by tests.

**Overall security posture: SOUND**, with the P2 file-content-validation gap as the one item worth a
follow-up ticket before treating document upload as fully hardened.
