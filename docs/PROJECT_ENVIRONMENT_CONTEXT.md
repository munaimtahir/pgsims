# PGSIMS Project Environment Context

This document is the canonical infrastructure and environment context for PGSIMS. Future AI-agent
and developer sessions must read it before Android, backend, deployment, VPS, networking, or Caddy
work.

## Canonical terminology

### Laptop

“Laptop” means the current local development machine.

Local repository:

```text
/home/munaim/Documents/github/pgsims
```

The laptop is used primarily for Android development and associated local development tasks.

Dedicated Android emulator:

```text
pgsims
```

### VPS

“VPS” means the Google Cloud VM hosting the deployed PGSIMS backend.

VPS repository:

```text
/home/munaim/srv/apps/pgsims
```

The laptop can access the VPS through the configured SSH alias:

```bash
ssh test
```

The connection is already configured and supports the administrative access required for normal
development and deployment operations, including passwordless sudo. Do not expose or alter SSH
credentials.

## Operating locations

### Android work

Default execution location:

```text
Laptop
/home/munaim/Documents/github/pgsims
```

Use the dedicated Android emulator `pgsims` for Android testing unless the task explicitly requires
another target.

### Backend and deployment work

Default execution location:

```text
VPS
/home/munaim/srv/apps/pgsims
```

Access:

```bash
ssh test
```

### Caddy work

Maintained source configuration:

```text
/home/munaim/config/caddy/CaddyFile
```

Active system configuration:

```text
/etc/caddy/CaddyFile
```

The maintained configuration is synchronised to the system configuration. Treat Caddy as shared
infrastructure: preserve unrelated application routes and validate any modification before reload.

## Multi-application server constraint

The VPS hosts multiple applications. Server-wide configuration, Docker resources, ports, networks,
reverse proxies, and shared services must never be changed without considering their effect on other
applications.

## Repository synchronisation

The laptop repository and VPS repository must not be assumed to be on the same commit. Before
cross-environment work, compare the following on both environments:

```bash
git branch --show-current
git rev-parse HEAD
git status
```

Git should normally be the canonical transfer mechanism for source changes. A change is not
considered available in the other environment until it has been transferred there and verified.

## Infrastructure safety rules

Before any infrastructure or deployment change:

- Do not perform destructive production database operations without explicit authorization and a
  verified recovery path.
- Do not seed demo data into production accidentally.
- Do not delete persistent Docker volumes.
- Do not run indiscriminate Docker prune commands.
- Do not modify unrelated VPS applications.
- Do not overwrite `.env` files.
- Do not expose secrets, passwords, tokens, or SSH keys.
- Do not change SSH configuration unnecessarily.
- Do not modify global networking without understanding its dependencies.
- Do not replace the complete shared Caddy configuration; make the smallest scoped change needed.
- Do not restart unrelated services.

For Caddy changes, validate the complete resulting configuration and preserve routes for every
hosted application before reloading the service. This document establishes context and safety
defaults; it does not authorize production changes by itself.

## Verification note

On 2026-09-10, read-only checks through `ssh test` confirmed the VPS repository path and SSH
access. The supplied Caddy paths require manual review: `/home/munaim/config/caddy` was not found,
and `/etc/caddy/CaddyFile` was not found. The VPS currently has an active-looking file at
`/etc/caddy/Caddyfile` (lowercase `f`). No Caddy configuration was changed during this verification.
