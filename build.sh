#!/bin/bash

# Install dependencies
pipenv install --dev

# Activate virtual environment
source .venv/bin/activate

# Run Django migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Deactivate virtual environment
deactivate
