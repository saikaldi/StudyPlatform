from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TestCategoryViewSet,
    TestViewSet,
    TestContentViewSet,
    TestFullDescriptionViewSet,
    UserAnswerViewSet,
    UserStatisticViewSet,
    SubjectCategoryViewSet
)  # AdditionalInstructionViewSet, TestInstructionViewSet


router = DefaultRouter()
router.register(r"testcategories", TestCategoryViewSet, basename="testcategory")
router.register(r"subjectcategories", SubjectCategoryViewSet, basename="subjectcategory")
router.register(r"tests", TestViewSet, basename="test")
router.register(r"TestContent", TestContentViewSet, basename="TestContent")
router.register(r"testfulldescriptions", TestFullDescriptionViewSet, basename="testfulldescription")
# router.register(r"testinstructions", TestInstructionViewSet, basename="testinstruction")
# router.register(r"additionalinstructions", AdditionalInstructionViewSet, basename="additionalinstruction")
router.register(r"useranswers", UserAnswerViewSet, basename="useranswer")
router.register(r"userstatistics", UserStatisticViewSet, basename="userstatistics")

urlpatterns = [
    path("", include(router.urls)),
]
