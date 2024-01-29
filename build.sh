#!/bin/bash

# Install dependencies
pipenv install --dev

# Check for pending migrations
python manage.py makemigrations --dry-run --check > /dev/null 2>&1
PENDING_MIGRATIONS=$?

# Apply migrations if there are pending changes
if [ $PENDING_MIGRATIONS -eq 0 ]; then
    python manage.py migrate
fi

# Collect static files
python manage.py collectstatic --noinput
