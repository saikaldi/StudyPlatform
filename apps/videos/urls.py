from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'videos', views.VideoViewSet)
router.register(r'purchases', views.PurchaseViewSet)
router.register(r'tests', views.TestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]