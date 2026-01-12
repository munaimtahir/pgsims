#!/bin/bash

# Backend deployment script for PGSIMS
# Rebuilds and redeploys only the web (backend) service

set -e  # Exit on error

echo "=========================================="
echo "Backend Deployment Script - PGSIMS"
echo "=========================================="

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Set explicit project name to ensure we only affect pgsims
COMPOSE_PROJECT_NAME="pgsims"

# Stop the web service
echo "Stopping web service (pgsims project only)..."
docker compose -p "$COMPOSE_PROJECT_NAME" stop web || true

# Remove the web container if it exists
echo "Removing web container..."
docker compose -p "$COMPOSE_PROJECT_NAME" rm -f web || true

# Remove the web image to force rebuild (scoped to pgsims project)
echo "Removing existing web image..."
docker compose -p "$COMPOSE_PROJECT_NAME" rmi -f web || true
# Also remove by container name pattern specific to pgsims
docker rmi $(docker images -q --filter "reference=pgsims*web*" 2>/dev/null) 2>/dev/null || true
docker rmi $(docker images -q --filter "reference=*sims_web*" 2>/dev/null) 2>/dev/null || true

# Rebuild the web image without cache
echo "Rebuilding web image (no cache)..."
docker compose -p "$COMPOSE_PROJECT_NAME" build --no-cache web

# Start the web service
echo "Starting web service..."
docker compose -p "$COMPOSE_PROJECT_NAME" up -d web

# Wait a moment for the service to start
sleep 5

# Show logs
echo "=========================================="
echo "Web service logs (last 30 lines):"
echo "=========================================="
docker compose -p "$COMPOSE_PROJECT_NAME" logs --tail=30 web

# Check service status
echo "=========================================="
echo "Backend deployment complete!"
echo "Checking service status..."
docker compose -p "$COMPOSE_PROJECT_NAME" ps web

echo "=========================================="
echo "Backend is now running on:"
echo "  http://127.0.0.1:8001"
echo "  https://pgsims.alshifalab.pk"
echo "=========================================="
