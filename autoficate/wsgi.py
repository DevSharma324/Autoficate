"""
WSGI config for autoficate project.

It exposes the WSGI callable as a module-level variable named ``app``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoficate.settings')

application = get_wsgi_application()

# Specify the correct path to STATIC_ROOT
static_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'staticfiles')

# `app` required for Vercel deployment
app = WhiteNoise(application, root=static_root)