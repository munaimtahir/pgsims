#!/bin/bash
# Docker Compose Deployment Script for PGSIMS
# VPS: 34.16.82.13
# Domain: pgsims.alshifalab.pk
# Caddy reverse proxy configuration already set up
# Frontend: pgsims.alshifalab.pk -> 127.0.0.1:8082
# Backend: api.pgsims.alshifalab.pk -> 127.0.0.1:8014

set -e  # Exit on error

VPS_IP="34.16.82.13"
DOMAIN="pgsims.alshifalab.pk"
API_DOMAIN="api.pgsims.alshifalab.pk"
PROJECT_DIR="${PROJECT_DIR:-/home/munaim/srv/apps/pgsims}"

echo "🚀 PGSIMS Docker Compose Deployment Script"
echo "=========================================="
echo "VPS IP: $VPS_IP"
echo "Domain: $DOMAIN"
echo "API Domain: $API_DOMAIN"
echo "Project Directory: $PROJECT_DIR"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Step 1: Verify Docker and Docker Compose
print_info "Step 1: Verifying Docker and Docker Compose installation..."

if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed!"
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    print_success "Docker installed. Please log out and log back in, then run this script again."
    exit 1
fi

if ! command -v docker compose &> /dev/null && ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed!"
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    print_success "Docker Compose installed"
fi

# Use docker compose (v2) or docker-compose (v1)
if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

print_success "Docker and Docker Compose are installed"
docker --version
$DOCKER_COMPOSE --version

# Step 2: Navigate to project directory
print_info "Step 2: Setting up project directory..."

if [ ! -d "$PROJECT_DIR" ]; then
    print_error "Project directory $PROJECT_DIR not found!"
    exit 1
fi

cd "$PROJECT_DIR"
print_success "Changed to project directory: $PROJECT_DIR"

# Step 3: Verify required files exist
print_info "Step 3: Verifying required files..."

if [ ! -f "docker-compose.yml" ]; then
    print_error "docker-compose.yml not found!"
    exit 1
fi

if [ ! -f "Dockerfile" ]; then
    print_error "Dockerfile not found!"
    exit 1
fi

if [ ! -f "Dockerfile.frontend" ]; then
    print_error "Dockerfile.frontend not found!"
    exit 1
fi

print_success "All required files found"

# Step 4: Verify Caddyfile configuration
print_info "Step 4: Verifying Caddyfile configuration..."

CADDYFILE="/home/munaim/srv/proxy/caddy/Caddyfile"
if [ -f "$CADDYFILE" ]; then
    if grep -q "pgsims.alshifalab.pk" "$CADDYFILE" && grep -q "127.0.0.1:8082" "$CADDYFILE" && grep -q "127.0.0.1:8014" "$CADDYFILE"; then
        print_success "Caddyfile is configured correctly for PGSIMS"
    else
        print_warning "Caddyfile may need updates. Please verify it includes:"
        echo "  - pgsims.alshifalab.pk -> 127.0.0.1:8082"
        echo "  - api.pgsims.alshifalab.pk -> 127.0.0.1:8014"
    fi
else
    print_warning "Caddyfile not found at $CADDYFILE. Please ensure Caddy is configured."
fi

# Step 5: Create or update .env file
print_info "Step 5: Setting up environment variables..."

if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    
    # Generate secret key
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' 2>/dev/null || openssl rand -hex 32)
    
    # Generate database password
    DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
    
    cat > .env << EOF
# Django Settings
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,$API_DOMAIN,$VPS_IP,localhost,127.0.0.1

# Database Settings
DB_NAME=sims_db
DB_USER=sims_user
DB_PASSWORD=$DB_PASSWORD
DB_HOST=db
DB_PORT=5432

# Redis Settings
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/1

# Reverse Proxy Settings (for Caddy)
USE_PROXY_HEADERS=True
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://$DOMAIN,https://$API_DOMAIN
CORS_ALLOWED_ORIGINS=https://$DOMAIN

# Frontend API URL
NEXT_PUBLIC_API_URL=https://$API_DOMAIN

# Email Settings (optional - configure if needed)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
# EMAIL_HOST=your-smtp-server.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@domain.com
# EMAIL_HOST_PASSWORD=your-email-password
EOF
    
    print_success ".env file created with generated SECRET_KEY and DB_PASSWORD"
    print_warning "IMPORTANT: Save the DB_PASSWORD securely! You'll need it for database backups."
    echo "DB_PASSWORD: $DB_PASSWORD"
