# UI Verification (Smoke & Workflow Mapping)

## Target Assessment:
Determine if the `Next.js` interface successfully implements and encapsulates the underlying REST API models required for the Backup Center, maintaining safety and operational clarity.

### Component 1: `BackupList`
- **Visibility**: Renders seamlessly inside `/dashboard/utrmc/backup`.
- **Workflow**: Displays backup lists differentiating between `Disaster` and `Routine` bundles.
- **Action Links**: `Download` and `Delete` handlers are functional, directly communicating to API boundaries safely via active access tokens.

### Component 2: `CreateBackupModal`
- **Visibility**: Activated seamlessly using `PlusIcon`.
- **Workflow**: Implements two distinct radio options restricting payloads: 
  - *Routine Data*: Best for operations
  - *Disaster Recovery*: Hard infrastructure recovery
- **Action Links**: Form successfully executes asynchronous `POST` via authenticated user payload.

### Component 3: `RestoreModal` (The 4-Step State Machine)
- **Step 1: Upload**: File dropzone successfully identifies and validates `.zip` extension constraints locally before emitting to REST.
- **Step 2: Verification**: Parses manifest data received from `/api/validate` effectively preventing corrupted data flows. 
- **Step 3: Dry-Run**: Simulated integration confirms environment integrity.
- **Step 4: Hard Confirmation**: Forces the user to supply:
   - Account Authentication Password
   - String match `"RESTORE"`
   - Final Checkbox 
- **Action Links**: Destructive request binds flawlessly into safety locks preventing any accidental overwrites. 

### Conclusion:
Manual UI review coupled with React state behavior analysis confirms the application operates exactly as defined in the `BACKUP_CONCEPT_LOCK.md` document, adhering strictly to the User Safety Guardrails.
