# Playwright MCP Agent Setup

This repository now ships a reusable Playwright MCP server configuration for local AI agents.

## Included Files

- `.mcp.json`: workspace MCP server config with server name `playwright`.
- `scripts/mcp/playwright-mcp.sh`: launcher script used by the MCP server.
- `scripts/mcp/package.json` + `scripts/mcp/package-lock.json`: pinned MCP dependency manifest and lockfile.

## What It Runs

The launcher starts:

```bash
npx --yes --prefix scripts/mcp playwright-mcp --headless --output-dir output/playwright/mcp
```

`@playwright/mcp` is pinned via committed lockfile (`scripts/mcp/package-lock.json`), and the launcher auto-runs:

```bash
npm ci --prefix scripts/mcp
```

on first use if the binary is not installed locally.

Artifacts are stored under `output/playwright/mcp/`.

## How To Use From AI Agents

1. Point your MCP-capable client to this workspace `.mcp.json`.
2. Reload/restart the client so it re-reads MCP servers.
3. Use server name `playwright` from the client/tool picker.

## Smoke Check

Run:

```bash
bash scripts/mcp/playwright-mcp.sh --version
```

Expected: a version string from `@playwright/mcp`.