else
    print_info ".env file already exists. Updating configuration..."
    
    # Update ALLOWED_HOSTS if needed
    if ! grep -q "$DOMAIN" .env || ! grep -q "$VPS_IP" .env; then
        print_warning "Updating ALLOWED_HOSTS to include $DOMAIN and $VPS_IP..."
        # Read current ALLOWED_HOSTS
        CURRENT_HOSTS=$(grep "^ALLOWED_HOSTS=" .env | cut -d'=' -f2 || echo "")
        if [ -n "$CURRENT_HOSTS" ]; then
            # Check if domains/IPs are already in the list
            if [[ ! "$CURRENT_HOSTS" == *"$DOMAIN"* ]]; then
                sed -i "s/^ALLOWED_HOSTS=.*/ALLOWED_HOSTS=$DOMAIN,$API_DOMAIN,$VPS_IP,localhost,127.0.0.1/" .env
            fi
        else
            echo "ALLOWED_HOSTS=$DOMAIN,$API_DOMAIN,$VPS_IP,localhost,127.0.0.1" >> .env
        fi
    fi
    
    # Update CSRF_TRUSTED_ORIGINS if needed
    if ! grep -q "CSRF_TRUSTED_ORIGINS=" .env || ! grep -q "$DOMAIN" .env; then
        print_warning "Updating CSRF_TRUSTED_ORIGINS..."
        if grep -q "^CSRF_TRUSTED_ORIGINS=" .env; then
            sed -i "s|^CSRF_TRUSTED_ORIGINS=.*|CSRF_TRUSTED_ORIGINS=https://$DOMAIN,https://$API_DOMAIN|" .env
        else
            echo "CSRF_TRUSTED_ORIGINS=https://$DOMAIN,https://$API_DOMAIN" >> .env
        fi
    fi
    
    # Update CORS_ALLOWED_ORIGINS if needed
    if ! grep -q "CORS_ALLOWED_ORIGINS=" .env || ! grep -q "$DOMAIN" .env; then
        print_warning "Updating CORS_ALLOWED_ORIGINS..."
        if grep -q "^CORS_ALLOWED_ORIGINS=" .env; then
            sed -i "s|^CORS_ALLOWED_ORIGINS=.*|CORS_ALLOWED_ORIGINS=https://$DOMAIN|" .env
        else
            echo "CORS_ALLOWED_ORIGINS=https://$DOMAIN" >> .env
        fi
    fi
    
    # Update NEXT_PUBLIC_API_URL if needed
    if ! grep -q "NEXT_PUBLIC_API_URL=" .env || ! grep -q "$API_DOMAIN" .env; then
        print_warning "Updating NEXT_PUBLIC_API_URL..."
        if grep -q "^NEXT_PUBLIC_API_URL=" .env; then
            sed -i "s|^NEXT_PUBLIC_API_URL=.*|NEXT_PUBLIC_API_URL=https://$API_DOMAIN|" .env
        else
            echo "NEXT_PUBLIC_API_URL=https://$API_DOMAIN" >> .env
        fi
    fi
    
    # Ensure SECRET_KEY exists
    if ! grep -q "^SECRET_KEY=" .env || [ -z "$(grep '^SECRET_KEY=' .env | cut -d'=' -f2)" ]; then
        print_warning "SECRET_KEY not found. Generating new one..."
        SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' 2>/dev/null || openssl rand -hex 32)
        if grep -q "^SECRET_KEY=" .env; then
            sed -i "s|^SECRET_KEY=.*|SECRET_KEY=$SECRET_KEY|" .env
        else
            echo "SECRET_KEY=$SECRET_KEY" >> .env
        fi
    fi
    
    # Ensure DB_PASSWORD exists
    if ! grep -q "^DB_PASSWORD=" .env || [ -z "$(grep '^DB_PASSWORD=' .env | cut -d'=' -f2)" ]; then
        print_warning "DB_PASSWORD not found. Generating new one..."
        DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
        if grep -q "^DB_PASSWORD=" .env; then
            sed -i "s|^DB_PASSWORD=.*|DB_PASSWORD=$DB_PASSWORD|" .env
        else
            echo "DB_PASSWORD=$DB_PASSWORD" >> .env
        fi
        echo "New DB_PASSWORD: $DB_PASSWORD"
    fi
    
    print_success ".env file updated"
fi

# Step 6: Stop any existing containers
print_info "Step 6: Stopping any existing containers..."

$DOCKER_COMPOSE down 2>/dev/null || true
print_success "Existing containers stopped (if any)"

# Step 7: Build Docker images
print_info "Step 7: Building Docker images..."
print_warning "This may take several minutes on first run..."

$DOCKER_COMPOSE build
print_success "Docker images built successfully"

