from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryVideoViewSet, VideoViewSet, TestViewSet, AnswerViewSet, ResultViewSet


router = DefaultRouter()
router.register(r'categories', CategoryVideoViewSet, basename='categoryvideo')
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'tests', TestViewSet, basename='test')
router.register(r'answers', AnswerViewSet, basename='answer')
router.register(r'results', ResultViewSet, basename='result')

urlpatterns = [
    path('', include(router.urls)),
]
