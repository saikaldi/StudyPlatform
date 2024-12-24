from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# /api/v1/ деп башталсын созсуз
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.core.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
