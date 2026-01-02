#!/bin/bash
# Pre-Deployment Fix Script
# Resolves package lock and prepares server for SIMS deployment

echo "🔧 Pre-Deployment Fix for SIMS Server 139.162.9.224"
echo "=================================================="

echo "📋 Step 1: Checking package lock status..."
if ps aux | grep -q "[u]nattended-upgrade"; then
    echo "⚠️  Found unattended-upgrades running"
    ps aux | grep "[u]nattended-upgrade"
    
    echo ""
    echo "🛑 Stopping unattended-upgrades to prevent deployment hang..."
    
    # Stop unattended-upgrades processes
    sudo pkill -f unattended-upgrade
    sudo pkill -f apt.systemd.daily
    
    # Wait for processes to stop
    sleep 3
    
    # Remove lock files
    echo "🧹 Cleaning up package lock files..."
    sudo rm -f /var/lib/dpkg/lock-frontend
    sudo rm -f /var/lib/dpkg/lock
    sudo rm -f /var/cache/apt/archives/lock
    
    # Reconfigure dpkg
    echo "🔧 Reconfiguring package manager..."
    sudo dpkg --configure -a
    
    echo "✅ Package lock resolved!"
else
    echo "✅ No package lock detected"
fi

echo ""
echo "📋 Step 2: Updating package lists..."
sudo apt update

echo ""
echo "📋 Step 3: Installing essential packages..."
sudo apt install -y python3-venv python3-pip python3-dev build-essential

echo ""
echo "📋 Step 4: Pre-creating virtual environment..."
cd /opt/sims_project || { echo "❌ Project directory not found"; exit 1; }

if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created successfully"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "📋 Step 5: Testing virtual environment..."
source venv/bin/activate
python --version
pip --version
deactivate

echo ""
echo "✅ Pre-deployment fix completed!"
echo "🚀 You can now run the main deployment script safely."
echo ""
echo "Next command:"
echo "   bash deploy_server.sh"
