from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r"categories", views.CategoryViewSet, basename="subject")
router.register(
    r"subject-categories", views.SubjectCategoryViewSet, basename="subjectcategory"
)
router.register(r"category-video", views.CategoryVideoViewSet)
router.register(r"video", views.VideoViewSet)
router.register(r"test-content", views.TestContentViewSet)
router.register(r"user-statistic", views.UserStatisticViewSet)
router.register(r"user-answer", views.UserAnswerViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
