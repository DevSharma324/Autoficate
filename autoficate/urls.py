from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
import os

from main.views import IndexView, Custom404View, LogoutView, SignupView

from django.conf.urls import handler404

handler404 = Custom404View

urlpatterns = [
    path(os.environ.get("ADMIN_PATH"), admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("signup/", SignupView, name="signup"),
    path("logout/", LogoutView),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
