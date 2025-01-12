from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, GraduateViewSet, TeacherViewSet, FeedbackViewSet


router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'graduates', GraduateViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'feedbacks', FeedbackViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
