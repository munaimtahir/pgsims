#!/bin/bash
# Backend Deployment Script for PGSIMS
# Rebuilds and restarts Django backend containers (web, worker, beat)
# Removes old images and builds fresh containers

set -e

PROJECT_DIR="${PROJECT_DIR:-/home/munaim/srv/apps/pgsims}"
COMPOSE_FILE="docker-compose.phc.yml"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo "=========================================="
echo "PGSIMS Backend Deployment Script"
echo "=========================================="
echo ""

cd "$PROJECT_DIR"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is available
if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if compose file exists
if [ ! -f "$COMPOSE_FILE" ]; then
    print_error "Docker Compose file not found: $COMPOSE_FILE"
    exit 1
fi

print_info "Step 1: Stopping existing backend containers..."
$DOCKER_COMPOSE -f "$COMPOSE_FILE" stop web worker beat 2>/dev/null || true
print_success "Containers stopped"

print_info "Step 2: Removing old backend containers..."
$DOCKER_COMPOSE -f "$COMPOSE_FILE" rm -f web worker beat 2>/dev/null || true
print_success "Old containers removed"

print_info "Step 3: Removing old backend images..."
# Remove images with the project name prefix
docker images | grep -E "pgsims-(web|worker|beat)" | awk '{print $3}' | xargs -r docker rmi -f 2>/dev/null || true
# Also try to remove by name
docker rmi pgsims-web pgsims-worker pgsims-beat 2>/dev/null || true
print_success "Old images removed (if any existed)"

print_info "Step 4: Pruning unused Docker resources..."
docker system prune -f --volumes=false > /dev/null 2>&1 || true
print_success "Docker system pruned"

print_info "Step 5: Building fresh backend images..."
print_warning "This may take several minutes on first build..."
$DOCKER_COMPOSE -f "$COMPOSE_FILE" build --no-cache web worker beat
print_success "Backend images built successfully"

print_info "Step 6: Starting backend containers..."
$DOCKER_COMPOSE -f "$COMPOSE_FILE" up -d web worker beat
print_success "Backend containers started"

print_info "Step 7: Waiting for services to be healthy..."
sleep 15

print_info "Step 8: Verifying backend containers are running..."
ALL_RUNNING=true
for container in sims_web_phc sims_worker_phc sims_beat_phc; do
    if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        print_success "Container $container is running"
    else
        print_error "Container $container is not running!"
        ALL_RUNNING=false
    fi
done

if [ "$ALL_RUNNING" = false ]; then
    print_error "Some containers failed to start. Checking logs..."
    $DOCKER_COMPOSE -f "$COMPOSE_FILE" logs --tail=50 web worker beat
    exit 1
fi

print_info "Step 9: Running database migrations..."
# Wait for database to be ready
sleep 5
$DOCKER_COMPOSE -f "$COMPOSE_FILE" exec -T web python manage.py migrate --noinput 2>/dev/null || \
    $DOCKER_COMPOSE -f "$COMPOSE_FILE" exec web python manage.py migrate --noinput
print_success "Database migrations completed"

print_info "Step 10: Collecting static files..."
$DOCKER_COMPOSE -f "$COMPOSE_FILE" exec -T web python manage.py collectstatic --noinput 2>/dev/null || \
    $DOCKER_COMPOSE -f "$COMPOSE_FILE" exec web python manage.py collectstatic --noinput
print_success "Static files collected"

print_info "Step 11: Verifying backend health..."
sleep 5
if curl -f -s "http://localhost:8014/healthz/" > /dev/null 2>&1; then
    print_success "Backend is healthy and responding on port 8014"
    curl -s "http://localhost:8014/healthz/" | head -1
    echo ""
else
    print_warning "Backend health check failed. This might be normal if services are still starting."
    print_info "Check logs with: $DOCKER_COMPOSE -f $COMPOSE_FILE logs web"
fi

echo ""
echo "=========================================="
print_success "BACKEND DEPLOYMENT COMPLETE"
echo "=========================================="
echo ""
echo "📋 Container Status:"
$DOCKER_COMPOSE -f "$COMPOSE_FILE" ps web worker beat
echo ""
echo "🌐 Backend URLs:"
echo "   Health Check: http://localhost:8014/healthz/"
echo "   Production:   https://pgsims.alshifalab.pk/"
echo ""
echo "📋 Useful Commands:"
echo "   View logs:     $DOCKER_COMPOSE -f $COMPOSE_FILE logs -f web"
echo "   Restart:       $DOCKER_COMPOSE -f $COMPOSE_FILE restart web worker beat"
echo "   Stop all:      $DOCKER_COMPOSE -f $COMPOSE_FILE stop"
echo ""
echo "=========================================="
