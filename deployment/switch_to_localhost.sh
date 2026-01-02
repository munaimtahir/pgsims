#!/bin/bash
# Switch SIMS deployment to localhost
# This script switches the active configuration to localhost

set -e

echo "========================================="
echo "Switching SIMS to Localhost Configuration"
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

# Backup current .env if it exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}Backing up current .env to .env.backup${NC}"
    cp .env .env.backup
fi

# Copy localhost config to .env
echo -e "${YELLOW}Copying localhost configuration...${NC}"
cp .env.localhost .env
echo -e "${GREEN}✓ Switched to localhost configuration${NC}"

# Frontend configuration
if [ -d "frontend" ] && [ -f "frontend/.env.localhost" ]; then
    if [ -f "frontend/.env.local" ]; then
        echo -e "${YELLOW}Backing up frontend/.env.local to frontend/.env.local.backup${NC}"
        cp frontend/.env.local frontend/.env.local.backup
    fi
    echo -e "${YELLOW}Switching frontend to localhost configuration...${NC}"
    cp frontend/.env.localhost frontend/.env.local
    echo -e "${GREEN}✓ Frontend switched to localhost${NC}"
fi

echo ""
echo -e "${GREEN}✓ Configuration switched to localhost${NC}"
echo ""
echo "Next steps:"
echo "  1. Review .env file and adjust if needed"
echo "  2. Run: ./deployment/deploy_localhost.sh"
echo "  3. Or manually: docker compose -f docker-compose.localhost.yml up -d"
echo ""

