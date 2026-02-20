#!/bin/bash
# SIMS Localhost Deployment Script
# This script sets up and deploys SIMS on localhost

set -e

echo "========================================="
echo "SIMS Localhost Deployment Script"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env.localhost exists
if [ ! -f ".env.localhost" ]; then
    echo -e "${RED}Error: .env.localhost file not found!${NC}"
    echo "Please create .env.localhost file first."
    exit 1
fi

# Copy .env.localhost to .env
echo -e "${YELLOW}Setting up environment configuration...${NC}"
if [ -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env already exists. Backing up to .env.backup${NC}"
    cp .env .env.backup
fi
cp .env.localhost .env
echo -e "${GREEN}✓ Environment configuration copied${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed!${NC}"
    echo "Please install Docker Desktop for Windows/Mac or Docker for Linux"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed!${NC}"
    exit 1
fi

# Use docker compose (v2) if available, otherwise docker-compose (v1)
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo ""
echo -e "${YELLOW}Starting services with Docker Compose...${NC}"
echo "Using: $DOCKER_COMPOSE -f docker-compose.localhost.yml"

# Build and start services
$DOCKER_COMPOSE -f docker-compose.localhost.yml up -d --build

echo ""
echo -e "${GREEN}✓ Services started${NC}"
echo ""

# Wait for services to be ready
echo -e "${YELLOW}Waiting for services to be ready...${NC}"
sleep 10

# Run migrations
echo ""
echo -e "${YELLOW}Running database migrations...${NC}"
$DOCKER_COMPOSE -f docker-compose.localhost.yml exec -T web python manage.py migrate --noinput
echo -e "${GREEN}✓ Migrations completed${NC}"

# Collect static files
echo ""
echo -e "${YELLOW}Collecting static files...${NC}"
$DOCKER_COMPOSE -f docker-compose.localhost.yml exec -T web python manage.py collectstatic --noinput
echo -e "${GREEN}✓ Static files collected${NC}"

# Create superuser if needed
echo ""
echo -e "${YELLOW}Checking for superuser...${NC}"
echo "To create a superuser, run:"
echo "  $DOCKER_COMPOSE -f docker-compose.localhost.yml exec web python manage.py createsuperuser"
echo ""

echo "========================================="
echo -e "${GREEN}Deployment Complete!${NC}"
echo "========================================="
echo ""
echo "Access the application at:"
echo "  - Django Admin: http://localhost:8000/admin/"
echo "  - Main App:    http://localhost:8000/"
echo "  - Health Check: http://localhost:8000/healthz/"
echo ""
echo "To view logs:"
echo "  $DOCKER_COMPOSE -f docker-compose.localhost.yml logs -f"
echo ""
echo "To stop services:"
echo "  $DOCKER_COMPOSE -f docker-compose.localhost.yml down"
echo ""

