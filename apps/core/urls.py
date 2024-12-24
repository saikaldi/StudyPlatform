from django.urls import path, include
from rest_framework import routers
from .views import GraduateView, AbountUsView, FeedbackView

router = routers.DefaultRouter()
router.register(r'graduates', GraduateView, basename='graduates')
router.register(r'aboutus', AbountUsView)
router.register(r'feedback', FeedbackView)

urlpatterns = [
    path('', include(router.urls)),
]   