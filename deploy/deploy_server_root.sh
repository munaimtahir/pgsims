#!/bin/bash
# SIMS Deployment Script for Nginx Server 139.162.9.224 (ROOT VERSION)
# Run this script on your server to deploy the SIMS project

echo "🚀 SIMS Deployment Script for Nginx Server 139.162.9.224 (ROOT)"
echo "=================================================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "⚠️  Running as root. Proceeding with root deployment..."
   SUDO_CMD=""  # No sudo needed when running as root
else
   echo "ℹ️  Running as regular user with sudo..."
   SUDO_CMD="sudo"
fi

# Update system packages
echo "📦 Updating system packages..."
apt update
apt install -y nginx python3-venv python3-pip python3-dev build-essential

# Set working directory
echo "📁 Navigating to project directory..."
cd /opt/sims_project || { echo "❌ Project directory not found. Please upload your project files first."; exit 1; }

echo "📁 Setting up directories..."
# Create necessary directories
mkdir -p static
mkdir -p staticfiles  
mkdir -p media
mkdir -p logs
mkdir -p backups

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔐 Setting environment variables..."
# Set environment variables for production
export SECRET_KEY="$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
export DEBUG="False"
export ALLOWED_HOSTS="139.162.9.224,localhost,127.0.0.1"

echo "📦 Installing dependencies..."
# Activate virtual environment and install requirements
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn  # Install Gunicorn for Nginx

echo "🗄️ Setting up database..."
# Run migrations
python manage.py migrate

echo "📁 Collecting static files..."
# Collect static files
python manage.py collectstatic --noinput

echo "👤 Creating superuser..."
# Create superuser (interactive)
echo "Please create an admin user for the system:"
python manage.py createsuperuser

echo "🔧 Setting file permissions..."
# Set proper permissions (adjusted for root)
if [[ $EUID -eq 0 ]]; then
    # Running as root - set ownership to www-data
    chown -R www-data:www-data /opt/sims_project
    chmod -R 755 /opt/sims_project
    chmod -R 775 /opt/sims_project/media
    chmod -R 775 /opt/sims_project/logs
    chmod 664 /opt/sims_project/db.sqlite3
else
    # Running as regular user - use sudo
    $SUDO_CMD chown -R www-data:www-data /opt/sims_project
    $SUDO_CMD chmod -R 755 /opt/sims_project
    $SUDO_CMD chmod -R 775 /opt/sims_project/media
    $SUDO_CMD chmod -R 775 /opt/sims_project/logs
    $SUDO_CMD chmod 664 /opt/sims_project/db.sqlite3
fi

echo "⚙️ Setting up Nginx and Gunicorn..."
# Check what's using port 80
echo "🔍 Checking port 80 usage..."
if ss -tulpn | grep -q ":80 "; then
    echo "📋 Port 80 is in use. Checking services..."
    ss -tulpn | grep ":80 "
    
    # Stop common web servers that might conflict
    echo "🛑 Stopping conflicting services..."
    systemctl stop apache2 2>/dev/null && echo "   ✅ Stopped Apache2" || echo "   ℹ️  Apache2 not running"
    systemctl stop nginx 2>/dev/null && echo "   ✅ Stopped Nginx" || echo "   ℹ️  Nginx not running"
    
    # Disable Apache2 to prevent conflicts
    if systemctl is-enabled --quiet apache2 2>/dev/null; then
        echo "🔧 Disabling Apache2 to prevent startup conflicts..."
        systemctl disable apache2
    fi
fi

# Stop any existing SIMS services
systemctl stop sims 2>/dev/null || true

# Remove any existing socket files
rm -f /opt/sims_project/sims.sock

# Copy Nginx configuration
cp nginx_sims.conf /etc/nginx/sites-available/sims
ln -sf /etc/nginx/sites-available/sims /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default  # Remove default site

# Copy systemd service file
cp sims.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable sims

echo "🧪 Testing configuration..."
# Test Nginx configuration
nginx -t

# Test that Django can start
python manage.py check --deploy

echo "🚀 Starting services..."
# Start SIMS service first
systemctl start sims

# Wait a moment for service to start
sleep 3

# Check if SIMS service started successfully
if systemctl is-active --quiet sims; then
    echo "✅ SIMS service started successfully"
else
    echo "❌ SIMS service failed to start"
    echo "📋 Checking logs:"
    journalctl -u sims -n 10 --no-pager
    exit 1
fi

# Start Nginx
systemctl restart nginx

# Check if Nginx started successfully
if systemctl is-active --quiet nginx; then
    echo "✅ Nginx started successfully"
else
    echo "❌ Nginx failed to start"
    echo "📋 Checking logs:"
    journalctl -u nginx -n 10 --no-pager
    exit 1
fi

echo "✅ Deployment complete!"
echo ""
echo "🔍 Final checks..."
# Check socket file
if [ -S "/opt/sims_project/sims.sock" ]; then
    echo "✅ Gunicorn socket created successfully"
    ls -la /opt/sims_project/sims.sock
else
    echo "⚠️  Socket file not found, checking service status..."
    systemctl status sims --no-pager
fi
echo ""
echo "🌐 Access your SIMS system at:"
echo "   Homepage: http://139.162.9.224:81/"
echo "   Login:    http://139.162.9.224:81/users/login/"
echo "   Admin:    http://139.162.9.224:81/admin/"
echo ""
echo "🔧 Service management commands:"
echo "   systemctl status sims     # Check SIMS status"
echo "   systemctl restart sims    # Restart SIMS"
echo "   systemctl status nginx    # Check Nginx status"
echo "   systemctl restart nginx   # Restart Nginx"
echo ""
echo "📋 Next steps:"
echo "   1. Test all functionality"
echo "   2. Set up SSL certificates (recommended)"
echo "   3. Configure firewall rules"
echo "   4. Set up automated backups"
