from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from main.views import IndexView, Custom404View, LogoutView, SignupView

from django.conf.urls import handler404

handler404 = Custom404View

urlpatterns = [
    path("admin/", admin.site.urls),
    path("app/", IndexView.as_view(), name="index"),
    path("signup/", SignupView, name="signup"),
    path("logout/", LogoutView),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
