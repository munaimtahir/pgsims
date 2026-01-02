#!/bin/bash
# SIMS Quick Deployment Script
# This script deploys SIMS using Docker Compose

set -e

echo "=========================================="
echo "SIMS Deployment Script"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Creating .env from template..."
    python3 << 'PYEOF'
import secrets
import string
alphabet = string.ascii_letters + string.digits + string.punctuation
secret_key = ''.join(secrets.choice(alphabet) for i in range(50))
env_content = f"""# SIMS Environment Configuration
SECRET_KEY={secret_key}
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1
JWT_ACCESS_TOKEN_MINUTES=60
JWT_REFRESH_TOKEN_DAYS=7
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
"""
with open('.env', 'w') as f:
    f.write(env_content)
print("✅ Created .env file")
PYEOF
fi

# Check if frontend/.env.local exists
if [ ! -f frontend/.env.local ]; then
    echo "Creating frontend/.env.local..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > frontend/.env.local
    echo "✅ Created frontend/.env.local"
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v docker compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

echo ""
echo "Building Docker images..."
docker compose build

echo ""
echo "Starting services..."
docker compose up -d

echo ""
echo "Waiting for services to be ready..."
sleep 10

echo ""
echo "Checking service status..."
docker compose ps

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "Services are running. Access the application at:"
echo "  - Frontend: http://localhost:81/"
echo "  - Backend API: http://localhost:81/api/"
echo "  - Admin: http://localhost:81/admin/"
echo ""
echo "To view logs: docker compose logs -f"
echo "To stop: docker compose down"
echo ""
