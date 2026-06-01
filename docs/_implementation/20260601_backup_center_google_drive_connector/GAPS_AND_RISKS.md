# Gaps and Risks

- Live OAuth cannot be claimed working without real credentials and a real upload/download exercise.
- `drive.file` scope limits access to app-created files; ensure folder/files are created by the app.
- Large backups may require resumable uploads; implementation should prefer resumable for reliability.

