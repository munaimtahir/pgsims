#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUTPUT_DIR="${PLAYWRIGHT_MCP_OUTPUT_DIR:-$ROOT_DIR/output/playwright/mcp}"
MCP_DIR="$ROOT_DIR/scripts/mcp"

mkdir -p "$OUTPUT_DIR"

if [[ ! -x "$MCP_DIR/node_modules/.bin/playwright-mcp" ]]; then
  npm ci --prefix "$MCP_DIR" >/dev/null
fi

exec npx --yes --prefix "$MCP_DIR" playwright-mcp --headless --output-dir "$OUTPUT_DIR" "$@"
