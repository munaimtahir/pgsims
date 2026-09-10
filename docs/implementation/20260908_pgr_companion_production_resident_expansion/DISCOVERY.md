# Discovery

Starting source: `ed1d137c76beec33ddc7cb2c6140fc01a94102de` on `main`.

`android/app-companion` is the single canonical PGR Companion application.
The production Android URL in the release BuildConfig is `https://android.pgsims.alshifalab.pk/`.

The active backend domains are `users`, `training`, `academics`, `supervision`, and `rotations`.
The production VM checkout began at `afca40153a1b4a0e0266ab2ee249b2e273e82c98`; its backend is
a Docker image (not a bind-mounted source checkout), exposed internally on port 8014 behind the
public Android host. Health was HTTP 200. The rollback path is to return the checkout to `afca401`
and rebuild/restart the backend/worker/beat compose services; no schema migration is introduced.

There are two logbook model families. The active web resident workflow is
`academics.LogbookEntry` at `/api/academics/logbook-entries/`; Android uses that contract. The
separate `training.LogbookEntry` is not substituted for it.
