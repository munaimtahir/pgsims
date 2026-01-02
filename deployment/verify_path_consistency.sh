#!/bin/bash
# Path Consistency Verification Script
# Verifies that all deployment scripts and configurations use /opt/sims_project

echo "🔍 SIMS Path Consistency Verification"
echo "======================================"
echo ""

PROJECT_DIR="/opt/sims_project"
ERRORS=0
WARNINGS=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_file() {
    local file="$1"
    local pattern="$2"
    local description="$3"
    
    if [ ! -f "$file" ]; then
        echo -e "${YELLOW}⚠️  File not found: $file${NC}"
        ((WARNINGS++))
        return
    fi
    
    # Skip the verification script itself
    if [ "$(basename "$file")" = "verify_path_consistency.sh" ]; then
        return 0
    fi
    
    if grep -q "$pattern" "$file"; then
        echo -e "${RED}❌ $description${NC}"
        echo "   File: $file"
        echo "   Found: $pattern"
        ((ERRORS++))
        return 1
    else
        echo -e "${GREEN}✅ $description${NC}"
        return 0
    fi
}

echo "📋 Checking deployment scripts..."
echo "-----------------------------------"

# Check deployment scripts
check_file "deploy_server.sh" "/var/www/sims_project" "deploy_server.sh uses correct path"
check_file "deploy_server_no_venv.sh" "/var/www/sims_project" "deploy_server_no_venv.sh uses correct path"
check_file "deploy_server_root.sh" "/var/www/sims_project" "deploy_server_root.sh uses correct path"
check_file "deploy_server_quick.sh" "/var/www/sims_project" "deploy_server_quick.sh uses correct path"
check_file "DEPLOY_NOW.sh" "/var/www/sims_project" "DEPLOY_NOW.sh uses correct path"
check_file "fix_403_error.sh" "/var/www/sims_project" "fix_403_error.sh uses correct path"
check_file "diagnose_nginx_403.sh" "/var/www/sims_project" "diagnose_nginx_403.sh uses correct path"
check_file "pre_deployment_fix.sh" "/var/www/sims_project" "pre_deployment_fix.sh uses correct path"
check_file "verify_server_setup.sh" "/var/www/sims_project" "verify_server_setup.sh uses correct path"

echo ""
echo "📋 Checking service files..."
echo "-----------------------------------"

check_file "sims_no_venv.service" "/var/www/sims_project" "sims_no_venv.service uses correct path"
check_file "gunicorn.conf.py" "/var/www/sims_project" "gunicorn.conf.py uses correct path"

echo ""
echo "📋 Checking configuration files..."
echo "-----------------------------------"

check_file "server_config.env" "/var/www/sims_project" "server_config.env uses correct path"
check_file "server_config_172.237.95.120.env" "/var/www/sims_project" "server_config_172.237.95.120.env uses correct path"

echo ""
echo "📋 Verifying correct path usage..."
echo "-----------------------------------"

# Check that /opt/sims_project is used in key files
KEY_FILES=(
    "deploy_server.sh"
    "deploy_server_no_venv.sh"
    "sims_no_venv.service"
    "gunicorn.conf.py"
)

for file in "${KEY_FILES[@]}"; do
    if [ -f "$file" ]; then
        if grep -q "/opt/sims_project" "$file"; then
            echo -e "${GREEN}✅ $file references /opt/sims_project${NC}"
        else
            echo -e "${YELLOW}⚠️  $file does not reference /opt/sims_project${NC}"
            ((WARNINGS++))
        fi
    fi
done

echo ""
echo "📋 Checking Docker deployment..."
echo "-----------------------------------"

if [ -f "deploy_docker_compose.sh" ]; then
    if grep -q "PROJECT_DIR.*/opt/sims_project" "deploy_docker_compose.sh"; then
        echo -e "${GREEN}✅ Docker deployment script uses /opt/sims_project${NC}"
    else
        echo -e "${RED}❌ Docker deployment script may not use /opt/sims_project${NC}"
        ((ERRORS++))
    fi
else
    echo -e "${YELLOW}⚠️  deploy_docker_compose.sh not found${NC}"
    ((WARNINGS++))
fi

echo ""
echo "======================================"
echo "📊 Summary"
echo "======================================"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! All paths are consistent.${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  $WARNINGS warning(s) found, but no critical errors.${NC}"
    exit 0
else
    echo -e "${RED}❌ $ERRORS error(s) and $WARNINGS warning(s) found.${NC}"
    echo ""
    echo "Please review the files listed above and update them to use /opt/sims_project"
    exit 1
fi
