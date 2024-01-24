import time

import os
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoficate.settings')

start_time = time.time()


application = get_wsgi_application()
# Specify the correct path to STATIC_ROOT
static_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), settings.STATIC_ROOT)

# `app` required for Vercel deployment
app = WhiteNoise(application, root=static_root)


end_time = time.time()
elapsed_time = end_time - start_time
print(
    f"\nWSGI took {elapsed_time:.6f} seconds to execute.\n"
)