# Implementation report

`InstitutionalRepository` now reads the production resident workflow endpoints in the same
authenticated snapshot and retains the existing one-refresh-only token policy. The Material 3 UI
has five destinations: Home, Training, Logbook, Requirements, and Profile.

Training shows programme data, the backend-selected current rotation, full rotation history and
detail dialog, and supervisor assignments. Home has a concise current-training card. Logbook uses
the active academic API for list/detail, draft creation, editable draft/returned entries, and
submission. Requirements presents server-backed assessment, research, workshop and document state.
No Android-side workflow or completion rules were added.

`prepare_android_production_e2e` is a production-guarded, synthetic-only management command for
the fixed `android.demo.*` records. It needs an external environment password and creates labelled
previous/current/upcoming rotation fixtures only for the synthetic resident.
