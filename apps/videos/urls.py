from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register(r'category-video', CategoryVideoViewSet, basename='CategoryVideo')
router.register(r'video', VideoViewSet, basename='Video')
router.register(r'test', TestViewSet, basename='Test')
router.register(r'answer', AnswerViewSet, basename='Answer')
router.register(r'result', ResultViewSet, basename='Result')

urlpatterns = [
    path('', include(router.urls)),
    # path('video/<int:pk>/', VideoDetailViewSet.as_view(), name='video-detail'),
    path('video/<int:video_id>/submit_answers/', VideoViewSet.as_view({'post': 'submit_answers'}), name='submit-answers'),

]


