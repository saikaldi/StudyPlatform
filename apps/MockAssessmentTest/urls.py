from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MockAssessmentTestViewSet, MockAssessmentTestContentViewSet, MockAssessmentTestFullDescriptionViewSet, 
    MockAssessmentTestInstructionViewSet, MockAssessmentTestViewSet, 
    MockAssessmentAnswerViewSet, MockAssessmentUserStatisticViewSet, submit_answer, get_mock_results, MockAssessmentUserViewSet
)

router = DefaultRouter()
router.register(r'mock-assessment-test-tests', MockAssessmentTestViewSet, basename='test')
router.register(r'mock-assessment-test-test-contents', MockAssessmentTestContentViewSet, basename='test-content')
router.register(r'mock-assessment-test-test-descriptions', MockAssessmentTestFullDescriptionViewSet, basename='test-description')
router.register(r'mock-assessment-test-test-instructions', MockAssessmentTestInstructionViewSet, basename='test-instruction')
router.register(r'mock-assessments', MockAssessmentUserViewSet, basename='mock-assessment')
router.register(r'mock-assessment-answers', MockAssessmentAnswerViewSet, basename='mock-assessment-answer')
router.register(r'mock-assessment-test-user-statistics', MockAssessmentUserStatisticViewSet, basename='user-statistic')

urlpatterns = [
    path('tests/<int:test_id>/answer/', submit_answer),
    path('results/<int:session_id>/', get_mock_results),
    path('', include(router.urls)),
]