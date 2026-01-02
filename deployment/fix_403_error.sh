#!/bin/bash
# SIMS 403 Forbidden Error Fix Script for 172.236.152.35

echo "🔧 SIMS 403 Forbidden Error Fix Script"
echo "======================================"

cd /opt/sims_project || { echo "❌ Project directory not found"; exit 1; }

echo "1. 📁 Fixing file permissions..."
# Fix ownership
sudo chown -R www-data:www-data /opt/sims_project
sudo chown -R www-data:www-data /opt/sims_project/*

# Fix permissions
sudo chmod -R 755 /opt/sims_project
sudo chmod -R 755 /opt/sims_project/staticfiles
sudo chmod -R 755 /opt/sims_project/media
sudo chmod -R 775 /opt/sims_project/logs
sudo chmod 644 /opt/sims_project/db.sqlite3 2>/dev/null || echo "No SQLite database found"
sudo chmod 664 /opt/sims_project/db.sqlite3 2>/dev/null || echo "SQLite permissions already set"

echo "2. 🧹 Cleaning up old socket files..."
sudo rm -f /opt/sims_project/sims.sock

echo "3. 🔄 Restarting services..."
sudo systemctl stop sims
sudo systemctl stop nginx

# Start services in order
echo "Starting SIMS service..."
sudo systemctl start sims
sleep 3

echo "Starting Nginx..."
sudo systemctl start nginx

echo "4. ✅ Checking service status..."
echo "SIMS Service Status:"
sudo systemctl status sims --no-pager -l

echo ""
echo "Nginx Status:"
sudo systemctl status nginx --no-pager -l

echo ""
echo "5. 🔍 Checking socket file..."
if [ -S "/opt/sims_project/sims.sock" ]; then
    echo "✅ Socket file exists"
    ls -la /opt/sims_project/sims.sock
else
    echo "❌ Socket file not found"
    echo "Check Gunicorn logs:"
    sudo journalctl -u sims -n 20 --no-pager
fi

echo ""
echo "6. 🌐 Testing HTTP connection..."
curl -I http://localhost/ 2>/dev/null || echo "❌ Local HTTP test failed"

echo ""
echo "7. 📋 Quick diagnostic commands:"
echo "sudo journalctl -u sims -f          # Follow SIMS logs"
echo "sudo tail -f /var/log/nginx/error.log  # Follow Nginx error logs"
echo "sudo systemctl restart sims         # Restart SIMS service"
echo "sudo systemctl restart nginx        # Restart Nginx"

echo ""
echo "🎯 Fix script complete!"
echo "Try accessing http://172.236.152.35/ now"
