from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import CategoryVideoViewSet, VideoViewSet, TestViewSet, AnswerViewSet, ResultViewSet


router = DefaultRouter()
router.register(r'category-video', CategoryVideoViewSet, basename='CategoryVideo')
router.register(r'video', VideoViewSet, basename='Video')
router.register(r'test', TestViewSet, basename='Test')
router.register(r'answer', AnswerViewSet, basename='Answer')
router.register(r'result', ResultViewSet, basename='Result')

urlpatterns = [
    path('', include(router.urls)),
]


