# PGSIMS — PROJECT ENVIRONMENT & INFRASTRUCTURE CONTEXT

**Purpose:**  
This document defines the canonical terminology, development-machine topology, repository locations, VPS access method, deployment architecture, and infrastructure safety rules for the PGSIMS project.

Future AI-agent and developer sessions should treat the information in this document as persistent project context unless explicitly superseded.

---

# 1. CANONICAL TERMINOLOGY

Throughout all PGSIMS development sessions:

## Laptop

**Laptop** means the current local development machine.

The primary local repository is:

```text
/home/munaim/Documents/github/pgsims
```

This machine is used particularly for:

- Android development
- Android builds
- Android testing
- Android emulator testing
- local repository work
- Git operations
- development tooling

The Android emulator dedicated to this project is named:

```text
pgsims
```

When instructions refer to:

```text
the laptop
local machine
local repository
Android development machine
```

they should normally be interpreted as this machine unless explicitly stated otherwise.

---

# 2. LOCAL REPOSITORY

Canonical laptop repository:

```text
/home/munaim/Documents/github/pgsims
```

Before performing repository operations, agents should normally establish:

```bash
cd /home/munaim/Documents/github/pgsims
git status
git branch --show-current
git rev-parse HEAD
```

Do not assume that the local repository and deployed VPS repository are on the same commit without verifying.

---

# 3. ANDROID DEVELOPMENT ENVIRONMENT

Android development is primarily performed on the laptop.

Dedicated Android emulator:

```text
pgsims
```

Agents working on Android should therefore normally perform:

- Gradle builds
- Android Studio / CLI operations
- APK/AAB generation
- emulator installation
- runtime testing
- UI workflow testing
- Android screenshots or recordings

from the laptop repository:

```text
/home/munaim/Documents/github/pgsims
```

The backend remains remote and is hosted on the VPS.

Android development should use the appropriate deployed backend/API configuration rather than creating an independent backend unless specifically required.

---

# 4. VPS DEFINITION

Throughout this project:

**VPS** means the Google Cloud virtual machine hosting the deployed PGSIMS backend and other applications.

The PGSIMS repository/deployment location on the VPS is:

```text
/home/munaim/srv/apps/pgsims
```

When instructions refer to:

```text
VPS
server
backend server
Google Cloud VM
production/deployed server
```

they generally refer to this machine unless another environment is explicitly identified.

---

# 5. VPS ACCESS FROM THE LAPTOP

The laptop has SSH configuration allowing direct access to the VPS through the SSH alias:

```text
test
```

Connect using:

```bash
ssh test
```

The configured SSH access allows the development agent to operate on the VPS without repeatedly entering credentials.

The VPS account also has passwordless sudo capability for authorised administrative operations.

Therefore commands such as:

```bash
ssh test
```

can be used by development agents to access the VPS and inspect or manage the deployed environment.

## Important

The SSH alias should be treated as infrastructure configuration already established on the laptop.

Agents should **not** modify SSH keys, SSH aliases, authentication settings, or sudo configuration unless specifically instructed.

Never copy private SSH keys or credentials into the repository.

---

# 6. BACKEND DEPLOYMENT LOCATION

The deployed PGSIMS application/backend resides at:

```text
/home/munaim/srv/apps/pgsims
```

Typical server-side operations should begin with:

```bash
ssh test
cd /home/munaim/srv/apps/pgsims
```

Before making changes, establish the deployed baseline:

```bash
git status
git branch --show-current
git rev-parse HEAD
```

The deployed repository must not be assumed to be identical to the laptop repository.

Always compare the relevant commits/branches before deployment or debugging when repository state matters.

---

# 7. MULTI-APPLICATION VPS

The Google Cloud VPS hosts **multiple applications**.

PGSIMS is therefore not the only workload on this server.

This is a critical infrastructure constraint.

Agents must avoid:

- changing global network settings unnecessarily,
- changing firewall rules without understanding other applications,
- binding services to ports already used by other applications,
- stopping shared infrastructure,
- restarting unrelated services,
- deleting shared Docker resources,
- deleting shared networks,
- modifying global proxy configuration without validation,
- performing broad cleanup commands that could affect other deployed applications.

Examples of potentially dangerous operations include indiscriminate use of:

```bash
docker system prune
docker network prune
docker volume prune
```

or global service/network changes.

These should not be performed unless their effect on all hosted applications has been explicitly assessed.

---

# 8. CADDY REVERSE-PROXY ARCHITECTURE

Network routing and reverse proxy configuration for applications hosted on the VPS is managed using **Caddy**.

The maintained Caddy configuration file is:

```text
/home/munaim/config/caddy/CaddyFile
```

The active system Caddy configuration is:

```text
/etc/caddy/CaddyFile
```

The maintained project/server configuration is synchronised to the system Caddy configuration.

Conceptually:

```text
/home/munaim/config/caddy/CaddyFile
                │
                │ synchronised to
                ▼
/etc/caddy/CaddyFile
                │
                ▼
          Caddy service
                │
                ├── PGSIMS
                ├── Other application
                ├── Other application
                └── Other VPS services
```

Because Caddy routes traffic for multiple applications, any Caddy modification must be treated as a **shared-infrastructure change**.

---

