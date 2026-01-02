#!/bin/bash
# Verification script for SIMS Docker Compose deployment
# Checks all services and endpoints

set -e

SERVER_IP="139.162.9.224"
SERVER_PORT="81"
PROJECT_DIR="${PROJECT_DIR:-/opt/sims_project}"

echo "🔍 SIMS Deployment Verification"
echo "==============================="
echo ""

cd "$PROJECT_DIR"

# Use docker compose (v2) or docker-compose (v1)
if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check 1: Container Status
echo "1. Checking container status..."
echo "--------------------------------"
$DOCKER_COMPOSE ps
echo ""

# Check 2: Individual Container Health
echo "2. Checking individual containers..."
echo "-------------------------------------"
ALL_HEALTHY=true

for container in sims_db sims_redis sims_web sims_worker sims_beat sims_nginx; do
    if docker ps --format '{{.Names}}\t{{.Status}}' | grep -q "^${container}"; then
        STATUS=$(docker ps --format '{{.Names}}\t{{.Status}}' | grep "^${container}" | awk '{print $2}')
        if echo "$STATUS" | grep -q "Up"; then
            print_success "$container is running"
        else
            print_error "$container is not running properly: $STATUS"
            ALL_HEALTHY=false
        fi
    else
        print_error "$container is not running"
        ALL_HEALTHY=false
    fi
done
echo ""

# Check 3: Network Connectivity
echo "3. Checking network connectivity..."
echo "------------------------------------"
if docker network ls | grep -q "sims_network"; then
    print_success "Docker network 'sims_network' exists"
else
    print_error "Docker network 'sims_network' not found"
fi
echo ""

# Check 4: Database Connection
echo "4. Checking database connection..."
echo "----------------------------------"
if $DOCKER_COMPOSE exec -T db pg_isready -U sims_user > /dev/null 2>&1; then
    print_success "Database is accepting connections"
else
    print_error "Database is not accepting connections"
fi
echo ""

# Check 5: Redis Connection
echo "5. Checking Redis connection..."
echo "--------------------------------"
if $DOCKER_COMPOSE exec -T redis redis-cli ping > /dev/null 2>&1; then
    print_success "Redis is responding"
else
    print_error "Redis is not responding"
fi
echo ""

# Check 6: Web Application Health
echo "6. Checking web application health..."
echo "--------------------------------------"
if curl -f -s "http://localhost:$SERVER_PORT/healthz/" > /dev/null 2>&1; then
    print_success "Health endpoint is responding"
    curl -s "http://localhost:$SERVER_PORT/healthz/"
    echo ""
else
    print_error "Health endpoint is not responding"
fi
echo ""

# Check 7: Homepage Accessibility
echo "7. Checking homepage accessibility..."
echo "-------------------------------------"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$SERVER_PORT/" || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    print_success "Homepage is accessible (HTTP $HTTP_CODE)"
elif [ "$HTTP_CODE" = "302" ] || [ "$HTTP_CODE" = "301" ]; then
    print_success "Homepage is redirecting (HTTP $HTTP_CODE) - this is normal"
else
    print_error "Homepage returned HTTP $HTTP_CODE"
fi
echo ""

# Check 8: Static Files
echo "8. Checking static files..."
echo "---------------------------"
if $DOCKER_COMPOSE exec -T web test -d /app/staticfiles && [ "$($DOCKER_COMPOSE exec -T web ls -A /app/staticfiles | wc -l)" -gt 0 ]; then
    print_success "Static files are collected"
else
    print_warning "Static files may not be collected properly"
fi
echo ""

# Check 9: Port Listening
echo "9. Checking port $SERVER_PORT..."
echo "---------------------------------"
if ss -tulpn 2>/dev/null | grep -q ":$SERVER_PORT " || netstat -tulpn 2>/dev/null | grep -q ":$SERVER_PORT "; then
    print_success "Port $SERVER_PORT is listening"
else
    print_warning "Port $SERVER_PORT may not be listening (check firewall)"
fi
echo ""

# Check 10: Recent Logs (last 10 lines)
echo "10. Recent logs from web container..."
echo "-------------------------------------"
$DOCKER_COMPOSE logs --tail=10 web
echo ""

# Summary
echo "=========================================="
if [ "$ALL_HEALTHY" = true ]; then
    print_success "DEPLOYMENT VERIFICATION COMPLETE"
    echo ""
    echo "🌐 Access URLs:"
    echo "   Homepage: http://$SERVER_IP:$SERVER_PORT/"
    echo "   Login:    http://$SERVER_IP:$SERVER_PORT/users/login/"
    echo "   Admin:    http://$SERVER_IP:$SERVER_PORT/admin/"
    echo "   Health:   http://$SERVER_IP:$SERVER_PORT/healthz/"
else
    print_error "SOME ISSUES DETECTED"
    echo ""
    echo "Please check the logs:"
    echo "  $DOCKER_COMPOSE logs -f"
    echo ""
    echo "Or check specific service:"
    echo "  $DOCKER_COMPOSE logs -f [service_name]"
fi
echo "=========================================="
