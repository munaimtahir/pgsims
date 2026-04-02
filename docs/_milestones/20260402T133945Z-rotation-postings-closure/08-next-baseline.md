# Next Baseline

## Stable to Assume

- Recovery truth baseline remains valid.
- Rotation workflow is now operational on the active surface.
- Postings workflow is now operational on the active surface.
- Resident schedule, supervisor dashboard, UTRMC overview, and UTRMC postings route are the canonical active surfaces for these workflows.
- Contract/runtime agreement is materially improved for rotation/postings payloads and statuses.

## Must Not Be Assumed Complete

- Deferred legacy modules are still not part of active scope.
- Broader non-happy-path operational coverage for rotation/postings is not exhaustive.
- Historical docs outside `docs/contracts/`, recovery pack, and this milestone pack are not authoritative.

## Recommended Next Milestone

Active-surface depth hardening on verified routes:

- broaden regression coverage for secondary happy paths on resident/supervisor/UTRMC surfaces
- tighten remaining contract docs where historical endpoint wording is still broader than active usage
- harden program-administration and roster-management paths without reactivating deferred legacy modules

## Do-Not-Touch Areas

- Logbook
- Cases
- Legacy analytics
- Canonical department/hospital model invariants
- Stable backend audit/history foundations unless required by a future verified workflow closure

## Verification Gates Before New Feature Work

- `docs/contracts/TRUTH_TESTS.md` must pass
- current-tree workflow gate must remain green
- any new contract change must update `docs/contracts/` in the same pass
