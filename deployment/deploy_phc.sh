#!/bin/bash
# Deployment script for PGSIMS on pgsims.alshifalab.pk
# Server IP: 34.124.150.231
# Domain: pgsims.alshifalab.pk
# Backend Port: 8014

set -e

PROJECT_DIR="${PROJECT_DIR:-/home/munaim/srv/apps/pgsims}"
SERVER_IP="34.124.150.231"
DOMAIN="pgsims.alshifalab.pk"
BACKEND_PORT="8014"

echo "=========================================="
echo "PGSIMS Deployment Script"
echo "=========================================="
echo ""
echo "Domain: $DOMAIN"
echo "Server IP: $SERVER_IP"
echo "Backend Port: $BACKEND_PORT"
echo ""

cd "$PROJECT_DIR"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# Step 1: Check .env file
print_info "Step 1: Checking environment configuration..."

if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from example..."
    if [ -f "deployment/.env.phc.example" ]; then
        cp deployment/.env.phc.example .env
        print_warning "Please edit .env file and set SECRET_KEY, DB_PASSWORD, and other required values"
        print_warning "Press Enter to continue after editing .env, or Ctrl+C to abort..."
        read
    else
        print_error ".env file not found and no example available. Please create .env manually."
        exit 1
    fi
else
    print_success ".env file exists"
fi

# Verify required environment variables
if ! grep -q "SECRET_KEY=" .env || grep -q "SECRET_KEY=your-secret-key" .env; then
    print_warning "SECRET_KEY not set or using default. Please set a strong SECRET_KEY in .env"
fi

if ! grep -q "DB_PASSWORD=" .env || grep -q "DB_PASSWORD=your-strong" .env; then
    print_warning "DB_PASSWORD not set or using default. Please set a strong DB_PASSWORD in .env"
fi

# Step 2: Verify Caddy configuration
print_info "Step 2: Checking Caddy configuration..."

if [ -f "/etc/caddy/Caddyfile" ]; then
    if grep -q "pgsims.alshifalab.pk" /etc/caddy/Caddyfile; then
        print_success "Caddyfile contains pgsims.alshifalab.pk configuration"
    else
        print_warning "Caddyfile exists but doesn't contain pgsims.alshifalab.pk configuration"
        print_info "Please add the configuration from deployment/Caddyfile.pgsims to /etc/caddy/Caddyfile"
        print_info "Then run: sudo caddy validate --config /etc/caddy/Caddyfile"
        print_info "And: sudo systemctl reload caddy"
    fi
else
    print_warning "Caddyfile not found at /etc/caddy/Caddyfile"
    print_info "Please copy deployment/Caddyfile.pgsims to /etc/caddy/Caddyfile and configure Caddy"
fi

# Step 3: Stop existing containers
print_info "Step 3: Stopping existing containers..."
$DOCKER_COMPOSE -f docker-compose.phc.yml down 2>/dev/null || true
print_success "Existing containers stopped (if any)"

# Step 4: Build Docker images
print_info "Step 4: Building Docker images..."
print_warning "This may take several minutes on first run..."

$DOCKER_COMPOSE -f docker-compose.phc.yml build --no-cache
print_success "Docker images built successfully"

# Step 5: Start all services
print_info "Step 5: Starting all services..."

$DOCKER_COMPOSE -f docker-compose.phc.yml up -d
print_success "Services started"

# Step 6: Wait for services to be healthy
print_info "Step 6: Waiting for services to be healthy..."
sleep 15

# Step 7: Verify containers are running
print_info "Step 7: Verifying containers are running..."

ALL_RUNNING=true
for container in sims_db_phc sims_redis_phc sims_web_phc sims_worker_phc sims_beat_phc; do
    if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        print_success "Container $container is running"
    else
        print_error "Container $container is not running!"
        ALL_RUNNING=false
    fi
done

if [ "$ALL_RUNNING" = false ]; then
    print_error "Some containers failed to start. Checking logs..."
    $DOCKER_COMPOSE -f docker-compose.phc.yml logs --tail=50
    exit 1
fi

# Step 8: Run database migrations
print_info "Step 8: Running database migrations..."

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 5

$DOCKER_COMPOSE -f docker-compose.phc.yml exec -T web python manage.py migrate --noinput
print_success "Database migrations completed"

# Step 9: Collect static files
print_info "Step 9: Collecting static files..."

$DOCKER_COMPOSE -f docker-compose.phc.yml exec -T web python manage.py collectstatic --noinput
print_success "Static files collected"

# Step 10: Verify backend is accessible
print_info "Step 10: Verifying backend is accessible..."

sleep 5
if curl -f -s "http://localhost:$BACKEND_PORT/healthz/" > /dev/null 2>&1; then
    print_success "Backend is responding on port $BACKEND_PORT"
    curl -s "http://localhost:$BACKEND_PORT/healthz/" | head -1
    echo ""
else
    print_warning "Backend health check failed. This might be normal if services are still starting."
    print_info "Check logs with: $DOCKER_COMPOSE -f docker-compose.phc.yml logs web"
fi

# Step 11: Summary
echo ""
echo "=========================================="
print_success "DEPLOYMENT COMPLETE"
echo "=========================================="
echo ""
echo "🌐 Access URLs:"
echo "   Homepage: https://$DOMAIN/"
echo "   Login:    https://$DOMAIN/users/login/"
echo "   Admin:    https://$DOMAIN/admin/"
echo "   Health:   https://$DOMAIN/healthz/"
echo ""
echo "📋 Next Steps:"
echo "   1. Create superuser:"
echo "      $DOCKER_COMPOSE -f docker-compose.phc.yml exec web python manage.py createsuperuser"
echo ""
echo "   2. (Optional) Seed demo data:"
echo "      $DOCKER_COMPOSE -f docker-compose.phc.yml exec web python scripts/preload_demo_data.py"
echo ""
echo "   3. Verify Caddy is routing correctly:"
echo "      curl https://$DOMAIN/healthz/"
echo ""
echo "   4. Check logs if needed:"
echo "      $DOCKER_COMPOSE -f docker-compose.phc.yml logs -f"
echo ""
echo "=========================================="
