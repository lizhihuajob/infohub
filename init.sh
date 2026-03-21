#!/bin/bash
set -e

mkdir -p /app/data /app/logs /app/staticfiles /app/media

chmod 777 /app/data /app/logs /app/staticfiles /app/media

if [ -f /app/data/db.sqlite3 ]; then
    chmod 666 /app/data/db.sqlite3
fi

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

ADMIN_USERNAME="${DJANGO_ADMIN_USERNAME:-admin}"
ADMIN_EMAIL="${DJANGO_ADMIN_EMAIL:-admin@example.com}"
ADMIN_PASSWORD="${DJANGO_ADMIN_PASSWORD:-}"

if [ -n "$ADMIN_PASSWORD" ]; then
    echo "Creating superuser if not exists..."
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = '${ADMIN_USERNAME}'
email = '${ADMIN_EMAIL}'
password = '${ADMIN_PASSWORD}'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser created: {username}')
else:
    print(f'Superuser already exists: {username}')
EOF
else
    echo "DJANGO_ADMIN_PASSWORD not set, skipping superuser creation"
fi

echo "Starting Gunicorn server..."
exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    myblog.wsgi:application
