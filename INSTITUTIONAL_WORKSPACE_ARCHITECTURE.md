# Institutional workspace architecture

PGR Companion has two explicit data boundaries. The separation is the whole design, because the
generic offline product is what Google Play approved and it must keep standing on its own.

## The two workspaces

**Personal Workspace** — `LocalStore.kt`, `MainActivity.kt`. Plain `SharedPreferences` plus
app-private files. No network, no account, useful with the radio off. This is the approved
baseline and it is reachable before, during and after any institutional failure.

**Institutional Workspace** — `InstitutionalRepository.kt`, `InstitutionalScreen.kt`. Calls the
canonical PGR SIMS backend. Its state is server-derived and is never written into the personal
store; the personal store is never read from here. The reverse direction is equally closed: the
personal records are never sent to the institution.

FMU is the first institution in the UI. The repository boundary takes a base URL and a token store,
so a second institution is a construction-site change, not a rewrite — and neither app startup nor
any personal feature becomes institution-bound.

## State machine

`InstitutionalState` — `DISCONNECTED` → `SIGNING_IN` → `CONNECTED`, with `ERROR` reachable from
`CONNECTED` when a read fails. Sign-out returns to `DISCONNECTED` from anywhere.

`DISCONNECTED` renders the sign-in pane. `ERROR` renders the failure with a Retry and a Sign-out,
plus an explicit statement that the other four tabs are unaffected. A failure never escapes this
screen.

## Session handling

A JWT access/refresh pair is stored in AndroidX `EncryptedSharedPreferences`. Passwords are never
stored and never logged; there is no logging interceptor in any build type, because these request
bodies carry credentials.

- A `401` triggers exactly one refresh, then replays the original request.
- The backend rotates refresh tokens, so the rotated value is persisted; if the response omits one,
  the existing token is kept.
- A rejected refresh clears the session rather than retrying, so a revoked or spent token cannot
  produce a request loop.
- Refresh and logout use a client with no auth interceptor, so a stale bearer token cannot ride
  along on the call that is meant to replace or revoke it.
- Logout blacklists the refresh token server-side on a best-effort basis and clears local tokens
  regardless of whether that call succeeds. It touches nothing else.

If the device keystore is unusable — a real failure mode on some OEM builds and on restored backups
— token storage falls back to memory instead of throwing. Losing an institutional session is
recoverable; taking down the offline Personal Workspace with it is not. For the same reason the
repository is constructed lazily and never on the startup path.

## Reading institutional state

One `snapshot()` gathers identity, onboarding, documents, training and supervisor assignments.
Identity is required; every other section is optional.

This matters because the resident-only endpoints return `403` for `SUPERVISOR` and `ADMIN`
accounts. Treating that as a failure would blank the screen for a supervisor who signed in
correctly. Instead those sections are collected into `unavailable` and reported as
"Not available to this account", and the rest of the screen renders.

## Rendering institutional fields

The connected view renders what the backend declares rather than a hardcoded form. `sections`
arrives as `{key, title, fields[{field, label, value, required}]}` and is rendered from that,
mirroring the rule that the web client's `/complete-profile` is built from backend-declared fields.
Editing one field PATCHes that field alone and re-reads the server's state; the backend stays
authoritative for permissions, validation and review status.

Uploads are validated against the backend's own limits before the request is made (10 MB;
`pdf`/`jpg`/`jpeg`/`png`/`doc`/`docx`), so an oversized or wrong-typed file produces a legible
sentence rather than a server rejection. The picked file's real display name is resolved through
the content resolver, because the backend validates on the filename's extension; the staged copy in
the cache directory is deleted in a `finally` block whether or not the upload succeeds.
