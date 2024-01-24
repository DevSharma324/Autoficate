#!/bin/bash

# Check if pipenv is installed, and install it if not
if ! command -v pipenv &> /dev/null
then
    pip install pipenv
fi

# Install project dependencies using pipenv
pipenv install --dev

# Activate virtual environment
source $(pipenv --venv)/bin/activate

# Run collectstatic to gather static files
python manage.py collectstatic --noinput

# Additional build steps, if any

# Deactivate virtual environment
deactivate
