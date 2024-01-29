#!/bin/bash

# Install Pipenv and dependencies
pip install pipenv
pipenv install --dev

# Activate the virtual environment
pipenv shell

# Run Django migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Deactivate the virtual environment
exit
