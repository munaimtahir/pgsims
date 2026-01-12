#!/bin/bash

# Full deployment script for PGSIMS
# Rebuilds and redeploys web, worker, and beat services

set -e  # Exit on error

echo "=========================================="
echo "Full Application Deployment Script - PGSIMS"
echo "=========================================="

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Set explicit project name to ensure we only affect pgsims
COMPOSE_PROJECT_NAME="pgsims"

# Stop all backend services
echo "Stopping web, worker, and beat services (pgsims project only)..."
docker compose -p "$COMPOSE_PROJECT_NAME" stop web worker beat || true

# Remove containers if they exist
echo "Removing containers..."
docker compose -p "$COMPOSE_PROJECT_NAME" rm -f web worker beat || true

# Remove existing images to force rebuild (scoped to pgsims project)
echo "Removing existing images..."
docker compose -p "$COMPOSE_PROJECT_NAME" rmi -f web worker beat || true
# Also remove by container name patterns specific to pgsims
docker rmi $(docker images -q --filter "reference=pgsims*web*" 2>/dev/null) 2>/dev/null || true
docker rmi $(docker images -q --filter "reference=pgsims*worker*" 2>/dev/null) 2>/dev/null || true
docker rmi $(docker images -q --filter "reference=pgsims*beat*" 2>/dev/null) 2>/dev/null || true
docker rmi $(docker images -q --filter "reference=*sims_web*" 2>/dev/null) 2>/dev/null || true
docker rmi $(docker images -q --filter "reference=*sims_worker*" 2>/dev/null) 2>/dev/null || true
docker rmi $(docker images -q --filter "reference=*sims_beat*" 2>/dev/null) 2>/dev/null || true

# Rebuild all images without cache
echo "Rebuilding web, worker, and beat images (no cache)..."
docker compose -p "$COMPOSE_PROJECT_NAME" build --no-cache web worker beat

# Start all services
echo "Starting web, worker, and beat services..."
docker compose -p "$COMPOSE_PROJECT_NAME" up -d web worker beat

# Wait a moment for services to start
echo "Waiting for services to start..."
sleep 5

# Show logs
echo "=========================================="
echo "Web service logs (last 30 lines):"
echo "=========================================="
docker compose -p "$COMPOSE_PROJECT_NAME" logs --tail=30 web

echo "=========================================="
echo "Worker service logs (last 20 lines):"
echo "=========================================="
docker compose -p "$COMPOSE_PROJECT_NAME" logs --tail=20 worker

echo "=========================================="
echo "Beat service logs (last 20 lines):"
echo "=========================================="
docker compose -p "$COMPOSE_PROJECT_NAME" logs --tail=20 beat

# Check service status
echo "=========================================="
echo "Full deployment complete!"
echo "Checking service status..."
docker compose -p "$COMPOSE_PROJECT_NAME" ps web worker beat

echo "=========================================="
echo "Services are now running:"
echo "  Web:    http://127.0.0.1:8001"
echo "  Production: https://pgsims.alshifalab.pk"
echo "=========================================="
