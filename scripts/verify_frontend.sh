#!/bin/bash
# Frontend Verification Script
# Verifies Next.js frontend setup and build

set -e  # Exit on error

cd frontend

echo "=== Frontend Verification Script ==="
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm ci
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

# Check environment variables
if [ -z "$NEXT_PUBLIC_API_URL" ]; then
    echo "⚠️  NEXT_PUBLIC_API_URL not set."
    if [ -f .env.local ]; then
        echo "✅ Using .env.local"
    else
        echo "⚠️  Defaulting to http://localhost:8000 (development only)"
    fi
fi

echo ""
echo "=== Running Linter ==="
npm run lint || echo "⚠️  Linter found issues (check output above)"
echo ""

echo "=== Building Frontend ==="
npm run build
echo ""

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "Build artifacts created in: frontend/.next/"
    echo ""
    echo "To start the dev server:"
    echo "  npm run dev"
    echo ""
    echo "To start production server:"
    echo "  npm run start"
else
    echo "❌ Build failed. Check errors above."
    exit 1
fi
