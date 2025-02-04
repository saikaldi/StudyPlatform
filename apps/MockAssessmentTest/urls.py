from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TestViewSet, TestContentViewSet, TestFullDescriptionViewSet, 
    TestInstructionViewSet, MockAssessmentTestViewSet, 
    MockAssessmentAnswerViewSet, UserStatisticViewSet, submit_answer, get_mock_results
)

router = DefaultRouter()
router.register(r'mock-assessment-test-tests', TestViewSet, basename='test')
router.register(r'mock-assessment-test-test-contents', TestContentViewSet, basename='test-content')
router.register(r'mock-assessment-test-test-descriptions', TestFullDescriptionViewSet, basename='test-description')
router.register(r'mock-assessment-test-test-instructions', TestInstructionViewSet, basename='test-instruction')
router.register(r'mock-assessments', MockAssessmentTestViewSet, basename='mock-assessment')
router.register(r'mock-assessment-answers', MockAssessmentAnswerViewSet, basename='mock-assessment-answer')
router.register(r'mock-assessment-test-user-statistics', UserStatisticViewSet, basename='user-statistic')

urlpatterns = [
    path('tests/<int:test_id>/answer/', submit_answer),
    path('results/<int:session_id>/', get_mock_results),
    path('', include(router.urls)),
]