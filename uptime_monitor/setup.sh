#!/bin/bash
# =============================================================
# UptimeChecker — Setup Script
# =============================================================
# Usage: bash setup.sh
# Run this from the uptime_monitor/ directory (where manage.py lives).

set -e

echo "============================================="
echo "  UptimeChecker — Project Setup"
echo "============================================="

# 1. Install Python dependencies
echo ""
echo "[1/4] Installing Python dependencies..."
pip install -r requirements.txt

# 2. Run migrations
echo ""
echo "[2/4] Running database migrations..."
python manage.py migrate

# 3. Collect static files
echo ""
echo "[3/4] Collecting static files..."
python manage.py collectstatic --noinput

# 4. Create superuser (admin/admin123) if it doesn't exist
echo ""
echo "[4/4] Creating superuser (admin) if not present..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('  Superuser created: admin / admin123')
else:
    print('  Superuser already exists — skipping.')
"

echo ""
echo "============================================="
echo "  Setup complete!"
echo ""
echo "  Run the dev server:"
echo "    python manage.py runserver"
echo ""
echo "  Then open: http://127.0.0.1:8000/"
echo "  Admin panel: http://127.0.0.1:8000/admin/"
echo "    username: admin"
echo "    password: admin123"
echo ""
echo "  Run URL checks manually:"
echo "    python manage.py check_urls"
echo "============================================="
