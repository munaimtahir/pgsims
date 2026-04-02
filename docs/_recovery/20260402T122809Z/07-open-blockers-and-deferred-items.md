# Open Blockers and Deferred Items

## Items still not safe to build on

### 1) Logbook workflow
- Status:
  Deferred
- Why:
  Historical claims remain, but it is not part of the active frontend route tree or active backend include set.
- Why not included now:
  Reactivating it would be feature expansion and boundary reopening, not stabilization.

### 2) Cases workflow
- Status:
  Deferred
- Why:
  Same active-surface absence as logbook.
- Why not included now:
  Requires explicit scope recovery rather than a small wiring fix.

### 3) Legacy analytics surface
- Status:
  Legacy
- Why:
  Historical docs and endpoint inventories overstate runtime truth.
- Why not included now:
  The active mission was truth alignment, not analytics redesign.

### 4) Rotation lifecycle closure
- Status:
  Partial
- Why:
  Backend support is strong, but the end-to-end user-facing lifecycle is not as fully closed or verified as research and leave.
- Why not included now:
  There was enough scope pressure already in truth alignment, frontend baseline recovery, and leave closure.

### 5) Docker runtime drift
- Status:
  Blocked
- Why:
  Long-running containers can be healthy while still serving stale application code relative to the checked-out tree.
- Why not included now:
  This requires a separate reproducibility hardening pass around rebuild discipline and deployment verification.

### 6) Build truth weakness in Next.js config
- Status:
  Partial
- Why:
  Build passes even if lint/type would fail unless explicit commands are also run.
- Why not included now:
  The immediate baseline was restored by explicit gates, but CI/build policy hardening is still separate work.
