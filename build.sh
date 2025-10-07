#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

echo "Starting build process..."

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Creating migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

echo "Build completed successfully!"