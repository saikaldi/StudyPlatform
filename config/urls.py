from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("api/v1/admin/", admin.site.urls),
    path("api/v1/", include("apps.AboutStaffStudents.urls")),
    path("api/v1/", include("apps.users.urls")),
    path("api/v1/", include("apps.OrtTest.urls")),
    path("api/v1/", include("apps.payments.urls")),
    path("api/v1/", include("apps.VideoCourse.urls")),
    path("api/v1/swagger/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/swagger/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
