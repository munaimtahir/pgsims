#!/bin/bash
# Helper script to create Django superuser in Docker container
# Usage: ./create_superuser.sh

set -e

PROJECT_DIR="${PROJECT_DIR:-/opt/sims_project}"

echo "👤 Creating Django Superuser"
echo "============================"

cd "$PROJECT_DIR"

# Use docker compose (v2) or docker-compose (v1)
if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Check if containers are running
if ! $DOCKER_COMPOSE ps | grep -q "sims_web.*Up"; then
    echo "❌ SIMS web container is not running!"
    echo "Please start the services first:"
    echo "  cd $PROJECT_DIR"
    echo "  $DOCKER_COMPOSE up -d"
    exit 1
fi

echo "Creating superuser in the web container..."
echo "You will be prompted to enter username, email, and password."
echo ""

$DOCKER_COMPOSE exec web python manage.py createsuperuser

echo ""
echo "✅ Superuser created successfully!"
echo ""
echo "You can now log in at: http://139.162.9.224:81/admin/"
