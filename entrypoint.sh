#!/bin/sh
set -e

echo "Creating migrations..."
python manage.py makemigrations blog comments --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating initial data..."
python init_data.py

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
