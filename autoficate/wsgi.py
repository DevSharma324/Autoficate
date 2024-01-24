import time

import os
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoficate.settings')

start_time = time.time()


application = get_wsgi_application()
# Specify the correct path to STATIC_ROOT
static_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "staticfiles")

# `app` required for Vercel deployment
app = WhiteNoise(application, root=static_root)


end_time = time.time()
elapsed_time = end_time - start_time
print(
    f"\nWSGI took {elapsed_time:.6f} seconds to execute.\n"
)
list_dirs_1 = lambda p='.': [d for d in os.listdir(p) if os.path.isdir(os.path.join(p, d))]; print(list_dirs(str(settings.STATIC_ROOT)))
list_dirs_2 = lambda p='.': [d for d in os.listdir(p) if os.path.isdir(os.path.join(p, d))]; print(list_dirs(str(static_root)))

print("Settings " + settings.STATIC_ROOT + " - "  + str(list_dirs_1))
print("Custom " + static_root + " - "  + str(list_dirs_2))
