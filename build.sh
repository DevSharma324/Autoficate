#!/bin/bash

# Install dependencies
pipenv install --dev

# Collect static files
python manage.py collectstatic --noinput
