#!/bin/bash
# Switch SIMS deployment to VPS
# This script switches the active configuration to VPS (139.162.9.224:81)

set -e

echo "========================================="
echo "Switching SIMS to VPS Configuration"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env.vps exists
if [ ! -f ".env.vps" ]; then
    echo -e "${RED}Error: .env.vps file not found!${NC}"
    echo "Please create .env.vps file first."
    exit 1
fi

# Backup current .env if it exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}Backing up current .env to .env.backup${NC}"
    cp .env .env.backup
fi

# Copy VPS config to .env
echo -e "${YELLOW}Copying VPS configuration...${NC}"
cp .env.vps .env
echo -e "${GREEN}✓ Switched to VPS configuration${NC}"

# Frontend configuration
if [ -d "frontend" ] && [ -f "frontend/.env.vps" ]; then
    if [ -f "frontend/.env.local" ]; then
        echo -e "${YELLOW}Backing up frontend/.env.local to frontend/.env.local.backup${NC}"
        cp frontend/.env.local frontend/.env.local.backup
    fi
    echo -e "${YELLOW}Switching frontend to VPS configuration...${NC}"
    cp frontend/.env.vps frontend/.env.local
    echo -e "${GREEN}✓ Frontend switched to VPS${NC}"
fi

echo ""
echo -e "${GREEN}✓ Configuration switched to VPS${NC}"
echo ""
echo "Next steps:"
echo "  1. Review .env file and update SECRET_KEY and DB_PASSWORD"
echo "  2. Deploy to VPS using: docker compose up -d"
echo "  3. Run migrations: docker compose exec web python manage.py migrate"
echo ""

