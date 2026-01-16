#!/bin/bash
# Backend Verification Script
# Verifies Django backend setup, migrations, and system checks

set -e  # Exit on error

echo "=== Backend Verification Script ==="
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

# Activate venv
source .venv/bin/activate
echo "✅ Virtual environment activated"

# Check if requirements are installed
if ! python -c "import django" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

# Check environment variables
if [ -z "$SECRET_KEY" ]; then
    echo "⚠️  SECRET_KEY not set. Loading from .env..."
    if [ -f .env ]; then
        export $(grep -v '^#' .env | xargs)
    else
        echo "❌ .env file not found. SECRET_KEY is required."
        exit 1
    fi
fi

echo ""
echo "=== Running Django System Checks ==="
python manage.py check --deploy || python manage.py check
echo ""

echo "=== Checking Migration Status ==="
python manage.py showmigrations
echo ""

echo "=== Applying Migrations (if needed) ==="
python manage.py migrate --plan
read -p "Apply migrations? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py migrate
    echo "✅ Migrations applied"
else
    echo "⏭️  Skipping migrations"
fi

echo ""
echo "=== Verification Complete ==="
echo ""
echo "To start the server:"
echo "  python manage.py runserver"
