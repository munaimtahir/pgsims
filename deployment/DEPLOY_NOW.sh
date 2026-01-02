#!/bin/bash
# Quick Deployment Script for SIMS on VPS (139.162.9.224:81)
# Run this script ON THE VPS SERVER after cloning/pulling the repository

set -e  # Exit on error

echo "🚀 SIMS Deployment Script for 139.162.9.224:81"
echo "================================================"
echo ""

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  This script needs sudo privileges. Running with sudo..."
    exec sudo bash "$0" "$@"
fi

# Step 1: Navigate to project directory
echo "📁 Step 1: Setting up project directory..."
if [ ! -d "/opt/sims_project" ]; then
    echo "❌ Project directory /opt/sims_project not found!"
    echo "Please clone the repository first:"
    echo "  sudo mkdir -p /opt"
    echo "  sudo git clone https://github.com/munaimtahir/sims.git /opt/sims_project"
    echo "  sudo chown -R \$USER:\$USER /opt/sims_project"
    exit 1
fi

cd /opt/sims_project

# Step 2: Update system packages
echo ""
echo "📦 Step 2: Updating system packages..."
apt update
apt install -y python3 python3-pip python3-dev build-essential nginx git

# Step 3: Install Python dependencies
echo ""
echo "📦 Step 3: Installing Python dependencies..."
pip3 install --break-system-packages -r requirements.txt
pip3 install --break-system-packages gunicorn

# Step 4: Create necessary directories
echo ""
echo "📁 Step 4: Creating directories..."
mkdir -p static staticfiles media logs backups

# Step 5: Set environment variables
echo ""
echo "🔐 Step 5: Setting environment variables..."
export SECRET_KEY="$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
export DEBUG="False"
export ALLOWED_HOSTS="139.162.9.224,localhost,127.0.0.1"
export DJANGO_SETTINGS_MODULE="sims_project.settings"

# Step 6: Run database migrations
echo ""
echo "🗄️  Step 6: Running database migrations..."
python3 manage.py migrate --noinput

# Step 7: Collect static files
echo ""
echo "📁 Step 7: Collecting static files..."
python3 manage.py collectstatic --noinput

# Step 8: Set file permissions
echo ""
echo "🔧 Step 8: Setting file permissions..."
chown -R www-data:www-data /opt/sims_project
chmod -R 755 /opt/sims_project
chmod -R 775 /opt/sims_project/media
chmod -R 775 /opt/sims_project/logs
[ -f db.sqlite3 ] && chmod 664 db.sqlite3 || true

# Step 9: Configure Nginx
echo ""
echo "⚙️  Step 9: Configuring Nginx..."
# Stop conflicting services
systemctl stop apache2 2>/dev/null || true
systemctl stop nginx 2>/dev/null || true
systemctl stop sims 2>/dev/null || true

# Remove old socket file
rm -f /opt/sims_project/sims.sock

# Copy nginx configuration
cp deployment/nginx_sims.conf /etc/nginx/sites-available/sims
ln -sf /etc/nginx/sites-available/sims /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
if ! nginx -t; then
    echo "❌ Nginx configuration test failed!"
    exit 1
fi

# Step 10: Configure systemd service
echo ""
echo "⚙️  Step 10: Configuring systemd service..."
cp deployment/sims_no_venv.service /etc/systemd/system/sims.service
systemctl daemon-reload
systemctl enable sims

# Step 11: Test Django configuration
echo ""
echo "🧪 Step 11: Testing Django configuration..."
python3 manage.py check --deploy

# Step 12: Start services
echo ""
echo "🚀 Step 12: Starting services..."
systemctl start sims
sleep 3

# Check if SIMS service started
if systemctl is-active --quiet sims; then
    echo "✅ SIMS service started successfully"
else
    echo "❌ SIMS service failed to start"
    echo "Checking logs..."
    journalctl -u sims -n 20 --no-pager
    exit 1
fi

# Restart nginx
systemctl restart nginx

# Check if nginx started
if systemctl is-active --quiet nginx; then
    echo "✅ Nginx started successfully"
else
    echo "❌ Nginx failed to start"
    echo "Checking logs..."
    journalctl -u nginx -n 20 --no-pager
    exit 1
fi

# Step 13: Configure firewall
echo ""
echo "🔥 Step 13: Configuring firewall..."
if command -v ufw &> /dev/null; then
    ufw allow 81/tcp
    echo "✅ Firewall rule added for port 81"
fi

# Final verification
echo ""
echo "🔍 Step 14: Verifying deployment..."
sleep 2

# Check socket file
if [ -S "/opt/sims_project/sims.sock" ]; then
    echo "✅ Gunicorn socket file exists"
else
    echo "⚠️  Socket file not found, but service is running"
fi

# Check if port 81 is listening
if ss -tulpn | grep -q ":81 "; then
    echo "✅ Port 81 is listening"
else
    echo "⚠️  Port 81 is not listening - check nginx configuration"
fi

echo ""
echo "================================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "================================================"
echo ""
echo "🌐 Access your application at:"
echo "   Homepage: http://139.162.9.224:81/"
echo "   Login:    http://139.162.9.224:81/users/login/"
echo "   Admin:    http://139.162.9.224:81/admin/"
echo ""
echo "👤 Create admin user:"
echo "   cd /opt/sims_project"
echo "   export ALLOWED_HOSTS='139.162.9.224,localhost,127.0.0.1'"
echo "   python3 manage.py createsuperuser"
echo ""
echo "📋 Useful commands:"
echo "   sudo systemctl status sims      # Check SIMS status"
echo "   sudo systemctl restart sims    # Restart SIMS"
echo "   sudo systemctl status nginx    # Check Nginx status"
echo "   sudo journalctl -u sims -f     # View SIMS logs"
echo "   sudo tail -f /var/log/nginx/sims_error.log  # View Nginx errors"
echo ""

