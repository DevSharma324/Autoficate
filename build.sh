#!/bin/bash

# Install dependencies
pipenv install --dev

# Activate Virtual Environment
pipenv shell

# Collect static files
python manage.py collectstatic --noinput
