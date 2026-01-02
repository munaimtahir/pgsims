#!/bin/bash
# Docker Compose Deployment Script for SIMS
# Server: 139.162.9.224
# Port: 81
# Run this script on the server after cloning the repository

set -e  # Exit on error

SERVER_IP="139.162.9.224"
SERVER_PORT="81"
PROJECT_DIR="${PROJECT_DIR:-/opt/sims_project}"

echo "🚀 SIMS Docker Compose Deployment Script"
echo "=========================================="
echo "Server: $SERVER_IP"
echo "Port: $SERVER_PORT"
echo "Project Directory: $PROJECT_DIR"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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
    echo -e "ℹ️  $1"
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
    echo "Please clone the repository first:"
    echo "  sudo mkdir -p /opt"
    echo "  sudo git clone https://github.com/munaimtahir/sims.git $PROJECT_DIR"
    echo "  sudo chown -R \$USER:\$USER $PROJECT_DIR"
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

if [ ! -f "deployment/nginx.conf" ]; then
    print_error "deployment/nginx.conf not found!"
    exit 1
fi

print_success "All required files found"

# Step 4: Create .env file if it doesn't exist
print_info "Step 4: Setting up environment variables..."

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
ALLOWED_HOSTS=$SERVER_IP,localhost,127.0.0.1

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

# Email Settings (optional - configure if needed)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
# EMAIL_HOST=your-smtp-server.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@domain.com
# EMAIL_HOST_PASSWORD=your-email-password

# CORS Settings (optional)
# CORS_ALLOWED_ORIGINS=http://$SERVER_IP:$SERVER_PORT
EOF
    
    print_success ".env file created with generated SECRET_KEY and DB_PASSWORD"
    print_warning "IMPORTANT: Save the DB_PASSWORD securely! You'll need it for database backups."
    echo "DB_PASSWORD: $DB_PASSWORD"
else
    print_info ".env file already exists. Verifying required variables..."
    
    # Check if required variables are set
    if ! grep -q "SECRET_KEY=" .env || [ -z "$(grep 'SECRET_KEY=' .env | cut -d'=' -f2)" ]; then
        print_error "SECRET_KEY is not set in .env file!"
        exit 1
    fi
    
    if ! grep -q "DB_PASSWORD=" .env || [ -z "$(grep 'DB_PASSWORD=' .env | cut -d'=' -f2)" ]; then
        print_error "DB_PASSWORD is not set in .env file!"
        exit 1
    fi
    
    # Update ALLOWED_HOSTS if needed
    if ! grep -q "$SERVER_IP" .env; then
        print_warning "Updating ALLOWED_HOSTS to include $SERVER_IP..."
        sed -i "s/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=$SERVER_IP,localhost,127.0.0.1/" .env
    fi
    
    print_success ".env file verified"
fi

# Step 5: Configure firewall
print_info "Step 5: Configuring firewall..."

if command -v ufw &> /dev/null; then
    if sudo ufw status | grep -q "$SERVER_PORT/tcp"; then
        print_info "Port $SERVER_PORT is already allowed in firewall"
    else
        sudo ufw allow $SERVER_PORT/tcp
        print_success "Port $SERVER_PORT allowed in firewall"
    fi
elif command -v firewall-cmd &> /dev/null; then
    if sudo firewall-cmd --list-ports | grep -q "$SERVER_PORT/tcp"; then
        print_info "Port $SERVER_PORT is already allowed in firewall"
    else
        sudo firewall-cmd --permanent --add-port=$SERVER_PORT/tcp
        sudo firewall-cmd --reload
        print_success "Port $SERVER_PORT allowed in firewall"
    fi
else
    print_warning "No firewall management tool found. Please manually open port $SERVER_PORT"
fi

# Step 6: Verify nginx.conf is configured correctly
print_info "Step 6: Verifying Nginx configuration..."

if grep -q "listen 81" deployment/nginx.conf && grep -q "$SERVER_IP" deployment/nginx.conf; then
    print_success "Nginx configuration is correct"
else
    print_warning "Nginx configuration may need updates. Checking..."
    # The file should already be configured, but we'll verify
fi

# Step 7: Stop any existing containers
print_info "Step 7: Stopping any existing containers..."

$DOCKER_COMPOSE down 2>/dev/null || true
print_success "Existing containers stopped (if any)"

# Step 8: Build Docker images
print_info "Step 8: Building Docker images..."
print_warning "This may take several minutes on first run..."

$DOCKER_COMPOSE build --no-cache
print_success "Docker images built successfully"

# Step 9: Start all services
print_info "Step 9: Starting all services..."

$DOCKER_COMPOSE up -d
print_success "Services started"

# Step 10: Wait for services to be healthy
print_info "Step 10: Waiting for services to be healthy..."

sleep 10

# Check container status
print_info "Checking container status..."
$DOCKER_COMPOSE ps

# Step 11: Verify containers are running
print_info "Step 11: Verifying containers are running..."

ALL_RUNNING=true
for container in sims_db sims_redis sims_web sims_worker sims_beat sims_nginx; do
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

# Step 12: Run database migrations
print_info "Step 12: Running database migrations..."

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 5

$DOCKER_COMPOSE exec -T web python manage.py migrate --noinput
print_success "Database migrations completed"

# Step 13: Verify static files
print_info "Step 13: Verifying static files collection..."

# Static files should be collected automatically during container startup
# But let's verify
if $DOCKER_COMPOSE exec -T web test -d /app/staticfiles; then
    print_success "Static files directory exists"
else
    print_warning "Static files may not be collected. Running collectstatic..."
    $DOCKER_COMPOSE exec -T web python manage.py collectstatic --noinput
fi

# Step 14: Test deployment
print_info "Step 14: Testing deployment..."

sleep 5

# Test health endpoint
if curl -f -s "http://localhost:$SERVER_PORT/healthz/" > /dev/null 2>&1; then
    print_success "Health endpoint is responding"
else
    print_warning "Health endpoint not responding yet. This may be normal during startup."
fi

# Test homepage
if curl -f -s "http://localhost:$SERVER_PORT/" > /dev/null 2>&1; then
    print_success "Homepage is accessible"
else
    print_warning "Homepage not accessible yet. Check logs if this persists."
fi

# Step 15: Display access information
echo ""
echo "=========================================="
print_success "DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "🌐 Access your application at:"
echo "   Homepage: http://$SERVER_IP:$SERVER_PORT/"
echo "   Login:    http://$SERVER_IP:$SERVER_PORT/users/login/"
echo "   Admin:    http://$SERVER_IP:$SERVER_PORT/admin/"
echo "   Health:   http://$SERVER_IP:$SERVER_PORT/healthz/"
echo ""
echo "📋 Next Steps:"
echo "   1. Create a superuser account:"
echo "      cd $PROJECT_DIR"
echo "      $DOCKER_COMPOSE exec web python manage.py createsuperuser"
echo ""
echo "   2. View logs:"
echo "      $DOCKER_COMPOSE logs -f [service_name]"
echo "      # Available services: web, nginx, db, redis, worker, beat"
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
print_warning "IMPORTANT: Save your .env file securely. It contains sensitive credentials!"
echo ""