# 9. CADDY SAFETY RULES

Before modifying Caddy:

1. Inspect the maintained configuration:

```bash
sudo cat /home/munaim/config/caddy/CaddyFile
```

2. Determine whether the requested change is truly required.

3. Preserve all unrelated application routes.

4. Modify only the relevant block.

5. Validate the resulting configuration before reload.

Where appropriate:

```bash
sudo caddy validate --config /etc/caddy/CaddyFile
```

or validate the maintained configuration before synchronising it.

6. Only reload Caddy after successful validation.

Do not replace the complete Caddy configuration with a PGSIMS-only configuration.

Do not remove or alter routes belonging to other hosted applications.

---

# 10. INFRASTRUCTURE SOURCE-OF-TRUTH RULE

For Caddy configuration, treat:

```text
/home/munaim/config/caddy/CaddyFile
```

as the maintained configuration location.

The operational system file is:

```text
/etc/caddy/CaddyFile
```

Agents should avoid making an undocumented change directly to:

```text
/etc/caddy/CaddyFile
```

that is not reflected in the maintained configuration, because it could later be overwritten during synchronisation.

---

# 11. DEVELOPMENT TOPOLOGY

The canonical PGSIMS topology is:

```text
┌─────────────────────────────────────────────────────────┐
│ LAPTOP                                                  │
│                                                         │
│ Repository:                                             │
│ /home/munaim/Documents/github/pgsims                   │
│                                                         │
│ Primary uses:                                           │
│ • Android development                                   │
│ • Git/source development                                │
│ • Gradle builds                                         │
│ • Android testing                                       │
│                                                         │
│ Android emulator:                                       │
│ pgsims                                                  │
└───────────────────────┬─────────────────────────────────┘
                        │
                        │ SSH
                        │ alias: test
                        ▼
┌─────────────────────────────────────────────────────────┐
│ GOOGLE CLOUD VPS                                        │
│                                                         │
│ PGSIMS backend repository:                              │
│ /home/munaim/srv/apps/pgsims                           │
│                                                         │
│ Hosts multiple applications                             │
│                                                         │
│ Shared reverse proxy: Caddy                             │
│                                                         │
│ Maintained config:                                      │
│ /home/munaim/config/caddy/CaddyFile                    │
│                                                         │
│ Active config:                                          │
│ /etc/caddy/CaddyFile                                   │
└─────────────────────────────────────────────────────────┘
```

---

# 12. DEFAULT OPERATING ASSUMPTIONS FOR AI AGENTS

Unless explicitly instructed otherwise:

### Android work

Perform on:

```text
Laptop
/home/munaim/Documents/github/pgsims
```

Use emulator:

```text
pgsims
```

### Backend source/deployment inspection

Perform on:

```text
VPS
/home/munaim/srv/apps/pgsims
```

Access with:

```bash
ssh test
```

### Reverse proxy/network routing

Inspect:

```text
/home/munaim/config/caddy/CaddyFile
```

Active configuration:

```text
/etc/caddy/CaddyFile
```

Treat Caddy as shared infrastructure.

---

# 13. REPOSITORY SYNCHRONISATION RULE

The laptop repository and VPS repository represent different working environments.

Never assume synchronization.

Before operations involving both environments compare:

```text
Laptop SHA
VPS SHA
Laptop branch
VPS branch
Laptop git status
VPS git status
```

If they differ, determine why before copying files, pulling, pushing, merging, deploying, or troubleshooting version-specific behaviour.

Git should normally be used as the canonical mechanism for transferring source-code changes between development and deployed environments rather than ad-hoc file copying.

---

# 14. PRODUCTION / DEPLOYMENT SAFETY

Before a server-side action that could affect runtime behaviour, establish:

- current Git branch,
- current Git SHA,
- working-tree status,
- running services,
- application/container names where relevant,
- database/environment being used,
- whether the operation could affect other VPS applications.

Do not:

- flush a production database,
- seed synthetic records into production unintentionally,
- run destructive migrations casually,
- delete persistent volumes,
- overwrite `.env` files,
- expose secrets,
- restart unrelated applications,
- modify shared Caddy routes unnecessarily.

---

# 15. TERMINOLOGY SUMMARY

| Term | Canonical meaning |
|---|---|
| **Laptop** | Current local development machine |
| **Laptop repository** | `/home/munaim/Documents/github/pgsims` |
| **Android emulator** | `pgsims` |
| **VPS** | Google Cloud VM hosting the backend |
| **VPS repository** | `/home/munaim/srv/apps/pgsims` |
| **VPS SSH alias** | `test` |
| **SSH command** | `ssh test` |
| **Maintained Caddy config** | `/home/munaim/config/caddy/CaddyFile` |
| **Active Caddy config** | `/etc/caddy/CaddyFile` |

---

# 16. CONTEXT PRECEDENCE

This document defines the current project environment topology.

If future documentation conflicts with this document:

1. verify the actual infrastructure,
2. prefer newer explicit project decisions,
3. update this document,
4. avoid maintaining contradictory context in multiple files.

The intent is for this file to remain the **canonical environment/infrastructure reference** for future PGSIMS development sessions.

---

**Document:** `docs/PROJECT_ENVIRONMENT_CONTEXT.md`