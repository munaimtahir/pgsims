# Logbook domain audit

The active resident logbook is `academics.LogbookEntry`, not a parallel Android model. Existing
resident-scoped routes provide list, categories, create, patch and submit actions. The server sets
resident/training ownership and enforces the active-primary-supervisor requirement, editable states
and submission transition. Android sends only category, date, title and optional non-identifying
reflection fields, shows backend status/feedback and refreshes server state after a mutation.

Production verification used a synthetic resident only. A synthetic entry was created, edited and
submitted through the API; a separate synthetic draft was created through the API-36 Android UI.
No patient-identifying data was used.
