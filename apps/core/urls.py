from django.urls import path, include
from rest_framework import routers
from .views import GraduateView, AbountTeacherView, FeedbackView

router = routers.DefaultRouter()
router.register(r'graduates', GraduateView, basename='graduates')
router.register(r'about-teacher', AbountTeacherView, basename='about-teacher')
router.register(r'feedback', FeedbackView)

urlpatterns = [
    path('', include(router.urls)),
]   