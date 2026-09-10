# AUDIT LOGGING REVIEW

## `django-simple-history`
The application systematically utilizes `django-simple-history` to create historical records of every major model in the application.

This includes:
* `ResidentSupervisorAssignment`
* `ResidentTrainingRecord`
* `ResidentSubmission`
* `LogbookEntry`
* `User` (and associated profile records)

## Functional Trails
Beyond the raw DB change capture provided by `simple-history`, functional audit actions such as `SubmissionReview` explicitly track state transitions, reviewer comments, actions (`start-review`, `return`, `verify`), and timestamps.
