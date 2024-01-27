import time

import os
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoficate.settings")

start_time = time.time()

# `app` required for Vercel deployment
app = WhiteNoise(get_wsgi_application(), root=settings.STATIC_ROOT)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nWSGI took {elapsed_time:.6f} seconds to execute.\n")
