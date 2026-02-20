#!/bin/bash
# SIMS Quick Deployment Script (Skip Package Lock Issues)
# Run this after pre_deployment_fix.sh

echo "🚀 SIMS Quick Deployment Script"
echo "================================"

# Set working directory
echo "📁 Navigating to project directory..."
cd /opt/sims_project || { echo "❌ Project directory not found"; exit 1; }

echo "📁 Setting up directories..."
mkdir -p static staticfiles media logs backups

echo "🔐 Setting environment variables..."
export SECRET_KEY="$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
export DEBUG="False"
export ALLOWED_HOSTS="139.162.9.224,localhost,127.0.0.1"

echo "📦 Installing dependencies (using existing venv)..."
source venv/bin/activate
pip install --no-cache-dir -r requirements.txt
pip install --no-cache-dir gunicorn

echo "🗄️ Setting up database..."
python manage.py migrate

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🔧 Setting file permissions..."
sudo chown -R www-data:www-data /opt/sims_project
sudo chmod -R 755 /opt/sims_project
sudo chmod -R 775 /opt/sims_project/media
sudo chmod -R 775 /opt/sims_project/logs
sudo chmod 664 /opt/sims_project/db.sqlite3

echo "⚙️ Setting up services..."
# Stop conflicting services
sudo systemctl stop apache2 2>/dev/null || true
sudo systemctl stop nginx 2>/dev/null || true
sudo systemctl stop sims 2>/dev/null || true

# Clean up
sudo rm -f /opt/sims_project/sims.sock

# Copy configuration files
sudo cp nginx_sims.conf /etc/nginx/sites-available/sims
sudo ln -sf /etc/nginx/sites-available/sims /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

sudo cp sims.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sims

echo "🧪 Testing configuration..."
sudo nginx -t
python manage.py check --deploy

echo "🚀 Starting services..."
sudo systemctl start sims
sleep 3

if sudo systemctl is-active --quiet sims; then
    echo "✅ SIMS service started"
else
    echo "❌ SIMS service failed"
    sudo journalctl -u sims -n 10 --no-pager
    exit 1
fi

sudo systemctl restart nginx

if sudo systemctl is-active --quiet nginx; then
    echo "✅ Nginx started"
else
    echo "❌ Nginx failed"
    sudo journalctl -u nginx -n 10 --no-pager
    exit 1
fi

echo ""
echo "✅ Deployment complete!"
echo "🌐 Access SIMS at: http://172.236.152.35/"
echo ""
echo "👤 Create admin user:"
echo "   source venv/bin/activate"
echo "   python manage.py createsuperuser"
