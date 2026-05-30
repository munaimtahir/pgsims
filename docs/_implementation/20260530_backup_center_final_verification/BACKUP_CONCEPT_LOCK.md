# BACKUP_CONCEPT_LOCK — Backup Center v1.2

Date (UTC): 2026-05-30

## Pathway 1: Routine Application Data Backup
**User label:** Regular System Backup  
**File extension:** `.pgsimsbak`  
**Goal:** One file that can restore the complete internal PGSIMS application state on a compatible PGSIMS install.

### Included
1. Full database dump (engine-aware):
   - PostgreSQL: native `pg_dump` (custom format) for `pg_restore`
   - SQLite: `dumpdata` JSON fixture
2. Full `media/` folder (uploads) when present
3. `manifest.json` (app/version/git/db/media/counts)
4. `backup_report.json` (operator-facing mirror of manifest)
5. `checksum.sha256` (component integrity checks, plus optional media tree hash)

### Explicit guarantees (by design + tests)
- Preserves primary keys and relationships via native dump/fixture restore
- Preserves Django password hashes stored in the database
- Users can log in post-restore using the same password as the backed-up system (sessions may expire)

### Excluded
- Plaintext secrets (no `.env`, tokens, DB passwords)
- Runtime cache/temp folders
- Browser sessions (acceptable limitation)

## Pathway 2: Full Disaster Recovery Backup
**User label:** Full Server Recovery Backup  
**File extension:** `.pgsimsdr`  
**Goal:** One larger file for rebuilding on a new server; includes an internal routine backup plus recovery notes.

### Included
- Internal Routine Application Data Backup (`.pgsimsbak`)
- `deployment_metadata.json`
- `env.template` (template only; no secrets)
- `restore_instructions.md`

### Secrets rule
- No unencrypted secrets are included.
- Any encrypted secrets bundle is **not implemented in this sprint** (deferred by design for safety).

