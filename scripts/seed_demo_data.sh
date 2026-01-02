#!/bin/bash
# Demo Data Seeding Script for SIMS
# This script runs the demo data seeding process

set -e

echo "=========================================="
echo "SIMS Demo Data Seeding Script"
echo "=========================================="
echo ""

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# Check if we're in a virtual environment or Docker
if [ -f "manage.py" ]; then
    echo "✓ Found manage.py"
else
    echo "❌ manage.py not found. Are you in the project root?"
    exit 1
fi

# Check if migrations need to be run
echo "Checking database migrations..."
python3 manage.py migrate --check 2>/dev/null || {
    echo "Running database migrations..."
    python3 manage.py migrate --noinput
}

# Run the seeding script
echo ""
echo "Running demo data seeding script..."
echo ""

if python3 scripts/preload_demo_data.py; then
    echo ""
    echo "=========================================="
    echo "✅ Demo data seeding completed successfully!"
    echo "=========================================="
    echo ""
    echo "Demo credentials:"
    echo "  Admin:      username: admin,     password: admin123"
    echo "  Supervisor: username: dr_smith,  password: supervisor123"
    echo "  Supervisor: username: dr_jones,  password: supervisor123"
    echo "  PG Student: username: pg_ahmed,  password: student123"
    echo "  PG Student: username: pg_fatima, password: student123"
    echo ""
    exit 0
else
    echo ""
    echo "❌ Demo data seeding failed!"
    echo "Check the error messages above for details."
    exit 1
fi

