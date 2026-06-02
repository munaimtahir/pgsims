# Gaps and Risks (2026-06-02 UTC)

- Automated E2E does not perform live Google OAuth (by design). Manual verification is still required for connect/upload/verify/download in a real environment.
- Backup History “Restore-ready” state does not include a `restore_job_id` in list payload; UI re-download is the supported way to prepare a restore upload.