# Step 8: Start all services
print_info "Step 8: Starting all services..."

$DOCKER_COMPOSE up -d
print_success "Services started"

# Step 9: Wait for services to be healthy
print_info "Step 9: Waiting for services to be healthy..."

sleep 15

# Check container status
print_info "Checking container status..."
$DOCKER_COMPOSE ps

# Step 10: Verify containers are running
print_info "Step 10: Verifying containers are running..."

ALL_RUNNING=true
for container in sims_db sims_redis sims_web sims_worker sims_beat sims_frontend; do
    if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        print_success "Container $container is running"
    else
        print_error "Container $container is not running!"
        ALL_RUNNING=false
    fi
done

if [ "$ALL_RUNNING" = false ]; then
    print_error "Some containers failed to start. Checking logs..."
    $DOCKER_COMPOSE logs --tail=50
    exit 1
fi

# Step 11: Run database migrations
print_info "Step 11: Running database migrations..."

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

$DOCKER_COMPOSE exec -T web python manage.py migrate --noinput
print_success "Database migrations completed"

# Step 12: Verify static files
print_info "Step 12: Verifying static files collection..."

# Static files should be collected automatically during container startup
# But let's verify
if $DOCKER_COMPOSE exec -T web test -d /app/staticfiles; then
    print_success "Static files directory exists"
else
    print_warning "Static files may not be collected. Running collectstatic..."
    $DOCKER_COMPOSE exec -T web python manage.py collectstatic --noinput
fi

# Step 13: Verify ports are listening
print_info "Step 13: Verifying ports are listening..."

if ss -tuln | grep -q ":8082"; then
    print_success "Port 8082 (frontend) is listening"
else
    print_warning "Port 8082 may not be listening yet"
fi

if ss -tuln | grep -q ":8014"; then
    print_success "Port 8014 (backend) is listening"
else
    print_warning "Port 8014 may not be listening yet"
fi

# Step 14: Test local endpoints
print_info "Step 14: Testing local endpoints..."

sleep 5

# Test backend health endpoint
if curl -f -s "http://127.0.0.1:8014/healthz/" > /dev/null 2>&1; then
    print_success "Backend health endpoint is responding"
else
    print_warning "Backend health endpoint not responding yet. This may be normal during startup."
fi

# Test frontend
if curl -f -s "http://127.0.0.1:8082" > /dev/null 2>&1; then
    print_success "Frontend is accessible"
else
    print_warning "Frontend not accessible yet. Check logs if this persists."
fi

# Step 15: Verify Caddy can reach the services
print_info "Step 15: Verifying Caddy configuration..."

if command -v caddy &> /dev/null; then
    print_info "Checking if Caddy is running..."
    if systemctl is-active --quiet caddy || pgrep -x caddy > /dev/null; then
        print_success "Caddy is running"
    else
        print_warning "Caddy may not be running. Please start it with: sudo systemctl start caddy"
    fi
else
    print_warning "Caddy command not found. Please ensure Caddy is installed and configured."
fi

# Step 16: Display access information
echo ""
echo "=========================================="
print_success "DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "🌐 Access your application at:"
echo "   Frontend: https://$DOMAIN"
echo "   Backend API: https://$API_DOMAIN"
echo "   VPS IP: http://$VPS_IP (if firewall allows)"
echo ""
echo "📋 Next Steps:"
echo "   1. Create a superuser account:"
echo "      cd $PROJECT_DIR"
echo "      $DOCKER_COMPOSE exec web python manage.py createsuperuser"
echo ""
echo "   2. View logs:"
echo "      $DOCKER_COMPOSE logs -f [service_name]"
echo "      # Available services: web, frontend, db, redis, worker, beat"
echo ""
echo "   3. Check container status:"
echo "      $DOCKER_COMPOSE ps"
echo ""
echo "   4. Restart services:"
echo "      $DOCKER_COMPOSE restart"
echo ""
echo "   5. Stop services:"
echo "      $DOCKER_COMPOSE down"
echo ""
echo "   6. Backup database:"
echo "      $DOCKER_COMPOSE exec db pg_dump -U sims_user sims_db > backup_\$(date +%Y%m%d_%H%M%S).sql"
echo ""
echo "   7. Reload Caddy (if needed):"
echo "      sudo systemctl reload caddy"
echo ""
print_warning "IMPORTANT: Save your .env file securely. It contains sensitive credentials!"
echo ""
print_info "Verify public access:"
echo "   - Frontend: curl -I https://$DOMAIN"
echo "   - Backend: curl -I https://$API_DOMAIN/healthz/"
echo ""
